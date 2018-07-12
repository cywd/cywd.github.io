---
layout: post
title: "QuartzCore/CAGradientLayer.h"
excerpt: "QuartzCore/CAGradientLayer.h"
categories: [OC, QuartzCore]
tags: [OC, QuartzCore]
date: 2016-04-16 
modified: 
comments: true
---

* TOC
{:toc}
---

# 整体描述

`CAGradientLayer`常见应用于锁屏底部闪烁的滑动来解锁。`CAGradientLayer`用来绘制渐变色，指定几个颜色值、渐变结束位置，就能在layer中绘制出渐变效果。

# 源码

```objective-c
/* CoreAnimation - CAGradientLayer.h

   Copyright (c) 2008-2016, Apple Inc.
   All rights reserved. */

/* The gradient layer draws a color gradient over its background color,
 * filling the shape of the layer (i.e. including rounded corners). */

#import <QuartzCore/CALayer.h>
#import <Foundation/NSArray.h>

NS_ASSUME_NONNULL_BEGIN

CA_CLASS_AVAILABLE (10.6, 3.0, 9.0, 2.0)
@interface CAGradientLayer : CALayer

/* The array of CGColorRef objects defining the color of each gradient
 * stop. Defaults to nil. Animatable. */
// 颜色的集合
@property(nullable, copy) NSArray *colors;

/* An optional array of NSNumber objects defining the location of each
 * gradient stop as a value in the range [0,1]. The values must be
 * monotonically increasing. If a nil array is given, the stops are
 * assumed to spread uniformly across the [0,1] range. When rendered,
 * the colors are mapped to the output colorspace before being
 * interpolated. Defaults to nil. Animatable. */
// 颜色分割线，颜色分配严格遵守Layer的坐标系统,locations,startPoint,endPoint都是以Layer坐标系统进行计算的.而locations并不是表示颜色值所在位置,它表示的是颜色在Layer坐标系相对位置处要开始进行渐变颜色了.
@property(nullable, copy) NSArray<NSNumber *> *locations;

/* The start and end points of the gradient when drawn into the layer's
 * coordinate space. The start point corresponds to the first gradient
 * stop, the end point to the last gradient stop. Both points are
 * defined in a unit coordinate space that is then mapped to the
 * layer's bounds rectangle when drawn. (I.e. [0,0] is the bottom-left
 * corner of the layer, [1,1] is the top-right corner.) The default values
 * are [.5,0] and [.5,1] respectively. Both are animatable. */
// 起始点
@property CGPoint startPoint;
// 结束点
@property CGPoint endPoint;

/* The kind of gradient that will be drawn. Currently the only allowed
 * value is `axial' (the default value). */

@property(copy) NSString *type;

@end

/** `type' values. **/

CA_EXTERN NSString * const kCAGradientLayerAxial
    CA_AVAILABLE_STARTING (10.6, 3.0, 9.0, 2.0);

NS_ASSUME_NONNULL_END

```

# 应用

```objective-c
CAGradientLayer *gradientLayer = [CAGradientLayer layer];
gradientLayer.backgroundColor = [UIColor blueColor].CGColor;
gradientLayer.frame    = (CGRect){CGPointZero, CGSizeMake(200, 200)};
gradientLayer.position = self.view.center;
// 颜色分配
gradientLayer.colors = @[(__bridge id)[UIColor redColor].CGColor,
                      (__bridge id)[UIColor yellowColor].CGColor,
                      (__bridge id)[UIColor blueColor].CGColor];
gradientLayer.locations = @[@(0.25), @(0.5), @(0.75)];
// 起始点
gradientLayer.startPoint = CGPointMake(0, 0);
// 结束点
gradientLayer.endPoint   = CGPointMake(1, 0);
[self.view.layer addSublayer:gradientLayer];
```

