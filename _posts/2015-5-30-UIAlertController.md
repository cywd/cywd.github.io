---
layout: post
title: "在iOS 8中使用UIAlertController"
excerpt: "在iOS 8中使用UIAlertController"
categories: [OC, Swift]
tags: [UIAlertController, OC, Swift]
date: 2015-5-30 
modified: 
comments: true
---

* TOC
{:toc}
## **UIAlertView**

OC


```objective-c
UIAlertView *alertview = [[UIAlertView alloc] initWithTitle:@"标题" message:@"这个是UIAlertView的默认样式" delegate:self cancelButtonTitle:@"取消" otherButtonTitles:@"好的", nil];
[alertview show];
```

swift

```swift
var alertView = UIAlertView(title: "标题", message: "这个是UIAlertView的默认样式", delegate: self, cancelButtonTitle: "取消")
alertView.show()
```

## **UIAlertController**

### alertView

OC

```objective-c
UIAlertController *alertController = [UIAlertController alertControllerWithTitle:@"标题" message:@"这个是UIAlertController的默认样式" preferredStyle:UIAlertControllerStyleAlert];
UIAlertAction *cancelAction = [UIAlertAction actionWithTitle:@"取消" style:UIAlertActionStyleCancel handler:nil];
UIAlertAction *okAction = [UIAlertAction actionWithTitle:@"好的" style:UIAlertActionStyleDefault handler:nil];
[alertController addAction:cancelAction];
[alertController addAction:okAction];
```

swift

```swift
var alertController = UIAlertController(title: "标题", message: "这个是UIAlertController的默认样式", preferredStyle: UIAlertControllerStyle.Alert)
var cancelAction = UIAlertAction(title: "取消", style: UIAlertActionStyle.Cancel, handler: nil)
var okAction = UIAlertAction(title: "好的", style: UIAlertActionStyle.Default, handler: nil)
alertController.addAction(cancelAction)
alertController.addAction(okAction)
```

### actionSheet

OC

```objective-c
UIAlertController *alertController = [UIAlertController alertControllerWithTitle:@"标题" message:@"信息" preferredStyle: UIAlertControllerStyleActionSheet];
UIAlertAction *cancelAction = [UIAlertAction actionWithTitle:@"取消" style:UIAlertActionStyleCancel handler:nil];
UIAlertAction *okAction = [UIAlertAction actionWithTitle:@"好的" style:UIAlertActionStyleDefault handler:^(UIAlertAction *action) {
    
}];
[alertController addAction:cancelAction];
[alertController addAction:okAction];
```

swift

```swift
var alertController = UIAlertController(title: "标题", message: "这个是UIAlertController的默认样式", preferredStyle: UIAlertControllerStyle.ActionSheet)
var cancelAction = UIAlertAction(title: "取消", style: UIAlertActionStyle.Cancel, handler: nil)
var okAction = UIAlertAction(title: "好的", style: UIAlertActionStyle.Default, handler: nil)
alertController.addAction(cancelAction)
alertController.addAction(okAction)
```

### 