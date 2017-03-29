#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os
from bs4 import BeautifulSoup


# 将解析到的文件保存到文件中
def _string_list_save(save_path, filename, movie_info_list):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path + "/" + filename
    with open(path, "w+", encoding="utf-8") as fp:
        for movie_info in movie_info_list:
            fp.write("%s\t\t%s\n" % (movie_info['rank'], movie_info['name']))


# 解析界面
def _parse_page_info(soup):
    my_page_info = []
    for tag in soup.find_all('div', class_='item'):
        movie_rank = tag.em.get_text()
        movie_name = tag.span.get_text()
        movie_info = {"rank": movie_rank, "name": movie_name}
        my_page_info.append(movie_info)
    return my_page_info


# 获得下一页的后缀
def _get_next_page_suffix(soup):
    suffix_url = ''
    next_page_tag = soup.find_all('span', class_='next')
    if len(next_page_tag) == 1:
        next_link_tag = next_page_tag[0].find_all('link')
        if len(next_link_tag) == 1:
            suffix_url = next_link_tag[0]['href']
    return suffix_url


# 通过递归的方式获得所有网页信息
def _get_html_page(prefix_url, suffix_url):
    my_page_info = []

    '''
    url=网址前缀+后缀
    如:'https://movie.douban.com/top250?start=25&filter=' 获取第二页（每页显示25条信息）
    网址前缀为：‘https://movie.douban.com/top250’
    后缀为：‘?start=25&filter=’
    '''
    url = prefix_url + suffix_url

    # 下载网页
    print("downloading...%s" % url)
    my_page = requests.get(url).content

    # 使用html.parser而不是lxml解析，防止遇到较大的网页时解析出现问题
    soup = BeautifulSoup(my_page, "html.parser")

    # 解析当前网页的信息
    current_page_info = _parse_page_info(soup)

    # 将当前的信息
    my_page_info += current_page_info

    # 获得下一页的后缀
    new_suffix_url = _get_next_page_suffix(soup)
    # 如果还有下一页则继续递归
    if new_suffix_url != '':
        my_page_info += _get_html_page(prefix_url, new_suffix_url)

    return my_page_info


def spider(url, save_path, filename):
    # 通过递归的方式获得所有网页信息
    movie_info_list = _get_html_page(url, "")
    # 将解析出的文件保存到文件中
    _string_list_save(save_path, filename, movie_info_list)


if __name__ == '__main__':
    print("start")
    start_url = "https://movie.douban.com/top250"
    spider(start_url, "./", "douban_top250.txt")
    print("end")
