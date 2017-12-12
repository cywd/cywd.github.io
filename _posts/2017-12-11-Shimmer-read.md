---
layout: post
title: Shimmer解读
excerpt: ""
categories: ["iOS"]
tags: ["iOS", "源码阅读"]
date: 2017-12-11
comments: true
---

* TOC
{:toc}
---

# 结构

```
FBShimmering
├── FBShimmering-Prefix.pch
├── FBShimmering.h
├── FBShimmeringLayer.h
├── FBShimmeringLayer.m
├── FBShimmeringView.h
└── FBShimmeringView.m
```

*`FBShimmering`*   // 一个协议，主要封装了一些常用的属性。

*`FBShimmeringView`*  // 实现了`FBShimmering` 协议，主要是修改其图层`FBShimmeringLayer`，对外提供了`contentView`。

*`FBShimmeringLayer`*  // 实现了`FBShimmering` 协议，是实现整个动画效果的核心部分。包含了两个`layer`，一个是包含内容的`contentLayer`，另一个便是用户蒙层闪光效果的`maskLayer`。

# 源码分析

## FBShimmering.h

```objective-c
/**
 Copyright (c) 2014-present, Facebook, Inc.
 All rights reserved.
 
 This source code is licensed under the BSD-style license found in the
 LICENSE file in the root directory of this source tree. An additional grant
 of patent rights can be found in the PATENTS file in the same directory.
 */

#import <CoreGraphics/CoreGraphics.h>
#import <Foundation/Foundation.h>

typedef NS_ENUM(NSInteger, FBShimmerDirection) {
  //! Shimmer animation goes from left to right
  FBShimmerDirectionRight,
  //! Shimmer animation goes from right to left
  FBShimmerDirectionLeft,
  //! Shimmer animation goes from below to above
  FBShimmerDirectionUp,
  //! Shimmer animation goes from above to below
  FBShimmerDirectionDown,
};

static const float FBShimmerDefaultBeginTime = CGFLOAT_MAX;

@protocol FBShimmering <NSObject>

//! @abstract Set this to YES to start shimming and NO to stop. Defaults to NO.
@property (assign, nonatomic, readwrite, getter = isShimmering) BOOL shimmering;

//! @abstract The time interval between shimmerings in seconds. Defaults to 0.4.
@property (assign, nonatomic, readwrite) CFTimeInterval shimmeringPauseDuration;

//! @abstract The opacity of the content while it is shimmering. Defaults to 0.5.
@property (assign, nonatomic, readwrite) CGFloat shimmeringAnimationOpacity;

//! @abstract The opacity of the content before it is shimmering. Defaults to 1.0.
@property (assign, nonatomic, readwrite) CGFloat shimmeringOpacity;

//! @abstract The speed of shimmering, in points per second. Defaults to 230.
@property (assign, nonatomic, readwrite) CGFloat shimmeringSpeed;

//! @abstract The highlight length of shimmering. Range of [0,1], defaults to 1.0.
@property (assign, nonatomic, readwrite) CGFloat shimmeringHighlightLength;

//! @abstract Same as "shimmeringHighlightLength", just for downward compatibility. @deprecated
@property (assign, nonatomic, readwrite, getter = shimmeringHighlightLength, setter = setShimmeringHighlightLength:) CGFloat shimmeringHighlightWidth DEPRECATED_MSG_ATTRIBUTE("Use shimmeringHighlightLength");

//! @abstract The direction of shimmering animation. Defaults to FBShimmerDirectionRight.
@property (assign, nonatomic, readwrite) FBShimmerDirection shimmeringDirection;

//! @abstract The duration of the fade used when shimmer begins. Defaults to 0.1.
@property (assign, nonatomic, readwrite) CFTimeInterval shimmeringBeginFadeDuration;

//! @abstract The duration of the fade used when shimmer ends. Defaults to 0.3.
@property (assign, nonatomic, readwrite) CFTimeInterval shimmeringEndFadeDuration;

/**
 @abstract The absolute CoreAnimation media time when the shimmer will fade in.
 @discussion Only valid after setting {@ref shimmering} to NO.
 */
@property (assign, nonatomic, readonly) CFTimeInterval shimmeringFadeTime;

/**
 @abstract The absolute CoreAnimation media time when the shimmer will begin.
 @discussion Only valid after setting {@ref shimmering} to YES.
 */
@property (assign, nonatomic) CFTimeInterval shimmeringBeginTime;

@end


```

