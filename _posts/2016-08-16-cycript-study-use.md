---
layout: post
title: Cycript的学习和使用
excerpt: "ios逆向里的Cyript"
categories: [iOS逆向]
tags: [iOS逆向，Cyript]
date: 2016-08-16
comments: true
---

* TOC
{:toc}
---

### 前言

知识学会很久了，苦于一直没有能越狱的设备，刚好PP盘古刚刚发布了iOS9.3.3越狱，这就把我的iPad给越狱了，记录实践一下。

###简介
`Cycript`是由`saurik`推出的一款脚本语言，是混合了`objective-c`与`javascript`语法的一个工具，让开发者在命令行下和应用交互，在运行时查看和修改应用。
###基本使用
安装：可以在`Cydia`里搜索`cycript`来下载安装，可以配合`MTerminal`使用。
使用：可以通过`MTerminal`，后者`ssh`到`iOS`中执行。
ssh到笔者的iPad：

![Snip20160816_11.png](/img/article/cycript/Snip20160816_8.png)

输入`cycript`，出现 `cy#`提示符，说明已经成功启动`Cycript`。

![Snip20160816_11.png](/img/article/cycript/Snip20160816_6.png)

`control+D`，来退出`Cydia`.

下面以SpringBoard为例
找到SpringBoard进程
![Snip20160816_11.png](/img/article/cycript/Snip20160816_9.png)
获取到进程的id是 1181 ,然后用 `cycript - p`或`cycript -p` 命令注入这个进程
![Snip20160816_11.png](/img/article/cycript/Snip20160816_10.png)
想要在SpringBoard界面弹出一个提示框，用cycript的话，只要两句代码就可以了，而且是实时注入的。

```
cy# alertView = [[UIAlertView alloc] initWithTitle:@"test" message:@"Cyrill" delegate:nil cancelButtonTitle:@"OK" otherButtonTitles:nil]
#"<UIAlertView: 0x156f9f0a0; frame = (0 0; 0 0); layer = <CALayer: 0x156f96fc0>>"
cy# [alertView show]
```
知道内存地址，获取对象,比如刚刚生成的UIAlertView对象的内存地址是 0x156f9f0a0

```
cy# [#0x156f9f0a0 show]
```
一样可以弹出提示框.


###问题
~~笔者在使用`Cycript`的过程中发现了个问题，似乎是在iOS9.3.3以后才存在。下面是问题：
![Snip20160816_11.png](/img/article/cycript/Snip20160816_11.png)
从AppStore中下载的App，无法被注入，进入`cy#`，从越狱市场下载的App和系统自带的都可以被注入。~~

最近这个问题又不见了，原因还不清楚。