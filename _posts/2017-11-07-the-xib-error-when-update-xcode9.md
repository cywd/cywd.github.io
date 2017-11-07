---
layout: post
title: 升级到Xcode9后Xib报错问题的解决
excerpt: "升级到Xcode9后Xib报错问题的解决"
categories: [iOS]
tags: [iOS]
date: 2017-11-07
comments: true
---

* TOC
{:toc}
---

在升级到Xcode9 遇到以下错误：`Compiling IB documents for earlier than iOS 7 is no longer supported`

将`Builds for` 选项设置为iOS10 以后就OK了。

参考：[stackoverflow](https://stackoverflow.com/questions/44429415/illegal-configuration-compiling-ib-documents-for-earlier-than-ios-7-is-no-longe)