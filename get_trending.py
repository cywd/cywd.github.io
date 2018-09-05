# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib import request
import os
import subprocess
import sys
import json
import yaml
from collections import OrderedDict

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


def save_file():
    print("begin request")
    json = url_open(url_str)
    print("get json data, ready write to file 'trending.json'")
    with open(file_path, 'wb') as f:
        f.write(json)
        f.close()
        print("write file success")

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

