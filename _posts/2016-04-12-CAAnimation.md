---
layout: post
title: "QuartzCore/CAAnimation.h"
excerpt: "QuartzCore/CAAnimation.h"
categories: [OC, QuartzCore]
tags: [OC, QuartzCore, CAAnimation]
date: 2016-04-12  
modified: 
comments: true
---

* TOC
{:toc}
---

# 整体描述

`CAAnimation.h`主要是各类动画的基类，我们一般不会使用它来做动画。

除了`CAMediaTiming`协议中的方法，增加了`CAAnimationDelegate`的代理属性等。

# 源码

```objective-c
/* CoreAnimation - CAAnimation.h

   Copyright (c) 2006-2016, Apple Inc.
   All rights reserved. */

#import <QuartzCore/CALayer.h>
#import <Foundation/NSObject.h>

@class NSArray, NSString, CAMediaTimingFunction, CAValueFunction;
@protocol CAAnimationDelegate;

NS_ASSUME_NONNULL_BEGIN

/** The base animation class. **/

CA_CLASS_AVAILABLE (10.5, 2.0, 9.0, 2.0)
@interface CAAnimation : NSObject
    <NSCoding, NSCopying, CAMediaTiming, CAAction>
{
@private
  void *_attr;
  uint32_t _flags;
}

/* Creates a new animation object. */
// 快速实例化
+ (instancetype)animation;

/* Animations implement the same property model as defined by CALayer.
 * See CALayer.h for more details. */

+ (nullable id)defaultValueForKey:(NSString *)key;
- (BOOL)shouldArchiveValueForKey:(NSString *)key;

/* A timing function defining the pacing of the animation. Defaults to
 * nil indicating linear pacing. */
// 控制动画的节奏。系统提供的包括：kCAMediaTimingFunctionLinear （匀速），kCAMediaTimingFunctionEaseIn （慢进快出），kCAMediaTimingFunctionEaseOut （快进慢出），kCAMediaTimingFunctionEaseInEaseOut （慢进慢出，中间加速），kCAMediaTimingFunctionDefault （默认），当然也可通过自定义创建CAMediaTimingFunction。
@property(nullable, strong) CAMediaTimingFunction *timingFunction;

/* The delegate of the animation. This object is retained for the
 * lifetime of the animation object. Defaults to nil. See below for the
 * supported delegate methods. */
// 代理
@property(nullable, strong) id <CAAnimationDelegate> delegate;

/* When true, the animation is removed from the render tree once its
 * active duration has passed. Defaults to YES. */
// 是否让图层保持显示动画执行后的状态，默认为YES，也就是动画执行完毕后从涂层上移除，恢复到执行前的状态，如果设置为NO，并且设置fillMode为kCAFillModeForwards，则保持动画执行后的状态。
@property(getter=isRemovedOnCompletion) BOOL removedOnCompletion;

@end

/* Delegate methods for CAAnimation. */

@protocol CAAnimationDelegate <NSObject>
@optional

/* Called when the animation begins its active duration. */

- (void)animationDidStart:(CAAnimation *)anim;

/* Called when the animation either completes its active duration or
 * is removed from the object it is attached to (i.e. the layer). 'flag'
 * is true if the animation reached the end of its active duration
 * without being removed. */

- (void)animationDidStop:(CAAnimation *)anim finished:(BOOL)flag;

@end


/** Subclass for property-based animations. **/

CA_CLASS_AVAILABLE (10.5, 2.0, 9.0, 2.0)
@interface CAPropertyAnimation : CAAnimation
// 属性动画，针对对象的可动画属性进行效果的设置，一般不直接使用。
    
/* Creates a new animation object with its `keyPath' property set to
 * 'path'. */

+ (instancetype)animationWithKeyPath:(nullable NSString *)path;

/* The key-path describing the property to be animated. */
// CALayer的某个属性名，并通过这个属性的值进行修改，达到相应的动画效果。
@property(nullable, copy) NSString *keyPath;

/* When true the value specified by the animation will be "added" to
 * the current presentation value of the property to produce the new
 * presentation value. The addition function is type-dependent, e.g.
 * for affine transforms the two matrices are concatenated. Defaults to
 * NO. */
