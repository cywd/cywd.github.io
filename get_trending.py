# !/usr/bin/env python3
# coding:utf-8

import urllib.request
import os, sys, re, subprocess, random


url = 'http://trending.codehub-app.com/v2/trending/'
folder = "json"
filename = "treding.json"
file_path = "./" + folder + filename
folder_path = ""


def git_add():
    cmd = ['git', 'add', '.']
    p = subprocess.Popen(cmd, cwd="./")
    p.wait()


def git_commit():
    centext = "'upload git trending '"
    cmd = ['git', 'commit', '-m', centext]
    p = subprocess.Popen(cmd, cwd="./")
    p.wait()


def git_push():
    cmd = ['git', 'push', '-u', 'origin', 'master']
    p = subprocess.Popen(cmd, cwd="./")
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

    req = urllib.request.urlopen(url)
    json = req.read()

    with open(file_path, 'wb') as f:
        f.write(json)
        f.close()

    file_handle()



def treding():
    if not os.path.exists(folder):
        os.mkdir(folder)  # 新建文件夹
        print('成功创建文件夹', folder)

    save_file()


if __name__ == '__main__':
    treding()
