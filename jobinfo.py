# -*- coding: utf-8 -*-

import requests
import os
import sys
from bs4 import BeautifulSoup
import jieba.posseg as fenci


def _string_list_save(save_path, filename, slist):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path + "/" + filename + ".txt"
    with open(path, "w+") as fp:
        for s in slist:
            fp.write("%s\t\t%s\n" % (s['title'].encode("utf8"), s['url'].encode("utf8")))


def _get_page_info(soup):
    my_page_info = []
    class_types = ['style2 stylebg','style2']
    for class_type in class_types:
        for tag in soup.find_all('div', class_=class_type):
            title = tag.span.a.getText()
            print title
            url = tag.span.a['href']
            item = {'title':title, 'url':url}
            my_page_info.append(item)
    return my_page_info


def _get_next_page_suffix(soup):
    suffix_url = ''
    next_page_tag = soup.find_all('a', class_='next')
    if len(next_page_tag) == 1:
        suffix_url = next_page_tag[0]['href']

    return suffix_url


def _get_movie_list(prefix_url, suffix_url):
    my_page_info = []
    url = prefix_url + suffix_url
    print("downloading...%s" % url)
    my_page = requests.get(url).content
    soup = BeautifulSoup(my_page, "html.parser", from_encoding='gb18030')
    my_page_info += _get_page_info(soup)

    new_suffix_url = _get_next_page_suffix(soup)
    if new_suffix_url != '':
        my_page_info += _get_movie_list(prefix_url, new_suffix_url)

    return my_page_info


def spider(url, save_path, filename):
    movie_info_list = _get_movie_list(url, "")
    save_infos = []
    key_words = [u'生物', u'生命科学', u'生物医学工程', u'生物医学光子学', u'光学']
    for item in movie_info_list:
        print 'search', item['title']
        job_detail = requests.get(item['url']).content
        soup = BeautifulSoup(job_detail, "html.parser", from_encoding='gb18030')
        context = soup.find('div', class_='article_body').getText()
        words = fenci.cut(context)
        for w in words:
            if w.word in key_words:
                save_infos.append(item)
                break

    _string_list_save(save_path, filename, save_infos)


if __name__ == '__main__':
    print "start"
    start_url = "http://www.gaoxiaojob.com/zhaopin/chengshi/shenzhen/"
    spider(start_url, "/home/transfer/netspider", "douban")
    print "end dd"
