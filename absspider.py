# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


class AbsUlrCollector:
    def get_next_page_suffix(self, soup):
        return ''

    def parse_page_info(self, soup):
        return ''

    def save_page_info(self, info):
        pass

    def get_url_list(self, prefix_url, suffix_url='', builder='html.parser', encoding='gb18030'):
        url = prefix_url + suffix_url
        print("downloading...%s" % url)

        page = requests.get(url).content
        soup = BeautifulSoup(page, builder, from_encoding=encoding)

        info = self.parse_page_info(soup)

        self.save_page_info(info)

        new_suffix_url = self.get_next_page_suffix(soup)
        if new_suffix_url != '':
            self.get_url_list(prefix_url, new_suffix_url)


class AbsContexParse:
    def get_context(self, soup):
        return ''

    def process_context(self, url, context):
        return ''

    def analysis_page(self, url, builder='html.parser', encoding='gb18030'):
        page = requests.get(url).content
        soup = BeautifulSoup(page, builder, from_encoding=encoding)

        context = self.get_context(soup)

        return self.process_context(url, context)


if __name__ == '__main__':
    pass
