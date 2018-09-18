# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib import request
import os
import subprocess
import sys
import json
import yaml
import codecs
import requests
from collections import OrderedDict
from pyquery import PyQuery as pq

# the treading
url_str = 'http://trending.codehub-app.com/v2/trending/'
langs_str = 'https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml'
foldername = "json"
filename = "trending.json"
# folder_path = "./" + foldername + "/"
file_path = "./" + filename

def git_pull():
    print("prepare to do 'git pull'")
    cmd = ['git', 'pull']
    p = subprocess.Popen(cmd, cwd="./")
    p.wait()

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
    git_pull()
    git_add()
    git_commit()
    git_push()


def url_open(url):
    if not ('http' in url):
        url = 'http://' + url

    print('url is :' + url)
    req = request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0')
    response = request.urlopen(req)
    return response.read()

def scrape(language, file_path):

    HEADERS = {
        'User-Agent'		: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept'			: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding'	: 'gzip,deflate,sdch',
        'Accept-Language'	: 'zh-CN,zh;q=0.8'
    }
    print("begin request")
    url = 'https://github.com/trending/{language}'.format(language=language)
    r = requests.get(url, headers=HEADERS)
    assert r.status_code == 200

    # print(r.encoding)

    d = pq(r.content)
    items = d('ol.repo-list li')

    # codecs to solve the problem utf-8 codec like chinese
    with codecs.open(file_path, "w", encoding='utf-8') as f:

        arr = []
        for item in items:
            i = pq(item)
            title = i("h3 a").text()
            language = i("div.f6 span[itemprop='programmingLanguage']").text()
            star = i("div.f6 svg.octicon-star").closest("a").text()
            fork = i("div.f6 svg.octicon-repo-forked").closest("a").text()
            description = i("p.col-9").text()
            hrefurl = i("h3 a").attr("href")
            urllist = hrefurl.split('/')
            owner = urllist[1]
            name = urllist[2]
            full_name = owner + '/' + name
            url = "https://github.com" + hrefurl
            # ownerImg = i("p.repo-list-meta a img").attr("src")
            # print(ownerImg)


            data = {}
            data["name"] = name
            data["full_name"] = full_name
            data["forks_count"] = fork
            data["stargazers_count"] = star
            data["language"] = language
            data["repositoryDescription"] = description

            arr.append(data)

        print("get json data, ready write to file 'trending.json'")
        f.write(json.dumps(arr, indent=4, ensure_ascii=False))


def save_file():
    scrape("", file_path)

    getColors()

    file_handle()


def trending():
    if not os.path.exists(foldername):
        os.mkdir(foldername)  
        print('create folder success', foldername)

    os.chdir(foldername)
    folder_top = os.getcwd()
    print(folder_top)
    save_file()


# ----------------------------------------------
def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python Orderered Dictionary.
    """
    class OrderedLoader(Loader):
        pass
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        lambda loader, node: object_pairs_hook(loader.construct_pairs(node)))

    return yaml.load(stream, OrderedLoader)


def order_by_keys(dict):
    """
    Sort a dictionary by keys, case insensitive ie [ Ada, eC, Fortran ]
    Default ordering, or using json.dump with sort_keys=True, produces
    [ Ada, Fortran, eC ]
    """
    from collections import OrderedDict
    return OrderedDict(sorted(dict.items(), key=lambda s: s[0].lower()))


def getFile(url):
    """
        Return the URL body, or False if page not found

        Keyword arguments:
        url -- url to parse
    """
    try:
        r = request.urlopen(url)
    except:
        sys.exit("Request fatal error :  %s" % sys.exc_info()[1])
    
    if r.status != 200:
        return False

    return r.read()


def write_json(text, filename='colors.json'):
    """
    Write a JSON file from a dictionary
    """
    with open(filename, 'w') as f:
        f.write(json.dumps(text, indent=4) + '\n')


def getColors():
    print("geting list of language")
    yml = getFile(langs_str)
    langs_yml = ordered_load(yml)
    langs_yml = order_by_keys(langs_yml)
    # List construction done, count keys
    lang_count = len(langs_yml)
    print("Found %d languages" % lang_count)

    # Construct the wanted list
    langs = OrderedDict()
    for lang in langs_yml.keys():
        if ("type" not in langs_yml[lang] or
                    "color" in langs_yml[lang] or
                    langs_yml[lang]["type"] == "programming"):
            print("   Parsing the color for '%s' ..." % (lang))
            langs[lang] = OrderedDict()
            langs[lang]["color"] = langs_yml[lang]["color"] if "color" in langs_yml[lang] else None
            langs[lang]["url"] = "https://github.com/trending?l=" + (
            langs_yml[lang]["search_term"] if "search_term" in langs_yml[lang] else lang)
            langs[lang]["url"] = langs[lang]["url"].replace(' ', '-').replace('#', 'sharp')
    print("Writing a new JSON file ...")
    write_json(langs)

    print("All done!")


if __name__ == '__main__':
    trending()

