# -*- coding: utf-8 -*-
import textwrap
import urlparse

from bs4.element import Tag


class UrlAbsolutizer(object):
    @classmethod
    def is_absolute(cls, url):
        parsed_url = urlparse.urlparse(url)
        return bool(parsed_url.netloc)

    @classmethod
    def absolutize(cls, url, path):
        try:
            if not cls.is_absolute(path):
                return urlparse.urljoin(url, path)
        except:
            pass
        return path


class DefaultFormatter(object):
    MAX_LINE_LENGTH = 80

    def __init__(self, url):
        self._url = url

    def format(self, tag):
        for img in tag.find_all('img'):
            image_url = (
                UrlAbsolutizer.absolutize(self._url, img.get('src'))
            )
            img.string = u'{{{src}}}'.format(
                src=image_url
            )
        for a in tag.find_all('a'):
            text = a.text.strip()
            link_url = (
                UrlAbsolutizer.absolutize(self._url, a.get('href'))
            )
            a.string = u'[{text}]({href})'.format(
                text=text,
                href=link_url,
            ) if text else u'[{href}]'.format(
                href=link_url,
            )
        paragraphs = []
        for paragraph_tag in tag.contents:
            if not isinstance(paragraph_tag, Tag):
                continue
            paragraph_text = paragraph_tag.get_text()
            paragraph_text = paragraph_text.strip()
            if not paragraph_text:
                continue
            wrapped_paragraph_text = textwrap.fill(
                paragraph_text,
                width=self.MAX_LINE_LENGTH
            )
            paragraphs.append(wrapped_paragraph_text)
        return u'\n\n'.join(paragraphs)
