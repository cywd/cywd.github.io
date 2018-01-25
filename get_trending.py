# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import os
import subprocess

url_str = 'http://trending.codehub-app.com/v2/trending/'
foldername = "json"
filename = "trending.json"
folder_path = "./" + foldername + "/"
file_path = folder_path + filename


def git_add():
    cmd = ['git', 'add', '.']
    p = subprocess.Popen(cmd, cwd=folder_path)
    p.wait()


def git_commit():
    centext = "'refresh git trending'"
    cmd = ['git', 'commit', '-m', centext]
    p = subprocess.Popen(cmd, cwd=folder_path)
    p.wait()


def git_push():
    cmd = ['git', 'push', '-u', 'origin', 'master']
    p = subprocess.Popen(cmd, cwd=folder_path)
    p.wait()


def file_handle():
    git_add()
    git_commit()
    git_push()


def url_open(url):
    if not ('http' in url):
        url = 'http://' + url

    print('url is :' + url)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0')
    response = urllib.request.urlopen(req)
    return response.read()


def save_file():
    print("开始请求")
    json = url_open(url_str)
    print("得到json数据，准备写入文件")
    with open(file_path, 'wb') as f:
        f.write(json)
        f.close()
        print("成功写入文件")

    print("准备提交github")
    file_handle()


def trending():
    if not os.path.exists(foldername):
        os.mkdir(foldername)  # 新建文件夹
        print('成功创建文件夹', foldername)
    save_file()


if __name__ == '__main__':
    trending()
