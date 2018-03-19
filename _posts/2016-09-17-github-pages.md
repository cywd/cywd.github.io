---
layout: post
title: GitHub Pages 如何绑定域名
excerpt: "其实主要是谈纯中文域名的绑定"
categories: [Git]
tags: [Git, 域名]
date: 2016-09-17
comments: true
---

* TOC
{:toc}
---

## 前言

今天买了个域名，人生第一个纯中文域名。在GitHub Pages绑定新域名的时候遇到了一些问题，在此记录下。由于我的中文域名有些特别的意义，所以一下以`回忆.我爱你`这个域名作为代替，我爱你的纯中文域名。

## 正文

关于怎么在`GitHub`建立自己的博客就不说了，我这边是用的`Jekyll`搭建博客。

我的域名是在阿里云上注册购买的，[disqus](http://disqus.com/) 也有很多人推荐的。

绑定域名，其中一种方法是设置两个A记录。分别是`@`和`www`，IP地址填`GitHub Pages`的IP地址。

我采用的是另外一种方法。

CNAME

其实`GitHub`官方已经讲得很清楚了。在仓库根目录建一个`CNAME`文件，里面填上你的新域名。（不要`http://` 或 `https://`），在购买的域名解析那里加两项，type为`CNAME`的记录，分别是`@`和`www`，后面的地址就填`GitHub Pages`的地址（同样不要不要`http://` 或 `https://`）。

英文的域名就不说了，没有什么问题过个10分钟左右就绑定好了，访问新的域名就可以去到`GitHub Pages `的博客了。

ps: 拿  `回忆.我爱你` 做例子

不过到了中文域名就出问题了，首先，`CNAME`里面直接填`回忆.我爱你`的话，`GitHub`是不识别这是一个合法的域名的。

![回忆.我爱你Safari](/img/article/GitHubPages/safari.png)

我用safari去访问`回忆.我爱你`结果出现这样的提示，我就想，后面这一串`xn--zbs20s.xn--6qq986b3xl`是不是中文域名对应的非中文地址呢。既然`GitHub`无法解析中文域名，那这个呢`xn--zbs20s.xn--6qq986b3xl`，于是我就在`CNAME`里填上了这个`xn--zbs20s.xn--6qq986b3xl`，10分钟之后，恩，Ok了。

## 后记

中文域名确实比较蛋疼，即使我通过这种方式绑定了中文域名，不过`GitHub`还是会有个警告提示。

![警告提示](/img/article/GitHubPages/waring.png)