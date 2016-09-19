---
layout: post
title: UIBlurEffect毛玻璃效果
excerpt: "UIBlurEffect最早出现于iOS 8，到了iOS 10，又增加了两个枚举值，看下效果"
categories: [OC]
tags: [OC]
date: 2016-09-19
comments: true
---

* TOC
{:toc}
代码如下：

```objective-c
    UIImageView *imgView = [[UIImageView alloc] initWithFrame:self.view.bounds];
    imgView.image = [UIImage imageNamed:@"1.jpg"];
    [self.view addSubview:imgView];
    
    // 毛玻璃
    UIBlurEffect *blur1 = [UIBlurEffect effectWithStyle:UIBlurEffectStyleExtraLight];
    UIBlurEffect *blur2 = [UIBlurEffect effectWithStyle:UIBlurEffectStyleLight];
    UIBlurEffect *blur3 = [UIBlurEffect effectWithStyle:UIBlurEffectStyleDark];
    UIBlurEffect *blur4 = [UIBlurEffect effectWithStyle:UIBlurEffectStyleRegular];
    UIBlurEffect *blur5 = [UIBlurEffect effectWithStyle:UIBlurEffectStyleProminent];
    
    NSArray *arr = @[blur1, blur2, blur3, blur4, blur5];
   
    CGFloat x = 50;
    __block CGFloat y = 100;
    CGFloat w = self.view.bounds.size.width-100;
    CGFloat h = 50;
    
    [arr enumerateObjectsUsingBlock:^(id  _Nonnull obj, NSUInteger idx, BOOL * _Nonnull stop) {
        
        UIVisualEffectView *effe = [[UIVisualEffectView alloc] initWithFrame:CGRectMake(x, y, w, h)];
        effe.effect = obj;
        [self.view addSubview:effe];
        
        y += h + 10;
        
    }];
```

效果图如下：

![各种的效果图](/img/article/UIBlurEffect/see.png)