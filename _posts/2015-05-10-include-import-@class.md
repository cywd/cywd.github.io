---
layout: post
title: "关于#include "", #include <>, #import "",#import <>, @import, @class"
excerpt: ""
categories: [OC]
tags: [OC]
date: 2015-05-10
modified: 
comments: true
---

* TOC
{:toc}


## #include " " 和 #include <>

`#include "xxx.h"`:它用于对系统自带的头文件的引用,编译器会在系统文件目录下去查找该文件.

`#include <xxx.h>`用户自定义的文件用双引号引用,编译器首先会在用户目录下查找,然后到安装目录中查找,最后在系统文件中查找。

**在使用`#include`的时候要注意处理重复引用 *(这也是objc中#include与#import的区别)***

这样处理在编译时就不会有重复引用的错误出现

```
#ifndef _CLASSC_H

#define _CLASSC_H

#include "ClassC"

#endif
```



## #import " " 和 #import < >

`#import`大部分功能和`#include`是一样的,但是他处理了重复引用的问题,我们在引用文件的时候不用再去自己进行重复引用处理.

**`#import`比起`#include`的好处就是不会引起交叉编译。**



## @import 

iOS7新关键字。

使用`@import`的最大好处之一是当需要使用某个苹果自己的框架时，再也不需要在项目的`setting`中做 "点击'+'号按钮搜索依赖框架添加" 这样的操作了，`@import`内部会自动实现这个过程。这样我们就可以使用代码完成以前需要在图形界面完成的动作。苹果又为开发者做出了改进。但是目前使用`@import`仅适用于苹果自己的框架，当在项目中想使用`@import`导入自己搭建的框架或者第三方框架时，是无效的。

以前写程序导入系统头文件的时候都这么写`#import , `现在你多了一种选择， 你可以这么写:

`@import Cocoa;` 并且免去了添加框架的操作.

实际开发中上可能并不需要使用`@import`关键字。如果你选择使用"modules"(Xcode5中默认开启)，所有的`#import` 和 `#include`指令都会自动映射使用`@import`。



## @class 

`import`会包含这个类的所有信息，包括实体变量和方法（.h文件中），而`@class`只是告诉编译器，其后面声明的名称是类的名称，至于这些类是如何定义的，后面会再告诉你。

在头文件中， 我们一般只需要知道被引用的类的名称就可以了。 不需要知道其内部的实体变量和方法，所以在头文件中一般使用`@class`来声明这个名称是类的名称。 而在实现类里面，因为会用到这个引用类的内部的实体变量和方法，所以需要使用`#import`来包含这个被引用类的头文件。

## 总结

一般来说，导入`objective-c`的头文件时用`#import`，包含`c/c++`头文件时用`#include`。

头文件里一般使用'@class'。引入系统的头文件时可以使用'@import'。

## 参考

[(http://stackoverflow.com/questions/18947516/import-vs-import-ios-7)](http://stackoverflow.com/questions/18947516/import-vs-import-ios-7)