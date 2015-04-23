# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from pure_content.analysis import AverageParagraphLengthAnalyzer


class ContentParser(object):
    average_paragraph_length_analyzer = AverageParagraphLengthAnalyzer()

    def parse(self, html_page_stream):
        document = BeautifulSoup(html_page_stream)
        body = document.body
        for script in body(['script', 'style']):
            script.extract()
        analyzer = self.average_paragraph_length_analyzer
        tag_stats = analyzer.get_stats(document.body)
        title = document.title.get_text() if document.title else None
        if not tag_stats:
            return title, u''
        content_tag = max(tag_stats.keys(), key=lambda tag: len(tag_stats[tag]))
        return title, content_tag.get_text()
