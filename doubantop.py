#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os
import sys
from bs4 import BeautifulSoup


def _string_list_save(save_path, filename, slist):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path + "/" + filename + ".txt"
    with open(path, "w+") as fp:
        for s in slist:
            fp.write("%s\t\t%s\n" % (s['rank'].encode("utf8"), s['name'].encode("utf8")))


def _get_page_info(soup):
    my_page_info = []
    for tag in soup.find_all('div', class_='item'):
        movie_rank = tag.em.get_text()
        movie_name = tag.span.get_text()
        movie_info = {"rank": movie_rank, "name": movie_name}
        my_page_info.append(movie_info)
    return my_page_info


def _get_next_page_suffix(soup):
    suffix_url = ''
    next_page_tag = soup.find_all('span', class_='next')
    if len(next_page_tag) == 1:
        next_link_tag = next_page_tag[0].find_all('link')
        if len(next_link_tag) == 1:
            suffix_url = next_link_tag[0]['href']
    return suffix_url


def _get_movie_list(prefix_url, suffix_url):
    my_page_info = []
    url = prefix_url + suffix_url
    print("downloading...%s" % url)
    my_page = requests.get(url).content
    soup = BeautifulSoup(my_page, "lxml")
    my_page_info += _get_page_info(soup)

    new_suffix_url = _get_next_page_suffix(soup)
    if new_suffix_url != '':
        my_page_info += _get_movie_list(prefix_url, new_suffix_url)

    return my_page_info


def spider(url, save_path, filename):
    movie_info_list = _get_movie_list(url, "")
    _string_list_save(save_path, filename, movie_info_list)


if __name__ == '__main__':
    print "start"
    start_url = "https://movie.douban.com/top250"
    spider(start_url, "/home/transfer/netspider", "douban")
    print "end"
