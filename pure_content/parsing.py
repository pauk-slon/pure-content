# -*- coding: utf-8 -*-
import os
import urlparse

from bs4 import BeautifulSoup

from pure_content.analysis import AverageParagraphLengthAnalyzer
from pure_content.formatting import DefaultFormatter


class UrlAbsolutizer(object):
    def __init__(self, url):
        self._url = url

    def is_absolute(self, url):
        parsed_url = urlparse.urlparse(url)
        return bool(parsed_url.netloc)

    def absolutize(self, url):
        try:
            if not self.is_absolute(url):
                return urlparse.urljoin(self._url, url)
        except:
            pass
        return url


class ContentParser(object):
    average_paragraph_length_analyzer = AverageParagraphLengthAnalyzer()

    def _absolutize_urls(self, page_url, content_tag,
                         tag_name, url_attribute):
        absolutizer = UrlAbsolutizer(page_url)
        for tag in content_tag.find_all(tag_name):
            if tag.get(url_attribute):
                page_url = tag[url_attribute]
                tag[url_attribute] = absolutizer.absolutize(page_url)

    def _parse_images(self, content_tag):
        images = {}
        for img_tag in content_tag.find_all('img'):
            if not img_tag.get('src'):
                continue
            image_url = img_tag['src']
            parsed_url = urlparse.urlparse(image_url)
            _filename, ext = os.path.splitext(parsed_url.path)
            new_image_name = u'{number:03}{ext}'.format(
                number=len(images) + 1,
                ext=ext
            )
            images[new_image_name] = image_url
            img_tag['src'] = new_image_name
        return images

    def parse(self, page_url, page_stream):
        document = BeautifulSoup(page_stream)
        body = document.body
        for no_main_content_element in body(['script', 'style', 'aside']):
            no_main_content_element.extract()
        analyzer = self.average_paragraph_length_analyzer
        tag_stats = analyzer.get_stats(document.body)
        title = document.title.get_text() if document.title else None
        if not tag_stats:
            return title, u''
        content_tag = max(tag_stats.keys(), key=lambda tag: len(tag_stats[tag]))
        self._absolutize_urls(page_url, content_tag, 'a', 'href')
        self._absolutize_urls(page_url, content_tag, 'img', 'src')
        images = self._parse_images(content_tag)
        formatter = DefaultFormatter(page_url)
        formatted_text = formatter.format(content_tag)
        return {
            'title': title,
            'text': formatted_text,
            'images': images,
        }
