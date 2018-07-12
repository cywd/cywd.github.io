---
layout: post
title: "QuartzCore/CADisplayLink.h"
excerpt: "QuartzCore/CADisplayLink.h"
categories: [OC, QuartzCore]
tags: [OC, QuartzCore]
date: 2016-04-14
modified: 
comments: true
---

* TOC
{:toc}
---

# 整体描述

`CADisplayLink`最主要的特征是能提供一个周期性的调用我们赋给它的`selector`的机制，从这点上看它很像定时器`NSTimer`。`CADisplayLink`在正常情况下会在每次刷新结束都被调用，精确度相当高，从而保证了动画的流畅性。`NSTimer`的精确度就显得低了点，比如`NSTimer`的触发时间到的时候，`runloop`如果在忙于别的调用，触发时间就会推迟到下一个`runloop`周期。更有甚者，在`OS X 10.9`以后为了尽量避免在`NSTimer`触发时间到了而去中断当前处理的任务，`NSTimer`新增了`tolerance`属性，让用户可以设置可以容忍的触发的时间范围。

# 源码

```objective-c
/* CoreAnimation - CADisplayLink.h

   Copyright (c) 2009-2016, Apple Inc.
   All rights reserved. */

#import <QuartzCore/CABase.h>
#import <Foundation/NSObject.h>

@class NSString, NSRunLoop;

NS_ASSUME_NONNULL_BEGIN

/** Class representing a timer bound to the display vsync. **/

CA_CLASS_AVAILABLE_IOS(3.1, 9.0, 2.0)
@interface CADisplayLink : NSObject
{
@private
  void *_impl;
}

/* Create a new display link object for the main display. It will
 * invoke the method called 'sel' on 'target', the method has the
 * signature '(void)selector:(CADisplayLink *)sender'. */
// 生成一个绑定了触发事件的实例
+ (CADisplayLink *)displayLinkWithTarget:(id)target selector:(SEL)sel;

/* Adds the receiver to the given run-loop and mode. Unless paused, it
 * will fire every vsync until removed. Each object may only be added
 * to a single run-loop, but it may be added in multiple modes at once.
 * While added to a run-loop it will implicitly be retained. */
// 把它添加到一个runloop中，触发事件SEL
- (void)addToRunLoop:(NSRunLoop *)runloop forMode:(NSRunLoopMode)mode;

/* Removes the receiver from the given mode of the runloop. This will
 * implicitly release it when removed from the last mode it has been
 * registered for. */
// 从runloop中移除
- (void)removeFromRunLoop:(NSRunLoop *)runloop forMode:(NSRunLoopMode)mode;

/* Removes the object from all runloop modes (releasing the receiver if
 * it has been implicitly retained) and releases the 'target' object. */
// 从所有runloop模式中删除对象(如果隐式保留了接收方，则释放接收方)并释放“目标”对象
// 简单来说就是销毁CADisplayLink这个计时器
// 调用这个方法，会从所有runLoop中移除当前实例，这个方法可以用于不需要计时器后对他进行释放前的操作。
- (void)invalidate;

/* The current time, and duration of the display frame associated with
 * the most recent target invocation. Time is represented using the
 * normal Core Animation conventions, i.e. Mach host time converted to
 * seconds. */
// 获取上一次selector被执行的时间戳。这个属性是一个只读属性，而且你要记住的是只有当selector被执行过一次之后这个值才会被取到有效值。这个属性同上是用来比较当前图层时间与上一次selector执行时间只差，从而来计算本次UI应该发生的改变的进度（例如视图做移动效果）。
@property(readonly, nonatomic) CFTimeInterval timestamp;
// 获取当前设备的屏幕刷新时间间隔。同timestamp一样，他也是个只读属性，并且也需要selector触发一次才可以取值。值的一提的是，当前iOS设备的刷新频率都是60HZ。也就是说每16.7ms刷新一次。作用也与timestamp相同，都可以用于辅助计算。不过需要说明的一点是，如果CPU过于繁忙，duration的值是会浮动的。
@property(readonly, nonatomic) CFTimeInterval duration;

/* The next timestamp that the client should target their render for. */
// 下次的时间
@property(readonly, nonatomic) CFTimeInterval targetTimestamp CA_AVAILABLE_IOS_STARTING(10.0, 10.0, 3.0);

/* When true the object is prevented from firing. Initial state is
 * false. */
// 要暂停对 selector 的调用设置为YES， 默认是NO
@property(getter=isPaused, nonatomic) BOOL paused;

/* Defines how many display frames must pass between each time the
 * display link fires. Default value is one, which means the display
 * link will fire for every display frame. Setting the interval to two
 * will cause the display link to fire every other display frame, and
 * so on. The behavior when using values less than one is undefined.
 * DEPRECATED - use preferredFrameRate. */
// 事件触发间隔。是指两次selector触发之间间隔几次屏幕刷新，默认值为1，也就是说屏幕每刷新一次，执行一次selector，如果设置为2.调用次数为 屏幕刷新次数/2，这个也可以间接用来控制动画速度。iOS设备屏幕默认刷新频率时60。废弃，请使用preferredFramesPerSecond
@property(nonatomic) NSInteger frameInterval
  CA_AVAILABLE_BUT_DEPRECATED_IOS (3.1, 10.0, 2.0, 3.0, 9.0, 10.0, "use preferredFramesPerSecond");

/* Defines the desired callback rate in frames per second for this display link.
 * A value of 100.0 would result in 100 callbacks per second.
 *
 * Default value is zero, which means the display link will fire at the native
 * cadence of the display hardware. CoreAnimation will make the best attempt
 * at issuing callbacks at the requested rate, but there are no guarantees. */
/* 默认值是60。值为100时，就会每秒100次调用，如果设置为0，意味着会按照本机硬件的频率调用。CoreAnimation将尽最大努力以请求的速率发出回调，但并没有保证，这取决于两点
1.CPU的空闲程度
如果CPU忙于其它计算，就没法保证以60HZ执行屏幕的绘制动作，导致跳过若干次调用回调方法的机会，跳过次数取决CPU的忙碌程度。
2.执行回调方法所用的时间。
如果执行回调时间大于重绘每帧的间隔时间，就会导致跳过若干次回调调用机会，这取决于执行时间长短。

这样比之前frameInterval设置要清晰很多 */
@property(nonatomic) NSInteger preferredFramesPerSecond CA_AVAILABLE_IOS_STARTING(10.0, 10.0, 3.0);

@end

NS_ASSUME_NONNULL_END
```

# 应用

`CADisplayLink`使用场合相对专一，适合做界面的不停重绘，比如视频播放的时候需要不停地获取下一帧用于界面渲染。

`NSTimer`的使用范围要广泛的多，各种需要单次或者循环定时处理的任务都可以使用。

使用方法类似：

```objective-c
CADisplayLink *displayLink = [CADisplayLink displayLinkWithTarget:self selector:@selector(displayLinkFunc)];
// displayLink.frameInterval = 2;
displayLink.preferredFramesPerSecond = 30;
[displayLink setPaused:YES];
[displayLink addToRunLoop:[NSRunLoop currentRunLoop] forMode:NSRunLoopCommonModes];
```

