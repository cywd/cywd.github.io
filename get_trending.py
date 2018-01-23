# !/usr/bin/env python3
# coding:utf-8

import urllib.request
import os, sys, re


def url_open(url):

    if not ('http' in url):
        url = 'http://' + url
    print('url is :' + url)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0')
    response = urllib.request.urlopen(req)
    return response.read()


def save_file(url):
    filename = "treding.json"

    req = urllib.request.urlopen(url)
    json = req.read()

    with open(filename, 'wb') as f:
        f.write(json)
        f.close()


def treding(folder='json'):
    if not os.path.exists(folder):
        os.mkdir(folder)  # 新建文件夹
        print('成功创建文件夹', folder)

    os.chdir(folder)  # 跳转到文件夹

    url = 'http://trending.codehub-app.com/v2/trending/'
    save_file(url)


if __name__ == '__main__':
    treding()
