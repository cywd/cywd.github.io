---
layout: post
title: Swift4 setValuesForKeys()不赋值的问题
excerpt: "Swift4以后调用setValuesForKeys()无法赋值"
categories: [iOS]
tags: [iOS， Swift]
date: 2017-11-22
comments: true
---

* TOC
{:toc}
---

## 前言

当我们想要`Dict` 转成`Model`的时候会这样写：

更新到`swift4`语法

```swift
init(dict: [String: AnyObject]) {
    super.init()
    setValuesForKeys(dict)
}
override func setValue(_ value: Any?, forUndefinedKey key: String) {
    print(key)
}
```

但是！！！

到了`Swift4`以后`setValuesForKeys()` 看上去失效了

## 原因

在`swift3`中，编译器自动推断`@objc`，换句话说，它自动添加`@objc`

在`swift4`中，编译器不再自动推断，你必须显式添加`@objc`

## 解决

有两种

1.

```
class ABCModel: NSObject {
	@objc var a: String = ""
}
```

2.

```swift
@objcMembers
class ABCModel: NSObject {
	var a: String = ""
	var b: String?
	var c: Int = 0
	var d: Bool = false
}
```

## 注意

如果有`Int`、 `Bool` 等基础类型，请手动赋默认值不然会不匹配

另外如果本来是 Bool 的 你用 String 去接收，会抛出异常，异常类似：

```
[__NSCFBoolean length]: unrecognized selector sent to instance 0x10cb5f3a0
```

