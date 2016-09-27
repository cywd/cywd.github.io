---
layout: post
title: "assign, copy, retain, nonatomic, strong, weak属性"
excerpt: "assign, copy, retain, nonatomic, strong, weak属性"
categories: [OC]
tags: [OC]
date: 2014-05-11 
modified: 
comments: true
---

* TOC
{:toc}
---

### assign:

简单赋值，不改变索引计数。相当于指针赋值，不对引用计数进行操作。

一般用于数据类型 （NSInteger，CGFloat）和C数据类型（int, float, double, char, 等等）。

assign 其实也可以修饰对象，但是编译的时候会产生警告（Assigning retained object to unsafe property; object will be released after assignment），在释放之后，地址还是存在的，也就是说指针并没有被置为nil，造成野指针。

### copy：

建立一个索引计数为1的对象，然后释放旧对象。常用于NSString的拷贝。

copy其实是内容拷贝，比如copy一个NSString对象，拷贝到新的NSString对象，地址改变了，但是旧对象没有变化，新的对象retain为1。

### retain：

释放旧的对象，将旧对象的值赋予输入对象，再提高输入对象的索引计数为1。对其他NSObject和其子类。

retain到另外一个NSString之 后，地址相同（建立一个指针，指针拷贝），内容相同，这个对象的retain值+1

copy其实是建立了一个相同的对象，而retain不是。 copy是内容拷贝，retain是指针拷贝。

1. 比如一个NSString 对象，地址为0×1111 ，内容为@”String”，Copy 到另外一个NSString 之后，地址为0×2222 ，内容相同。
2. 新的对象retain为1 ，旧有对象没有变化retain 到另外一个NSString 之后，地址相同（建立一个指针，指针拷贝），内容当然相同，这个对象的retain值+1。

当引用计数为0时，dealloc函数被调用，内存被回收

### 深拷贝和浅拷贝的区别:

深拷贝就是内容拷贝，浅拷贝就是指针拷贝。

对于不可变对象copy采用的是浅复制，引用计数器加1。对于可变对象copy采用的是深复制，引用计数器不变。

### atomic:

设置成员变量的@property属性时，默认为atomic，提供多线程安全。

在多线程环境下，原子操作是必要的，否则有可能引起错误的结果。加了atomic，setter函数会变成下面这样：

   {lock}
​     if (property != newValue) {
​      [property release];
​       property = [newValue retain];
​     }
   {unlock}

### nonatomic：

非原子性访问，对属性赋值的时候不加锁，多线程并发访问会提高性能。如果不加此属性，则默认是两个访问方法都为原子型事务访问。

atomic是线程安全的,nonatomic是线程不安全的。如果只是单线程操作的话用nonatomic最好,因为后者效率高一些。

### strong强引用和weak弱引用的区别:

强引用：当前对象被其他对象引用时，会执行retain操作，引用计数器+1。当retainCount=0时，该对象才会被销毁。因为我们要进行对象的内存管理，所以这是默认的引用方式。（默认是强引用）。

弱引用：当前对象的生命周期不被是否由其他对象引用限制，它本该什么时候销毁就什么时候被销毁。即使它的引用没断，但是当它的生存周期到了时就会被销毁。

在定义属性时，若声明为retain类型的，则就是强引用；若声明为assign类型的，则就是弱引用。后来内存管理都由ARC来完成后，若是强引用，则就声明为strong；若是弱引用，则就声明为weak。

总的来说，retain和strong是一致的（强引用）；assign和weak是基本一致的（弱引用）。之所以说基本一致是因为还是有所不同的，weak严格的说应当叫“归零弱引用”，即当对象被销毁后，会自动的把它的指针置为nil，这样可以防止野指针错误。而assign销毁对象后不会把该对象的指针置nil，对象已经被销毁，但指针还在指向它，这就成了野指针。

strong：和retain相似,只要有一个strong指针指向对象，该对象就不会被销毁。

weak：声明为weak的指针，weak指针指向的对象一旦被释放，weak的指针都将被赋值为nil。

unsafe_unretained：用unsafe_unretained声明的指针，指针指向的对象一旦被释放，这些指针将成为野指针。

xib控件一般也是用weak修饰。 xib 添加控件是添加在根视图 View 上面, 而 控制器 Controller 对其根视图 View 默认是强引用的,当我们的子控件添加到 view 上面的时候, self.view addSubView: 这个方法会对添加的控件进行强引用,如果再用strong进行修饰，等于有两条强指针对子控件进行强引用,所以用 weak 修饰。

纯代码布局一般用strong。如果通过懒加载处理界面控件，需要使用strong强指针。

代理 也是用 weak 进行修饰的,其目的是为了防止控件的循环引用。

### `__block`和`__weak` 修饰符的区别:

 (1) __ block不管是ARC还是MRC模式下都可以使用,可以修饰对象,还可以修饰基本数据类型。

 (2) __ weak只能在ARC模式下使用,也只能修饰对象（NSString）,不能修饰基本数据类型(int)。

(3) __ block 对象可以在block中被重新赋值。