// 属性动画是否以当前动画效果为基础，默认为NO。
@property(getter=isAdditive) BOOL additive;

/* The `cumulative' property affects how repeating animations produce
 * their result. If true then the current value of the animation is the
 * value at the end of the previous repeat cycle, plus the value of the
 * current repeat cycle. If false, the value is simply the value
 * calculated for the current repeat cycle. Defaults to NO. */
// 指定动画是否为累加效果，默认为NO。
@property(getter=isCumulative) BOOL cumulative;

/* If non-nil a function that is applied to interpolated values
 * before they are set as the new presentation value of the animation's
 * target property. Defaults to nil. */
// 此属性配合CALayer的transform属性使用。
@property(nullable, strong) CAValueFunction *valueFunction;

@end


/** Subclass for basic (single-keyframe) animations. **/

CA_CLASS_AVAILABLE (10.5, 2.0, 9.0, 2.0)
@interface CABasicAnimation : CAPropertyAnimation
/* 该类提供了基本的、单关键帧的Layer属性动画 */
// 通过keyPath对应属性进行控制，需要设置fromValue以及toValue

/* The objects defining the property values being interpolated between.
 * All are optional, and no more than two should be non-nil. The object
 * type should match the type of the property being animated (using the
 * standard rules described in CALayer.h). The supported modes of
 * animation are:
 *
 * - both `fromValue' and `toValue' non-nil. Interpolates between
 * `fromValue' and `toValue'.
 *
 * - `fromValue' and `byValue' non-nil. Interpolates between
 * `fromValue' and `fromValue' plus `byValue'.
 *
 * - `byValue' and `toValue' non-nil. Interpolates between `toValue'
 * minus `byValue' and `toValue'.
 *
 * - `fromValue' non-nil. Interpolates between `fromValue' and the
 * current presentation value of the property.
 *
 * - `toValue' non-nil. Interpolates between the layer's current value
 * of the property in the render tree and `toValue'.
 *
 * - `byValue' non-nil. Interpolates between the layer's current value
 * of the property in the render tree and that plus `byValue'. */

@property(nullable, strong) id fromValue; // 所改变属性的起始值
@property(nullable, strong) id toValue;   // 所改变属性的结束值
@property(nullable, strong) id byValue;   // 所改变属性相同起始值的改变量。在不设置toValue时，toValue = fromValue + byValue，也就是在当前的位置上增加多少。

@end


/** General keyframe animation class. **/

CA_CLASS_AVAILABLE (10.5, 2.0, 9.0, 2.0)
@interface CAKeyframeAnimation : CAPropertyAnimation
// 关键帧动画，同样通过keyPath对应属性进行控制，但它可以通过values或者path进行多个阶段的控制

/* An array of objects providing the value of the animation function for
 * each keyframe. */
// 关键帧组成的数组，动画会依次显示其中的每一帧。
@property(nullable, copy) NSArray *values;

/* An optional path object defining the behavior of the animation
 * function. When non-nil overrides the `values' property. Each point
 * in the path except for `moveto' points defines a single keyframe for
 * the purpose of timing and interpolation. Defaults to nil. For
 * constant velocity animation along the path, `calculationMode' should
 * be set to `paced'. Upon assignment the path is copied. */
// 关键帧路径，动画进行的要素，优先级比values高，但是只对CALayer的anchorPoint和position起作用。
@property(nullable) CGPathRef path;

/* An optional array of `NSNumber' objects defining the pacing of the
 * animation. Each time corresponds to one value in the `values' array,
 * and defines when the value should be used in the animation function.
 * Each value in the array is a floating point number in the range
 * [0,1]. */
// 每一帧对应的时间，如果不设置，则各关键帧平分设定时间。
@property(nullable, copy) NSArray<NSNumber *> *keyTimes;

/* An optional array of CAMediaTimingFunction objects. If the `values' array
 * defines n keyframes, there should be n-1 objects in the
 * `timingFunctions' array. Each function describes the pacing of one
 * keyframe to keyframe segment. */
