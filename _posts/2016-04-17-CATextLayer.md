---
layout: post
title: "QuartzCore/CATextLayer.h"
excerpt: "QuartzCore/CATextLayer.h"
categories: [OC, QuartzCore]
tags: [OC, QuartzCore]
date: 2016-04-17  
modified: 
comments: true
---

* TOC
{:toc}
---

# 整体介绍

`CATextLayer`是`CALayer`的子类，它以图层的形式包含了`UILabel`几乎所有的绘制特性，并且额外提供了一些新的特性。

同样，`CATextLayer`也要比`UILabel`渲染得快得多。很少有人知道在`iOS 6`及之前的版本，`UILabel`其实是通过WebKit来实现绘制的，这样就造成了当有很多文字的时候就会有极大的性能压力。而`CATextLayer`使用了`Core text`，并且渲染得非常快。

```objective-c
/* CoreAnimation - CATextLayer.h

   Copyright (c) 2006-2016, Apple Inc.
   All rights reserved. */

#import <QuartzCore/CALayer.h>

/* The text layer provides simple text layout and rendering of plain
 * or attributed strings. The first line is aligned to the top of the
 * layer. */

NS_ASSUME_NONNULL_BEGIN

CA_CLASS_AVAILABLE (10.5, 2.0, 9.0, 2.0)
@interface CATextLayer : CALayer
{
@private
  struct CATextLayerPrivate *_state;
}

/* The text to be rendered, should be either an NSString or an
 * NSAttributedString. Defaults to nil. */
// 文本呈现，可以是一个NSString或者NSAttributedString；默认为nil
@property(nullable, copy) id string;

/* The font to use, currently may be either a CTFontRef, a CGFontRef,
 * or a string naming the font. Defaults to the Helvetica font. Only
 * used when the `string' property is not an NSAttributedString. */
// 字体使用，可能是一个CTFontRef，一个CGFontRef或者一个字符串命名体，默认为Helvetica字体；仅当string不是一个NSAttributedString的时候使用
@property(nullable) CFTypeRef font;

/* The font size. Defaults to 36. Only used when the `string' property
 * is not an NSAttributedString. Animatable (Mac OS X 10.6 and later.) */
// 字号，默认36 仅当string不是一个NSAttributedString的时候使用；
@property CGFloat fontSize;

/* The color object used to draw the text. Defaults to opaque white.
 * Only used when the `string' property is not an NSAttributedString.
 * Animatable (Mac OS X 10.6 and later.) */
// 用来绘制文本的颜色，默认为不透明的白色；仅当string不是一个NSAttributedString的时候使用；
@property(nullable) CGColorRef foregroundColor;

/* When true the string is wrapped to fit within the layer bounds.
 * Defaults to NO.*/
// 文本自适应图层大小，默认是NO
@property(getter=isWrapped) BOOL wrapped;

/* Describes how the string is truncated to fit within the layer
 * bounds. The possible options are `none', `start', `middle' and
 * `end'. Defaults to `none'. */
// 描述如何将字符串截断以适应图层大小，设置缩短的部位，可选择没有，开始，中间，和结束
@property(copy) NSString *truncationMode;

/* Describes how individual lines of text are aligned within the layer
 * bounds. The possible options are `natural', `left', `right',
 * `center' and `justified'. Defaults to `natural'. */
// 对齐方式
@property(copy) NSString *alignmentMode;

/* Sets allowsFontSubpixelQuantization parameter of CGContextRef
 * passed to the -drawInContext: method. Defaults to NO. */
// 默认NO
@property BOOL allowsFontSubpixelQuantization;

@end

/* Truncation modes. */

CA_EXTERN NSString * const kCATruncationNone
    CA_AVAILABLE_STARTING (10.5, 3.2, 9.0, 2.0);
CA_EXTERN NSString * const kCATruncationStart
    CA_AVAILABLE_STARTING (10.5, 3.2, 9.0, 2.0);
CA_EXTERN NSString * const kCATruncationEnd
    CA_AVAILABLE_STARTING (10.5, 3.2, 9.0, 2.0);
CA_EXTERN NSString * const kCATruncationMiddle
    CA_AVAILABLE_STARTING (10.5, 3.2, 9.0, 2.0);

/* Alignment modes. */

CA_EXTERN NSString * const kCAAlignmentNatural
    CA_AVAILABLE_STARTING (10.5, 3.2, 9.0, 2.0);
CA_EXTERN NSString * const kCAAlignmentLeft
    CA_AVAILABLE_STARTING (10.5, 3.2, 9.0, 2.0);
CA_EXTERN NSString * const kCAAlignmentRight
    CA_AVAILABLE_STARTING (10.5, 3.2, 9.0, 2.0);
CA_EXTERN NSString * const kCAAlignmentCenter
    CA_AVAILABLE_STARTING (10.5, 3.2, 9.0, 2.0);
CA_EXTERN NSString * const kCAAlignmentJustified
    CA_AVAILABLE_STARTING (10.5, 3.2, 9.0, 2.0);

NS_ASSUME_NONNULL_END

```

# 应用

```objective-c
CATextLayer *textLayer = [CATextLayer layer];
textLayer.string = @"test";
textLayer.bounds = CGRectMake(0, 0, 200, 20);
textLayer.font = @"HiraKakuProN-W3"; // 字体的名字 不是 UIFont
textLayer.fontSize = 12.f;//字体的大小

// UIFont *font = [UIFont systemFontOfSize:14]; 
// CFStringRef fontCFString = (__bridge CFStringRef)font.fontName;
// CGFontRef fontRef = CGFontCreateWithFontName(fontCFString);
// textLayer.font = fontRef;
// textLayer.fontSize = font.pointSize;
// CGFontRelease(fontRef); //与CFRelease的功能相当 当字体的null的时候不会引起程序出错

textLayer.wrapped = YES;
textLayer.alignmentMode = kCAAlignmentCenter;
textLayer.position = CGPointMake(100, 100);
textLayer.contentsScale = [UIScreen mainScreen].scale;
textLayer.foregroundColor =[UIColor redColor].CGColor;
[self.view.layer addSublayer:textLayer];
```

