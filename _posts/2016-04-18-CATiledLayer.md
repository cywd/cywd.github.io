---
layout: post
title: "QuartzCore/CATiledLayer.h"
excerpt: "QuartzCore/CATiledLayer.h"
categories: [OC, QuartzCore]
tags: [OC, QuartzCore]
date: 2016-04-18 
modified: 
comments: true
---

* TOC
{:toc}
---

# 整体描述

CATiledLayer提供异步加载图片各部分的功能。layer的drawLayer:inContext:方法会在出现时回调，用来绘制对应部分的内容。可以通过Context的clip bounds和CTM（当前图形上下文的仿射变换，CGContextGetCTM方法）来判断是图片的哪一部分以及大小。

# 源码

```objective-c
/* CoreAnimation - CATiledLayer.h

   Copyright (c) 2006-2016, Apple Inc.
   All rights reserved. */

/* This is a subclass of CALayer providing a way to asynchronously
 * provide tiles of the layer's content, potentially cached at multiple
 * levels of detail.
 *
 * As more data is required by the renderer, the layer's
 * -drawInContext: method is called on one or more background threads
 * to supply the drawing operations to fill in one tile of data. The
 * clip bounds and CTM of the drawing context can be used to determine
 * the bounds and resolution of the tile being requested.
 *
 * Regions of the layer may be invalidated using the usual
 * -setNeedsDisplayInRect: method. However update will be asynchronous,
 * i.e. the next display update will most likely not contain the
 * changes, but a future update will.
 *
 * Note: do not attempt to directly modify the `contents' property of
 * an CATiledLayer object - doing so will effectively turn it into a
 * regular CALayer. */

#import <QuartzCore/CALayer.h>

NS_ASSUME_NONNULL_BEGIN

CA_CLASS_AVAILABLE (10.5, 2.0, 9.0, 2.0)
@interface CATiledLayer : CALayer

/* The time in seconds that newly added images take to "fade-in" to the
 * rendered representation of the tiled layer. The default implementation
 * returns 0.25 seconds. */
// 新添加的图像以秒为单位的时间被“淡入”到平铺层的呈现。默认实现返回0.25秒。
+ (CFTimeInterval)fadeDuration;

// 以下两个属性看http://www.cocoachina.com/bbs/read.php?tid-31201.html

/* The number of levels of detail maintained by this layer. Defaults to
 * one. Each LOD is half the resolution of the previous level. If too
 * many levels are specified for the current size of the layer, then
 * the number of levels is clamped to the maximum value (the bottom
 * most LOD must contain at least a single pixel in each dimension). */

@property size_t levelsOfDetail;

/* The number of magnified levels of detail for this layer. Defaults to
 * zero. Each previous level of detail is twice the resolution of the
 * later. E.g. specifying 'levelsOfDetailBias' of two means that the
 * layer devotes two of its specified levels of detail to
 * magnification, i.e. 2x and 4x. */

@property size_t levelsOfDetailBias;

/* The maximum size of each tile used to create the layer's content.
 * Defaults to (256, 256). Note that there is a maximum tile size, and
 * requests for tiles larger than that limit will cause a suitable
 * value to be substituted. */
// 用于创建层内容的每个块的最大大小。默认为(256,256)。注意，有一个最大的块大小，如果请求的块大于这个限制，将导致一个合适的值被替换。
@property CGSize tileSize;

@end

NS_ASSUME_NONNULL_END

```

# 应用

比如超大图的显示，可以使用CATiledLayer，分成若干小图加载，这样内存会控制在一个范围，不会过高。

使用这个layer的好处之一就是，它不需要你自己计算分块显示的区域，它自己直接提供，你只需要根据这个区域计算图片相应区域，然后画图就可以了。
第二个好处就是它是在其他线程画图，不会因为阻塞主线程而导致卡顿。
第三个好处就是它自己实现了只在屏幕区域显示图片，屏幕区域外不会显示，而且当移动图片时，它会自动绘制之前未绘制的区域，当你缩放时它也会自动重绘。

# 参考

[http://www.cocoachina.com/bbs/read.php?tid-31201.html](http://www.cocoachina.com/bbs/read.php?tid-31201.html)

 

 

 