// 每一帧对应的动画节奏。动画节奏的一个集合
@property(nullable, copy) NSArray<CAMediaTimingFunction *> *timingFunctions;

/* The "calculation mode". Possible values are `discrete', `linear',
 * `paced', `cubic' and `cubicPaced'. Defaults to `linear'. When set to
 * `paced' or `cubicPaced' the `keyTimes' and `timingFunctions'
 * properties of the animation are ignored and calculated implicitly. */
// 动画的计算模式，系统提供了对应的几种模式。
@property(copy) NSString *calculationMode;

/* For animations with the cubic calculation modes, these properties
 * provide control over the interpolation scheme. Each keyframe may
 * have a tension, continuity and bias value associated with it, each
 * in the range [-1, 1] (this defines a Kochanek-Bartels spline, see
 * http://en.wikipedia.org/wiki/Kochanek-Bartels_spline).
 *
 * The tension value controls the "tightness" of the curve (positive
 * values are tighter, negative values are rounder). The continuity
 * value controls how segments are joined (positive values give sharp
 * corners, negative values give inverted corners). The bias value
 * defines where the curve occurs (positive values move the curve before
 * the control point, negative values move it after the control point).
 *
 * The first value in each array defines the behavior of the tangent to
 * the first control point, the second value controls the second
 * point's tangents, and so on. Any unspecified values default to zero
 * (giving a Catmull-Rom spline if all are unspecified). */
// 动画张力控制。
@property(nullable, copy) NSArray<NSNumber *> *tensionValues;
// 动画连续性控制。
@property(nullable, copy) NSArray<NSNumber *> *continuityValues;
// 动画偏差率控制。
@property(nullable, copy) NSArray<NSNumber *> *biasValues;

/* Defines whether or objects animating along paths rotate to match the
 * path tangent. Possible values are `auto' and `autoReverse'. Defaults
 * to nil. The effect of setting this property to a non-nil value when
 * no path object is supplied is undefined. `autoReverse' rotates to
 * match the tangent plus 180 degrees. */
//  动画沿路径旋转方式，系统提供了两种模式。`auto' and `autoReverse'。默认是nil。
@property(nullable, copy) NSString *rotationMode;

@end

/* `calculationMode' strings. */

CA_EXTERN NSString * const kCAAnimationLinear
    CA_AVAILABLE_STARTING (10.5, 2.0, 9.0, 2.0);
CA_EXTERN NSString * const kCAAnimationDiscrete
    CA_AVAILABLE_STARTING (10.5, 2.0, 9.0, 2.0);
CA_EXTERN NSString * const kCAAnimationPaced
    CA_AVAILABLE_STARTING (10.5, 2.0, 9.0, 2.0);
CA_EXTERN NSString * const kCAAnimationCubic
    CA_AVAILABLE_STARTING (10.7, 4.0, 9.0, 2.0);
CA_EXTERN NSString * const kCAAnimationCubicPaced
    CA_AVAILABLE_STARTING (10.7, 4.0, 9.0, 2.0);

/* `rotationMode' strings. */

CA_EXTERN NSString * const kCAAnimationRotateAuto
    CA_AVAILABLE_STARTING (10.5, 2.0, 9.0, 2.0);
CA_EXTERN NSString * const kCAAnimationRotateAutoReverse
    CA_AVAILABLE_STARTING (10.5, 2.0, 9.0, 2.0);

/** Subclass for mass-spring animations. */

CA_CLASS_AVAILABLE (10.11, 9.0, 9.0, 2.0)
@interface CASpringAnimation : CABasicAnimation
// 带有初始速度以及阻尼指数等物理参数的属性动画。

/* The mass of the object attached to the end of the spring. Must be greater
   than 0. Defaults to one. */
// 质量
@property CGFloat mass;

/* The spring stiffness coefficient. Must be greater than 0.
 * Defaults to 100. */
// 弹簧的劲度系数
@property CGFloat stiffness;

/* The damping coefficient. Must be greater than or equal to 0.
 * Defaults to 10. */
// 阻尼系数
@property CGFloat damping;

