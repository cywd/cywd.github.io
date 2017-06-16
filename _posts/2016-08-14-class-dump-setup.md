---
layout: post
title: "class-dump的安装"
excerpt: "class-dump的安装"
categories: [iOS逆向]
tags: [iOS逆向]
date: 2016-08-14 
modified: 
comments: true
---

* TOC
{:toc}
---

# 简介
*class-dump is a command-line utility for examining the Objective-C segment of Mach-O files. It generates declarations for the classes, categories and protocols. This is the same information provided by using 'otool -ov', but presented as normal Objective-C declarations.*

这是class-dump的官方解释，我们用的最多就是做iOS的逆向工程。class-dump，是可以把Objective-C运行时的声明的信息导出来的工具。其实就是可以导出.h文件。用class-dump可以把未经加密的app的头文件导出来。

官方网址：[http://stevenygard.com/projects/class-dump/](http://stevenygard.com/projects/class-dump/)

# 安装
class-dump的下载地址：[http://stevenygard.com/download/class-dump-3.5.tar.gz](http://stevenygard.com/download/class-dump-3.5.tar.gz)

点击下载后解压后会有class-dump和源码文件。将class-dump 复制到/usr/bin/class-dump。如果是OS X 10.11，因为没有/usr/bin文件夹的写权限，所以将class-dump复制到/usr/local/bin/class-dump即可。

同时打开Terminal，执行命令赋予其执行权限：
`sudo chmod 777 /usr/bin/class-dump`

![Snip20160814_3.png](http://upload-images.jianshu.io/upload_images/567057-c798c82bd0cbda3c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)