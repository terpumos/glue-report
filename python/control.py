#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from  cut_html import PlotlyCut
import webbrowser
import codecs
import markdown
from jinja2 import Environment, FileSystemLoader
from markdown_include.include import MarkdownInclude

class JoinReport(object):
    def __init__(self, files=None, title=None):
        self.files = files
        self.context = {}
        markdown_include = MarkdownInclude(
                configs={'base_path':'../templates/figures/', 'encoding': 'iso-8859-1'}
        )
        extensions = ['markdown.extensions.toc', markdown_include]
        self.md = markdown.Markdown(output_format="html5",
                                    extensions=extensions)

    def read_md(self):
        open_config = {'filename': '../markdown/text1.md',
                       'mode': 'r',
                       'encoding': 'utf-8'}
        with codecs.open(**open_config) as input_file:
            text = input_file.read()
            html = self.md.convert(text)
        self.context['text1'] = html

    def read_title_md(self):
        open_config = {'filename': '../markdown/title.md',
                       'mode': "r",
                       'encoding': "utf-8"}
        with codecs.open(**open_config) as input_file:
            text = input_file.read()
            html = markdown.markdown(text, output_format="html5")
        self.context['title'] = html

    def prepare_toc(self):
        self.context['toc'] = self.md.toc

    def build(self):
        pc = PlotlyCut()
        pc.walker()
        self.read_md()
        self.prepare_toc()
        self.read_title_md()
        env = Environment(loader=FileSystemLoader('../templates'))
        template = env.get_template("doc.html")
        html_out = template.render(self.context)
        output_file = codecs.open("../templates/report.html", "w",
                                  encoding="utf-8", errors="xmlcharrefreplace")
        output_file.write(html_out)
        output_file.close()

    def open_tab(self):
        webbrowser.open("../templates/report.html",new=2)


if __name__ == "__main__":
    join_report = JoinReport()
    join_report.build()
    join_report.open_tab()
