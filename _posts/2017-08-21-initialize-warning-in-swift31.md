---
layout: post
title: 在Swift3.1中，使用initialize出现警告的解决方案
excerpt: "Method 'initialize()' defines Objective-C class method 'initialize', which is not guaranteed to be invoked by Swift and will be disallowed in future versions。"
categories: [Swift]
tags: [Swift]
date: 2017-08-21
comments: true
---

* TOC
{:toc}
---

# 前言

在Swift3.1中使用`initialize`会出现如下警告：

```
Method 'initialize()' defines Objective-C class method 'initialize', which is not guaranteed to be invoked by Swift and will be disallowed in future versions。
```

以下是国外论坛上的一种方案：

1.

```
Define the following Swift code. The purpose is to provide a simple entry point for any class that you would like to imbue with behaviour akin to initialize() - this can now be done simply by conforming to SelfAware. It also provides a single function to run this behaviour for every conforming class.

/// 定义 `protocol`
public protocol SelfAware: class {
    static func awake()
}

// 创建代理执行单例
class NothingToSeeHere{

    static func harmlessFunction(){
        let typeCount = Int(objc_getClassList(nil, 0))
        let  types = UnsafeMutablePointer<AnyClass?>.allocate(capacity: typeCount)
        let autoreleaseintTypes = AutoreleasingUnsafeMutablePointer<AnyClass?>(types)
        objc_getClassList(autoreleaseintTypes, Int32(typeCount)) //获取所有的类
        for index in 0 ..< typeCount{
            (types[index] as? SelfAware.Type)?.awake() //如果该类实现了SelfAware协议，那么调用awake方法
        }
        types.deallocate(capacity: typeCount)
    }
}

```

2.

```
That's all good and well, but we still need a way to actually run the function we defined, i.e. NothingToSeeHere.harmlessFunction(), on application start up. Previously, this answer suggested using Objective-C code to do this. However, it seems that we can do what we need using only Swift. For macOS or other platforms where UIApplication is not available, a variation of the following will be needed.

/// 执行单例
extension UIApplication {
    private static let runOnce:Void = {
        //使用静态属性以保证只调用一次(该属性是个方法)
        NothingToSeeHere.harmlessFunction()
        UIButton.harmlessFunction()
    }()

    open override var next: UIResponder?{
        UIApplication.runOnce
        return super.next
    }
}
```

3.

```

We now have an entry point at application start up, and a way to hook into this from classes of your choice. All that is left to do: instead of implementing initialize(), conform to SelfAware and implement the defined method, awake().

/// 将类设置为代理并在代理中实现运行时代吗
extension UIButton:SelfAware{
    public static func awake() {
        
    }

```

# 参考

- [Swift 3.1 deprecates initialize(). How can I achieve the same thing?](https://stackoverflow.com/questions/42824541/swift-3-1-deprecates-initialize-how-can-i-achieve-the-same-thing)