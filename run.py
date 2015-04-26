# -*- coding: utf-8 -*-
import logging
import re
from argparse import ArgumentParser
from urllib2 import URLError, HTTPError

from pure_content.processing import WebPagePurist


logger = logging.getLogger('pure_content')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '[%(asctime)s] %(message)s'
)
error_log = logging.FileHandler('error.log')
error_log.setLevel(logging.ERROR)
error_log.setFormatter(formatter)
logger.addHandler(error_log)
output_log = logging.StreamHandler()
output_log.setLevel(logging.DEBUG)
logger.addHandler(output_log)


def validate_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
        r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$',
        re.IGNORECASE | re.UNICODE,
    )
    return regex.match(url)


def main():
    argument_parser = ArgumentParser()
    argument_parser.add_argument(
        '-u', '--url',
        type=unicode,
        help=u'URL of a web page which will be clean'
    )
    args = argument_parser.parse_args()
    url = args.url
    if not url:
        logger.error(u'URL is not specified')
        return
    if not validate_url(url):
        logger.error(
            u'"{url}" is a not correct url'.format(
                url=url,
            )
        )
        return
    web_page_purist = WebPagePurist()
    try:
        web_page_purist.purify(url)
    except (URLError, HTTPError) as error:
        logger.exception(error)


if __name__ == '__main__':
    main()
