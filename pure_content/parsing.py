# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from pure_content.analysis import AverageParagraphLengthAnalyzer
from pure_content.formatting import DefaultFormatter


class ContentParser(object):
    average_paragraph_length_analyzer = AverageParagraphLengthAnalyzer()
    formatter = DefaultFormatter()

    def parse(self, html_page_stream):
        document = BeautifulSoup(html_page_stream)
        body = document.body
        for no_main_content_element in body(['script', 'style', 'aside']):
            no_main_content_element.extract()
        analyzer = self.average_paragraph_length_analyzer
        tag_stats = analyzer.get_stats(document.body)
        title = document.title.get_text() if document.title else None
        if not tag_stats:
            return title, u''
        content_tag = max(tag_stats.keys(), key=lambda tag: len(tag_stats[tag]))
        formatter = self.formatter
        formatted_text = formatter.format(content_tag)
        return title, formatted_text
