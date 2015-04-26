# -*- coding: utf-8 -*-
import re
from argparse import ArgumentParser
from contextlib import closing
from urllib2 import urlopen, URLError, HTTPError

from pure_content.parsing import ContentParser
from pure_content.storage import Container


def validate_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
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
        print u'URL is not specified'
        return
    if not validate_url(url):
        print u'"{url}" is a not correct url'.format(
            url=url,
        )
        return
    try:
        with closing(urlopen(url)) as html_page_stream:
            content_parser = ContentParser()
            title, content = content_parser.parse(url, html_page_stream)
    except (URLError, HTTPError) as error:
        print error
        return
    container = Container(url, title, content)
    container.save()
    print 'Saved to:'
    print container.get_path()

if __name__ == '__main__':
    main()
