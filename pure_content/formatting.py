# -*- coding: utf-8 -*-
import textwrap

from bs4.element import Tag


class DefaultFormatter(object):
    MAX_LINE_LENGTH = 80

    def format(self, tag):
        for img in tag.find_all('img'):
            img.string = u'{{{src}}}'.format(
                src=img['src']
            )
        for a in tag.find_all('a'):
            text = a.text.strip()
            a.string = u'[{text}]({href})'.format(
                text=text,
                href=a.get('href'),
            ) if text else u'[{href}]'.format(
                href=a.get('href'),
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
