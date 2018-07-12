---
layout: post
title: "QuartzCore/CoreAnimation.h"
excerpt: "QuartzCore/CoreAnimation.h"
categories: [OC, QuartzCore]
tags: [OC, QuartzCore]
date: 2016-04-11 
modified: 
comments: true
---

* TOC
{:toc}
---

作用是引入了如下这些头文件

```objective-c
/* CoreAnimation - CoreAnimation.h

   Copyright (c) 2006-2016, Apple Inc.
   All rights reserved. */

#ifndef COREANIMATION_H
#define COREANIMATION_H

#include <QuartzCore/CABase.h>
#include <QuartzCore/CATransform3D.h>

#ifdef __OBJC__
#import <Foundation/Foundation.h>
#import <QuartzCore/CAAnimation.h>
#import <QuartzCore/CADisplayLink.h>
#import <QuartzCore/CAEAGLLayer.h>
#import <QuartzCore/CAEmitterBehavior.h>
#import <QuartzCore/CAEmitterCell.h>
#import <QuartzCore/CAEmitterLayer.h>
#import <QuartzCore/CAGradientLayer.h>
#import <QuartzCore/CALayer.h>
#import <QuartzCore/CAMediaTiming.h>
#import <QuartzCore/CAMediaTimingFunction.h>
#import <QuartzCore/CAReplicatorLayer.h>
#import <QuartzCore/CAScrollLayer.h>
#import <QuartzCore/CAShapeLayer.h>
#import <QuartzCore/CATextLayer.h>
#import <QuartzCore/CATiledLayer.h>
#import <QuartzCore/CATransaction.h>
#import <QuartzCore/CATransform3D.h>
#import <QuartzCore/CATransformLayer.h>
#import <QuartzCore/CAValueFunction.h>
#endif

#endif /* COREANIMATION_H */

```

