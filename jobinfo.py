# -*- coding: utf-8 -*-

from gaoxiaojob import GaoxiaoContexParse
from gaoxiaojob import GaoxiaoJobInfoUrlCollector
from myemail import MyEmail
import configparser
import time

if __name__ == '__main__':
    db_name = 'jbDb'
    collection_name = 'info_url'

    # 从网站获取需要抓取的url
    jobInfoUrl = GaoxiaoJobInfoUrlCollector(db_name, collection_name)
    start_url = "http://www.gaoxiaojob.com/zhaopin/chengshi/shenzhen/"
    jobInfoUrl.get_url_list(start_url)

    # 解析器
    key_words = [u'生物', u'生命科学', u'生物医学工程', u'生物医学光子学']
    parse = GaoxiaoContexParse(db_name, collection_name, key_words)

    # 解析有用的网页
    context = ''
    times = 0
    info_list = jobInfoUrl.get_urls()
    for item in info_list:
        times += 1
        print(times)

        if parse.analysis_page(item['url']):
            print('find %s\n' % item['title'])
            context += ('%s\n%s\n\n' % (item['title'], item['url']))

    if context != '':
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
