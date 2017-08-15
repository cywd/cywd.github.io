---
layout: post
title: NSTask使用
excerpt: "关于怎么在mac程序上使用shell命令"
categories: [Cocoa]
tags: [Cocoa]
date: 2017-08-15
comments: true
---

* TOC
{:toc}
---

# 使用

```
- (NSString *)cmd:(NSString *)cmd
{
    // 初始化并设置shell路径
    NSTask *task = [[NSTask alloc] init];
    [task setLaunchPath: @"/bin/bash"];
    // -c 用来执行string-commands（命令字符串），也就说不管后面的字符串里是什么都会被当做shellcode来执行
    // 当然也可以使用  [task setLaunchPath: @"/bin/pwd"];  来调用pwd。 另外比如说想调用python，要写完整路径，比如：/usr/local/bin/python3 。 
    // 打开程序可以使用 /usr/bin/open
    NSArray *arguments = [NSArray arrayWithObjects: @"-c", cmd, nil];
    [task setArguments: arguments];
    
    // 正常是会在控制台输出
    // 新建输出管道作为Task的输出
    NSPipe *pipe = [NSPipe pipe];
    [task setStandardOutput: pipe];
    
    // 开始task
    NSFileHandle *file = [pipe fileHandleForReading];
    [task launch];
    
    // 获取运行结果
    NSData *data = [file readDataToEndOfFile];
    return [[NSString alloc] initWithData: data encoding: NSUTF8StringEncoding];
}
```

该方法传入一个NSString类型的命令字符串，返回运行结果。但是使用这种方法没法记忆上一次操作，没法做到像在终端中执行多次命令那样自如。

例如：先cd到桌面，然后在桌面新建文件夹，在终端中我们是这么实现的：

```
cd Desktop
mkdir test
```

使用NSTask调用：

```
// 这种调用方式结果是错误的，因为一条命令执行完Task就会销毁，相当于输入完终端关闭，再打开再输出，所以这时执行第二条语句时第一条语句已经不起作用了
[self cmd:@"cd Desktop"];
[self cmd:@"mkdir test"];

// 应使用下面这种方式实现
[self cmd:@"cd Desktop; mkdir test"];
```





# 参考

[使用NSTask调用shell](http://www.cnblogs.com/JanaChen/p/5883966.html)

[Swift3.0 开发一款名叫 cocoaPods助手](http://www.jianshu.com/p/4293ef7a5227)