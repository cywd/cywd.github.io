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

## 8.开启ARC和MRC

```
-fobjc-arc     MRC
-fno-objc-arc  ARC
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

比较的时候FOUNDATION_EXPORT 可以 == 这种方式进行比较，#define 只是单纯的替换.

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

## 26.在APPDelegate中禁用第三方键盘

```objective-c
#pragma mark - 禁用第三方键盘
- (BOOL)application:(UIApplication *)application shouldAllowExtensionPointIdentifier:(UIApplicationExtensionPointIdentifier)extensionPointIdentifier {
    return NO;
}
```

## 27.自动滚动调整

```objective-c
self.automaticallyAdjustsScrollViewInsets = NO;  // 自动滚动调整，默认为YES
```

## 28.修改Cell分割线距离

```objective-c
- (void)tableView:(UITableView *)tableView willDisplayCell:(UITableViewCell *)cell forRowAtIndexPath:(NSIndexPath *)indexPath {
	if ([cell respondsToSelector:@selector(setSeparatorInset:)]) {
        [cell setSeparatorInset:UIEdgeInsetsMake(0, 15, 0, 15)];
    }
    if ([cell respondsToSelector:@selector(setLayoutMargins:)]) {
        [cell setSeparatorInset:UIEdgeInsetsMake(0, 15, 0, 15)];
    }
    if ([cell respondsToSelector:@selector(setPreservesSuperviewLayoutMargins:)]) {
        [cell setPreservesSuperviewLayoutMargins:NO];
    }
}
```

## 29.将汉字转换为拼音

```objective-c
- (NSString *)chineseToPinyin:(NSString *)chinese withSpace:(BOOL)withSpace {
    if(chinese) {
        CFStringRef hanzi = (__bridge CFStringRef)chinese;
        CFMutableStringRef string =CFStringCreateMutableCopy(NULL,0, hanzi);
        CFStringTransform(string,NULL, kCFStringTransformMandarinLatin,NO);
        CFStringTransform(string,NULL, kCFStringTransformStripDiacritics,NO);
        NSString*pinyin = (NSString*)CFBridgingRelease(string);
        
        if(!withSpace) {
            pinyin = [pinyin stringByReplacingOccurrencesOfString:@" "withString:@""];
        }
        return pinyin;
    }
    return nil;
}
```

## 30.dispatch_once和@synchronized的单例模式

### @synchronized

```objective-c
+ (id)sharedInstance {
    static Instance *obj = nil;
    @synchronized([Instance class]) {
        if(!obj) 
            obj = [[Instance alloc] init];
    }
    return obj;
}
```

### dispatch_once

```objective-c
+ (id)sharedInstance {
    static dispatch_once_t pred;
    static Instance *obj = nil;
    dispatch_once(&pred, ^{
        obj = [[Instance alloc] init];
    });
    return obj;
}
```

### 区别

使用`@synchronized`，这样性能不是很好，因为每次调用+ (id)sharedInstance函数都会付出取锁的代价。
GCD的单例首先满足了线程安全问题，其次很好满足静态分析器要求。GCD可以确保以更快的方式完成这些检测，它可以保证block中的代码在任何线程通过dispatch_once调用之前被执行，但它不会强制每次调用这个函数都让代码进行同步控制。实际上，如果你去看这个函数所在的头文件，你会发现目前它的实现其实是一个宏，进行了内联的初始化测试，这意味着通常情况下，你不用付出函数调用的负载代价，并且会有更少的同步控制负载。

因此，单例模式的时候尽量使用GCD。

## 31.取绝对值的用法

```objective-c
int abs(int i);         // 处理int类型的取绝对值  
double fabs(double i);  // 处理double类型的取绝对值  
float fabsf(float i);   // 处理float类型的取绝对值  
```
## 32.当子视图需要超出父视图响应事件

```objective-c
// 可以重写 hitTest 
- (UIView *)hitTest:(CGPoint)point withEvent:(UIEvent *)event {
    UIView *v = [super hitTest:point withEvent:event];
    if (v == nil) {
        CGPoint tp = [self.cameraButton convertPoint:point fromView:self];
        if (CGRectContainsPoint(self.cameraButton.bounds, tp)) {
            v = self.cameraButton;
        }
    }
    return v;
}
```

## 33.判断当前ViewController是push还是present方式显示的

### 1.通过判断self有没有present方式显示的父视图presentingViewController

```objective-c
- (IBAction)dismiss:(id)sender {
    if (self.presentingViewController) {
        [self dismissViewControllerAnimated:YES completion:nil];
    } else {
        [self.navigationController popViewControllerAnimated:YES];
    }
}
```

### 2.通过判断self.navigationController.viewControllers的最后一个是否是当前控制器，或者self.navigationController.topViewController == self

```objective-c
- (IBAction)dismiss:(id)sender {
    if (self.navigationController.topViewController == self) {
        [self.navigationController popViewControllerAnimated:YES];
    } else {
        [self dismissViewControllerAnimated:YES completion:nil];
    }
}
```
## 34.提取.ipa中的Assets.car

利用工具[iOS-Images-Extractor](https://github.com/devcxm/iOS-Images-Extractor)

[中文使用方法看这里](https://github.com/devcxm/iOS-Images-Extractor/blob/master/README_zh-Hans.md)

到终端分别执行下面的四条命令：

```
git clone https://github.com/devcxm/iOS-Images-Extractor
cd iOS-Images-Extractor
git submodule update --init --recursive
open iOSImagesExtractor.xcworkspace
```

### 提取素材

将Assets.car拖动到刚才运行的应用中。

先点击“start”开始解压，然后点击“Output Dir”来查看导出的目录，就可以看到所有的素材了。

## 35获取LaunchImage的图片

```
+ (UIImage *)getTheLaunchImage
{
    CGSize viewSize = [UIScreen mainScreen].bounds.size;

    NSString *viewOrientation = nil;
    if (([[UIApplication sharedApplication] statusBarOrientation] == UIInterfaceOrientationPortraitUpsideDown) || ([[UIApplication sharedApplication] statusBarOrientation] == UIInterfaceOrientationPortrait)) {
        viewOrientation = @"Portrait";
    } else {
        viewOrientation = @"Landscape";
    }


    NSString *launchImage = nil;

    NSArray* imagesDict = [[[NSBundle mainBundle] infoDictionary] valueForKey:@"UILaunchImages"];
    for (NSDictionary* dict in imagesDict)
    {
        CGSize imageSize = CGSizeFromString(dict[@"UILaunchImageSize"]);

        if (CGSizeEqualToSize(imageSize, viewSize) && [viewOrientation isEqualToString:dict[@"UILaunchImageOrientation"]])
        {
            launchImage = dict[@"UILaunchImageName"];
        }
    }

    return [UIImage imageNamed:launchImage];

}
```

参考：[如何从Images.xcassets中获取LaunchImage的图片](https://www.ianisme.com/ios/1825.html)

## 36.禁止手机睡眠

```objective-c
[UIApplication sharedApplication].idleTimerDisabled = YES;
```

## 37.隐藏某行cell

```
- (CGFloat)tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath
{
// 如果是你需要隐藏的那一行，返回高度为0
    if(indexPath.row == YouWantToHideRow)
        return 0; 
    return 44;
}
 
