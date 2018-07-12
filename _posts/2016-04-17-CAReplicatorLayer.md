---
layout: post
title: "QuartzCore/CAReplicatorLayer.h"
excerpt: "QuartzCore/CAReplicatorLayer.h"
categories: [OC, QuartzCore]
tags: [OC, QuartzCore]
date: 2016-04-17  
modified: 
comments: true
---

* TOC
{:toc}
---

# 整体描述

`CAReplicatorLayer`创建`layer`和它的`sublayer`的多个副本，副本可以设置`transform`来变形，或者设置颜色、透明度的变化。

`CAReplicatorLaye`r的目的是为了高效生成许多相似的图层。它会绘制一个或多个图层的子图层，并在每个复制体上应用不同的变换。

`CAReplicatorLayer` 它独有的特性，其子类具有相同的属性。

# 源码

```objective-c
/* CoreAnimation - CAReplicatorLayer.h

   Copyright (c) 2008-2016, Apple Inc.
   All rights reserved. */

#import <QuartzCore/CALayer.h>

NS_ASSUME_NONNULL_BEGIN

/* The replicator layer creates a specified number of copies of its
 * sublayers, each copy potentially having geometric, temporal and
 * color transformations applied to it.
 *
 * Note: the CALayer -hitTest: method currently only tests the first
 * instance of z replicator layer's sublayers. This may change in the
 * future. */

CA_CLASS_AVAILABLE (10.6, 3.0, 9.0, 2.0)
@interface CAReplicatorLayer : CALayer

/* The number of copies to create, including the source object.
 * Default value is one (i.e. no extra copies). Animatable. */

@property NSInteger instanceCount; // 拷贝图层的次数,包括其所有的子图层,默认值是1,也就是没有任何子图层被复制

/* Defines whether this layer flattens its sublayers into its plane or
 * not (i.e. whether it's treated similarly to a transform layer or
 * not). Defaults to NO. If YES, the standard restrictions apply (see
 * CATransformLayer.h). */

@property BOOL preservesDepth; // 如果设置为YES,图层将保持于CATransformLayer类似的性质和相同的限制

/* The temporal delay between replicated copies. Defaults to zero.
 * Animatable. */

@property CFTimeInterval instanceDelay; // 在短时间内的复制延时,一般用在动画上(支持动画的延时)

/* The matrix applied to instance k-1 to produce instance k. The matrix
 * is applied relative to the center of the replicator layer, i.e. the
 * superlayer of each replicated sublayer. Defaults to the identity
 * matrix. Animatable. */

@property CATransform3D instanceTransform; // 复制图层在被创建时产生的和上一个复制图层的位移(位移的锚点时CAReplicatorlayer的中心点)

/* The color to multiply the first object by (the source object). Defaults
 * to opaque white. Animatable. */

@property(nullable) CGColorRef instanceColor; // 设置多个复制图层的颜色,默认为白色

/* The color components added to the color of instance k-1 to produce
 * the modulation color of instance k. Defaults to the clear color (no
 * change). Animatable. */

@property float instanceRedOffset;  // 设置每个复制图层相对上一个复制图层的红色偏移量
@property float instanceGreenOffset; // 设置每个复制图层相对上一个复制图层的绿色偏移量
@property float instanceBlueOffset; // 设置每个复制图层相对上一个复制图层的蓝色偏移量
@property float instanceAlphaOffset; // 设置每个复制图层相对上一个复制图层的透明度偏移量

@end

NS_ASSUME_NONNULL_END
```