/* The initial velocity of the object attached to the spring. Defaults
 * to zero, which represents an unmoving object. Negative values
 * represent the object moving away from the spring attachment point,
 * positive values represent the object moving towards the spring
 * attachment point. */
// 初始速度
@property CGFloat initialVelocity;

/* Returns the estimated duration required for the spring system to be
 * considered at rest. The duration is evaluated for the current animation
 * parameters. */
// 结算时间，根据上述参数计算出的预计时间，相对于你设置的时间，这个时间比较准确。
@property(readonly) CFTimeInterval settlingDuration;

@end

/** Transition animation subclass. **/

CA_CLASS_AVAILABLE (10.5, 2.0, 9.0, 2.0)
@interface CATransition : CAAnimation
// 转场动画，系统提供了很多酷炫效果

/* The name of the transition. Current legal transition types include
 * `fade', `moveIn', `push' and `reveal'. Defaults to `fade'. */
// 转场动画类型。
@property(copy) NSString *type;

/* An optional subtype for the transition. E.g. used to specify the
 * transition direction for motion-based transitions, in which case
 * the legal values are `fromLeft', `fromRight', `fromTop' and
 * `fromBottom'. */
//  转场动画方向。
@property(nullable, copy) NSString *subtype;

/* The amount of progress through to the transition at which to begin
 * and end execution. Legal values are numbers in the range [0,1].
 * `endProgress' must be greater than or equal to `startProgress'.
 * Default values are 0 and 1 respectively. */
// 动画起点进度（整体的百分比）。
@property float startProgress;
// 动画终点进度（整体的百分比）。
@property float endProgress;

/* An optional filter object implementing the transition. When set the
 * `type' and `subtype' properties are ignored. The filter must
 * implement `inputImage', `inputTargetImage' and `inputTime' input
 * keys, and the `outputImage' output key. Optionally it may support
 * the `inputExtent' key, which will be set to a rectangle describing
 * the region in which the transition should run. Defaults to nil. */
// 自定义转场。
@property(nullable, strong) id filter;

@end

/* Common transition types. */
// 淡出效果
CA_EXTERN NSString * const kCATransitionFade
    CA_AVAILABLE_STARTING (10.5, 2.0, 9.0, 2.0);
// 新视图移动到旧视图上
CA_EXTERN NSString * const kCATransitionMoveIn
    CA_AVAILABLE_STARTING (10.5, 2.0, 9.0, 2.0);
// 新视图将旧视图推出去
CA_EXTERN NSString * const kCATransitionPush
    CA_AVAILABLE_STARTING (10.5, 2.0, 9.0, 2.0);
// 移开旧视图显示新视图
CA_EXTERN NSString * const kCATransitionReveal
    CA_AVAILABLE_STARTING (10.5, 2.0, 9.0, 2.0);

/* Common transition subtypes. */
// 从右侧转场
CA_EXTERN NSString * const kCATransitionFromRight
    CA_AVAILABLE_STARTING (10.5, 2.0, 9.0, 2.0);
// 从左侧转场
CA_EXTERN NSString * const kCATransitionFromLeft
    CA_AVAILABLE_STARTING (10.5, 2.0, 9.0, 2.0);
// 从顶部转场
CA_EXTERN NSString * const kCATransitionFromTop
    CA_AVAILABLE_STARTING (10.5, 2.0, 9.0, 2.0);
// 从底部转场
CA_EXTERN NSString * const kCATransitionFromBottom
    CA_AVAILABLE_STARTING (10.5, 2.0, 9.0, 2.0);


/** Animation subclass for grouped animations. **/

CA_CLASS_AVAILABLE (10.5, 2.0, 9.0, 2.0)
@interface CAAnimationGroup : CAAnimation
// 动画组，方便对于多动画的统一控制管理。
    
/* An array of CAAnimation objects. Each member of the array will run
 * concurrently in the time space of the parent animation using the
 * normal rules. */
// 所有动画效果元素的集合。
@property(nullable, copy) NSArray<CAAnimation *> *animations;

@end

NS_ASSUME_NONNULL_END
```

