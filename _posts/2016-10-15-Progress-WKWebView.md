---
layout: post
title: "WKWebView上方带进度条"
excerpt: "用WKWebView实现带进度条的WebView"
categories: [OC]
tags: [OC]
date: 2016-10-15
comments: true
---

* TOC
{:toc}
---

## 实现带进度条的WebView

这里使用了WKWebView，比UIWebView要好很多。

WKWebView自带属性

estimatedProgress 可以获取进度

title 可以获取title

WKWebView 的estimatedProgress和title 都是KVO模式，需要添加监控：

```objective-c
#define kProgressKey @"estimatedProgress"
#define kTitleKey    @"title"
#define kOldKey      @"old"
#define kNewKey      @"new"

[_webView addObserver:self forKeyPath:kProgressKey options:NSKeyValueObservingOptionNew context:nil];
[_webView addObserver:self forKeyPath:kTitleKey options:NSKeyValueObservingOptionNew context:NULL];
```



```objective-c
- (void)observeValueForKeyPath:(NSString *)keyPath ofObject:(id)object change:(NSDictionary<NSString *,id> *)change context:(void *)context{
    if ([keyPath isEqualToString:kProgressKey]) {
        self.progresslayer.opacity = 1;
        //不要让进度条倒着走...有时候goback会出现这种情况
        if ([change[kNewKey] floatValue] < [change[kOldKey] floatValue]) {
            return;
        }
        self.progresslayer.frame = CGRectMake(0, 0, self.view.bounds.size.width * [change[kNewKey] floatValue], 3);
        if ([change[kNewKey] floatValue] == 1) {
            dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(.4 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
                self.progresslayer.opacity = 0;
            });
            dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(.5 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
                self.progresslayer.frame = CGRectMake(0, 0, 0, 3);
            });
        }
    } else if ([keyPath isEqualToString:kTitleKey]) {
        if (object == self.webView) {
            self.title = self.webView.title;
        } else {
            [super observeValueForKeyPath:keyPath ofObject:object change:change context:context];
        }
    } else {
        [super observeValueForKeyPath:keyPath ofObject:object change:change context:context];
    }
}
```

另外别忘记移除

```objective-c
[self.webView removeObserver:self forKeyPath:kProgressKey];
[self.webView removeObserver:self forKeyPath:kTitleKey];
```

[https://github.com/CoderCYLee/CYProgressWebVIew]:https://github.com/CoderCYLee/CYProgressWebVIew

