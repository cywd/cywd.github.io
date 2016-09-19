---
layout: post
title: "iOS开发的一些Tips"
excerpt: "iOS开发的一些Tips，记录下便于日后查看"
categories: [OC, Tips]
tags: [OC, Tips]
date: 2014-10-23 
modified: 
comments: true
---

* TOC
{:toc}


## 1.如何快速的查看一段代码的执行时间。

```objective-c
#define TICK   NSDate *startTime = [NSDate date]
#define TOCK   NSLog(@"Time: %f", -[startTime timeIntervalSinceNow])
// 使用时
TICK
// do your work here
TOCK
```

## 2.当view旋转缩放的时候出现锯齿

使用`layer`的`allowsEdgeAntialiasing`属性消除锯齿

```objective-c
self.layer.allowsEdgeAntialiasing = YES;
// 设置对应view的这个属性
```

## 3.UIContentMode的显示方式，备忘

引用网上的图，不知道原作者是谁。

![引用网上的图](/img/article/tips/3.jpg)

## 4.统计项目中代码行数  

终端cd到相应目录，执行

```shell
find . "(" -name ".m" -or -name ".mm" -or -name ".cpp" -or -name ".h" -or -name ".rss" -or -name ".xib"  ")" -print | xargs wc -l
```
## 5.宏的##和#作用

在宏里面, ##的作用:连接2个标识符

```objective-c
#define method(name) - (void)load##name {}method(abc)  
//- (void)loadabc {}method(ddd)  
//- (void)loadddd {}method(ttt)  
//- (void)loadttt {}
```

在宏里面, #的作用:给右边的标识符加上双引号""

```c
#define test(name) @#nametest(abc) // @"abc"
```