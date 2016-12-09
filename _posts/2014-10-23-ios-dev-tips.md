---
layout: post
title: "iOS开发的一些Tips"
excerpt: "iOS开发的一些Tips，记录下便于日后查看"
categories: [OC, Tips]
tags: [OC, Tips]
date: 2014-10-23 
modified: 
comments: true
---

* TOC
{:toc}
---

## 1.如何快速的查看一段代码的执行时间。

```objective-c
#define TICK   NSDate *startTime = [NSDate date]
#define TOCK   NSLog(@"Time: %f", -[startTime timeIntervalSinceNow])
// 使用时
TICK
// do your work here
TOCK
```

## 2.当view旋转缩放的时候出现锯齿

使用`layer`的`allowsEdgeAntialiasing`属性消除锯齿

```objective-c
self.layer.allowsEdgeAntialiasing = YES;
// 设置对应view的layer这个属性
```

## 3.UIContentMode的显示方式，备忘

引用网上的图，不知道原作者是谁。

![引用网上的图](/img/article/tips/3.jpg)

## 4.统计项目中代码行数  

终端cd到相应目录，执行

```shell
find . "(" -name ".m" -or -name ".mm" -or -name ".cpp" -or -name ".h" -or -name ".rss" -or -name ".xib"  ")" -print | xargs wc -l
```

## 5.宏的##和#作用

在宏里面, ##的作用:连接2个标识符

```objective-c
#define method(name) - (void)load##name {}method(abc)  
//- (void)loadabc {}   method(abc)  
//- (void)loadddd {}   method(ddd)  
//- (void)loadttt {}   method(ttt) 
```

在宏里面, #的作用:给右边的标识符加上双引号""

```c
#define test(name) @#nametest(abc) // @"abc"
```

## 6.忽略未使用变量的警告

```objective-c
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wunused-variable"
	UIView *testView = [[UIView alloc] init];
#pragma clang diagnostic pop
```

## 7.忽略方法未声明警告

```objective-c
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wundeclared-selector"
    
    UIPanGestureRecognizer *panGesture = [[UIPanGestureRecognizer alloc] initWithTarget:self action:@selector(handleNavigationTransition:)];
    // 错误实例，这样做会在点击时崩溃
#pragma clang diagnostic pop
```

## 8.在APPDelegate中禁用第三方键盘

```objective-c
#pragma mark - 禁用第三方键盘
- (BOOL)application:(UIApplication *)application shouldAllowExtensionPointIdentifier:(UIApplicationExtensionPointIdentifier)extensionPointIdentifier {
    return NO;
}
```

## 9.判断是模拟器还是真机

```objective-c
#if TARGET_IPHONE_SIMULATOR //模拟器

#elif TARGET_OS_IPHONE //真机

#endif
```

## 10.给NSObject 增加属性

举例，比如我们希望button点击的时候，可以传递更多的属性。除开继承自UIButton添加属性外，还有这种方法。

```
UIButton *btn = [UIButton buttonWithType:UIButtonTypeSystem];

objc_setAssociatedObject(btn, "firstObject", @1, OBJC_ASSOCIATION_RETAIN_NONATOMIC);

[btn setFrame:CGRectMake(10, 250, 100, 50)];
[btn setTitle:@"Test To Logic" forState:UIControlStateNormal];
[self.view addSubview:btn];
btn.showsTouchWhenHighlighted = YES;
[btn addTarget:self action:@selector(click:) forControlEvents:UIControlEventTouchUpInside];

- (void)click:(UIButton *)sender {
	// 
    id first = objc_getAssociatedObject(sender, "firstObject");
}
```
## 11.CGfloat和float的区别?

command+左键点击CGFloat.

```
typedef CGFLOAT_TYPE CGFloat;
```

```
#if defined(__LP64__) && __LP64__
# define CGFLOAT_TYPE double
# define CGFLOAT_IS_DOUBLE 1
# define CGFLOAT_MIN DBL_MIN
# define CGFLOAT_MAX DBL_MAX
#else
# define CGFLOAT_TYPE float
# define CGFLOAT_IS_DOUBLE 0
# define CGFLOAT_MIN FLT_MIN
# define CGFLOAT_MAX FLT_MAX
#endif
```

64位系统下,CGFLOAT是double类型,32位系统下是float类型.
如果需要精确计算，不要使用CGFloat或float，1.1	有时计算不准确，后面几位会出现精度丢失，要用double.