## FBShimmeringView

```objective-c
/**
 Copyright (c) 2014-present, Facebook, Inc.
 All rights reserved.
 
 This source code is licensed under the BSD-style license found in the
 LICENSE file in the root directory of this source tree. An additional grant
 of patent rights can be found in the PATENTS file in the same directory.
 */

#import <UIKit/UIView.h>

#import "FBShimmering.h"

/**
  @abstract Lightweight, generic shimmering view.
 */
@interface FBShimmeringView : UIView <FBShimmering>

//! @abstract The content view to be shimmered.
@property (strong, nonatomic) UIView *contentView;

@end

```

```objective-c
/**
 Copyright (c) 2014-present, Facebook, Inc.
 All rights reserved.
 
 This source code is licensed under the BSD-style license found in the
 LICENSE file in the root directory of this source tree. An additional grant
 of patent rights can be found in the PATENTS file in the same directory.
 */

#import "FBShimmeringView.h"

#import "FBShimmeringLayer.h"

#if !__has_feature(objc_arc)
#error This file must be compiled with ARC. Convert your project to ARC or specify the -fobjc-arc flag.
#endif

@implementation FBShimmeringView

/*
通过实现 layerClass方法来修改 FBShimmeringView 的关联图层，对FBShimmeringView的操作就会由FBShimmeringLayer来实现。
*/
+ (Class)layerClass
{
  return [FBShimmeringLayer class];
}

/*
以下是通过宏定义的方式实现 FBShimmering 协议属性的 Get 和 Set 方法。
*/

#define __layer ((FBShimmeringLayer *)self.layer)

#define LAYER_ACCESSOR(accessor, ctype) \
- (ctype)accessor { \
  return [__layer accessor]; \
}

#define LAYER_MUTATOR(mutator, ctype) \
- (void)mutator (ctype)value { \
  [__layer mutator value]; \
}

#define LAYER_RW_PROPERTY(accessor, mutator, ctype) \
  LAYER_ACCESSOR (accessor, ctype) \
  LAYER_MUTATOR (mutator, ctype)

LAYER_RW_PROPERTY(isShimmering, setShimmering:, BOOL)
LAYER_RW_PROPERTY(shimmeringPauseDuration, setShimmeringPauseDuration:, CFTimeInterval)
LAYER_RW_PROPERTY(shimmeringAnimationOpacity, setShimmeringAnimationOpacity:, CGFloat)
LAYER_RW_PROPERTY(shimmeringOpacity, setShimmeringOpacity:, CGFloat)
LAYER_RW_PROPERTY(shimmeringSpeed, setShimmeringSpeed:, CGFloat)
LAYER_RW_PROPERTY(shimmeringHighlightLength, setShimmeringHighlightLength:, CGFloat)
LAYER_RW_PROPERTY(shimmeringDirection, setShimmeringDirection:, FBShimmerDirection)
LAYER_ACCESSOR(shimmeringFadeTime, CFTimeInterval)
LAYER_RW_PROPERTY(shimmeringBeginFadeDuration, setShimmeringBeginFadeDuration:, CFTimeInterval)
LAYER_RW_PROPERTY(shimmeringEndFadeDuration, setShimmeringEndFadeDuration:, CFTimeInterval)
LAYER_RW_PROPERTY(shimmeringBeginTime, setShimmeringBeginTime:, CFTimeInterval)

- (void)setContentView:(UIView *)contentView
{
  if (contentView != _contentView) {
    _contentView = contentView;
    [self addSubview:contentView];
    __layer.contentLayer = contentView.layer;
  }
}

- (void)layoutSubviews
{
  // Autolayout requires these to be set on the UIView, not the CALayer.
  // Do this *before* the layer has a chance to set the properties, as the
  // setters would be ignored (even for autolayout) if set to the same value.
  _contentView.bounds = self.bounds;
  _contentView.center = self.center;

  [super layoutSubviews];
}

@end

```

