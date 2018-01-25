# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import os
import subprocess

url_str = 'http://trending.codehub-app.com/v2/trending/'
foldername = "json"
filename = "trending.json"
# folder_path = "./" + foldername + "/"
file_path = "./" + filename


def git_add():
    print("prepare to do 'git add'")
    cmd = ['git', 'add', '.']
    p = subprocess.Popen(cmd, cwd="./")
    p.wait()


def git_commit():
    print("prepare to do 'git commit'")
    centext = "'refresh git trending'"
    cmd = ['git', 'commit', '-m', centext]
    p = subprocess.Popen(cmd, cwd="./")
    p.wait()


def git_push():
    print("prepare to do 'git push'")
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
    print("begin request")
    json = url_open(url_str)
    print("get json data, ready write to file 'trending.json'")
    with open(file_path, 'wb') as f:
        f.write(json)
        f.close()
        print("write file success")

    file_handle()


def trending():
    if not os.path.exists(foldername):
        os.mkdir(foldername)  
        print('create folder success', foldername)

    os.chdir(foldername)
    folder_top = os.getcwd()
    print(folder_top)
    save_file()


if __name__ == '__main__':
    trending()