## 12.FOUNDATION_EXPORT和#define

比较的时候FOUNDATION_EXPORT 可以 == ，#define 只是单纯的替换.

## 13.滑动的时候隐藏navigationbar(类似safari)

```
navigationController.hidesBarsOnSwipe = Yes;
```

## 14.去掉导航条返回键带的title

```
[[UIBarButtonItem appearance] setBackButtonTitlePositionAdjustment:UIOffsetMake(0, -60)
                                                     forBarMetrics:UIBarMetricsDefault];
```
## 15.isKindOfClass、isMemberOfClass和isSubclassOfClass

苛刻程度   `isKindOfClass < isSubclassOfClass < isMemberOfClass;`

```objective-c
// isKindOfClass:       
// isSubclassOfClass:   是子类
// isMemberOfClass:     类型需完全一样
```
## 16.代码中字符串换行

```objective-c
NSString *string = @"ABCDEFGHIJKL" \
         "MNOPQRSTUVsWXYZ";
```
## 17.判断一个字符串是否包含另一个字符串

```objective-c
[str1 rangeOfString:str2].length != 0 ? @"包含" : @"不包含" ;
```

## 18.引用

C++支持引用，Objective-C是从C衍变来的，不支持引用

## 19.重写description

输出重要变量的值，因为调试窗口variableView有时候变量值显示不出来。

## 20.UIScrollView等滚动条闪一下

```objective-c
scrollVIew.flashScrollIndicators = YES;
```

## 21.点击Cell中的按钮时，如何取所在的Cell

```objective-c
-(void)OnTouchBtnInCell:(UIButton *)btn 
{ 
  CGPoint point = btn.center; 
  point = [table convertPoint:point fromView:btn.superview]; 
  NSIndexPath* indexpath = [table indexPathForRowAtPoint:point]; 
  UITableViewCell *cell = [table cellForRowAtIndexPath:indexpath]; 
  /*... */
  // 也可以通过一路取btn的父窗口取到cell，但如果cell下通过好几层subview才到btn,就要取好几次 superview
  // 所以我用上面的方法，比较通用。这种  方法也适用于其它控件。 
} 
```

## 22.禁止程序运行时自动锁屏

```objective-c
[[UIApplication sharedApplication] setIdleTimerDisabled:YES]; 
```

## 23.allSubviews, allApplicationViews, pathToView

```
NSArray *allSubviews(UIView *aView)
{
	NSArray *results = [aView subviews];
	for (UIView *eachView in [aView subviews])
	{
		NSArray *riz = allSubviews(eachView);
		if (riz) results = [results arrayByAddingObjectsFromArray:riz];
	}
	return results;
}

// Return all views throughout the application
NSArray *allApplicationViews()
{
    NSArray *results = [[UIApplication sharedApplication] windows];
    for (UIWindow *window in [[UIApplication sharedApplication] windows])
	{
		NSArray *riz = allSubviews(window);
        if (riz) results = [results arrayByAddingObjectsFromArray: riz];
	}
    return results;
}

// Return an array of parent views from the window down to the view
NSArray *pathToView(UIView *aView)
{
    NSMutableArray *array = [NSMutableArray arrayWithObject:aView];
    UIView *view = aView;
    UIWindow *window = aView.window;
    while (view != window)
    {
        view = [view superview];
        [array insertObject:view atIndex:0];
    }
    return array;
}

```
## 24.非常规退出

苹果不建议程序主动退出，但还是有一个函数可以实现这个效果：    

```
exit(0)
```

不过这个函数不触发`applicationWillResignActive`等`AppDelegate method`.

## 25. Objective-C中的_cmd

Objective-C的编译器在编译后会在每个方法中加两个隐藏的参数:

一个是_cmd，当前方法的一个SEL指针。

另一个就是用的比较多的self，指向当前对象的一个指针。

_cmd可以赋值给SEL类型的变量，可以做为参数传递。

example:

```objective-c
// 例如一个显示消息的方法： 
- (void)ShowNotifyWithString:(NSString *)notifyString fromMethod:(SEL)originalMethod; 
// originalMethod就是调用这个方法的selector。 
// 调用： 
NSString *stmp = @"test"; 
[self ShowNotifyWithString:stmp fromMethod:_cmd]; 
// 打印当前方法名称： 
NSLog(@"%@", NSStringFromSelector(_cmd));
```

