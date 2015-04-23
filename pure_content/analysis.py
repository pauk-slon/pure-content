# -*- coding: utf-8 -*-
from bs4.element import Tag


class AverageParagraphLengthAnalyzer(object):
    MIN_PARAGRAPH_LENGTH = 80

    def _get_average_paragraph_length(self, text):
        lines = text.splitlines()
        lines = [
            line for line in lines
            if len(line.strip()) >= self.MIN_PARAGRAPH_LENGTH
        ]
        if lines:
            return sum(len(line) for line in lines) / len(lines)
        else:
            return -1

    def _get_tag_children_average_paragraph_lengths(self, tag):
        children = tag.contents
        tag_children_average_paragraph_lengths = []
        for child in children:
            if not isinstance(child, Tag):
                continue
            average_paragraph_length = self._get_average_paragraph_length(
                child.get_text(separator='\n')
            )
            if average_paragraph_length < self.MIN_PARAGRAPH_LENGTH:
                continue
            tag_children_average_paragraph_lengths.append(
                (child, average_paragraph_length)
            )
        return tag_children_average_paragraph_lengths

    def get_stats(self, body):
        tag_stats = {}
        for tag in body(['p', 'div', 'section']):
            average_paragraph_lengths = (
                self._get_tag_children_average_paragraph_lengths(tag)
            )
            weights = [avg_len for (_t, avg_len) in average_paragraph_lengths]
            if weights:
                tag_stats[tag] = weights
        return tag_stats
