---
layout: post
title: "工作中遇到的问题及解决方案"
excerpt: "平时碰到的问题，解决后记录"
categories: [Work]
tags: [OC, Mac, Swift, Work, Problem]
date: 2014-10-23 
modified: 
comments: true
---

## 1.ssh登录

问题：用ssh登录一个机器（换过ip地址），提示输入yes后，屏幕不断出现y，只有按ctrl + c结束。出现错误：

`The authenticity of host 192.168.0.xxx can't be established.`

`ssh  -o StrictHostKeyChecking=no  192.168.0.xxx`　就OK了。

某天机器又换IP了，ssh又报错了：

```
mmt@FS01:~$ ssh  -o StrictHostKeyChecking=no  192.168.0.130
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!    @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that the RSA host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
fe:d6:f8:59:03:a5:de:e8:29:ef:3b:26:6e:3d:1d:4b.
Please contact your system administrator.
Add correct host key in /home/mmt/.ssh/known_hosts to get rid of this message.
Offending key in /home/mmt/.ssh/known_hosts:38
Password authentication is disabled to avoid man-in-the-middle attacks.
Keyboard-interactive authentication is disabled to avoid man-in-the-middle attacks.
Permission denied (publickey,password).
```

注意这句`Add correct host key in /home/mmt/.ssh/known_hosts to get rid of this message.`，我们按提示输入：`mv  /home/mmt/.ssh/known_hosts known_hosts.bak`，再ssh，`ssh  -o StrictHostKeyChecking=no  192.168.0.130`,可以了。

## 2.Xcode更新后SVN失败

错误：

```
xcrun: error: active developer path ("/Applications/Xcode.app/Contents/Developer/") does not exist, use `xcode-select --switch path/to/Xcode.app` to specify the Xcode that you wish to use for command line developer tools (or see `man xcode-select`)
```

出现这个的原因，是因为更新了Xcode软件，在更新svn时，找不到这个软件，导致的。（或者多个Xcode）

解决办法就是：将Xcode的路径，重新设置一下。

sudo xcode-select --switch “Xcode的path，直接在应用程序里面找到Xcode，拖拽到这里即可”.

## 3.如下图

![问题3](/article/problem/p3.png)













