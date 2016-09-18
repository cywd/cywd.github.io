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

* TOC
{:toc}

## 1.ssh登录

问题：用ssh登录一个机器（换过ip地址），提示输入yes后，屏幕不断出现y，只有按ctrl + c结束。出现错误：

`The authenticity of host 192.168.0.xxx can't be established.`

`ssh  -o StrictHostKeyChecking=no  192.168.0.xxx`　就OK了。

某天机器又换IP了，ssh又报错了：

```
~ ssh -o StrictHostKeyChecking=no 192.168.0.130
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!    @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that the RSA host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
fe:d6:f8:59:03:a5:de:e8:29:ef:3b:26:6e:3d:1d:4b.
Please contact your system administrator.
Add correct host key in /home/cyrill/.ssh/known_hosts to get rid of this message.
Offending key in /home/cyrill/.ssh/known_hosts:38
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

![问题3](/img/article/problem/p3.png)

由于是从外包接手的项目，出现了这个问题。

意思是开启配置了Xcode中自带的Git,但是仓库路径无效,应该是仓库在别的电脑上.
结局办法:1.直接忽略.  2. 把工程下的.git删掉.

## 4.Xcode错误-`Could not launch app - No such file or directory Error.`

蛋疼的一个Xcode bug，基本上应该不是工程本身问题。
解决方法：
1、拔掉设备，删除之前Build的内容
2、退出Xcode，不是关闭窗口
3、删除那个/Users/XXX/Library/Developer/Xcode/DerivedData/XXX-grgrmtzqajhyqgghabyjttajwbsm文件夹
4、启动XCode连接设备，现在应该OK了

## 5.支付宝遇到的问题

![问题5](/img/article/problem/p5.png)

## 6.Xcode证书问题

![问题6](/img/article/problem/p6.png)

重新配置开发者中心的证书相关 或者  导入合适的 p12文件.

## 7.如下图

![问题7](/img/article/problem/p7.png)

系统的按钮偏移，说明的某个类扩展修改了系统的东西,找到对应的类扩展修改到正确的位置就好了。

## 8.Xcode 删除文件后编译出现的missing file的警告

进入“Missing File”对应的目录进行删除即可。

1.由于使用SVN导致的，可进行如下操作：

```
# cd /Users/lichunyang/Desktop/vKan/Code_1_0/VKan/VKan/ViewControllers/
# svn delete CYUploadPhotoViewController.m
```

2.由于使用GIT导致的，可进行如下操作：

```
# cd ~CYUploadPhotoViewController.m
# git rm CYUploadPhotoViewController.m
```




