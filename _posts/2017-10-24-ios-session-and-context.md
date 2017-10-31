---
layout: post
title: ios session和context 关系简述
excerpt: "ios session和context 关系简述"
categories: [iOS]
tags: [iOS]
date: 2017-10-24
comments: true
---

* TOC
{:toc}
---

在iOS框架中，凡是带session或者context后缀的，这种类一般自己不干活，作用一般都是两个：

1.管理其他类，帮助他们搭建沟通桥梁，好处就是解耦 

2.负责帮助我们管理复杂环境下的内存

context与session不同之处是：

一般与硬件打交道，例如摄像头捕捉ARSession，网卡的调用NSURLSession等使用的都是session后缀。

没有硬件参与，一般用context，如绘图上下文，自定义转场上下文等。
