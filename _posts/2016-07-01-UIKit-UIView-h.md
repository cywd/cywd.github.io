---
layout: post
title: "UIKit/UIView.h"
excerpt: "UIKit/UIView.h"
categories: [OC]
tags: [UIView, OC]
date: 2016-07-01 
modified: 
comments: true
---

* TOC
{:toc}

```objective-c
//
//  UIView.h
//  UIKit
//
//  Copyright (c) 2005-2017 Apple Inc. All rights reserved.
//

//基础框架入口
#import <Foundation/Foundation.h>
#import <QuartzCore/QuartzCore.h>
#import <UIKit/UIResponder.h>
#import <UIKit/UIInterface.h>
#import <UIKit/UIKitDefines.h>
#import <UIKit/UIAppearance.h>
#import <UIKit/UIDynamicBehavior.h>
#import <UIKit/NSLayoutConstraint.h>
#import <UIKit/UITraitCollection.h>
#import <UIKit/UIFocus.h>

//UIViewAnimationCurve设置动画块中的动画属性变化的曲线
typedef NS_ENUM(NSInteger, UIViewAnimationCurve) {
    UIViewAnimationCurveEaseInOut,         // slow at beginning and end  缓慢开始，中间加速 ，然后减速到结束
    UIViewAnimationCurveEaseIn,            // slow at beginning 缓慢开始 加速到结束
    UIViewAnimationCurveEaseOut,           // slow at end 加速开始 加速到结束
    UIViewAnimationCurveLinear
};

typedef NS_ENUM(NSInteger, UIViewContentMode) {
借鉴
http://blog.csdn.net/iunion/article/details/7494511
    UIViewContentModeScaleToFill, 缩放内容到合适比例大小
    UIViewContentModeScaleAspectFit,      // contents scaled to fit with fixed aspect. remainder is transparent缩放内容到合适的大小，边界多余部分透明
    UIViewContentModeScaleAspectFill,     // contents scaled to fill with fixed aspect. some portion of content may be clipped.缩放内容填充到指定大小，边界多余的部分省略
    UIViewContentModeRedraw,              // redraw on bounds change (calls -setNeedsDisplay)重绘视图边界
    UIViewContentModeCenter,              // contents remain same size. positioned adjusted. 视图保持等比缩放
    UIViewContentModeTop, // 视图顶部对齐
    UIViewContentModeBottom,// 视图底部对齐
    UIViewContentModeLeft, // 视图左侧对齐
    UIViewContentModeRight, // 视图右侧对齐
    UIViewContentModeTopLeft, // 视图左上角对齐
    UIViewContentModeTopRight, // 视图右上角对齐
    UIViewContentModeBottomLeft, // 视图左下角对齐
    UIViewContentModeBottomRight, // 视图右下角对齐
};
//过渡动画效果
typedef NS_ENUM(NSInteger, UIViewAnimationTransition) {
    UIViewAnimationTransitionNone,          //不使用动画
    UIViewAnimationTransitionFlipFromLeft,  //从左向右旋转翻页
    UIViewAnimationTransitionFlipFromRight, //从右向左旋转翻页
    UIViewAnimationTransitionCurlUp,        //卷曲翻页,从下往上
    UIViewAnimationTransitionCurlDown,      //卷曲翻页，从上往下
};

typedef NS_OPTIONS(NSUInteger, UIViewAutoresizing) {
    UIViewAutoresizingNone                 = 0,//不自动调整
    UIViewAutoresizingFlexibleLeftMargin   = 1 << 0,//自动调整与superView左边的距离，保证与superView右边的距离不变
    UIViewAutoresizingFlexibleWidth        = 1 << 1,//自动调整自己的宽度，保证与superView左边和右边的距离不变
    UIViewAutoresizingFlexibleRightMargin  = 1 << 2,//自动调整与superView右边的距离，保证与superView左边的距离不变
    UIViewAutoresizingFlexibleTopMargin    = 1 << 3,//自动调整与superView顶部的距离，保证与superView底部的距离不变
    UIViewAutoresizingFlexibleHeight       = 1 << 4,//自动调整自己的宽度，保证与superView上边和下边的距离不变
    UIViewAutoresizingFlexibleBottomMargin = 1 << 5//自动调整与superView底部的距离，保证与superView顶部的距离不变
};

typedef NS_OPTIONS(NSUInteger, UIViewAnimationOptions) {
    UIViewAnimationOptionLayoutSubviews            = 1 <<  0,
    UIViewAnimationOptionAllowUserInteraction      = 1 <<  1, // turn on user interaction while animating
    UIViewAnimationOptionBeginFromCurrentState     = 1 <<  2, // start all views from current value, not initial value
    UIViewAnimationOptionRepeat                    = 1 <<  3, // repeat animation indefinitely
    UIViewAnimationOptionAutoreverse               = 1 <<  4, // if repeat, run animation back and forth
    UIViewAnimationOptionOverrideInheritedDuration = 1 <<  5, // ignore nested duration
    UIViewAnimationOptionOverrideInheritedCurve    = 1 <<  6, // ignore nested curve
    UIViewAnimationOptionAllowAnimatedContent      = 1 <<  7, // animate contents (applies to transitions only)
    UIViewAnimationOptionShowHideTransitionViews   = 1 <<  8, // flip to/from hidden state instead of adding/removing
    UIViewAnimationOptionOverrideInheritedOptions  = 1 <<  9, // do not inherit any options or animation type

    UIViewAnimationOptionCurveEaseInOut            = 0 << 16, // default
    UIViewAnimationOptionCurveEaseIn               = 1 << 16,
    UIViewAnimationOptionCurveEaseOut              = 2 << 16,
    UIViewAnimationOptionCurveLinear               = 3 << 16,

    UIViewAnimationOptionTransitionNone            = 0 << 20, // default
    UIViewAnimationOptionTransitionFlipFromLeft    = 1 << 20,
    UIViewAnimationOptionTransitionFlipFromRight   = 2 << 20,
    UIViewAnimationOptionTransitionCurlUp          = 3 << 20,
    UIViewAnimationOptionTransitionCurlDown        = 4 << 20,
    UIViewAnimationOptionTransitionCrossDissolve   = 5 << 20,
    UIViewAnimationOptionTransitionFlipFromTop     = 6 << 20,
    UIViewAnimationOptionTransitionFlipFromBottom  = 7 << 20,
  
    UIViewAnimationOptionPreferredFramesPerSecondDefault     = 0 << 24,
    UIViewAnimationOptionPreferredFramesPerSecond60          = 3 << 24,
    UIViewAnimationOptionPreferredFramesPerSecond30          = 7 << 24,
} NS_ENUM_AVAILABLE_IOS(4_0);

typedef NS_OPTIONS(NSUInteger, UIViewKeyframeAnimationOptions) {
    UIViewKeyframeAnimationOptionLayoutSubviews            = UIViewAnimationOptionLayoutSubviews,
    UIViewKeyframeAnimationOptionAllowUserInteraction      = UIViewAnimationOptionAllowUserInteraction, // turn on user interaction while animating
    UIViewKeyframeAnimationOptionBeginFromCurrentState     = UIViewAnimationOptionBeginFromCurrentState, // start all views from current value, not initial value
    UIViewKeyframeAnimationOptionRepeat                    = UIViewAnimationOptionRepeat, // repeat animation indefinitely
    UIViewKeyframeAnimationOptionAutoreverse               = UIViewAnimationOptionAutoreverse, // if repeat, run animation back and forth
    UIViewKeyframeAnimationOptionOverrideInheritedDuration = UIViewAnimationOptionOverrideInheritedDuration, // ignore nested duration
    UIViewKeyframeAnimationOptionOverrideInheritedOptions  = UIViewAnimationOptionOverrideInheritedOptions, // do not inherit any options or animation type

    UIViewKeyframeAnimationOptionCalculationModeLinear     = 0 << 10, // default
    UIViewKeyframeAnimationOptionCalculationModeDiscrete   = 1 << 10,
    UIViewKeyframeAnimationOptionCalculationModePaced      = 2 << 10,
    UIViewKeyframeAnimationOptionCalculationModeCubic      = 3 << 10,
    UIViewKeyframeAnimationOptionCalculationModeCubicPaced = 4 << 10
} NS_ENUM_AVAILABLE_IOS(7_0);

typedef NS_ENUM(NSUInteger, UISystemAnimation) {
    UISystemAnimationDelete,    // removes the views from the hierarchy when complete 系统自带删除动画
} NS_ENUM_AVAILABLE_IOS(7_0);

typedef NS_ENUM(NSInteger, UIViewTintAdjustmentMode) {
    UIViewTintAdjustmentModeAutomatic,

    UIViewTintAdjustmentModeNormal,
    UIViewTintAdjustmentModeDimmed, //tintColor的默认值会自动变得模糊
} NS_ENUM_AVAILABLE_IOS(7_0);

typedef NS_ENUM(NSInteger, UISemanticContentAttribute) {
    UISemanticContentAttributeUnspecified = 0,
    UISemanticContentAttributePlayback, // for playback controls such as Play/RW/FF buttons and playhead scrubbers
    UISemanticContentAttributeSpatial, // for controls that result in some sort of directional change in the UI, e.g. a segmented control for text alignment or a D-pad in a game
    UISemanticContentAttributeForceLeftToRight,
    UISemanticContentAttributeForceRightToLeft
} NS_ENUM_AVAILABLE_IOS(9_0);


@protocol UICoordinateSpace <NSObject>

- (CGPoint)convertPoint:(CGPoint)point toCoordinateSpace:(id <UICoordinateSpace>)coordinateSpace NS_AVAILABLE_IOS(8_0);
- (CGPoint)convertPoint:(CGPoint)point fromCoordinateSpace:(id <UICoordinateSpace>)coordinateSpace NS_AVAILABLE_IOS(8_0);
- (CGRect)convertRect:(CGRect)rect toCoordinateSpace:(id <UICoordinateSpace>)coordinateSpace NS_AVAILABLE_IOS(8_0);
- (CGRect)convertRect:(CGRect)rect fromCoordinateSpace:(id <UICoordinateSpace>)coordinateSpace NS_AVAILABLE_IOS(8_0);

@property (readonly, nonatomic) CGRect bounds NS_AVAILABLE_IOS(8_0);

@end

@class UIBezierPath, UIEvent, UIWindow, UIViewController, UIColor, UIGestureRecognizer, UIMotionEffect, CALayer, UILayoutGuide;
//UIView是iOS系统中界面元素的基础，所有的界面元素都继承自它。UIView本身完全是由CoreAnimation来实现的。它真正的绘图部分是由一个叫CALayer（Core Animation Layer）的类来管理。UIView本身，更像是一个CALayer的管理器，访问它的跟绘图和坐标有关的属性，如frame，bounds等，而内部都是在访问它所包含的CALayer的相关属性。
//UIView继承自UIResponder UIResponder是所有事件的响应基石。

NS_CLASS_AVAILABLE_IOS(2_0) @interface UIView : UIResponder <NSCoding, UIAppearance, UIAppearanceContainer, UIDynamicItem, UITraitEnvironment, UICoordinateSpace, UIFocusItem, CALayerDelegate>

#if UIKIT_DEFINE_AS_PROPERTIES
@property(class, nonatomic, readonly) Class layerClass;                        // default is [CALayer class]. Used when creating the underlying layer for the view.
#else
//UIView有个layer属性，可以返回它的主CALayer实例，UIView有一个layerClass方法，返回主layer所使用的类，UIView的子类可以通过重载这个方法来让UIView使用不同的CALayer来显示
+ (Class)layerClass;   // default is [CALayer class]. Used when creating the underlying layer for the view.
#endif



// 当从代码实例化UIView的时候，initWithFrame会执行；
// 当从文件加载UIView的时候，initWithCoder会执行。
// 初始化方法并且给一个frame
- (instancetype)initWithFrame:(CGRect)frame;          // default initializer

- (nullable instancetype)initWithCoder:(NSCoder *)aDecoder NS_DESIGNATED_INITIALIZER;

//是否接受用户点击 getter=isUserInterractionEnabled 重构getter方法
@property(nonatomic,getter=isUserInteractionEnabled) BOOL userInteractionEnabled;  // default is YES. if set to NO, user events (touch, keys) are ignored and removed from the event queue.
//给UIView加一个tag默认是0
@property(nonatomic)                                 NSInteger tag;                // default is 0
//返回view的layer
@property(nonatomic,readonly,retain)                 CALayer  *layer;              // returns view's layer. Will always return a non-nil value. view is layer's delegate


#if UIKIT_DEFINE_AS_PROPERTIES
@property(nonatomic,readonly) BOOL canBecomeFocused NS_AVAILABLE_IOS(9_0); // NO by default //是否能被设置为高亮
#else
- (BOOL)canBecomeFocused NS_AVAILABLE_IOS(9_0); // NO by default
#endif
@property (readonly, nonatomic, getter=isFocused) BOOL focused NS_AVAILABLE_IOS(9_0);

@property (nonatomic) UISemanticContentAttribute semanticContentAttribute NS_AVAILABLE_IOS(9_0);

// This method returns the layout direction implied by the provided semantic content attribute relative to the application-wide layout direction (as returned by UIApplication.sharedApplication.userInterfaceLayoutDirection).
+ (UIUserInterfaceLayoutDirection)userInterfaceLayoutDirectionForSemanticContentAttribute:(UISemanticContentAttribute)attribute NS_AVAILABLE_IOS(9_0);

// This method returns the layout direction implied by the provided semantic content attribute relative to the provided layout direction. For example, when provided a layout direction of RightToLeft and a semantic content attribute of Playback, this method returns LeftToRight. Layout and drawing code can use this method to determine how to arrange elements, but might find it easier to query the container view’s effectiveUserInterfaceLayoutDirection property instead.
+ (UIUserInterfaceLayoutDirection)userInterfaceLayoutDirectionForSemanticContentAttribute:(UISemanticContentAttribute)semanticContentAttribute relativeToLayoutDirection:(UIUserInterfaceLayoutDirection)layoutDirection NS_AVAILABLE_IOS(10_0);

// Returns the user interface layout direction appropriate for arranging the immediate content of this view. Always consult the effectiveUserInterfaceLayoutDirection of the view whose immediate content is being arranged or drawn. Do not assume that the value propagates through the view’s subtree.
@property (readonly, nonatomic) UIUserInterfaceLayoutDirection effectiveUserInterfaceLayoutDirection NS_AVAILABLE_IOS(10_0);


@end

@interface UIView(UIViewGeometry)

// animatable. do not use frame if view is transformed since it will not correctly reflect the actual location of the view. use bounds + center instead.
//frame是指视图在其父视图坐标系中的位置与尺寸。可以用bounds和center代替
@property(nonatomic) CGRect            frame;

// use bounds/center and not frame if non-identity transform. if bounds dimension is odd, center may be have fractional part 
//是指视图在其自己的坐标系(有一个自身的坐标系)中的位置和尺寸(与父视图无关)
@property(nonatomic) CGRect            bounds;      // default bounds is zero origin, frame size. animatable
//该视图的中心点在其父视图坐标系中的位置坐标
@property(nonatomic) CGPoint          center;      // center is center of frame. animatable
// 形变属性(平移\缩放\旋转)
@property(nonatomic) CGAffineTransform transform;   // default is CGAffineTransformIdentity. animatable
@property(nonatomic) CGFloat          contentScaleFactor NS_AVAILABLE_IOS(4_0);
//getter=isMultipleTouchEnabled 重构getter方法 当前View是否支持多点触控事件 默认NO
@property(nonatomic,getter=isMultipleTouchEnabled) BOOL multipleTouchEnabled;   // default is NO
//决定当前的view是否是处理触摸事件的唯一对象(不能同时点击多个view) 默认是NO
@property(nonatomic,getter=isExclusiveTouch) BOOL      exclusiveTouch;         // default is NO

- (UIView *)hitTest:(CGPoint)point withEvent:(UIEvent *)event;   // recursively calls -pointInside:withEvent:. point is in the receiver's coordinate system
- (BOOL)pointInside:(CGPoint)point withEvent:(UIEvent *)event;   // default returns YES if point is in bounds

==========*******convertPonit****===================

 //将point由point所在的view转换到目标视图中，返回在目标视图view中
- (CGPoint)convertPoint:(CGPoint)point toView:(UIView *)view;
 //将point从view中转换到当前视图中，返回在当前视图的point。
CGPoint pointInView =  [self.redView convertPoint:pointInOriView fromView:self.view];

- (CGPoint)convertPoint:(CGPoint)point fromView:(UIView *)view;
// 将rect由rect所在视图转换到目标视图view中，返回在目标视图view中的rect
- (CGRect)convertRect:(CGRect)rect toView:(UIView *)view;
// 将rect从view中转换到当前视图中，返回在当前视图中的rect
- (CGRect)convertRect:(CGRect)rect fromView:(UIView *)view;

例把UITableViewCell中的subview(btn)的frame转换到 controllerA中
// controllerA 中有一个UITableView, UITableView里有多行UITableVieCell，cell上放有一个button

// 在controllerA中实现:

CGRect rc = [cell convertRect:cell.btn.frame toView:self.view];

或

CGRect rc = [self.view convertRect:cell.btn.frame fromView:cell];

// 此rc为btn在controllerA中的rect
或当已知btn时：

CGRect rc = [btn.superview convertRect:btn.frame toView:self.view];

或

CGRect rc = [self.view convertRect:btn.frame fromView:btn.superview];
=================***************==========================

//当你改变视图的边框矩形时，其内嵌的子视图的位置和尺寸往往需要改变，以适应原始视图的新尺寸。如果视图的autoresizesSubViews属性声明被设置为YES，其子视图会根据autoresizingMask属性的值自动进行尺寸调整
@property(nonatomic) BOOL              autoresizesSubviews; // default is YES. if set, subviews are adjusted according to their autoresizingMask if self.bounds changes
//设置视图的自动尺寸调整行为的方法是通过OR操作符讲期望的自定尺寸调整常量连接起来。并将结果赋值给视图的autoresizingMask属性。比如要使一个视图和其父视图左下角的相对位置保持不变可以加入UIViewAutoresizingFlexibleRightMargin
@property(nonatomic) UIViewAutoresizing autoresizingMask;    // simple resize. default is UIViewAutoresizingNone
//计算并且返回一个最适应接收子视图的大小
- (CGSize)sizeThatFits:(CGSize)size;     // return 'best' size to fit given size. does not actually resize view. Default is return existing view size
//移动并调整子视图的大小
- (void)sizeToFit;                       // calls sizeThatFits: with current view bounds and changes bounds size.

@end

@interface UIView(UIViewHierarchy)
//父View
@property(nonatomic,readonly) UIView      *superview;
//子view 子控件的子控件并不在里面
@property(nonatomic,readonly,copy) NSArray *subviews;
//窗口
@property(nonatomic,readonly) UIWindow    *window;
//将当前视图从父视图和窗口移除，并且把他的响应事件的响应链移除
- (void)removeFromSuperview;
//指定索引插入视图
- (void)insertSubview:(UIView *)view atIndex:(NSInteger)index;
//交换指定索引的两个View的位置
- (void)exchangeSubviewAtIndex:(NSInteger)index1 withSubviewAtIndex:(NSInteger)index2;
//视图的添加都是以栈的方式，先进先出
//添加一个子控件(新添加的控件默认都在subviews数组的后面，新添加的控件默认都显示在最上面\最顶部)
- (void)addSubview:(UIView *)view;
//添加一个子控件(被挡在siblingSubview下面)
- (void)insertSubview:(UIView *)view belowSubview:(UIView *)siblingSubview;
//添加一个子控件(盖在siblingSubview上面)
- (void)insertSubview:(UIView *)view aboveSubview:(UIView *)siblingSubview;
//将某个子控件拉到最上面(最顶部)来显示
- (void)bringSubviewToFront:(UIView *)view;
//将某个子控件拉到最下面(最底部)来显示
- (void)sendSubviewToBack:(UIView *)view;
/***系统自动调用(留给子类去实现)***/
//通知视图已经添加子视图 默认不执行任何操作，子类可以重写
- (void)didAddSubview:(UIView *)subview;
//通知视图某个子视图即将被移除 默认不执行任何操作 子类可以重写
- (void)willRemoveSubview:(UIView *)subview;
//通知即将移动到新的父视图中
- (void)willMoveToSuperview:(UIView *)newSuperview;
//通知已经到新父视图
- (void)didMoveToSuperview;
//通知即将已移动到新的窗口
- (void)willMoveToWindow:(UIWindow *)newWindow;
//通知已经移动到新的窗口
- (void)didMoveToWindow;
/***系统自动调用***/
//是不是view的子控件或者子控件的子空间(是否为view的后代)
- (BOOL)isDescendantOfView:(UIView *)view;  // returns YES for self.
//通过tag获得对应的子控件(也可以是子控件的子控件)
- (UIView *)viewWithTag:(NSInteger)tag;     // recursive search. includes self
/***********布局*********/
// Allows you to perform layout before the drawing cycle happens. -layoutIfNeeded forces layout early
//使当前的layout弃用当收到并且触发一个layout更新在下一个更新循环中 进行标记
- (void)setNeedsLayout;
//立刻layout 一般和上面的setNeedsLayout配合使用
- (void)layoutIfNeeded;
/***系统自动调用(留给子类去实现)***/
//控件的frame，约束发生改变的时候就会调用，一般在这里重写布局子控件的位置和尺寸
//重写了这个方法后一定要调用[super layoutSubviews]
- (void)layoutSubviews;    // override point. called by layoutIfNeeded automatically. As of iOS 6.0, when constraints-based layout is used the base implementation applies the constraints-based layout, otherwise it does nothing.
/*
layoutSubviews在以下情况下会被调用：
1、init初始化不会触发layoutSubviews ,  但 initWithFrame 进行初始化时，当rect的值不为CGRectZero时,也会触发.
2、addSubview会触发layoutSubviews.
3、设置view的Frame会触发layoutSubviews，当然前提是frame的值设置前后发生了变化.
4、滚动一个UIScrollView会触发layoutSubviews.
5、旋转Screen会触发父UIView上的layoutSubviews事件.
6、改变一个UIView大小的时候也会触发父UIView上的layoutSubviews事件.
[1]、layoutSubviews对subviews重新布局
[2]、layoutSubviews方法调用先于drawRect
[3]、setNeedsLayout在receiver标上一个需要被重新布局的标记，在系统runloop的下一个周期自动调用layoutSubviews
[4]、layoutIfNeeded方法如其名，UIKit会判断该receiver是否需要layout
[5]、layoutIfNeeded遍历的不是superview链，应该是subviews链
*/

/* -layoutMargins returns a set of insets from the edge of the view's bounds that denote a default spacing for laying out content.
 If preservesSuperviewLayoutMargins is YES, margins cascade down the view tree, adjusting for geometry offsets, so that setting
 the left value of layoutMargins on a superview will affect the left value of layoutMargins for subviews positioned close to the
 left edge of their superview's bounds
   If your view subclass uses layoutMargins in its layout or drawing, override -layoutMarginsDidChange in order to refresh your 
 view if the margins change.
   On iOS 11.0 and later, please support both user interface layout directions by setting the directionalLayoutMargins property
 instead of the layoutMargins property. After setting the directionalLayoutMargins property, the values in the left and right
 fields of the layoutMargins property will depend on the user interface layout direction.
 */
//iOS8之后可以用 可以使用layoutMargins定义view之间的间距 这个属性只对autolayout布局生效
@property (nonatomic) UIEdgeInsets layoutMargins NS_AVAILABLE_IOS(8_0);

/* directionalLayoutMargins.leading is used on the left when the user interface direction is LTR and on the right for RTL.
 Vice versa for directionalLayoutMargins.trailing.
 */
@property (nonatomic) NSDirectionalEdgeInsets directionalLayoutMargins API_AVAILABLE(ios(11.0),tvos(11.0));

//这个属性默认是NO 如果把它设置为YES layoutMargins会根据屏幕中相关view的布局而改变
@property (nonatomic) BOOL preservesSuperviewLayoutMargins NS_AVAILABLE_IOS(8_0); // default is NO - set to enable pass-through or cascading behavior of margins from this view’s parent to its children

@property (nonatomic) BOOL insetsLayoutMarginsFromSafeArea API_AVAILABLE(ios(11.0),tvos(11.0));  // Default: YES // 默认按照safeArea insets

//在改变view的layoutMargins这个属性时，会触发这个方法，我们在自己的view里面可以重写这个方法来捕获layoutMargins的变化。我们可以在这个方法中触发drawing和layout的update
- (void)layoutMarginsDidChange NS_AVAILABLE_IOS(8_0);

/*safeAreaInsets 也就是 iPhoneX 的安全区域*/
@property (nonatomic,readonly) UIEdgeInsets safeAreaInsets API_AVAILABLE(ios(11.0),tvos(11.0));
/*当safeAreaInsets改变时会调用*/
- (void)safeAreaInsetsDidChange API_AVAILABLE(ios(11.0),tvos(11.0));

/* The edges of this guide are constrained to equal the edges of the view inset by the layoutMargins
 */
@property(readonly,strong) UILayoutGuide *layoutMarginsGuide NS_AVAILABLE_IOS(9_0);

/// This content guide provides a layout area that you can use to place text and related content whose width should generally be constrained to a size that is easy for the user to read. This guide provides a centered region that you can place content within to get this behavior for this view.
@property (nonatomic, readonly, strong) UILayoutGuide *readableContentGuide  NS_AVAILABLE_IOS(9_0);

/* The top of the safeAreaLayoutGuide indicates the unobscured top edge of the view (e.g, not behind
 the status bar or navigation bar, if present). Similarly for the other edges.
 */
@property(nonatomic,readonly,strong) UILayoutGuide *safeAreaLayoutGuide API_AVAILABLE(ios(11.0),tvos(11.0));
@end

@interface UIView(UIViewRendering)
/*
drawRect是对receiver的重绘
setNeedDisplay在receiver标上一个需要被重新绘图的标记，在下一个draw周期自动重绘，iphone device的刷新频率是60hz，也就是1/60秒后重绘
*/
//渲染 重写此方法 执行重绘 
- (void)drawRect:(CGRect)rect;
//需要重新渲染 标记为需要重绘 异步调用drawRect
- (void)setNeedsDisplay;
//需要重新渲染在某一块区域
- (void)setNeedsDisplayInRect:(CGRect)rect;


//YES：超出控件边框范围的内容都剪掉
@property(nonatomic)                 BOOL              clipsToBounds;              // When YES, content and subviews are clipped to the bounds of the view. Default is NO.
//背景色
@property(nonatomic,copy)            UIColor          *backgroundColor UI_APPEARANCE_SELECTOR; // default is nil. Can be useful with the appearance proxy on custom UIView subclasses.
//透明度(0.0~1.0)
@property(nonatomic)                 CGFloat          alpha;                      // animatable. default is 1.0
//YES:不透明 NO:透明 
/*
 决定该消息接收者(UIView instance)是否让其视图不透明,用处在于给绘图系统提供一个性能优化开关。
insertDemoTwo.opaque = NO;
该值为YES, 那么绘图在绘制该视图的时候把整个视图当作不透明对待。优化绘图过程并提升系统性能；为了性能方面的考量，默认被置为YES。
该值为NO,，不去做优化操作。 
一个不透明视图需要整个边界里面的内容都是不透明。基于这个原因，opaque设置为YES，要求对应的alpha必须为1.0。如果一个UIView实例opaque被设置为YES, 而同时它又没有完全填充它的边界(bounds),或者它包含了整个或部分的透明的内容视图，那么将会导致未知的结果。 
因此，如果视图部分或全部支持透明，那么你必须把opaque这个值设置为NO.
*/
@property(nonatomic,getter=isOpaque) BOOL              opaque;                     // default is YES. opaque views must fill their entire bounds or the results are undefined. the active CGContext in drawRect: will not have been cleared and may have non-zeroed pixels

/*YES:自动的清除之前的渲染(绘制前是否清屏)  NO:不自动清除   default is YES
insertDemoOne.clearsContextBeforeDrawing = YES;
提高描画性能（特别是在滚动过程）的另一个方法是将视图的clearsContextBeforeDrawing属性设置为NO。当这个属性被设置为YES时，UIKIt会在调用drawRect:方法之前，把即将被该方法更新的区域填充为透明的黑色。将这个属性设置为NO可以取消相应的填充操作，而由应用程序负责完全重画传给drawRect:方法的更新矩形中的部。这样的优化在滚动过程中通常是一个好的折衷。*/
@property(nonatomic)                 BOOL              clearsContextBeforeDrawing; // default is YES. ignored for opaque views. for non-opaque views causes the active CGContext in drawRect: to be pre-filled with transparent pixels
//YES:隐藏 NO:显示
@property(nonatomic,getter=isHidden) BOOL              hidden;                     // default is NO. doesn't check superviews
//内容模式主要用于指定控件内容（注意不是子控件）如何填充，一般UIImageView经常使用，默认为UIViewContentModeScaleToFill
@property(nonatomic)                 UIViewContentMode     contentMode;                // default is UIViewContentModeScaleToFill
/*http://blog.csdn.net/andyddd/article/details/7574885//视图拉伸和缩略 （0.0-1.0之间）iOS6.0弃用 被-[UIImage resizableImageWithCapInsets:]代替  imageDemo.image = [UIImage imageNamed:@"demo.png"];
 [imageDemo setContentStretch:CGRectMake(50.0/100.0, 75.0/150.0, 10.0/100.0, 10.0/150.0)];
当demo.png大于imageDemo的大小时，就缩小。
当demo.png小于imageDemo的大小时，就放大。*/
@property(nonatomic)                 CGRect            contentStretch NS_DEPRECATED_IOS(3_0,6_0); // animatable. default is unit rectangle { {0,0} {1,1} }. Now deprecated: please use -[UIImage resizableImageWithCapInsets:] to achieve the same effect.
//遮罩View
@property(nonatomic,retain)          UIView          *maskView NS_AVAILABLE_IOS(8_0);

/*
 -tintColor always returns a color. The color returned is the first non-default value in the receiver's superview chain (starting with itself).
 If no non-default value is found, a system-defined color is returned.
 If this view's -tintAdjustmentMode returns Dimmed, then the color that is returned for -tintColor will automatically be dimmed.
 If your view subclass uses tintColor in its rendering, override -tintColorDidChange in order to refresh the rendering if the color changes.
 */
//色调颜色
@property(nonatomic,retain) UIColor *tintColor NS_AVAILABLE_IOS(7_0);

/*
 -tintAdjustmentMode always returns either UIViewTintAdjustmentModeNormal or UIViewTintAdjustmentModeDimmed. The value returned is the first non-default value in the receiver's superview chain (starting with itself).
 If no non-default value is found, UIViewTintAdjustmentModeNormal is returned.
 When tintAdjustmentMode has a value of UIViewTintAdjustmentModeDimmed for a view, the color it returns from tintColor will be modified to give a dimmed appearance.
 When the tintAdjustmentMode of a view changes (either the view's value changing or by one of its superview's values changing), -tintColorDidChange will be called to allow the view to refresh its rendering.
 */
//色调调整模式
@property(nonatomic) UIViewTintAdjustmentMode tintAdjustmentMode NS_AVAILABLE_IOS(7_0);

/*
 The -tintColorDidChange message is sent to appropriate subviews of a view when its tintColor is changed by client code or to subviews in the view hierarchy of a view whose tintColor is implicitly changed when its superview or tintAdjustmentMode changes.
 */
//当tintColor属性改变时会触发方法的调用 iOS7之后可用
- (void)tintColorDidChange NS_AVAILABLE_IOS(7_0);

@end

@interface UIView(UIViewAnimation)
//类方法  开始一个动画 4.0以后不推荐使用
+ (void)beginAnimations:(NSString *)animationID context:(void *)context;  // additional context info passed to will start/did stop selectors. begin/commit can be nested
//结束动画 类似数据库的事物处理
+ (void)commitAnimations;                                                 // starts up any animations when the top level animation is commited

// no getters. if called outside animation block, these setters have no effect.
//设置动画委托
+ (void)setAnimationDelegate:(id)delegate;                          // default = nil
//当动画执行结束时 执行selector
+ (void)setAnimationWillStartSelector:(SEL)selector;                // default = NULL. -animationWillStart:(NSString *)animationID context:(void *)context
+ (void)setAnimationDidStopSelector:(SEL)selector;                  // default = NULL. -animationDidStop:(NSString *)animationID finished:(NSNumber *)finished context:(void *)context
//设置动画时间  时间参数为double类型 默认是0.2秒
+ (void)setAnimationDuration:(NSTimeInterval)duration;              // default = 0.2
//设置动画延迟时间
+ (void)setAnimationDelay:(NSTimeInterval)delay;                    // default = 0.0
//设置在动画块内部动画属性改变的开始时间
+ (void)setAnimationStartDate:(NSDate *)startDate;                  // default = now ([NSDate date])
//设置动画的旋转曲度变化 
+ (void)setAnimationCurve:(UIViewAnimationCurve)curve;              // default = UIViewAnimationCurveEaseInOut
//设置动画在动画模块中重复次数
+ (void)setAnimationRepeatCount:(float)repeatCount;                 // default = 0.0.  May be fractional
//设置动画块中的动画效果是否自动播放
+ (void)setAnimationRepeatAutoreverses:(BOOL)repeatAutoreverses;    // default = NO. used if repeat count is non-zero
//设置动画是否从当前状态开始播放
+ (void)setAnimationBeginsFromCurrentState:(BOOL)fromCurrentState;  // default = NO. If YES, the current view position is always used for new animations -- allowing animations to "pile up" on each other. Otherwise, the last end state is used for the animation (the default).
// 在动画块设置过渡效果 transition把一个过渡效果应用到视图中  view需要过渡的视图对象  cache
如果是YES，那么在开始和结束图片视图渲染一次并在动画中创建帧；否则，视图将会在每一帧都渲染。例如缓存，你不需要在视图转变中不停的更新，你只需要等到转换完成再去更新视图。
1、开始一个动画块。
2、在容器视图中设置转换。
3、在容器视图中移除子视图。
4、在容器视图中添加子视图。
5、结束动画块。
+ (void)setAnimationTransition:(UIViewAnimationTransition)transition forView:(UIView *)view cache:(BOOL)cache;  // current limitation - only one per begin/commit block
//设置是否开启动画 默认YES 
+ (void)setAnimationsEnabled:(BOOL)enabled;                         // ignore any attribute changes while set.
#if UIKIT_DEFINE_AS_PROPERTIES
@property(class, nonatomic, readonly) BOOL areAnimationsEnabled;
#else
//验证动画是否开启 YES:开启 NO:关闭
+ (BOOL)areAnimationsEnabled;
#endif
//先检查动画当前是否启用，然后禁止动画，执行block内方法，最后重新启用动画。它并不会阻塞基于CoreAnimation的动画
+ (void)performWithoutAnimation:(void (NS_NOESCAPE ^)(void))actionsWithoutAnimation NS_AVAILABLE_IOS(7_0);

#if UIKIT_DEFINE_AS_PROPERTIES
@property(class, nonatomic, readonly) NSTimeInterval inheritedAnimationDuration NS_AVAILABLE_IOS(9_0);
#else
+ (NSTimeInterval)inheritedAnimationDuration NS_AVAILABLE_IOS(9_0);
#endif

@end

@interface UIView(UIViewAnimationWithBlocks)
//动画效果处理块 duration动画时间 delay延迟时间 options动画参数 animations动画效果块 可以设置属性如下：frame bounds center 
//transform alpha backgroundColor contentStretch  completion完成后需要做的操作
+ (void)animateWithDuration:(NSTimeInterval)duration delay:(NSTimeInterval)delay options:(UIViewAnimationOptions)options animations:(void (^)(void))animations completion:(void (^)(BOOL finished))completion NS_AVAILABLE_IOS(4_0);
//没有延迟时间 没有动画参数 options默认为0
+ (void)animateWithDuration:(NSTimeInterval)duration animations:(void (^)(void))animations completion:(void (^)(BOOL finished))completion NS_AVAILABLE_IOS(4_0); // delay = 0.0, options = 0
//动画效果处理块 delay = 0.0, options = 0, completion = NULL
+ (void)animateWithDuration:(NSTimeInterval)duration animations:(void (^)(void))animations NS_AVAILABLE_IOS(4_0); // delay = 0.0, options = 0, completion = NULL

/* Performs `animations` using a timing curve described by the motion of a spring. When `dampingRatio` is 1, the animation will smoothly decelerate to its final model values without oscillating. Damping ratios less than 1 will oscillate more and more before coming to a complete stop. You can use the initial spring velocity to specify how fast the object at the end of the simulated spring was moving before it was attached. It's a unit coordinate system, where 1 is defined as travelling the total animation distance in a second. So if you're changing an object's position by 200pt in this animation, and you want the animation to behave as if the object was moving at 100pt/s before the animation started, you'd pass 0.5. You'll typically want to pass 0 for the velocity. */
//参考 http://www.tuicool.com/articles/ZR7nYv  http://www.woshipm.com/ucd/85600.html
// Spring(弹簧) Animation的API 比一般动画多了两个参数 usingSpringWithDamping(范围为0.0f~1.0f)，数值越小弹簧的震动的效果越明显
// initialSpringVelocity 表示初始速度，数值越大一开始移动越快
// dampingRatio 设置弹簧的阻尼比例
// velocity 设置弹簧的最初速度
+ (void)animateWithDuration:(NSTimeInterval)duration delay:(NSTimeInterval)delay usingSpringWithDamping:(CGFloat)dampingRatio initialSpringVelocity:(CGFloat)velocity options:(UIViewAnimationOptions)options animations:(void (^)(void))animations completion:(void (^)(BOOL finished))completion NS_AVAILABLE_IOS(7_0);



/* [UIView transitionWithView:_redView
                          duration:2.0
                           options:UIViewAnimationOptionTransitionCurlDown
                        animations:^{
            [_blackView removeFromSuperview];
            [_redView addSubview:_blackView];
        } completion:^(BOOL finished) {
     _redView.backgroundColor = [UIColor brownColor];
        }];***/
//国度动画效果块
+ (void)transitionWithView:(UIView *)view duration:(NSTimeInterval)duration options:(UIViewAnimationOptions)options animations:(void (^)(void))animations completion:(void (^)(BOOL finished))completion NS_AVAILABLE_IOS(4_0);

//视图之间切换的国度动画效果块
+ (void)transitionFromView:(UIView *)fromView toView:(UIView *)toView duration:(NSTimeInterval)duration options:(UIViewAnimationOptions)options completion:(void (^)(BOOL finished))completion NS_AVAILABLE_IOS(4_0); // toView added to fromView.superview, fromView removed from its superview

/* Performs the requested system-provided animation on one or more views. Specify addtional animations in the parallelAnimations block. These additional animations will run alongside the system animation with the same timing and duration that the system animation defines/inherits. Additional animations should not modify properties of the view on which the system animation is being performed. Not all system animations honor all available options.
 */
//在一组视图上执行指定的系统动画，并可以并行自定义动画。其中parallelAnimations就是与系统动画并行的自定义动画
+ (void)performSystemAnimation:(UISystemAnimation)animation onViews:(NSArray *)views options:(UIViewAnimationOptions)options animations:(void (^)(void))parallelAnimations completion:(void (^)(BOOL finished))completion NS_AVAILABLE_IOS(7_0);

@end

@interface UIView (UIViewKeyframeAnimations)
/***********
[UIViewanimateKeyframesWithDuration:2.0delay:0options:UIViewKeyframeAnimationOptionRepeatanimations:^{

        _blackView.frame = CGRectMake(30, 30, 50, 50);
        [UIView addKeyframeWithRelativeStartTime:0.5 relativeDuration:0 animations:^{
            _redView.frame = CGRectMake(50, 50, 50, 50);
        }];


    } completion:^(BOOL finished) {

        _redView.frame= CGRectMake(50, 50, 100, 100);;
       _blackView.frame = CGRectMake(30, 30, 80, 80);

    }];

*/
  
//为当前视图创建一个可以用于设置基本关键帧动画的block对象从IOS7开始使用
//这里说一下参数，第一个frameStartTime其实是个倍数从0到1，假设一个动画持续的时间是2秒
//设置frameStartTime为0.5，那么后面设置的动画，将会在整体动画执行1秒后开始执行
//第二个参数frameDuration同第一个，是指动画持续时间
//第四个是一个block对象，里面就是你设置的所要执行的动画，无参数和返回值
//这个方法可以结合  + (Class)layerClass 使用
+ (void)animateKeyframesWithDuration:(NSTimeInterval)duration delay:(NSTimeInterval)delay options:(UIViewKeyframeAnimationOptions)options animations:(void (^)(void))animations completion:(void (^)(BOOL finished))completion NS_AVAILABLE_IOS(7_0);

//指定一个关键帧的单个贞的时间和动画 iOS7后可用 
//frameStartTime是一个倍数从0到1，假设一个动画持续的时间是2秒 设置frameStartTime为0.5那么后面设置的动画将会在整体动画执行1秒后开始
frameDuration是指动画持续时间
+ (void)addKeyframeWithRelativeStartTime:(double)frameStartTime relativeDuration:(double)frameDuration animations:(void (^)(void))animations NS_AVAILABLE_IOS(7_0); // start time and duration are values between 0.0 and 1.0 specifying time and duration relative to the overall time of the keyframe animation

@end

@interface UIView (UIViewGestureRecognizers)

@property(nonatomic,copy) NSArray *gestureRecognizers NS_AVAILABLE_IOS(3_2);//手势识别器
/*
UIKit 中UIGestureRecognizer类的子类系列如下：
UITapGestureRecognizer – “轻击”手势。可以配置为“单击”和“连击”的识别。
UIPinchGestureRecognizer –“捏合”手势。该手势通常用于缩放视图或改变可视组件的大小。
UIPanGestureRecognizer – “平移”手势。识别拖拽或移动动作。
UISwipeGestureRecognizer – “轻扫”手势。当用户从屏幕上划过时识别为该手势。可以指定该动作的方向（上、下、左、右）。
UIRotationGestureRecognizer – “转动”手势。用户两指在屏幕上做相对环形运动。
UILongPressGestureRecognizer – “长按”手势。使用1指或多指触摸屏幕并保持一定时间。
*/
//给VIew添加一个手势
- (void)addGestureRecognizer:(UIGestureRecognizer*)gestureRecognizer NS_AVAILABLE_IOS(3_2);
//移除VIew的手势
- (void)removeGestureRecognizer:(UIGestureRecognizer*)gestureRecognizer NS_AVAILABLE_IOS(3_2);

// called when the recognizer attempts to transition out of UIGestureRecognizerStatePossible if a touch hit-tested to this view will be cancelled as a result of gesture recognition
// returns YES by default. return NO to cause the gesture recognizer to transition to UIGestureRecognizerStateFailed
// subclasses may override to prevent recognition of particular gestures. for example, UISlider prevents swipes parallel to the slider that start in the thumb
/*
手势识别处理方式在gesture recognizer视图转出《UIGestureRecognizerStatePossible》状态时调用，
如果返回NO,则转换到《UIGestureRecognizerStateFailed》;
如果返回YES,则继续识别触摸序列.(默认情况下为YES)。
[insertDemoOne gestureRecognizerShouldBegin:demoGesture];
*/
- (BOOL)gestureRecognizerShouldBegin:(UIGestureRecognizer *)gestureRecognizer NS_AVAILABLE_IOS(6_0);

@end

@interface UIView (UIViewMotionEffects)

/*! Begins applying `effect` to the receiver. The effect's emitted keyPath/value pairs will be
    applied to the view's presentation layer.

    Animates the transition to the motion effect's values using the present UIView animation
    context. */
  /*
当你打开装有iOS7以上的iPhone主屏，默认的背景是一幅蓝色的星空图片。当上下左右翻转iPhone时，有趣的效果将会出现，星空背景也会沿着各个方向发生位移，这与主屏上的各个App Icon形成了一种独特的视差效果。
//UIMotionEffect 
1. UIInterpolatingMotionEffect

UIInterpolatingMotionEffect是UIMotionEffect的子类，虽然扩展也不复杂，提供的方法也很简单，但在很多场景下可以比较直接和方便的满足我们的需求。

它有4个property:

1.keyPath，左右翻转屏幕将要影响到的属性，比如center.x。

2.type（UIInterpolatingMotionEffectType类型），观察者视角，也就是屏幕倾斜的方式，目前区分水平和垂直两种方式。

3&4.minimumRelativeValue和maximumRelativeValue，keyPath对应的值的变化范围，注意这个是id类型。min对应最小的offset，max对应最大的offset。

    UIInterpolatingMotionEffect * xEffect = [[UIInterpolatingMotionEffect alloc] initWithKeyPath:@"center.x" type:UIInterpolatingMotionEffectTypeTiltAlongHorizontalAxis];
    xEffect.minimumRelativeValue =  [NSNumber numberWithFloat:-40.0];
    xEffect.maximumRelativeValue = [NSNumber numberWithFloat:40.0];
    [targetView addMotionEffect:xEffect];
参考自http://www.cocoachina.com/ios/20150121/10967.html
*/
- (void)addMotionEffect:(UIMotionEffect *)effect NS_AVAILABLE_IOS(7_0);

/*! Stops applying `effect` to the receiver. Any affected presentation values will animate to
    their post-removal values using the present UIView animation context. */
//移除一个UIMotionEffect
- (void)removeMotionEffect:(UIMotionEffect *)effect NS_AVAILABLE_IOS(7_0);
//包含的UIMotionEffect
@property (copy, nonatomic) NSArray *motionEffects NS_AVAILABLE_IOS(7_0);

@end


//
// UIView Constraint-based Layout Support
//

typedef NS_ENUM(NSInteger, UILayoutConstraintAxis) {
    UILayoutConstraintAxisHorizontal = 0,
    UILayoutConstraintAxisVertical = 1
};

// Installing Constraints

/* A constraint is typically installed on the closest common ancestor of the views involved in the constraint.
 It is required that a constraint be installed on _a_ common ancestor of every view involved.  The numbers in a constraint are interpreted in the coordinate system of the view it is installed on.  A view is considered to be an ancestor of itself.
 */
@interface UIView (UIConstraintBasedLayoutInstallingConstraints)
//视图布局约束 
- (NSArray *)constraints NS_AVAILABLE_IOS(6_0);

//视图布局添加一个约束
- (void)addConstraint:(NSLayoutConstraint *)constraint NS_AVAILABLE_IOS(6_0); // This method will be deprecated in a future release and should be avoided.  Instead, set NSLayoutConstraint's active property to YES.
//视图布局上添加多个约束
- (void)addConstraints:(NSArray *)constraints NS_AVAILABLE_IOS(6_0); // This method will be deprecated in a future release and should be avoided.  Instead use +[NSLayoutConstraint activateConstraints:].
//移除视图布局一个约束
- (void)removeConstraint:(NSLayoutConstraint *)constraint NS_AVAILABLE_IOS(6_0); // This method will be deprecated in a future release and should be avoided.  Instead set NSLayoutConstraint's active property to NO.
//移除视图布局上多个约束
- (void)removeConstraints:(NSArray *)constraints NS_AVAILABLE_IOS(6_0); // This method will be deprecated in a future release and should be avoided.  Instead use +[NSLayoutConstraint deactivateConstraints:].
@end

// Core Layout Methods

/* To render a window, the following passes will occur, if necessary. 

 update constraints
 layout
 display

 Please see the conceptual documentation for a discussion of these methods.
 */

@interface UIView (UIConstraintBasedLayoutCoreMethods)
//调用新的视图布局自动触发,更新视图布局上的约束
- (void)updateConstraintsIfNeeded NS_AVAILABLE_IOS(6_0); // Updates the constraints from the bottom up for the view hierarchy rooted at the receiver. UIWindow's implementation creates a layout engine if necessary first.
//更新自定义视图布局 重写这个方法去适应特殊的约束在更新约束期间
- (void)updateConstraints NS_AVAILABLE_IOS(6_0); // Override this to adjust your special constraints during a constraints update pass
//判断视图是否需要更新约束
- (BOOL)needsUpdateConstraints NS_AVAILABLE_IOS(6_0);
//设置视图布局是否需要更新约束
- (void)setNeedsUpdateConstraints NS_AVAILABLE_IOS(6_0);
@end

// Compatibility and Adoption

@interface UIView (UIConstraintBasedCompatibility)

/* by default, the autoresizing mask on a view gives rise to constraints that fully determine the view's position.  Any constraints you set on the view are likely to conflict with autoresizing constraints, so you must turn off this property first. IB will turn it off for you.
 */
//标示是否自动遵循视图布局约束 默认是YES
- (BOOL)translatesAutoresizingMaskIntoConstraints NS_AVAILABLE_IOS(6_0); // Default YES
//设置是否自动遵循视图布局约束 
- (void)setTranslatesAutoresizingMaskIntoConstraints:(BOOL)flag NS_AVAILABLE_IOS(6_0);

/* constraint-based layout engages lazily when someone tries to use it (e.g., adds a constraint to a view).  If you do all of your constraint set up in -updateConstraints, you might never even receive updateConstraints if no one makes a constraint.  To fix this chicken and egg problem, override this method to return YES if your view needs the window to use constraint-based layout. 
 */
//返回是遵循自定义视图布局约束
+ (BOOL)requiresConstraintBasedLayout NS_AVAILABLE_IOS(6_0);

@end

// Separation of Concerns

@interface UIView (UIConstraintBasedLayoutLayering)

/* Constraints do not actually relate the frames of the views, rather they relate the "alignment rects" of views.  This is the same as the frame unless overridden by a subclass of UIView.  Alignment rects are the same as the "layout rects" shown in Interface Builder 3.  Typically the alignment rect of a view is what the end user would think of as the bounding rect around a control, omitting ornamentation like shadows and engraving lines.  The edges of the alignment rect are what is interesting to align, not the shadows and such. 
 */

/* These two methods should be inverses of each other.  UIKit will call both as part of layout computation.
 They may be overridden to provide arbitrary transforms between frame and alignment rect, though the two methods must be inverses of each other.
 However, the default implementation uses -alignmentRectInsets, so just override that if it's applicable.  It's easier to get right.
 A view that displayed an image with some ornament would typically override these, because the ornamental part of an image would scale up with the size of the frame. 
 Set the NSUserDefault UIViewShowAlignmentRects to YES to see alignment rects drawn.
 */
// AutoLayout并不会直接操作View的Frame，但是视图的alignment rect是起作用的。视图的默认alignmentRectInsets值就是(0,0,0,0)。
// 我们可以简单的对当前View设置用来布局的矩形，比如：
// 我们有一个自定义icon类型的Button，但是icon的大小比我们期望点击的Button区域要小。这个时候我们可以重写alignmentRectInsets，把icon放在适当的位置。
// 大多数情况下重写alignmentRectInsets这个方法可以满足我们的工作。如果需要更加个性化的修改，我们可以重写alignmentRectForFrame和frameForAlignmentRect这两个方法。比如我们不想减去视图固定的Insets，而是需要基于当前frame修改alignment rect。在重写这两个方法时，我们应该确保是互为可逆的。
- (CGRect)alignmentRectForFrame:(CGRect)frame NS_AVAILABLE_IOS(6_0);
- (CGRect)frameForAlignmentRect:(CGRect)alignmentRect NS_AVAILABLE_IOS(6_0);

/* override this if the alignment rect is obtained from the frame by insetting each edge by a fixed amount.  This is only called by alignmentRectForFrame: and frameForAlignmentRect:.
 */
#if UIKIT_DEFINE_AS_PROPERTIES
@property(nonatomic, readonly) UIEdgeInsets alignmentRectInsets NS_AVAILABLE_IOS(6_0);
#else
- (UIEdgeInsets)alignmentRectInsets NS_AVAILABLE_IOS(6_0);
#endif

/* When you make a constraint on the NSLayoutAttributeBaseline of a view, the system aligns with the bottom of the view returned from this method. A nil return is interpreted as the receiver, and a non-nil return must be in the receiver's subtree.  UIView's implementation returns self.
 */
//我们在使用布局约束中NSLayoutAttributeBaseline属性时，系统会默认返回当前视图的底部作为baseline。我们可以重写上述方法，但必须返回的是当前视图中的子视图
- (UIView *)viewForBaselineLayout NS_DEPRECATED_IOS(6_0, 9_0, "Override -viewForFirstBaselineLayout or -viewForLastBaselineLayout as appropriate, instead") __TVOS_PROHIBITED;


/* -viewForFirstBaselineLayout is called by the constraints system when interpreting
 the firstBaseline attribute for a view.
    For complex custom UIView subclasses, override this method to return the text-based
 (i.e., UILabel or non-scrollable UITextView) descendant of the receiver whose first baseline
 is appropriate for alignment.
    UIView's implementation returns [self viewForLastBaselineLayout], so if the same 
 descendant is appropriate for both first- and last-baseline layout you may override
 just -viewForLastBaselineLayout.
 */
@property(readonly,strong) UIView *viewForFirstBaselineLayout NS_AVAILABLE_IOS(9_0);

/* -viewForLastBaselineLayout is called by the constraints system when interpreting
 the lastBaseline attribute for a view.
    For complex custom UIView subclasses, override this method to return the text-based
 (i.e., UILabel or non-scrollable UITextView) descendant of the receiver whose last baseline
 is appropriate for alignment.
    UIView's implementation returns self.
 */
@property(readonly,strong) UIView *viewForLastBaselineLayout NS_AVAILABLE_IOS(9_0);

/* Override this method to tell the layout system that there is something it doesn't natively understand in this view, and this is how large it intrinsically is.  A typical example would be a single line text field.  The layout system does not understand text - it must just be told that there's something in the view, and that that something will take a certain amount of space if not clipped.  
 
 In response, UIKit will set up constraints that specify (1) that the opaque content should not be compressed or clipped, (2) that the view prefers to hug tightly to its content. 
 
 A user of a view may need to specify the priority of these constraints.  For example, by default, a push button 
 -strongly wants to hug its content in the vertical direction (buttons really ought to be their natural height)
 -weakly hugs its content horizontally (extra side padding between the title and the edge of the bezel is acceptable)
 -strongly resists compressing or clipping content in both directions. 
 
 However, you might have a case where you'd prefer to show all the available buttons with truncated text rather than losing some of the buttons. The truncation might only happen in portrait orientation but not in landscape, for example. In that case you'd want to setContentCompressionResistancePriority:forAxis: to (say) UILayoutPriorityDefaultLow for the horizontal axis.
 
 The default 'strong' and 'weak' priorities referred to above are UILayoutPriorityDefaultHigh and UILayoutPriorityDefaultLow.  
 
 Note that not all views have an intrinsicContentSize.  UIView's default implementation is to return (UIViewNoIntrinsicMetric, UIViewNoIntrinsicMetric).  The _intrinsic_ content size is concerned only with data that is in the view itself, not in other views. Remember that you can also set constant width or height constraints on any view, and you don't need to override instrinsicContentSize if these dimensions won't be changing with changing view content.
 */
UIKIT_EXTERN const CGFloat UIViewNoIntrinsicMetric NS_AVAILABLE_IOS(6_0); // -1
#if UIKIT_DEFINE_AS_PROPERTIES
@property(nonatomic, readonly) CGSize intrinsicContentSize NS_AVAILABLE_IOS(6_0);
#else
//通过重写intrinsicContentSize可以设置当前视图显示特定内容时的大小。比如我们设置一个自定义View，View里面包含一个Label显示文字，为了设置当前View在不同Size Class下内容的大小，我们可以这样:
 - (CGSize)intrinsicContentSize
{
  CGSize size = [label intrinsicContentSize];
  if (self.traitCollection.horizontalSizeClass == UIUserInterfaceSizeClassCompact) {
  size.width += 4.0f;
  } else {
    size.width += 40.0f;
  }
   if (self.traitCollection.verticalSizeClass == UIUserInterfaceSizeClassCompact) {
   size.height += 4.0;
  } else {
     size.height += 40.0;
  }       
   return size; 
 }

- (CGSize)intrinsicContentSize NS_AVAILABLE_IOS(6_0);
#endif

//当有任何会影响这个Label内容大小的事件发生时，我们应该调用invalidateIntrinsicContentSize：
    label.text = @"content update"
    [self invalidateIntrinsicContentSize];
    // 或者比如当前视图Size Class改变的时候
    - (void)traitCollectionDidChange:(UITraitCollection *)previousTraitCollection
    {
        [super traitCollectionDidChange:previousTraitCollection];
        if ((self.traitCollection.verticalSizeClass != previousTraitCollection.verticalSizeClass)
            || (self.traitCollection.horizontalSizeClass != previousTraitCollection.horizontalSizeClass)) {
            [self invalidateIntrinsicContentSize];
        } 
    }
- (void)invalidateIntrinsicContentSize NS_AVAILABLE_IOS(6_0); // call this when something changes that affects the intrinsicContentSize.  Otherwise UIKit won't notice that it changed. 

//返回放大的视图布局的轴线
- (UILayoutPriority)contentHuggingPriorityForAxis:(UILayoutConstraintAxis)axis NS_AVAILABLE_IOS(6_0);
//设置放大的视图布局的轴线
- (void)setContentHuggingPriority:(UILayoutPriority)priority forAxis:(UILayoutConstraintAxis)axis NS_AVAILABLE_IOS(6_0);
//返回缩小的视图布局的轴线
- (UILayoutPriority)contentCompressionResistancePriorityForAxis:(UILayoutConstraintAxis)axis NS_AVAILABLE_IOS(6_0);
//设置缩小的视图的轴线
- (void)setContentCompressionResistancePriority:(UILayoutPriority)priority forAxis:(UILayoutConstraintAxis)axis NS_AVAILABLE_IOS(6_0);
/*
上面最后四个API主要是通过修改水平或者垂直方向的优先级来实现视图是基于水平缩小(放大)还是垂直缩小(放大)。当我们的视图需要根据内部内容进行调整大小时，我们应该使用上述方法为当前视图设置初始值。而不应该重写这几个方法。*/
@end

// Size To Fit

UIKIT_EXTERN const CGSize UILayoutFittingCompressedSize NS_AVAILABLE_IOS(6_0);
UIKIT_EXTERN const CGSize UILayoutFittingExpandedSize NS_AVAILABLE_IOS(6_0);

@interface UIView (UIConstraintBasedLayoutFittingSize)
/* The size fitting most closely to targetSize in which the receiver's subtree can be laid out while optimally satisfying the constraints. If you want the smallest possible size, pass UILayoutFittingCompressedSize; for the largest possible size, pass UILayoutFittingExpandedSize.
 Also see the comment for UILayoutPriorityFittingSizeLevel.
 */
//满足约束视图的布局大小  
 下面这两个API可以获得当前使用AutoLayout视图的size。其中targetSize可以传入UILayoutFittingCompressedSize(最小情况下可能的Size)或者UILayoutFittingExpandedSize(最大情况下可能的Size)
- (CGSize)systemLayoutSizeFittingSize:(CGSize)targetSize NS_AVAILABLE_IOS(6_0); // Equivalent to sending -systemLayoutSizeFittingSize:withHorizontalFittingPriority:verticalFittingPriority: with UILayoutPriorityFittingSizeLevel for both priorities.
//
- (CGSize)systemLayoutSizeFittingSize:(CGSize)targetSize withHorizontalFittingPriority:(UILayoutPriority)horizontalFittingPriority verticalFittingPriority:(UILayoutPriority)verticalFittingPriority NS_AVAILABLE_IOS(8_0);
@end

@interface UIView (UILayoutGuideSupport)

/* UILayoutGuide objects owned by the receiver.
 */
@property(nonatomic,readonly,copy) NSArray<__kindof UILayoutGuide *> *layoutGuides NS_AVAILABLE_IOS(9_0);

/* Adds layoutGuide to the receiver, passing the receiver in -setOwningView: to layoutGuide.
 */
- (void)addLayoutGuide:(UILayoutGuide *)layoutGuide NS_AVAILABLE_IOS(9_0);

/* Removes layoutGuide from the receiver, passing nil in -setOwningView: to layoutGuide.
 */
- (void)removeLayoutGuide:(UILayoutGuide *)layoutGuide NS_AVAILABLE_IOS(9_0);
@end
  
@class NSLayoutXAxisAnchor,NSLayoutYAxisAnchor,NSLayoutDimension;
@interface UIView (UIViewLayoutConstraintCreation)
/* Constraint creation conveniences. See NSLayoutAnchor.h for details.
 */
@property(readonly, strong) NSLayoutXAxisAnchor *leadingAnchor NS_AVAILABLE_IOS(9_0);
@property(readonly, strong) NSLayoutXAxisAnchor *trailingAnchor NS_AVAILABLE_IOS(9_0);
@property(readonly, strong) NSLayoutXAxisAnchor *leftAnchor NS_AVAILABLE_IOS(9_0);
@property(readonly, strong) NSLayoutXAxisAnchor *rightAnchor NS_AVAILABLE_IOS(9_0);
@property(readonly, strong) NSLayoutYAxisAnchor *topAnchor NS_AVAILABLE_IOS(9_0);
@property(readonly, strong) NSLayoutYAxisAnchor *bottomAnchor NS_AVAILABLE_IOS(9_0);
@property(readonly, strong) NSLayoutDimension *widthAnchor NS_AVAILABLE_IOS(9_0);
@property(readonly, strong) NSLayoutDimension *heightAnchor NS_AVAILABLE_IOS(9_0);
@property(readonly, strong) NSLayoutXAxisAnchor *centerXAnchor NS_AVAILABLE_IOS(9_0);
@property(readonly, strong) NSLayoutYAxisAnchor *centerYAnchor NS_AVAILABLE_IOS(9_0);
@property(readonly, strong) NSLayoutYAxisAnchor *firstBaselineAnchor NS_AVAILABLE_IOS(9_0);
@property(readonly, strong) NSLayoutYAxisAnchor *lastBaselineAnchor NS_AVAILABLE_IOS(9_0);

@end


// Debugging

/* Everything in this section should be used in debugging only, never in shipping code.  These methods may not exist in the future - no promises. 
 */
@interface UIView (UIConstraintBasedLayoutDebugging)

/* This returns a list of all the constraints that are affecting the current location of the receiver.  The constraints do not necessarily involve the receiver, they may affect the frame indirectly.
 Pass UILayoutConstraintAxisHorizontal for the constraints affecting [self center].x and CGRectGetWidth([self bounds]), and UILayoutConstraintAxisVertical for the constraints affecting[self center].y and CGRectGetHeight([self bounds]).
 */
//获得实体在不同方向上所有的布局约束
- (NSArray *)constraintsAffectingLayoutForAxis:(UILayoutConstraintAxis)axis NS_AVAILABLE_IOS(6_0);

/* If there aren't enough constraints in the system to uniquely determine layout, we say the layout is ambiguous.  For example, if the only constraint in the system was x = y + 100, then there are lots of different possible values for x and y.  This situation is not automatically detected by UIKit, due to performance considerations and details of the algorithm used for layout. 
 The symptom of ambiguity is that views sometimes jump from place to place, or possibly are just in the wrong place.
 -hasAmbiguousLayout runs a check for whether there is another center and bounds the receiver could have that could also satisfy the constraints.
 -exerciseAmbiguousLayout does more.  It randomly changes the view layout to a different valid layout.  Making the UI jump back and forth can be helpful for figuring out where you're missing a constraint. 
 */
//可以知道当前视图的布局是否会有歧义。这里有一个私有API _autolayoutTrace可以获得整个视图树的字符串。
- (BOOL)hasAmbiguousLayout NS_AVAILABLE_IOS(6_0);

//这个方法会随机改变视图的layout到另外一个有效的layout。这样我们就可以很清楚的看到哪一个layout导致了整体的布局约束出现了错误，或者我们应该增加更多的布局约束。
- (void)exerciseAmbiguityInLayout NS_AVAILABLE_IOS(6_0);

// 我们应该让上面的四个方法只在DEBUG环境下被调用。
@end
  
/* Everything in this section should be used in debugging only, never in shipping code.  These methods may not exist in the future - no promises.
 */
@interface UILayoutGuide (UIConstraintBasedLayoutDebugging)

/* This returns a list of all the constraints that are affecting the current location of the receiver.  The constraints do not necessarily involve the receiver, they may affect the frame indirectly.
 Pass UILayoutConstraintAxisHorizontal for the constraints affecting [self center].x and CGRectGetWidth([self bounds]), and UILayoutConstraintAxisVertical for the constraints affecting[self center].y and CGRectGetHeight([self bounds]).
 */
- (NSArray<__kindof NSLayoutConstraint *> *)constraintsAffectingLayoutForAxis:(UILayoutConstraintAxis)axis NS_AVAILABLE_IOS(10_0);

/* If there aren't enough constraints in the system to uniquely determine layout, we say the layout is ambiguous.  For example, if the only constraint in the system was x = y + 100, then there are lots of different possible values for x and y.  This situation is not automatically detected by UIKit, due to performance considerations and details of the algorithm used for layout.
 The symptom of ambiguity is that views sometimes jump from place to place, or possibly are just in the wrong place.
 -hasAmbiguousLayout runs a check for whether there is another center and bounds the receiver could have that could also satisfy the constraints.
 */
#if UIKIT_DEFINE_AS_PROPERTIES
@property(nonatomic, readonly) BOOL hasAmbiguousLayout NS_AVAILABLE_IOS(10_0);
#else
- (BOOL)hasAmbiguousLayout NS_AVAILABLE_IOS(10_0);
#endif
@end

@interface UIView (UIStateRestoration)
//标示是否支持保存,恢复视图状态信息
@property (nonatomic, copy) NSString *restorationIdentifier NS_AVAILABLE_IOS(6_0);
//保存视图状态相关的信息
- (void) encodeRestorableStateWithCoder:(NSCoder *)coder NS_AVAILABLE_IOS(6_0);
//恢复和保持视图状态相关信息
- (void) decodeRestorableStateWithCoder:(NSCoder *)coder NS_AVAILABLE_IOS(6_0);
@end

@interface UIView (UISnapshotting)
//屏幕快照
/*
* When requesting a snapshot, 'afterUpdates' defines whether the snapshot is representative of what's currently on screen or if you wish to include any recent changes before taking the snapshot.

 If called during layout from a committing transaction, snapshots occurring after the screen updates will include all changes made, regardless of when the snapshot is taken and the changes are made. For example:

     - (void)layoutSubviews {
         UIView *snapshot = [self snapshotViewAfterScreenUpdates:YES];
         self.alpha = 0.0;
     }

 The snapshot will appear to be empty since the change in alpha will be captured by the snapshot. If you need to animate the view during layout, animate the snapshot instead.

* Creating snapshots from existing snapshots (as a method to duplicate, crop or create a resizable variant) is supported. In cases where many snapshots are needed, creating a snapshot from a common superview and making subsequent snapshots from it can be more performant. Please keep in mind that if 'afterUpdates' is YES, the original snapshot is committed and any changes made to it, not the view originally snapshotted, will be included.
 */
/*
http://www.csdn123.com/html/topnews201408/58/1858.htm
http://rralun.blog.163.com/blog/static/1039042962014929111334870/
http://www.cocoachina.com/ios/20141222/10713.html
// 这个方法能够高效的将当前显示的view截取成一个新的view.你可以用这个截取的view用来显示.例如,也许你只想用一张截图来做动画,
毕竟用原始的view做动画代价太高.因为是截取了已经存在的内容,这个方法只能反应出这个被截取的view当前的状态信息,而不能反应这个被截取的view以后要显示的信息.然而,不管怎么样,调用这个方法都会比将view做成截图来加载效率更高.*/
- (UIView *)snapshotViewAfterScreenUpdates:(BOOL)afterUpdates NS_AVAILABLE_IOS(7_0);
//缩放一个view默认是从中心点进行缩放的
- (UIView *)resizableSnapshotViewFromRect:(CGRect)rect afterScreenUpdates:(BOOL)afterUpdates withCapInsets:(UIEdgeInsets)capInsets NS_AVAILABLE_IOS(7_0);  // Resizable snapshots will default to stretching the center
// Use this method to render a snapshot of the view hierarchy into the current context. Returns NO if the snapshot is missing image data, YES if the snapshot is complete. Calling this method from layoutSubviews while the current transaction is committing will capture what is currently displayed regardless if afterUpdates is YES.
// 它允许你截取一个UIView或者其子类中的内容
- (BOOL)drawViewHierarchyInRect:(CGRect)rect afterScreenUpdates:(BOOL)afterUpdates NS_AVAILABLE_IOS(7_0);
//屏幕快照
@end
```

