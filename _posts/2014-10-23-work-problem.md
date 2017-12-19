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
---

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

注意这句`Add correct host key in /home/cyrill/.ssh/known_hosts to get rid of this message.`，我们按提示输入：`mv  /home/cyrill/.ssh/known_hosts known_hosts.bak`，再ssh，`ssh  -o StrictHostKeyChecking=no  192.168.0.130`,可以了。

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
解决办法:1.直接忽略.  2. 把工程下的.git删掉.

## 4.Xcode错误-`Could not launch app - No such file or directory Error.`

蛋疼的一个Xcode bug，基本上应该不是工程本身问题。
解决方法：
1、拔掉设备，删除之前Build的内容
2、退出Xcode，不是关闭窗口
3、删除那个/Users/XXX/Library/Developer/Xcode/DerivedData/XXX-grgrmtzqajhyqgghabyjttajwbsm文件夹
4、启动Xcode连接设备，现在应该OK了

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

## 9.imageNamed和imageWithContentsOfFile

读取图片有两种方式

1.`imageNamed`,其参数为图片的名字；

2.`imageWithContentsOfFile`，其参数是图片文件的路径。

二者的区别：

1.`imageNamed`: 这个方法用一个指定的名字在系统缓存中查找并返回一个图片对象如果它存在的话。如果缓存中没有找到相应的图片，这个方法从指定的文档中加载然后缓存并返回这个对象。因此`imageNamed`的优点是当加载时会缓存图片。所以当图片会频繁的使用时，那么用`imageNamed`的方法会比较好。

2.`imageWithContentsOfFile`：仅加载图片，图像数据不会缓存。因此对于较大的图片以及使用情况较少时，那就可以用该方法，降低内存消耗。

## 10.为什么ViewController does not accept kUTTypeText?  

需要包含  MobileCoreServices

```objective-c
#import <MobileCoreServices/MobileCoreServices.h>
```

## 11.performSelector:withObject:afterDelay:调用没有作用的问题及解决方法  

`performSelector:withObject:afterDelay:`和`[NSTimer timerWithTimeInterval:invocation:repeats:] ` 都要保证在主线程中.

## 12.No architectures to compile for (ONLY_ACTIVE_ARCH=YES, active arch=x86_64, VALID_

错误代码：`No architectures to compile for (ONLY_ACTIVE_ARCH=YES, active arch=x86_64, VALID_ARCHS=armv7 armv7s)`

xcodebuild 这个target的时候命令行报错。

![问题6](/img/article/problem/p12.jpg)

还有解决办法：

[来自stackoverflow](http://stackoverflow.com/questions/12889065/no-architectures-to-compile-for-only-active-arch-yes-active-arch-x86-64-valid)

## 13.集成支付宝报错`file not found`

在`Search Paths`里加上对应的路径

## 14.报警告：`warning: All interface orientations must be supported unless the app requires full screen.`

勾选

![问题14](/img/article/problem/p14.png)

## 15.报错`fatal error: too many errors emitted, stopping now`,提示`UIKit.h`等找不到

原因应该是设置了`prefix header = YES` 。

如果是需要`pch`的, 用`Cy-4AH`忽略它， `ifdef __OBJC__`放在`pch`里。

## 16.PCH位置

PCH 添加
 $(SRCROOT)/PCHDemo/PrefixHeader.pch

## 17.error in __connection_block_invoke_2: Connection interrupted

在执行异步任务的时候，切到后台，再回来就会报这个错误。意思是异步任务执行失败。

## 18.真机调试提示`.app: resource fork, Finder information, or similar detritus not allowed`

分别进入工程目录与DerivedData目录；执行 "xattr -rc ."；解决

## 19.iOS使用到OC与C++混编的时候出现Expected unqualified-id

```
Expected unqualified-id 
```

解决方法：

修改你的.pch(项目头文件) 

将所有的import与define的代码全部放在**#ifdef OBJC**与**#endif** 之间

```
#ifdef __OBJC__

// some ......

#endif // OC的头文件
```

## 20.免费App ID真机调试报错`The maximum number of apps for free development profiles has been reached.`

苹果免费App ID只能运行2个应用程序,当调试第三个的时候就会报这个错误,必须把之前的应用程序删除,才能调试新的。

可以在移动端删除或者`command+shift+2`，进入Device，选择你的设备，删除已安装的程序。

## 21.objc_msgSend 报错`Too many arguments to function call, expected 0, have 3`

查到一种解决方案是选中项目 - `Project` - `Build Settings` - `ENABLE_STRICT_OBJC_MSGSEND`  将其设置为 `NO` 即可

## 22.ios真机调试错误`Reason: no suitable image found. Did find:xxxxxxxx`

原因是：因为你的证书在上一次安装到现在安装失败这段时间里证书被重置过，那么两次的签名就不一样了，而你的Bundle identifier ID又是同一个，所以这次安装会失败。

解决：把手机上相应的APP删除，并把项目 clean下，然后重新运行，就可以成功运行了。

