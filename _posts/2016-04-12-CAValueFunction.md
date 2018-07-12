---
layout: post
title: "QuartzCore/CAValueFunction.h"
excerpt: "QuartzCore/CAValueFunction.h"
categories: [OC, QuartzCore]
tags: [OC, QuartzCore]
date: 2016-04-12  
modified: 
comments: true
---

* TOC
{:toc}
---

# 简介

是专门为了`transform`动画而设置的

# 头文件

```objective-c
/* CoreAnimation - CAValueFunction.h

   Copyright (c) 2008-2016, Apple Inc.
   All rights reserved. */

#import <QuartzCore/CABase.h>
#import <Foundation/NSObject.h>

NS_ASSUME_NONNULL_BEGIN

CA_CLASS_AVAILABLE (10.6, 3.0, 9.0, 2.0)
@interface CAValueFunction : NSObject <NSCoding>
{
@protected
  NSString *_string;
  void *_impl;
}

// 调用方法
+ (nullable instancetype)functionWithName:(NSString *)name;

@property(readonly) NSString *name;

@end

/** Value function names. **/

/* The `rotateX', `rotateY', `rotateZ' functions take a single input
 * value in radians, and construct a 4x4 matrix representing the
 * corresponding rotation matrix. */
// 设置为x轴旋转
CA_EXTERN NSString * const kCAValueFunctionRotateX
    CA_AVAILABLE_STARTING (10.6, 3.0, 9.0, 2.0);
// 设置为y轴旋转
CA_EXTERN NSString * const kCAValueFunctionRotateY
    CA_AVAILABLE_STARTING (10.6, 3.0, 9.0, 2.0);
// 设置为z轴旋转
CA_EXTERN NSString * const kCAValueFunctionRotateZ
    CA_AVAILABLE_STARTING (10.6, 3.0, 9.0, 2.0);

/* The `scale' function takes three input values and constructs a
 * 4x4 matrix representing the corresponding scale matrix. */
// 3个方向的缩放
CA_EXTERN NSString * const kCAValueFunctionScale
    CA_AVAILABLE_STARTING (10.6, 3.0, 9.0, 2.0);

/* The `scaleX', `scaleY', `scaleZ' functions take a single input value
 * and construct a 4x4 matrix representing the corresponding scaling
 * matrix. */
// x轴缩放
CA_EXTERN NSString * const kCAValueFunctionScaleX
    CA_AVAILABLE_STARTING (10.6, 3.0, 9.0, 2.0);
// y轴缩放
CA_EXTERN NSString * const kCAValueFunctionScaleY
    CA_AVAILABLE_STARTING (10.6, 3.0, 9.0, 2.0);
// z轴缩放
CA_EXTERN NSString * const kCAValueFunctionScaleZ
    CA_AVAILABLE_STARTING (10.6, 3.0, 9.0, 2.0);

/* The `translate' function takes three input values and constructs a
 * 4x4 matrix representing the corresponding scale matrix. */
// 3个方向的位移
CA_EXTERN NSString * const kCAValueFunctionTranslate
    CA_AVAILABLE_STARTING (10.6, 3.0, 9.0, 2.0);

/* The `translateX', `translateY', `translateZ' functions take a single
 * input value and construct a 4x4 matrix representing the corresponding
 * translation matrix. */
// x轴位移
CA_EXTERN NSString * const kCAValueFunctionTranslateX
    CA_AVAILABLE_STARTING (10.6, 3.0, 9.0, 2.0);
// y轴位移
CA_EXTERN NSString * const kCAValueFunctionTranslateY
    CA_AVAILABLE_STARTING (10.6, 3.0, 9.0, 2.0);
// z轴位移
CA_EXTERN NSString * const kCAValueFunctionTranslateZ
    CA_AVAILABLE_STARTING (10.6, 3.0, 9.0, 2.0);

NS_ASSUME_NONNULL_END

```



# 例子

因为我们没有办法直接改变`transform3D`中的属性，通过这个参数，可以帮助我们直接操作`transfrom3D`属性变化产生动画效果，举例如下，一个绕`Z`轴旋转的动画：

```objective-c
// 绕z轴旋转的动画
CABasicAnimation * basicAnimation = [CABasicAnimation animationWithKeyPath:@"transform"];
// 从0度开始
basicAnimation.fromValue = @0;
// 旋转到180度
basicAnimation.toValue = [NSNumber numberWithFloat:M_PI];
// 时间2S
basicAnimation.duration = 2;
// 设置为z轴旋转
basicAnimation.valueFunction = [CAValueFunction functionWithName:kCAValueFunctionRotateZ];
// 执行动画
[layer addAnimation:basicAnimation forKey:@"aZRoateBasicAnimationKey"];
```

当然如果不使用`valueFunction`也是可以实现的

```objc
// 绕z轴旋转的动画
CABasicAnimation * basicAnimation = [CABasicAnimation animationWithKeyPath:@"transform.rotation.z"];
// 从0度开始
basicAnimation.fromValue = @0;
// 旋转到180度
basicAnimation.toValue = [NSNumber numberWithFloat:M_PI];
// 时间2S
basicAnimation.duration = 2;
// 执行动画
[layer addAnimation:basicAnimation forKey:@"aZRoateBasicAnimationKey"];
```

