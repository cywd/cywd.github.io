---
layout: post
title: "QuartzCore/CAMediaTiming.h"
excerpt: "QuartzCore/CAMediaTiming.h"
categories: [OC, QuartzCore]
tags: [OC, QuartzCore]
date: 2016-04-12 
modified: 
comments: true
---

* TOC
{:toc}
---

这个就是声明了`CAMediaTiming`协议。

定义了时间，速度，重复次数等。

```objective-c
/* CoreAnimation - CAMediaTiming.h

   Copyright (c) 2006-2016, Apple Inc.
   All rights reserved. */

#import <QuartzCore/CABase.h>
#import <objc/objc.h>
#import <Foundation/NSObject.h>

/* The CAMediaTiming protocol is implemented by layers and animations, it
 * models a hierarchical timing system, with each object describing the
 * mapping from time values in the object's parent to local time.
 *
 * Absolute time is defined as mach time converted to seconds. The
 * CACurrentMediaTime function is provided as a convenience for querying the
 * current absolute time.
 *
 * The conversion from parent time to local time has two stages:
 *
 * 1. conversion to "active local time". This includes the point at
 * which the object appears in the parent's timeline, and how fast it
 * plays relative to the parent.
 *
 * 2. conversion from active to "basic local time". The timing model
 * allows for objects to repeat their basic duration multiple times,
 * and optionally to play backwards before repeating. */

@class NSString;

NS_ASSUME_NONNULL_BEGIN

@protocol CAMediaTiming

/* The begin time of the object, in relation to its parent object, if
 * applicable. Defaults to 0. */
// 用来设置动画延时，若想延迟1秒，就设置为CACurrentMediaTime()+1，其中CACurrentMediaTime()为图层当前时间。
@property CFTimeInterval beginTime;

/* The basic duration of the object. Defaults to 0. */
// 动画的持续时间，默认是0
@property CFTimeInterval duration;

/* The rate of the layer. Used to scale parent time to local time, e.g.
 * if rate is 2, local time progresses twice as fast as parent time.
 * Defaults to 1. */
// 动画速率，决定动画时间的倍率。当speed为2时，动画时间为设置的duration的1/2。
@property float speed;

/* Additional offset in active local time. i.e. to convert from parent
 * time tp to active local time t: t = (tp - begin) * speed + offset.
 * One use of this is to "pause" a layer by setting `speed' to zero and
 * `offset' to a suitable value. Defaults to 0. */
// 动画时间偏移量。比如设置动画时长为3秒，当设置timeOffset为1.5时，当前动画会从中间位置开始，并在到达指定位置时，走完之前跳过的前半段动画。
@property CFTimeInterval timeOffset;

/* The repeat count of the object. May be fractional. Defaults to 0. */
// 动画的重复次数
@property float repeatCount;

/* The repeat duration of the object. Defaults to 0. */
// 动画的重复时间
@property CFTimeInterval repeatDuration;

/* When true, the object plays backwards after playing forwards. Defaults
 * to NO. */
// 动画由初始值到最终值后，是否反过来回到初始值的动画。如果设置为YES，就意味着动画完成后会以动画的形式回到初始值。
@property BOOL autoreverses;

/* Defines how the timed object behaves outside its active duration.
 * Local time may be clamped to either end of the active duration, or
 * the element may be removed from the presentation. The legal values
 * are `backwards', `forwards', `both' and `removed'. Defaults to
 * `removed'. */
// 决定当前对象在非动画时间段的行为.比如动画开始之前，动画结束之后
@property(copy) NSString *fillMode;

@end

/* `fillMode' options. */
// fillMode 的选项
    
// 当动画结束后，layer会一直保持着动画最后的状态 
CA_EXTERN NSString * const kCAFillModeForwards
    CA_AVAILABLE_STARTING (10.5, 2.0, 9.0, 2.0);
// 在动画开始前，只需要将动画加入了一个layer，layer便立即进入动画的初始状态并等待动画开始。
CA_EXTERN NSString * const kCAFillModeBackwards
    CA_AVAILABLE_STARTING (10.5, 2.0, 9.0, 2.0);
//  这个其实就是上面两个的合成，动画加入之后在开始之前，layer便处于动画初始状态，动画结束后layer保持动画最后的状态
CA_EXTERN NSString * const kCAFillModeBoth
    CA_AVAILABLE_STARTING (10.5, 2.0, 9.0, 2.0);
// 这个是默认值，也就是说当动画开始前和动画结束后，动画对layer都没有影响，动画结束后，layer会恢复到之前的状态
CA_EXTERN NSString * const kCAFillModeRemoved
    CA_AVAILABLE_STARTING (10.5, 2.0, 9.0, 2.0); // default

NS_ASSUME_NONNULL_END

```

