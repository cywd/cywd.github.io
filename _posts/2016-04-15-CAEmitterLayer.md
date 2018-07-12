---
layout: post
title: "QuartzCore/CAEmitterLayer.h"
excerpt: "QuartzCore/CAEmitterLayer.h"
categories: [OC, QuartzCore]
tags: [OC, QuartzCore]
date: 2016-04-15  
modified: 
comments: true
---

* TOC
{:toc}
---

# 整体描述

`CAEmitterLayer`用来实现基于`Core Animation`的粒子发生器系统。每个粒子都是一个`CAEmitterCell`的实例。粒子绘制在背景色与`border`之上。在属性中，可以指定`Layer`中的`CAEmitterCell`数组，每个`cell`定义了自己的一组属性，如速度、粒子发生率、旋转、缩放或者内容等。每个粒子也都有一个`emitterCells`属性，可以做为一个粒子发生器来运作。`Layer`还可以设置发生器位置、发生器形状、发射单元的位置等等。

`CAEmitterLayer`通过`emitterPosition`指定了`emitter`的位置，在`view`的中间偏下的地方，并且形状为默认的一个点。renderMode定义了粒子的渲染方式，在这里让所有的粒子出现叠加增强的效果。`birthRate`让粒子每秒产生四个。

`CAEmitterCell`指定`contents`来定义了粒子的内容，`emissionLongitude`和`emissionLatitude`指定了经纬度，经度角代表了x-y轴平面上与x轴之间的夹角，纬度角代表了x-z轴平面上与x轴之间的夹角。`emissionRange`设置了一个范围，围绕着y轴负方向，建立了一个圆锥形，粒子从这个圆锥形的范围内打出。`lifetime`设置了粒子的存活时长，在1.6秒之后，粒子消失。`birthRate`定义每秒生成100个，与`CAEmitterLayer`的`birtuRate`相乘，即最终的粒子数量400个每秒。`velcity`指定了初速度，`velcityRange`设置初速度在300到500之间浮动，`yAcceleration`指定了沿y轴250的加速度，用于给粒子减速。`color`设置了粒子的颜色，并设置了每个色值的浮动范围，用于生成所有颜色的烟火。最后设置了名称，以后可以再次引用它。

`CAEmitterLayer`能够显示粒子效果通过`Core Animation`,而粒子是通过`CAEmitterCell`来创建的,这些粒子被绘制在图层的背景上方 



# 源码

```objective-c
/* CoreAnimation - CAEmitterLayer.h

   Copyright (c) 2007-2016, Apple Inc.
   All rights reserved. */

/* Particle emitter layer.
 *
 * Each emitter has an array of cells, the cells define how particles
 * are emitted and rendered by the layer.
 *
 * Particle system is affected by layer's timing. The simulation starts
 * at layer's beginTime.
 *
 * The particles are drawn above the backgroundColor and border of the
 * layer. */

#import <QuartzCore/CALayer.h>

@class CAEmitterCell;

NS_ASSUME_NONNULL_BEGIN

CA_CLASS_AVAILABLE (10.6, 5.0, 9.0, 2.0)
@interface CAEmitterLayer : CALayer

/* The array of emitter cells attached to the layer. Each object must
 * have the CAEmitterCell class. */

@property(nullable, copy) NSArray<CAEmitterCell *> *emitterCells; // 所有在数组中的粒子都会被随机的绘制在图层上

/* The birth rate of each cell is multiplied by this number to give the
 * actual number of particles created every second. Default value is one.
 * Animatable. */

@property float birthRate;

/* The cell lifetime range is multiplied by this value when particles are
 * created. Defaults to one. Animatable. */

@property float lifetime;

/* The center of the emission shape. Defaults to (0, 0, 0). Animatable. */

@property CGPoint emitterPosition; // 在粒子图层上粒子的发射点(支持隐式动画)
@property CGFloat emitterZPosition; // 粒子发射器的z轴中心,这个需要结合emitterSize和emitterDepth来使用,主要是用来设置emitterShape的.默认值是0

/* The size of the emission shape. Defaults to (0, 0, 0). Animatable.
 * Depending on the `emitterShape' property some of the values may be
 * ignored. */

@property CGSize emitterSize; // 这个就是粒子发射器的shape的大小,控制emitterShape的大小
@property CGFloat emitterDepth; // 粒子发射器的深度,也就是y轴的高emitterZPosition就是这个Z轴的中心

/* A string defining the type of emission shape used. Current options are:
 * `point' (the default), `line', `rectangle', `circle', `cuboid' and
 * `sphere'. */

