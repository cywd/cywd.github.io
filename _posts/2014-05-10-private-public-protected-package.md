---
layout: post
title: "@private @public @protected @package"
excerpt: "@private @public @protected @package"
categories: [OC]
tags: [OC]
date: 2014-05-10 
modified: 
comments: true
---

* TOC
{:toc}
---

## @private

```objective-c
The instance variable is accessible only within the class that declares it.
实例变量只能被声明它的类访问
```

## @protected

```objective-c
The instance variable is accessible within the class that declares it and within classes that inherit it. All instance variables without an explicit scope directive have @protected scope.
实例变量能被声明它的类和子类访问，所有没有显式制定范围的实例变量都是
```

## @public

```objective-c
The instance variable is accessible everywhere.
实例变量可以被在任何地方访问。
```

## @package

```objective-c
Using the modern runtime, an @package instance variable has @public scope inside the executable image that implements the class, but acts like @private outside.使用modern运行时，一个@package实例变量在实现这个类的可执行文件镜像中实际上是@public的，但是在外面就是@private【runtime需要再看一下苹果文档Runtime Programming Guide】

The @package scope for Objective-C instance variables is analogous to private_extern for C variables and functions. Any code outside the class implementation’s image that tries to use the instance variable gets a link error.

Objective-C中的@package与C语言中变量和函数的private_extern类似。任何在实现类的镜像之外的代码想使用这个实例变量都会引发link error

This scope is most useful for instance variables in framework classes, where @private may be too restrictive but @protected or @public too permissive.

这个类型最常用于框架类的实例变量，使用 @private 太限制，使用 @protected 或者 @public 又太开放
```








