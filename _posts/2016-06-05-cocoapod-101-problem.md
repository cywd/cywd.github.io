---
layout: post
title: "CocoaPods升级1.0.1后"
excerpt: "出现类似 The dependency `AFNetworking (~> 3.1.0)` is not used in any concrete target. 的问题。"
categories: [cocoaPods]
tags: [cocoaPods]
date: 2016-06-05 
modified: 
comments: true
---

* TOC
{:toc}
---

## 原因

cocoaPods升级后，Podfile文件的内容格式要求发生了变化，必须指出指出所用第三方库的target。

## 解决

修改Podfile的内容

修改之前

```
platform:ios,'7.0'

pod 'AFNetworking', '~> 3.1.0'
```

修改之后

```
platform:ios,'7.0'

target "PodDemo" do
pod 'AFNetworking', '~> 3.1.0'
end
```