@property(copy) NSString *emitterShape; // 粒子发射点图形形状

/* A string defining how particles are created relative to the emission
 * shape. Current options are `points', `outline', `surface' and
 * `volume' (the default). */

@property(copy) NSString *emitterMode; // 粒子发射器的模式

/* A string defining how particles are composited into the layer's
 * image. Current options are `unordered' (the default), `oldestFirst',
 * `oldestLast', `backToFront' (i.e. sorted into Z order) and
 * `additive'. The first four use source-over compositing, the last
 * uses additive compositing. */

@property(copy) NSString *renderMode; // 控制粒子的渲染模式,(比如是否粒子重叠加重色彩)默认值是kCAEmitterLayerUnordered.

/* When true the particles are rendered as if they directly inhabit the
 * three dimensional coordinate space of the layer's superlayer, rather
 * than being flattened into the layer's plane first. Defaults to NO.
 * If true, the effect of the `filters', `backgroundFilters' and shadow-
 * related properties of the layer is undefined. */

@property BOOL preservesDepth;

/* Multiplies the cell-defined particle velocity. Defaults to one.
 * Animatable. */

@property float velocity;

/* Multiplies the cell-defined particle scale. Defaults to one. Animatable. */

@property float scale;

/* Multiplies the cell-defined particle spin. Defaults to one. Animatable. */

@property float spin;

/* The seed used to initialize the random number generator. Defaults to
 * zero. Each layer has its own RNG state. For properties with a mean M
 * and a range R, random values of the properties are uniformly
 * distributed in the interval [M - R/2, M + R/2]. */

@property unsigned int seed;

@end

/** `emitterShape' values. **/
// 点
CA_EXTERN NSString * const kCAEmitterLayerPoint 
    CA_AVAILABLE_STARTING (10.6, 5.0, 9.0, 2.0);
// 线形
CA_EXTERN NSString * const kCAEmitterLayerLine 
    CA_AVAILABLE_STARTING (10.6, 5.0, 9.0, 2.0);
// 矩形
CA_EXTERN NSString * const kCAEmitterLayerRectangle
    CA_AVAILABLE_STARTING (10.6, 5.0, 9.0, 2.0);
// 长方体
CA_EXTERN NSString * const kCAEmitterLayerCuboid
    CA_AVAILABLE_STARTING (10.6, 5.0, 9.0, 2.0);
// 圆形
CA_EXTERN NSString * const kCAEmitterLayerCircle
    CA_AVAILABLE_STARTING (10.6, 5.0, 9.0, 2.0);
// 球体
CA_EXTERN NSString * const kCAEmitterLayerSphere
    CA_AVAILABLE_STARTING (10.6, 5.0, 9.0, 2.0);

/** `emitterMode' values. **/

CA_EXTERN NSString * const kCAEmitterLayerPoints
    CA_AVAILABLE_STARTING (10.6, 5.0, 9.0, 2.0);
CA_EXTERN NSString * const kCAEmitterLayerOutline
    CA_AVAILABLE_STARTING (10.6, 5.0, 9.0, 2.0);
CA_EXTERN NSString * const kCAEmitterLayerSurface
    CA_AVAILABLE_STARTING (10.6, 5.0, 9.0, 2.0);
CA_EXTERN NSString * const kCAEmitterLayerVolume
    CA_AVAILABLE_STARTING (10.6, 5.0, 9.0, 2.0);

/** `renderMode' values. **/
// 无序随机的
CA_EXTERN NSString * const kCAEmitterLayerUnordered 
    CA_AVAILABLE_STARTING (10.6, 5.0, 9.0, 2.0);
// 最新的在上层出现
CA_EXTERN NSString * const kCAEmitterLayerOldestFirst 
    CA_AVAILABLE_STARTING (10.6, 5.0, 9.0, 2.0);
// 最新的在下层出现
CA_EXTERN NSString * const kCAEmitterLayerOldestLast 
    CA_AVAILABLE_STARTING (10.6, 5.0, 9.0, 2.0);
// 由下层向上层涌动
CA_EXTERN NSString * const kCAEmitterLayerBackToFront 
    CA_AVAILABLE_STARTING (10.6, 5.0, 9.0, 2.0);
// 叠加显示
CA_EXTERN NSString * const kCAEmitterLayerAdditive 
    CA_AVAILABLE_STARTING (10.6, 5.0, 9.0, 2.0);

NS_ASSUME_NONNULL_END
```

