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
## 6.忽略未使用变量的警告

```objective-c
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wunused-variable"
	UIView *testView = [[UIView alloc] init];
#pragma clang diagnostic pop
```

## 7.忽略方法未声明警告

```objective-c
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wundeclared-selector"
    
    UIPanGestureRecognizer *panGesture = [[UIPanGestureRecognizer alloc] initWithTarget:self action:@selector(handleNavigationTransition:)];
    
#pragma clang diagnostic pop
```

## 8.在APPDelegate中禁用第三方键盘

```objective-c
#pragma mark - 禁用第三方键盘
- (BOOL)application:(UIApplication *)application shouldAllowExtensionPointIdentifier:(UIApplicationExtensionPointIdentifier)extensionPointIdentifier {
    return NO;
}
```

## 9.判断是模拟器还是真机

```objective-c
#if TARGET_IPHONE_SIMULATOR //模拟器

#elif TARGET_OS_IPHONE //真机

#endif
```

