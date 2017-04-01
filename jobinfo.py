# -*- coding: utf-8 -*-

from gaoxiaojob import GaoxiaoContexParse
from gaoxiaojob import GaoxiaoJobInfoUrlCollector
from myemail import MyEmail
import configparser
import time


url_collector_key = 'url_collector'
url_parse_key = 'parse'
start_url_key = 'start_url'


def make_spider():
    global url_collector_key
    global url_parse_key
    global start_url_key

    spider_list = []

    # 高校信息网站
    gaoxiao_db_name = 'jbDb'
    gaoxiao_collection_name = 'info_url'
    gaoxiao_key_words = [u'生物', u'生命科学', u'生物医学工程', u'生物医学光子学']
    gaoxiao_spider = {url_collector_key: GaoxiaoJobInfoUrlCollector(gaoxiao_db_name, gaoxiao_collection_name),
                      start_url_key: "http://www.gaoxiaojob.com/zhaopin/chengshi/shenzhen/",
                      url_parse_key: GaoxiaoContexParse(gaoxiao_db_name, gaoxiao_collection_name, gaoxiao_key_words)
                      }
    spider_list.append(gaoxiao_spider)

    return spider_list


def send_email(context):
    if not context:
        return

    config = configparser.ConfigParser()
    section_name = 'host'
    config.read("email.ini")
    user_name = config.get(section_name, 'user_name')
    pwd = config.get(section_name, 'pwd')
    host_name = config.get(section_name, 'host_name')
    port = config.getint(section_name, 'port')

    # 将获取的信息通过邮件发送出去
    email = MyEmail(user_name, pwd, host_name, port)
    to = config.get(section_name, 'send_to')
    title = 'job info ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    email.send_text(to, title, context)


def find_job_info():
    global url_collector_key
    global url_parse_key
    global start_url_key

    interest_context = ''

    spider_list = make_spider()
    for spider in spider_list:
        # 获得一系列的url
        collector = spider[url_collector_key]
        collector.get_url_list(spider[start_url_key])
        # 获得url
        url_list = collector.get_urls()

        parse = spider[url_parse_key]
        # 逐条获取url并进行解析
        total = url_list.count()
        cur = 0
        for url_item in url_list:
            cur += 1
            print('parse:{cur}/{total}'.format(cur=cur, total=total))
            if parse.analysis_page(url_item['url']):
                print('find %s\n' % url_item['title'])
                title = url_item['title']
                url = url_item['url']
                interest_context += ('{title}\n{url}\n\n'.format(title=title, url=url))

    # 发送邮件
    send_email(interest_context)


if __name__ == '__main__':
    find_job_info()
