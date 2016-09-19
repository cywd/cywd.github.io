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

