# -*- coding: utf-8 -*-
import logging
from contextlib import closing
from urllib2 import urlopen

from pure_content.parsing import ContentParser
from pure_content.storage import Container


logger = logging.getLogger('pure_content')


class WebPagePurist(object):
    content_parser = ContentParser()

    def _get_content(self, url):
        logger.debug('loading of {url}'.format(url=url))
        with closing(urlopen(url)) as html_page_stream:
            content_parser = self.content_parser
            parsed_page = content_parser.parse(url, html_page_stream)
        images = {}
        logger.debug(
            'parsed page {parsed_page}'.format(
                parsed_page=parsed_page
            )
        )
        for image_name, image_url in parsed_page['images'].items():
            logger.debug('loading of {image_url}'.format(image_url=image_url))
            try:
                with closing(urlopen(image_url)) as image_stream:
                    images[image_name] = {
                        'url': image_url,
                        'content': image_stream.read(),
                    }
            except Exception as error:
                logger.error(error)
        return parsed_page, images

    def purify(self, url):
        parsed_page, images = self._get_content(url)
        container = Container(
            url=url,
            title=parsed_page['title'],
            text=parsed_page['text'],
            images=images
        )
        container.save()
        logger.info('Saved to {path}'.format(path=container.get_path()))
