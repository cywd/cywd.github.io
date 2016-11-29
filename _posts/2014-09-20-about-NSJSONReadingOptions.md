---
layout: post
title: "关于NSJSONReadingOptions参数的含义"
excerpt: "关于NSJSONReadingOptions参数的含义"
categories: [OC, Tip]
tags: [OC, Mac, Tip]
date: 2014-09-20 
modified: 
comments: true
---

* TOC
{:toc}
---

## 1.NSJSONReadingOptions

```
enum { 
    NSJSONReadingMutableContainers = (1UL << 0), 
    NSJSONReadingMutableLeaves = (1UL << 1), 
    NSJSONReadingAllowFragments = (1UL << 2) 
}; 
typedef NSUInteger NSJSONReadingOptions; 
```

## 2.解释

### NSJSONReadingMutableContainers：

返回可变容器，NSMutableDictionary或NSMutableArray。 

### NSJSONReadingMutableLeaves：

返回的JSON对象中字符串的值为NSMutableString，目前在iOS 7上测试不好用，应该是个bug，参见： 
[http://stackoverflow.com/questions/19345864/nsjsonreadingmutableleaves-option-is-not-working](http://stackoverflow.com/questions/19345864/nsjsonreadingmutableleaves-option-is-not-working)  


### NSJSONReadingAllowFragments：

允许JSON字符串最外层既不是NSArray也不是NSDictionary，但必须是有效的JSON Fragment。例如使用这个选项可以解析 @“123” 这样的字符串。参见： 
[http://stackoverflow.com/questions/16961025/nsjsonserialization-nsjsonreadingallowfragments-reading](http://stackoverflow.com/questions/16961025/nsjsonserialization-nsjsonreadingallowfragments-reading)