# -*- coding: utf-8 -*-

from absspider import AbsUlrCollector, AbsContexParse
from mymongodb import MyMongoDb
import jieba.posseg as fenci


class GaoxiaoJobInfoUrlCollector(AbsUlrCollector):
    '''
    网页信息获取对象
    '''
    def __init__(self, db_name, collection_name):
        self.db = MyMongoDb(db_name, collection_name)

    def get_next_page_suffix(self, soup):
        '''
        获取“下一页”的后缀，用于递归获取网页信息
        :param soup: soup对象
        :return: 下一页网页后缀
        '''
        suffix_url = ''
        next_page_tag = soup.find_all('a', class_='next')
        if next_page_tag:
            suffix_url = next_page_tag[0]['href']
        return suffix_url

    def parse_page_info(self, soup):
        '''
        获取当前界面中的url信息
        :param soup: soup对象
        :return: 当前界面中url信息list
        '''
        page_info = []
        class_types = ['style2 stylebg', 'style2']
        for class_type in class_types:
            for tag in soup.find_all('div', class_=class_type):
                title = tag.span.a.getText()
                url = tag.span.a['href']
                # 第一次获取到的url，所以还未进行处理
                url_item = {'title': title, 'url': url, 'processed': False}
                page_info.append(url_item)
        return page_info

    def save_page_info(self, info):
        '''
        保存url信息
        :param info: url信息
        :return: none
        '''
        for info_item in info:
            # 如果已经存在则不再保存
            if self.db.contians({'url': info_item['url']}):
                continue
            # 保存
            print('insert:{title}'.format(title=info_item['title']))
            self.db.insert(info_item)

    def get_urls(self):
        '''
        获取还未分析过的url
        :return: url list
        '''
        return self.db.collection.find({'processed': False})


class GaoxiaoContexParse(AbsContexParse):
    '''
    根据网页信息进行解析，找到感兴趣的网页
    '''
    def __init__(self, db_name, collection_name, include_key_words):
        self.db = MyMongoDb(db_name, collection_name)
        self.include_key_words = include_key_words

    def get_context(self, soup):
        return soup.find('div', class_='article_body').getText()

    def process_context(self, url, context):
        # 已经分析，则更新数据库
        self.db.find_one_and_update({'url': url}, {'processed': True})

        words = fenci.cut(context)

        matched_kes = []
        for w in words:
            if w.word in self.include_key_words:
                if w.word not in matched_kes:
                    matched_kes.append(w.word)

        if len(matched_kes) > 0:
            print('\nmatch key ', end="")
            for word in matched_kes:
                print(word, end="")
            return True

        return False


if __name__ == '__main__':
    db_name = 'jbDb'
    collection_name = 'info_url'

    jobInfoUrl = GaoxiaoJobInfoUrlCollector(db_name, collection_name)
    start_url = "http://www.gaoxiaojob.com/zhaopin/chengshi/shenzhen/"
    jobInfoUrl.get_url_list(start_url)

    key_words = [u'生物', u'生命科学', u'生物医学工程', u'生物医学光子学']
    parse = GaoxiaoContexParse(db_name, collection_name, key_words)

    times = 0
    url_list = jobInfoUrl.get_urls()
    total = url_list.count()
    for item in url_list:
        times += 1
        print("{cur}/{total}".format(cur=times, total=total))
        if parse.analysis_page(item['url']):
            print('\tfind %s' % item['title'])
    print("完成")