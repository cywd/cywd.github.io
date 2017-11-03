---
layout: post
title: UIView的exclusiveTouch属性
excerpt: "UIView的exclusiveTouch属性"
categories: [iOS]
tags: [iOS]
date: 2017-11-02
comments: true
---

* TOC
{:toc}
---



## 简介

`ExclusiveTouch`是`UIView`的一个属性，默认为NO（不互斥），设置`UIView`接收手势的互斥性为YES，可以防止多个响应区域被“同时”点击，“同时”响应的问题，从而避免bug。具体来说，就是当设置了`exclusiveTouch=YES`的`UIView`是事件的第一响应者，那么到你的所有手指离开前，其他的视图`UIView`是不会响应任何触摸事件的，对于多点触摸事件，这个属性就非常重要，值得注意的是：手势识别（`GestureRecognizers`）会忽略此属性。

## 使用

可以通过 `[[UIView appearance] setExclusiveTouch:YES]; `这样调用。
`UIImageView` ，`UILabel`等，都可以添加手势，响应方式和`UIButton`相同。
全局设置响应区域的点击手势的互斥，是有效的。
但使用此方法时，在`iOS 8.0 ~ iOS 8.2`（目前仅在该版本下发现问题）下会引起崩溃。

## 用途

举个例子：在出现`UICollectionView`之前，我们如果要实现类似`GridView`的控件，通常做法是在`UITableView`的`cell`上加载几个子视图，来模拟实现`GridView`视图，但对于每一个子视图来说，就需要使用`exclusiveTouch`，否则当同时点击多个子视图，那么会触发每个子视图的事件。导致多次跳转等情况的发生。