## FBShimmeringLayer

```objective-c
/**
 Copyright (c) 2014-present, Facebook, Inc.
 All rights reserved.
 
 This source code is licensed under the BSD-style license found in the
 LICENSE file in the root directory of this source tree. An additional grant
 of patent rights can be found in the PATENTS file in the same directory.
 */

#import <QuartzCore/CALayer.h>

#import "FBShimmering.h"

/**
  @abstract Lightweight, generic shimmering layer.
 */
@interface FBShimmeringLayer : CALayer <FBShimmering>

//! @abstract The content layer to be shimmered.
@property (strong, nonatomic) CALayer *contentLayer;

@end

```

```objective-c
/**
 Copyright (c) 2014-present, Facebook, Inc.
 All rights reserved.
 
 This source code is licensed under the BSD-style license found in the
 LICENSE file in the root directory of this source tree. An additional grant
 of patent rights can be found in the PATENTS file in the same directory.
 */

#import "FBShimmeringLayer.h"

#import <QuartzCore/CAAnimation.h>
#import <QuartzCore/CAGradientLayer.h>
#import <QuartzCore/CATransaction.h>

#import <UIKit/UIGeometry.h>
#import <UIKit/UIColor.h>

#if !__has_feature(objc_arc)
#error This file must be compiled with ARC. Convert your project to ARC or specify the -fobjc-arc flag.
#endif


/*
这里判断了是否是模拟器。
引用了 UIKit 的私有方法 UIAnimationDragCoefficient。
这里先通过UIKIT_EXTERN的方式将其引入进来。返回一个float 类型的值。表示“拖拽系数”，默认是等于 1.0 的，这个值对应着模拟器的 “Slow Animations” 选项，当我们打开这个选项的时候，他的值会变成10，即慢了10倍。
*/
#if TARGET_IPHONE_SIMULATOR
UIKIT_EXTERN float UIAnimationDragCoefficient(void); // UIKit private drag coeffient, use judiciously
#endif

static CGFloat FBShimmeringLayerDragCoefficient(void)
{
#if TARGET_IPHONE_SIMULATOR
  return UIAnimationDragCoefficient();
#else
  return 1.0;
#endif
}

static void FBShimmeringLayerAnimationApplyDragCoefficient(CAAnimation *animation)
{
  CGFloat k = FBShimmeringLayerDragCoefficient();
  
  if (k != 0 && k != 1) {
    animation.speed = 1 / k;
  }
}

// animations keys
static NSString *const kFBShimmerSlideAnimationKey = @"slide";
static NSString *const kFBFadeAnimationKey = @"fade";
static NSString *const kFBEndFadeAnimationKey = @"fade-end";

static CABasicAnimation *fade_animation(CALayer *layer, CGFloat opacity, CFTimeInterval duration)
{
  CABasicAnimation *animation = [CABasicAnimation animationWithKeyPath:@"opacity"];
  animation.fromValue = @([(layer.presentationLayer ?: layer) opacity]);
  animation.toValue = @(opacity);
  animation.fillMode = kCAFillModeBoth;
  animation.removedOnCompletion = NO;
  animation.duration = duration;
  FBShimmeringLayerAnimationApplyDragCoefficient(animation);
  return animation;
}

static CABasicAnimation *shimmer_slide_animation(CFTimeInterval duration, FBShimmerDirection direction)
{
  CABasicAnimation *animation = [CABasicAnimation animationWithKeyPath:@"position"];
  animation.toValue = [NSValue valueWithCGPoint:CGPointZero];
  animation.duration = duration;
  animation.repeatCount = HUGE_VALF;
  FBShimmeringLayerAnimationApplyDragCoefficient(animation);
  if (direction == FBShimmerDirectionLeft ||
      direction == FBShimmerDirectionUp) {
    animation.speed = -fabsf(animation.speed);
  }
  return animation;
}

// take a shimmer slide animation and turns into repeating
static CAAnimation *shimmer_slide_repeat(CAAnimation *a, CFTimeInterval duration, FBShimmerDirection direction)
{
  CAAnimation *anim = [a copy];
  anim.repeatCount = HUGE_VALF;
  anim.duration = duration;
  anim.speed = (direction == FBShimmerDirectionRight || direction == FBShimmerDirectionDown) ? fabsf(anim.speed) : -fabsf(anim.speed);
  return anim;
}

// take a shimmer slide animation and turns into finish
static CAAnimation *shimmer_slide_finish(CAAnimation *a)
{
  CAAnimation *anim = [a copy];
  anim.repeatCount = 0;
  return anim;
}

@interface FBShimmeringMaskLayer : CAGradientLayer
@property (readonly, nonatomic) CALayer *fadeLayer;
@end

@implementation FBShimmeringMaskLayer

- (instancetype)init
{
  self = [super init];
  if (nil != self) {
    _fadeLayer = [[CALayer alloc] init];
    _fadeLayer.backgroundColor = [UIColor whiteColor].CGColor;
    [self addSublayer:_fadeLayer];
  }
  return self;
}

- (void)layoutSublayers
{
  [super layoutSublayers];
  CGRect r = self.bounds;
  _fadeLayer.bounds = r;
  _fadeLayer.position = CGPointMake(CGRectGetMidX(r), CGRectGetMidY(r));
}

@end

@interface FBShimmeringLayer ()
#if __IPHONE_OS_VERSION_MAX_ALLOWED >= 100000
// iOS 10 SDK has CALayerDelegate and CAAnimationDelegate as proper protocols.
<CALayerDelegate, CAAnimationDelegate>
#endif

@property (strong, nonatomic) FBShimmeringMaskLayer *maskLayer;
@end

@implementation FBShimmeringLayer
{
  CALayer *_contentLayer;
  FBShimmeringMaskLayer *_maskLayer;
}

#pragma mark - Lifecycle

@synthesize shimmering = _shimmering;
@synthesize shimmeringPauseDuration = _shimmeringPauseDuration;
@synthesize shimmeringAnimationOpacity = _shimmeringAnimationOpacity;
@synthesize shimmeringOpacity = _shimmeringOpacity;
@synthesize shimmeringSpeed = _shimmeringSpeed;
@synthesize shimmeringHighlightLength = _shimmeringHighlightLength;
@synthesize shimmeringDirection = _shimmeringDirection;
@synthesize shimmeringFadeTime = _shimmeringFadeTime;
@synthesize shimmeringBeginFadeDuration = _shimmeringBeginFadeDuration;
@synthesize shimmeringEndFadeDuration = _shimmeringEndFadeDuration;
@synthesize shimmeringBeginTime = _shimmeringBeginTime;
@dynamic shimmeringHighlightWidth;

- (instancetype)init
{
  self = [super init];
  if (nil != self) {
    // default configuration
    _shimmeringPauseDuration = 0.4;
    _shimmeringSpeed = 230.0;
    _shimmeringHighlightLength = 1.0;
    _shimmeringAnimationOpacity = 0.5;
    _shimmeringOpacity = 1.0;
    _shimmeringDirection = FBShimmerDirectionRight;
    _shimmeringBeginFadeDuration = 0.1;
    _shimmeringEndFadeDuration = 0.3;
    _shimmeringBeginTime = FBShimmerDefaultBeginTime;
  }
  return self;
}

#pragma mark - Properties

- (void)setContentLayer:(CALayer *)contentLayer
{
  // reset mask
  self.maskLayer = nil;

  // note content layer and add for display
  _contentLayer = contentLayer;
  self.sublayers = contentLayer ? @[contentLayer] : nil;

  // update shimmering animation
  [self _updateShimmering];
}

- (void)setShimmering:(BOOL)shimmering
{
  if (shimmering != _shimmering) {
    _shimmering = shimmering;
    [self _updateShimmering];
  }
}

- (void)setShimmeringSpeed:(CGFloat)speed
{
  if (speed != _shimmeringSpeed) {
    _shimmeringSpeed = speed;
    [self _updateShimmering];
  }
}

- (void)setShimmeringHighlightLength:(CGFloat)length
{
  if (length != _shimmeringHighlightLength) {
    _shimmeringHighlightLength = length;
    [self _updateShimmering];
  }
}

- (void)setShimmeringDirection:(FBShimmerDirection)direction
{
  if (direction != _shimmeringDirection) {
    _shimmeringDirection = direction;
    [self _updateShimmering];
  }
}

- (void)setShimmeringPauseDuration:(CFTimeInterval)duration
{
  if (duration != _shimmeringPauseDuration) {
    _shimmeringPauseDuration = duration;
    [self _updateShimmering];
  }
}

- (void)setShimmeringAnimationOpacity:(CGFloat)shimmeringAnimationOpacity
{
  if (shimmeringAnimationOpacity != _shimmeringAnimationOpacity) {
    _shimmeringAnimationOpacity = shimmeringAnimationOpacity;
    [self _updateMaskColors];
  }
}

- (void)setShimmeringOpacity:(CGFloat)shimmeringOpacity
{
  if (shimmeringOpacity != _shimmeringOpacity) {
    _shimmeringOpacity = shimmeringOpacity;
    [self _updateMaskColors];
  }
}

- (void)setShimmeringBeginTime:(CFTimeInterval)beginTime
{
  if (beginTime != _shimmeringBeginTime) {
    _shimmeringBeginTime = beginTime;
    [self _updateShimmering];
  }
}

- (void)layoutSublayers
{
  [super layoutSublayers];
  CGRect r = self.bounds;
  _contentLayer.anchorPoint = CGPointMake(0.5, 0.5);
  _contentLayer.bounds = r;
  _contentLayer.position = CGPointMake(CGRectGetMidX(r), CGRectGetMidY(r));
  
  if (nil != _maskLayer) {
    [self _updateMaskLayout];
  }
}

- (void)setBounds:(CGRect)bounds
{
  CGRect oldBounds = self.bounds;
  [super setBounds:bounds];
 
  if (!CGRectEqualToRect(oldBounds, bounds)) {
    [self _updateShimmering];
  }
}

#pragma mark - Internal

/*
清除蒙版
*/
- (void)_clearMask
{
  if (nil == _maskLayer) {
    return;
  }

  BOOL disableActions = [CATransaction disableActions];
  [CATransaction setDisableActions:YES];

  self.maskLayer = nil;
  _contentLayer.mask = nil;
  
  [CATransaction setDisableActions:disableActions];
}

- (void)_createMaskIfNeeded
{
  if (_shimmering && !_maskLayer) {
    _maskLayer = [FBShimmeringMaskLayer layer];
    _maskLayer.delegate = self;
    _contentLayer.mask = _maskLayer;
    [self _updateMaskColors];
    [self _updateMaskLayout];
  }
}

/*
为蒙版创建颜色数组。
注释也说了，蒙版对应的CALayer所表现出来的属性只能是透明度，颜色什么的都不好使
*/
- (void)_updateMaskColors
{
  if (nil == _maskLayer) {
    return;
  }

  // We create a gradient to be used as a mask.
  // In a mask, the colors do not matter, it's the alpha that decides the degree of masking.
  UIColor *maskedColor = [UIColor colorWithWhite:1.0 alpha:_shimmeringOpacity];
  UIColor *unmaskedColor = [UIColor colorWithWhite:1.0 alpha:_shimmeringAnimationOpacity];

  // Create a gradient from masked to unmasked to masked.
  _maskLayer.colors = @[(__bridge id)maskedColor.CGColor, (__bridge id)unmaskedColor.CGColor, (__bridge id)maskedColor.CGColor];
}

/*
更新蒙版布局 layout
*/
- (void)_updateMaskLayout
{
  // Everything outside the mask layer is hidden, so we need to create a mask long enough for the shimmered layer to be always covered by the mask.
  CGFloat length = 0.0f;
  if (_shimmeringDirection == FBShimmerDirectionDown ||
      _shimmeringDirection == FBShimmerDirectionUp) {
    length = CGRectGetHeight(_contentLayer.bounds);
  } else {
    length = CGRectGetWidth(_contentLayer.bounds);
  }
  if (0 == length) {
    return;
  }

  // extra distance for the gradient to travel during the pause.
  CGFloat extraDistance = length + _shimmeringSpeed * _shimmeringPauseDuration;

  // compute how far the shimmering goes
  CGFloat fullShimmerLength = length * 3.0f + extraDistance;
  CGFloat travelDistance = length * 2.0f + extraDistance;
  
  // position the gradient for the desired width
  CGFloat highlightOutsideLength = (1.0 - _shimmeringHighlightLength) / 2.0;
  _maskLayer.locations = @[@(highlightOutsideLength),
                           @(0.5),
                           @(1.0 - highlightOutsideLength)];

  CGFloat startPoint = (length + extraDistance) / fullShimmerLength;
  CGFloat endPoint = travelDistance / fullShimmerLength;
  
  // position for the start of the animation
  _maskLayer.anchorPoint = CGPointZero;
  if (_shimmeringDirection == FBShimmerDirectionDown ||
      _shimmeringDirection == FBShimmerDirectionUp) {
    _maskLayer.startPoint = CGPointMake(0.0, startPoint);
    _maskLayer.endPoint = CGPointMake(0.0, endPoint);
    _maskLayer.position = CGPointMake(0.0, -travelDistance);
    _maskLayer.bounds = CGRectMake(0.0, 0.0, CGRectGetWidth(_contentLayer.bounds), fullShimmerLength);
  } else {
    _maskLayer.startPoint = CGPointMake(startPoint, 0.0);
    _maskLayer.endPoint = CGPointMake(endPoint, 0.0);
    _maskLayer.position = CGPointMake(-travelDistance, 0.0);
    _maskLayer.bounds = CGRectMake(0.0, 0.0, fullShimmerLength, CGRectGetHeight(_contentLayer.bounds));
  }
}

/*
想来这个方法应该是最核心的部分。
*/
- (void)_updateShimmering
{
  // create mask if needed
  [self _createMaskIfNeeded];

  // if not shimmering and no mask, noop
  if (!_shimmering && !_maskLayer) {
    return;
  }

  // 保证 layout
  // ensure layout
  [self layoutIfNeeded];
  
  // 判断动画是否已失效
  BOOL disableActions = [CATransaction disableActions];
  if (!_shimmering) {
    if (disableActions) {
      // 假如不播放动画且动画已失效，清除maskLayer
      // simply remove mask
      [self _clearMask];
    } else {
      // 结束滑行
      // end slide
      CFTimeInterval slideEndTime = 0;

      // 根据key获取动画
      CAAnimation *slideAnimation = [_maskLayer animationForKey:kFBShimmerSlideAnimationKey];
      if (slideAnimation != nil) {

        // 获取滑动的总时间
        // determine total time sliding
        CFTimeInterval now = CACurrentMediaTime();
        CFTimeInterval slideTotalDuration = now - slideAnimation.beginTime;
		
        // 根据已播放时间和总体时间求出剩余时间
        // determine time offset into current slide
        CFTimeInterval slideTimeOffset = fmod(slideTotalDuration, slideAnimation.duration);

        // 结束动画
        // transition to non-repeating slide
        CAAnimation *finishAnimation = shimmer_slide_finish(slideAnimation);

        // 结束动画的开始时间
        // adjust begin time to now - offset
        finishAnimation.beginTime = now - slideTimeOffset;
		
        // 设定结束时间，并添加结束动画
        // note slide end time and begin
        slideEndTime = finishAnimation.beginTime + slideAnimation.duration;
        [_maskLayer addAnimation:finishAnimation forKey:kFBShimmerSlideAnimationKey];
      }
	  // 在结束动画播放完毕后播放淡入动画（这里需要注意的是，淡入淡出动画都是对maskLayer的子layer fadeLayer起作用）
      // fade in text at slideEndTime
      CABasicAnimation *fadeInAnimation = fade_animation(_maskLayer.fadeLayer, 1.0, _shimmeringEndFadeDuration);
      fadeInAnimation.delegate = self;
      [fadeInAnimation setValue:@YES forKey:kFBEndFadeAnimationKey];
      fadeInAnimation.beginTime = slideEndTime;
      [_maskLayer.fadeLayer addAnimation:fadeInAnimation forKey:kFBFadeAnimationKey];

      // 淡入淡出动画的开始时间为位移动画的结束时间(这一步只做数据展示，对整体动画没影响)
      // expose end time for synchronization
      _shimmeringFadeTime = slideEndTime;
    }
  } else {
    // 淡出
    // fade out text, optionally animated
    CABasicAnimation *fadeOutAnimation = nil;
    if (_shimmeringBeginFadeDuration > 0.0 && !disableActions) {
      fadeOutAnimation = fade_animation(_maskLayer.fadeLayer, 0.0, _shimmeringBeginFadeDuration);
      [_maskLayer.fadeLayer addAnimation:fadeOutAnimation forKey:kFBFadeAnimationKey];
    } else {
      BOOL innerDisableActions = [CATransaction disableActions];
      [CATransaction setDisableActions:YES];

      _maskLayer.fadeLayer.opacity = 0.0;
      [_maskLayer.fadeLayer removeAllAnimations];
      
      [CATransaction setDisableActions:innerDisableActions];
    }

    // 开始滑动动画
    // begin slide animation
    CAAnimation *slideAnimation = [_maskLayer animationForKey:kFBShimmerSlideAnimationKey];
    
    // compute shimmer duration
    CGFloat length = 0.0f;
    if (_shimmeringDirection == FBShimmerDirectionDown ||
        _shimmeringDirection == FBShimmerDirectionUp) {
      length = CGRectGetHeight(_contentLayer.bounds);
    } else {
      length = CGRectGetWidth(_contentLayer.bounds);
    }
    CFTimeInterval animationDuration = (length / _shimmeringSpeed) + _shimmeringPauseDuration;
    
    if (slideAnimation != nil) {
      // ensure existing slide animation repeats
      [_maskLayer addAnimation:shimmer_slide_repeat(slideAnimation, animationDuration, _shimmeringDirection) forKey:kFBShimmerSlideAnimationKey];
    } else {
      // add slide animation
      slideAnimation = shimmer_slide_animation(animationDuration, _shimmeringDirection);
      slideAnimation.fillMode = kCAFillModeForwards;
      slideAnimation.removedOnCompletion = NO;
      if (_shimmeringBeginTime == FBShimmerDefaultBeginTime) {
        _shimmeringBeginTime = CACurrentMediaTime() + fadeOutAnimation.duration;
      }
      slideAnimation.beginTime = _shimmeringBeginTime;
      
      [_maskLayer addAnimation:slideAnimation forKey:kFBShimmerSlideAnimationKey];
    }
  }
}

#pragma mark - CALayerDelegate

- (id<CAAction>)actionForLayer:(CALayer *)layer forKey:(NSString *)event
{
  // no associated actions
  return (id)kCFNull;
}

#pragma mark - CAAnimationDelegate

- (void)animationDidStop:(CAAnimation *)anim finished:(BOOL)flag
{
  if (flag && [[anim valueForKey:kFBEndFadeAnimationKey] boolValue]) {
    [_maskLayer.fadeLayer removeAnimationForKey:kFBFadeAnimationKey];

    [self _clearMask];
  }
}

@end

```

