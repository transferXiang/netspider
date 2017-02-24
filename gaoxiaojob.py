# -*- coding: utf-8 -*-

from absspider import AbsUlrCollector, AbsContexParse
from mymongodb import MyMongoDb
import jieba.posseg as fenci

class JobInfoUrlCollector(AbsUlrCollector):
    def __init__(self, db_name, cellection_name):
        self.db = MyMongoDb(db_name, cellection_name)

    def get_next_page_suffix(self, soup):
        suffix_url = ''
        next_page_tag = soup.find_all('a', class_='next')
        if len(next_page_tag) == 1:
            suffix_url = next_page_tag[0]['href']
        return suffix_url

    def parse_page_info(self, soup):
        page_info = []
        class_types = ['style2 stylebg', 'style2']
        for class_type in class_types:
            for tag in soup.find_all('div', class_=class_type):
                title = tag.span.a.getText()
                url = tag.span.a['href']
                item = {'title': title, 'url': url}
                page_info.append(item)
        return page_info

    def save_page_info(self, info):
        for info_item in info:
            if not self.db.contians(info_item['url']):
                self.db.insert(info_item)

    def get_urls(self):
        return self.db.find()


class GaoxiaoContexParse(AbsContexParse):
    def __init__(self, db_name, cellection_name, include_key_words):
        self.db = MyMongoDb(db_name, cellection_name)
        self.include_key_words = include_key_words

    def get_context(self, soup):
        return soup.find('div', class_='article_body').getText()

    def process_context(self, context):
        words = fenci.cut(context)

        mached_kes = []
        for w in words:
            if w.word in self.include_key_words:
                if w.word not in mached_kes:
                    mached_kes.append(w.word)

        if len(mached_kes) > 0:
            print '\nmatch key',
            for word in mached_kes:
                print word,
            print ''
            return True

        return False


if __name__ == '__main__':
    db_name = 'jbDb'
    cellection_name = 'info_url'

    jobInfoUrl = JobInfoUrlCollector(db_name, cellection_name)
    start_url = "http://www.gaoxiaojob.com/zhaopin/chengshi/shenzhen/"
    jobInfoUrl.get_url_list(start_url)

    key_words = [u'生物', u'生命科学', u'生物医学工程', u'生物医学光子学']
    parse = GaoxiaoContexParse(db_name, cellection_name, key_words)

    times = 0
    for item in jobInfoUrl.get_urls():
        times += 1
        if times % 100 == 0:
            print '.'
        else:
            print '.',
        if parse.analysis_page(item['url']):
            print('find %s\n' % item['title'])