// 然后再你需要隐藏cell的时候调用
[self.tableView beginUpdates];
[self.tableView endUpdates];
```

## 38.去除数组中重复的对象

```
NSArray *newArr = [oldArr valueForKeyPath:@“@distinctUnionOfObjects.self"];
```

## 39.UITextView中打开或禁用复制，剪切，选择，全选等功能

```
// 继承UITextView重写这个方法
- (BOOL)canPerformAction:(SEL)action withSender:(id)sender
{
// 返回NO为禁用，YES为开启
    // 粘贴
    if (action == @selector(paste:)) return NO;
    // 剪切
    if (action == @selector(cut:)) return NO;
    // 复制
    if (action == @selector(copy:)) return NO;
    // 选择
    if (action == @selector(select:)) return NO;
    // 选中全部
    if (action == @selector(selectAll:)) return NO;
    // 删除
    if (action == @selector(delete:)) return NO;
    // 分享
    if (action == @selector(share)) return NO;
    return [super canPerformAction:action withSender:sender];
}
```

## 40.为一个view添加虚线边框

```objective-c
CAShapeLayer *border = [CAShapeLayer layer];
border.strokeColor = [UIColor colorWithRed:67/255.0f green:37/255.0f blue:83/255.0f alpha:1].CGColor;
border.fillColor = nil;
border.lineDashPattern = @[@4, @2];
border.path = [UIBezierPath bezierPathWithRect:view.bounds].CGPath;
border.frame = view.bounds;
[view.layer addSublayer:border];
```

## 41.修改cell.imageView的大小

```objective-c
UIImage *icon = [UIImage imageNamed:@""];
CGSize itemSize = CGSizeMake(30, 30);
UIGraphicsBeginImageContextWithOptions(itemSize, NO ,0.0);
CGRect imageRect = CGRectMake(0.0, 0.0, itemSize.width, itemSize.height);
[icon drawInRect:imageRect];
cell.imageView.image = UIGraphicsGetImageFromCurrentImageContext();
UIGraphicsEndImageContext();
```

## 42.在指定的宽度下，让UILabel自动设置最佳font

```
label.adjustsFontSizeToFitWidth = YES;
```

## 43.统一收起键盘

```
[[[UIApplication sharedApplication] keyWindow] endEditing:YES];
```

## 44.判断图片类型

```
//通过图片Data数据第一个字节 来获取图片扩展名
- (NSString *)contentTypeForImageData:(NSData *)data
{
    uint8_t c;
    [data getBytes:&c length:1];
    switch (c)
    {
        case 0xFF:
            return @"jpeg";
 
        case 0x89:
            return @"png";
 
        case 0x47:
            return @"gif";
 
        case 0x49:
        case 0x4D:
            return @"tiff";
 
        case 0x52:
        if ([data length] < 12) {
            return nil;
        }
        NSString *testString = [[NSString alloc] initWithData:[data subdataWithRange:NSMakeRange(0, 12)] encoding:NSASCIIStringEncoding];
        if ([testString hasPrefix:@"RIFF"]
            && [testString hasSuffix:@"WEBP"])
        {
            return @"webp";
        }
        return nil;
    }
    return nil;
}
```

## 45.获取设备mac地址

```
+ (NSString *)macAddress {
    int                 mib[6];
    size_t              len;
    char                *buf;
    unsigned char       *ptr;
    struct if_msghdr    *ifm;
    struct sockaddr_dl  *sdl;
 
    mib[0] = CTL_NET;
    mib[1] = AF_ROUTE;
    mib[2] = 0;
    mib[3] = AF_LINK;
    mib[4] = NET_RT_IFLIST;
 
    if((mib[5] = if_nametoindex("en0")) == 0) {
        printf("Error: if_nametoindex error\n");
        return NULL;
    }
 
    if(sysctl(mib, 6, NULL, &len, NULL, 0) < 0) {
        printf("Error: sysctl, take 1\n");
        return NULL;
    }
 
    if((buf = malloc(len)) == NULL) {
        printf("Could not allocate memory. Rrror!\n");
        return NULL;
    }
 
    if(sysctl(mib, 6, buf, &len, NULL, 0) < 0) {
        printf("Error: sysctl, take 2");
        return NULL;
    }
 
    ifm = (struct if_msghdr *)buf;
    sdl = (struct sockaddr_dl *)(ifm + 1);
    ptr = (unsigned char *)LLADDR(sdl);
    NSString *outstring = [NSString stringWithFormat:@"X:X:X:X:X:X",
                           *ptr, *(ptr+1), *(ptr+2), *(ptr+3), *(ptr+4), *(ptr+5)];
    free(buf);
 
    return outstring;
}
```

## 46.不让控制器的view随着控制器的xib拉伸或压缩

```
self.view.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;
```

## 47.导入自定义字体库

```
1.找到你想用的字体的 ttf 格式，拖入工程
2.在工程的plist中增加一行数组，“Fonts provided by application”
3.为这个key添加一个item，value为你刚才导入的ttf文件名
4.直接使用即可：label.font = [UIFont fontWithName:@"你刚才导入的ttf文件名" size:20.0]；
```

## 48.获取到当前正在显示的controller

```
- (UIViewController *)getVisibleViewControllerFrom:(UIViewController*)vc {
    if ([vc isKindOfClass:[UINavigationController class]]) {
        return [self getVisibleViewControllerFrom:[((UINavigationController*) vc) visibleViewController]];
    }else if ([vc isKindOfClass:[UITabBarController class]]){
        return [self getVisibleViewControllerFrom:[((UITabBarController*) vc) selectedViewController]];
    } else {
        if (vc.presentedViewController) {
            return [self getVisibleViewControllerFrom:vc.presentedViewController];
        } else {
            return vc;
        }
    }
}
```

## 49.为imageView添加倒影

```
CGRect frame = self.frame;
    frame.origin.y += (frame.size.height + 1);
 
    UIImageView *reflectionImageView = [[UIImageView alloc] initWithFrame:frame];
    self.clipsToBounds = TRUE;
    reflectionImageView.contentMode = self.contentMode;
    [reflectionImageView setImage:self.image];
    reflectionImageView.transform = CGAffineTransformMakeScale(1.0, -1.0);
 
    CALayer *reflectionLayer = [reflectionImageView layer];
 
    CAGradientLayer *gradientLayer = [CAGradientLayer layer];
    gradientLayer.bounds = reflectionLayer.bounds;
    gradientLayer.position = CGPointMake(reflectionLayer.bounds.size.width / 2, reflectionLayer.bounds.size.height * 0.5);
    gradientLayer.colors = [NSArray arrayWithObjects:
                            (id)[[UIColor clearColor] CGColor],
                            (id)[[UIColor colorWithRed:1.0 green:1.0 blue:1.0 alpha:0.3] CGColor], nil];
 
    gradientLayer.startPoint = CGPointMake(0.5,0.5);
    gradientLayer.endPoint = CGPointMake(0.5,1.0);
    reflectionLayer.mask = gradientLayer;
 
    [self.superview addSubview:reflectionImageView];
```

## 50.画水印

```
// 画水印
- (void) setImage:(UIImage *)image withWaterMark:(UIImage *)mark inRect:(CGRect)rect
{
    if ([[[UIDevice currentDevice] systemVersion] floatValue] >= 4.0)
    {
        UIGraphicsBeginImageContextWithOptions(self.frame.size, NO, 0.0);
    }
    //原图
    [image drawInRect:self.bounds];
    //水印图
    [mark drawInRect:rect];
    UIImage *newPic = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();
    self.image = newPic;
}
```

## 51.获取一个视频的第一帧图片

```
    NSURL *url = [NSURL URLWithString:filepath];
    AVURLAsset *asset1 = [[AVURLAsset alloc] initWithURL:url options:nil];
    AVAssetImageGenerator *generate1 = [[AVAssetImageGenerator alloc] initWithAsset:asset1];
    generate1.appliesPreferredTrackTransform = YES;
    NSError *err = NULL;
    CMTime time = CMTimeMake(1, 2);
    CGImageRef oneRef = [generate1 copyCGImageAtTime:time actualTime:NULL error:&err];
    UIImage *one = [[UIImage alloc] initWithCGImage:oneRef];
 
    return one;
```

## 52.获取视频的时长

```
+ (NSInteger)getVideoTimeByUrlString:(NSString *)urlString {
    NSURL *videoUrl = [NSURL URLWithString:urlString];
    AVURLAsset *avUrl = [AVURLAsset assetWithURL:videoUrl];
    CMTime time = [avUrl duration];
    int seconds = ceil(time.value/time.timescale);
    return seconds;
}
```

## 53.当tableView占不满一屏时，去除下边多余的单元格

```
self.tableView.tableHeaderView = [UIView new];
self.tableView.tableFooterView = [UIView new];
```

## 54.isKindOfClass和isMemberOfClass的区别

```
isKindOfClass可以判断某个对象是否属于某个类，或者这个类的子类。
isMemberOfClass更加精准，它只能判断这个对象类型是否为这个类(不能判断子类)
```

## 55.某个字体的高度

```
font.lineHeight
```

## 56.删除NSUserDefaults所有记录

```
//方法一
  NSString *appDomain = [[NSBundle mainBundle] bundleIdentifier];
 [[NSUserDefaults standardUserDefaults] removePersistentDomainForName:appDomain];   
 //方法二  
- (void)resetDefaults {   
  NSUserDefaults * defs = [NSUserDefaults standardUserDefaults];
     NSDictionary * dict = [defs dictionaryRepresentation];
     for (id key in dict) {
          [defs removeObjectForKey:key];
     }
      [defs synchronize];
 }
// 方法三
[[NSUserDefaults standardUserDefaults] setPersistentDomain:[NSDictionary dictionary] forName:[[NSBundle mainBundle] bundleIdentifier]];
```

## 57.UILabel设置文字描边

```
子类化UILabel，重写drawTextInRect方法
- (void)drawTextInRect:(CGRect)rect
{
    CGContextRef c = UIGraphicsGetCurrentContext();
    // 设置描边宽度
    CGContextSetLineWidth(c, 1);
    CGContextSetLineJoin(c, kCGLineJoinRound);
    CGContextSetTextDrawingMode(c, kCGTextStroke);
    // 描边颜色
    self.textColor = [UIColor redColor];
    [super drawTextInRect:rect];
    // 文本颜色
    self.textColor = [UIColor yellowColor];
    CGContextSetTextDrawingMode(c, kCGTextFill);
    [super drawTextInRect:rect];
}
```

## 58.layoutSubviews方法什么时候调用？

```
1、init方法不会调用
2、addSubview方法等时候会调用
3、bounds改变的时候调用
4、scrollView滚动的时候会调用scrollView的layoutSubviews方法(所以不建议在scrollView的layoutSubviews方法中做复杂逻辑)
5、旋转设备的时候调用
6、子视图被移除的时候调用
```

[http://blog.logichigh.com/2011/03/16/when-does-layoutsubviews-get-called/](http://blog.logichigh.com/2011/03/16/when-does-layoutsubviews-get-called/)

## 59.摇一摇

```
1、打开摇一摇功能
    [UIApplication sharedApplication].applicationSupportsShakeToEdit = YES;
2、让需要摇动的控制器成为第一响应者
[self becomeFirstResponder];
3、实现以下方法
 
// 开始摇动
- (void)motionBegan:(UIEventSubtype)motion withEvent:(UIEvent *)event
// 取消摇动
- (void)motionCancelled:(UIEventSubtype)motion withEvent:(UIEvent *)event
// 摇动结束
- (void)motionEnded:(UIEventSubtype)motion withEvent:(UIEvent *)event
```

## 60.tableViewCell分割线顶到头

```
- (void)tableView:(UITableView *)tableView willDisplayCell:(UITableViewCell *)cell forRowAtIndexPath:(NSIndexPath *)indexPath {
    [cell setSeparatorInset:UIEdgeInsetsZero];
    [cell setLayoutMargins:UIEdgeInsetsZero];
    cell.preservesSuperviewLayoutMargins = NO;
}
 
- (void)viewDidLayoutSubviews {
    [self.tableView setSeparatorInset:UIEdgeInsetsZero];
    [self.tableView setLayoutMargins:UIEdgeInsetsZero];
}
```

## 61.判断一个字符串是否包含另一个字符串的另外一种方法

```objective-c
[str1 rangeOfString:str2].length != 0 ? @"包含" : @"不包含";
```

## 62.没有用到类的成员变量的，都写成类方法

## 63.category可以用来调试

```
// 除了隐藏私有方法外，我主要用它截住函数。 
// 例1：测试时我想知道TableViewCell有没有释放，就可以这样写 
@implementation UITableViewCell(dealloc) 
-(void)dealloc 
{ 
   NSLog(@"%@",NSStringFromSelector(_cmd)); 
    NSArray *array = allSubviews(self); 		// allSubviews是cookBook里的函数，可以取一个view的所有subView ,在这个文档后面也有
    NSLog(@"%@",array); 

    [super dealloc]; 
} 
@end 
// 其它的类也可以这样写，你随便输出什么 
// 例2：我调试程序，觉得table的大小变了，想找到在哪改变的，这样做：
 @implementation UITableView(setframe) 
-(void)setFrame:(CGRect)frame 
{ 
   NSLog(%"%@",self); 
    [super setFrame: frame]; 
} 
@end 
```

## 64.设置圆角和阴影要分层

```objective-c
CALayer *shadowLayer = [CALayer layer];
shadowLayer.shadowColor = [UIColor blackColor].CGColor;
shadowLayer.shadowOffset = CGSizeMake(0, 0);
shadowLayer.shadowRadius = 5;
shadowLayer.shadowOpacity = 1;
shadowLayer.frame = self.bounds;
shadowLayer.backgroundColor = [UIColor clearColor ].CGColor;
shadowLayer.cornerRadius = 5;
shadowLayer.borderColor = [UIColor whiteColor].CGColor;
shadowLayer.borderWidth = 2.0;
[self.layer addSublayer:shadowLayer];

CALayer *borderLayer = [CALayer layer];
borderLayer.cornerRadius = 5;
borderLayer.masksToBounds = YES;
borderLayer.frame = shadowLayer.bounds;
[shadowLayer addSublayer:borderLayer];

```

## 65.`_cmd`

```
表示该方法的selector，可以赋值给SEL类型的变量，可以做为参数传递。 
例如一个显示消息的方法： 
-(void)ShowNotifyWithString:(NSString *)notifyString fromMethod:(SEL) originalMethod; 
originalMethod就是调用这个方法的selector。 
调用： 
NSString *stmp = @"test"; 
[self ShowNotifyWithString:stmp fromMethod:_cmd]; 
如何记录当前方法名称： 
NSLog(NSStringFromSelector(_cmd));
```

