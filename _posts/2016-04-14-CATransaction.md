---
layout: post
title: "QuartzCore/CATransaction.h"
excerpt: "QuartzCore/CATransaction.h"
categories: [OC, QuartzCore]
tags: [OC, QuartzCore]
date: 2016-04-14 
modified: 
comments: true
---

* TOC
{:toc}
---

# 介绍

` Transactions`是`CoreAnimation`的用于将多个`layer tree`操作批量化为渲染树的原子更新的机制。 对`layer tree`的每个修改都需要事务作为其一部分。
` CoreAnimation`支持两种事务，“显式”事务和隐式事务。
 **显式事务**是程序员在修改层树之前调用`[CATransaction begin]`，然后是`[CATransaction commit]`。
 当层树由没有活动事务的线程修改时，`CoreAnimation`自动创建**隐式事务**。
 它们在线程的运行循环下一次迭代时自动提交。 在一些情况下（即，没有运行循环，或者运行循环被阻塞），可能有必要使用显式事务来及时地呈现树更新。

```objective-c
/* CoreAnimation - CATransaction.h

   Copyright (c) 2006-2016, Apple Inc.
   All rights reserved. */

#import <QuartzCore/CABase.h>
#import <Foundation/NSObject.h>

/* Transactions are CoreAnimation's mechanism for batching multiple layer-
 * tree operations into atomic updates to the render tree. Every
 * modification to the layer tree requires a transaction to be part of.
 *
 * CoreAnimation supports two kinds of transactions, "explicit" transactions
 * and "implicit" transactions.
 *
 * Explicit transactions are where the programmer calls `[CATransaction
 * begin]' before modifying the layer tree, and `[CATransaction commit]'
 * afterwards.
 *
 * Implicit transactions are created automatically by CoreAnimation when the
 * layer tree is modified by a thread without an active transaction.
 * They are committed automatically when the thread's run-loop next
 * iterates. In some circumstances (i.e. no run-loop, or the run-loop
 * is blocked) it may be necessary to use explicit transactions to get
 * timely render tree updates. */

@class CAMediaTimingFunction;

NS_ASSUME_NONNULL_BEGIN

CA_CLASS_AVAILABLE (10.5, 2.0, 9.0, 2.0)
@interface CATransaction : NSObject

/* Begin a new transaction for the current thread; nests. */
// 在当前线程开始一个事务
+ (void)begin;

/* Commit all changes made during the current transaction. Raises an
 * exception if no current transaction exists. */
// 提交当前事务期间进行的所有更改。 如果不存在当前事务，则引发异常。
+ (void)commit;

/* Commits any extant implicit transaction. Will delay the actual commit
 * until any nested explicit transactions have completed. */
// 提交任何现存的隐式事务。 将延迟实际的commituntil任何嵌套的显式事务已经完成。
+ (void)flush;

/* Methods to lock and unlock the global lock. Layer methods automatically
 * obtain this while modifying shared state, but callers may need to lock
 * around multiple operations to ensure consistency. The lock is a
 * recursive spin-lock (i.e shouldn't be held for extended periods). */
// 锁定和解锁全局锁的方法。 Layer方法自动在修改共享状态时获得这一点，但是调用者可能需要锁定多个操作以确保一致性。 锁是一个递归自旋锁（即不应长时间保持）。
+ (void)lock;
+ (void)unlock;

/* Accessors for the "animationDuration" per-thread transaction
 * property. Defines the default duration of animations added to
 * layers. Defaults to 1/4s. */
// “animationDuration”每个线程事务属性的访问器。 定义添加到图层的动画的默认持续时间。 默认为1 / 4s。
+ (CFTimeInterval)animationDuration;
+ (void)setAnimationDuration:(CFTimeInterval)dur;

/* Accessors for the "animationTimingFunction" per-thread transaction
 * property. The default value is nil, when set to a non-nil value any
 * animations added to layers will have this value set as their
 * "timingFunction" property. Added in Mac OS X 10.6. */
// “animationTimingFunction”每线程事务属性的访问器。 默认值为nil，当设置为非nil值时，添加到图层的任何动画都将此值设置为其“timingFunction”属性。 在Mac OS X 10.6中添加。
+ (nullable CAMediaTimingFunction *)animationTimingFunction;
+ (void)setAnimationTimingFunction:(nullable CAMediaTimingFunction *)function;

/* Accessors for the "disableActions" per-thread transaction property.
 * Defines whether or not the layer's -actionForKey: method is used to
 * find an action (aka. implicit animation) for each layer property
 * change. Defaults to NO, i.e. implicit animations enabled. */
// “disableActions”每线程事务属性的访问器。定义图层的-actionForKey：方法是否用于为每个图层属性更改找到一个操作（也称为implicitanimation）。 默认为NO，即启用了隐式动画。
+ (BOOL)disableActions;
+ (void)setDisableActions:(BOOL)flag;

/* Accessors for the "completionBlock" per-thread transaction property.
 * Once set to a non-nil value the block is guaranteed to be called (on
 * the main thread) as soon as all animations subsequently added by
 * this transaction group have completed (or been removed). If no
 * animations are added before the current transaction group is
 * committed (or the completion block is set to a different value), the
 * block will be invoked immediately. Added in Mac OS X 10.6. */
// 每个线程事务属性的“completionBlock”访问器。设置为非nil值后，一旦此事务组随后添加的所有动画都已完成（或已删除），块就被保证被调用（在主线程上） ）。 如果在提交当前事务组之前没有添加动画（或者完成块被设置为不同的值），则将立即调用该块。 在Mac OS X 10.6中添加。
#if __BLOCKS__
+ (nullable void (^)(void))completionBlock;
+ (void)setCompletionBlock:(nullable void (^)(void))block;
#endif

/* Associate arbitrary keyed-data with the current transaction (i.e.
 * with the current thread).
 *
 * Nested transactions have nested data scope, i.e. reading a key
 * searches for the innermost scope that has set it, setting a key
 * always sets it in the innermost scope.
 *
 * Currently supported transaction properties include:
 * "animationDuration", "animationTimingFunction", "completionBlock",
 * "disableActions". See method declarations above for descriptions of
 * each property.
 *
 * Attempting to set a property to a type other than its document type
 * has an undefined result. */
/*将任意键控数据与当前事务（即与当前线程）关联。
嵌套事务具有嵌套数据作用域，即读取一个键，搜索已设置它的最内层作用域，设置键总是将其设置在最内层作用域。
当前支持的事务属性包括：“animationDuration”，“animationTimingFunction”，“completionBlock”，“disableActions”。 有关每个属性的描述，请参阅上面的方法声明。 尝试将属性设置为非文档类型以外的类型具有未定义的结果。*/
+ (nullable id)valueForKey:(NSString *)key;
+ (void)setValue:(nullable id)anObject forKey:(NSString *)key;

@end

/** Transaction property ids. **/

CA_EXTERN NSString * const kCATransactionAnimationDuration
    CA_AVAILABLE_STARTING (10.5, 2.0, 9.0, 2.0);
CA_EXTERN NSString * const kCATransactionDisableActions
    CA_AVAILABLE_STARTING (10.5, 2.0, 9.0, 2.0);
CA_EXTERN NSString * const kCATransactionAnimationTimingFunction
    CA_AVAILABLE_STARTING (10.6, 3.0, 9.0, 2.0);
CA_EXTERN NSString * const kCATransactionCompletionBlock
    CA_AVAILABLE_STARTING (10.6, 4.0, 9.0, 2.0);

NS_ASSUME_NONNULL_END

```

# 用法

目前不太了解，等以后研究下。