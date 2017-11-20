---
layout: post
title: "nil、Nil、NULL与NSNull的区别"
excerpt: "nil、Nil、NULL与NSNull的区别,记录一下"
categories: [OC, Tips]
tags: [OC, Tips]
date: 2014-04-20 
modified: 
comments: true
---

* TOC
{:toc}
---

## 1.nil

### `objc.h`中的定义

```objective-c
#ifndef nil
# if __has_feature(cxx_nullptr)
#   define nil nullptr
# else
#   define nil __DARWIN_NULL
# endif
#endif
```

### 作用：指向一个对象的指针为空.

### 在Objective-C中用于id类型的对象

```objective-c
NSString *name = nil;
NSURL    *url  = nil;
id object      = nil;
```

## 2.Nil

### `objc.h`中的定义

```objective-c
#ifndef Nil
# if __has_feature(cxx_nullptr)
#   define Nil nullptr
# else
#   define Nil __DARWIN_NULL
# endif
#endif
```

### 作用：指向一个对象的指针为空.

### 在Objective-C中用于Class类型的对象

```objective-c
Class aClass = Nil;
Clsss bClass = [NSURL class];
```

## 3.NULL

### `stddef.h`里`#include <sys/_types/_null.h>`的定义

```objective-c
#ifndef NULL 
#define NULL  __DARWIN_NULL
#endif  /* NULL */
```

其中`__DARWIN_NULL`的定义在`usr/include/sys/__types.h `里

```
#ifdef __cplusplus
#  ifdef __GNUG__
#    define __DARWIN_NULL __null
#  else /* ! __GNUG__ */
#    ifdef __LP64__
#      define __DARWIN_NULL (0L)
#    else /* !__LP64__ */
#      define __DARWIN_NULL 0
#    endif /* __LP64__ */
#  endif /* __GNUG__ */
#else /* ! __cplusplus */
#  define __DARWIN_NULL ((void *)0)
#endif /* __cplusplus */
```

### 作用

指向其他类型（如：基本类型、C类型）的指针为空.

**NULL 一般用于表示 C 指针空值**

### 例子

```objective-c
int   *pInt     = NULL;
char  *chChar   = NULL;
struct stStruct = NULL;
```

## 4.NSNull

### 在`NSNull.h`里只有一个类方法

```objective-c
+ (NSNull *)null;
```

### 作用：用来表示空值的 Objective-C 对象(通常表示集合中的空值.)

### 例子

```objective-c
NSArray *array = [NSArray arrayWithObjects:[[NSObject alloc] init], [NSNull null], [[NSObject alloc] init], [[NSObject alloc] init], nil];
```

### 为什么上面`array`里面的空对象不直接用`nil`？

```objective-c
NSArray *array = [NSArray arrayWithObjects:[[NSObject alloc] init], nil,  [[NSObject alloc] init], [[NSObject alloc] init], nil];
```

那么数组到第二个位置就会结束。打印`[array count]`的话会显示1而不是4,
所以`[NSNull null]`通常可以作为一个数组的占位符，从而使数组的count计算准确。

## 5.总结

不管是 `NULL`、`nil` 还是 `Nil`，它们本质上是一样的，都是 `(void *)0`，只是写法不同。这样做的意义是为了区分不同的数据类型，虽然它们值相同，但我们需要理解它们之间的字面意义并用于不同场景，让代码更加明确，增加可读性。