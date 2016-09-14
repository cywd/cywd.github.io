---
layout: post
title: "Python爬取豆瓣妹子图片的尝试"
excerpt: "尝试用python爬取图片"
categories: [Python]
tags: [Python, 爬虫]
date: 2016-04-02 
modified: 
comments: true
---

## 尝试用python爬取图片

```python
#!/usr/bin/python
#-*- coding: utf-8 -*-
#encoding=utf-8

import urllib2
import urllib
import os
from bs4 import BeautifulSoup

def getAllImageLink(index):
    str = 'http://www.dbmeinv.com/?pager_offset=%s' % index
    html = urllib2.urlopen(str).read()
    soup = BeautifulSoup(html, "lxml")
    liResult = soup.findAll('li', attrs={"class": "span3"})
    # print liResult

    i=0

    for li in liResult:
        i = i+1
        imageEntityArray = li.findAll('img')
        
        for image in imageEntityArray:
            link = image.get('src')
            imageName = image.get('title')
            # filesavepath = '/Users/cyrill/Desktop/DBMeiNv/%s.jpg' % imageName
            filesavepath = '/Users/cyrill/Desktop/DBMeiNv/%s-%s.jpg' %(index, i)
            urllib.urlretrieve(link, filesavepath)
            # print filesavepath

if __name__ == '__main__':
    for index in range(1, 10, 1):
        getAllImageLink(index)
```



