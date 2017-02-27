# -*- coding: utf-8 -*-

from gaoxiaojob import GaoxiaoContexParse
from gaoxiaojob import GaoxiaoJobInfoUrlCollector
from myemail import MyEmail
import ConfigParser
import time

if __name__ == '__main__':
    db_name = 'jbDb'
    cellection_name = 'info_url'

    #  从网站获取需要抓取的url
    jobInfoUrl = GaoxiaoJobInfoUrlCollector(db_name, cellection_name)
    start_url = "http://www.gaoxiaojob.com/zhaopin/chengshi/shenzhen/"
    jobInfoUrl.get_url_list(start_url)

    key_words = [u'生物', u'生命科学', u'生物医学工程', u'生物医学光子学']
    parse = GaoxiaoContexParse(db_name, cellection_name, key_words)

    # 解析有用的网页
    context = ''
    times = 0
    infos = jobInfoUrl.get_urls()
    for item in infos:
        times += 1
        print times

        if parse.analysis_page(item['url']):
            print('find %s\n' % item['title'])
            context += ('%s\n%s\n\n' % (item['title'], item['url']))

    if context != '':
        config = ConfigParser.ConfigParser()
        config.read("email.ini")
        user_name = config.get('host', 'user_name')
        pwd = config.get('host', 'pwd')
        host_name = config.get('host', 'host_name')
        port = config.getint('host', 'port')

        # 将获取的信息通过邮件发送出去
        email = MyEmail(user_name, pwd, host_name, port)
        to = '448217518@qq.com'
        title = 'job info ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        email.send_text(to, title, context)
