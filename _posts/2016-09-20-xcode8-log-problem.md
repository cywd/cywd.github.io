---
layout: post
title: "Xcode8打印的问题"
excerpt: "升级Xcode8正式版以后,下方控制台打印出现了两个问题，一是会打印出来多余的调试信息，二是NSLog打印很长的JSON会发生显现不全的问题"
categories: [Xcode]
tags: [Xcode, Tips]
date: 2016-09-20
comments: true
---

* TOC
{:toc}
---

## 1.打印出来多余的调试信息

多出来的信息是什么，参考[活动追踪](https://objccn.io/issue-19-5/)

去掉的方法：

`Edit Scheme-> Run -> Arguments, 在Environment Variables里边添加 OS_ACTIVITY_MODE ＝ disable`

## 2.NSLog打印很长的JSON会发生显现不全的问题

目前的问题发生在Xcode8+iOS10的真机上。待解决。

目前的代替方案是 command + /  打开控制台进行查看，或者打断点，po 出来，实测 po 出来的是完整的。
