---
layout: post
title: LearnOpenGL 环境配置
excerpt: "Xcode/GLFW/GLAD"
categories: [OpenGL]
tags: [OpenGL]
date: 2018-01-12
comments: true
---

* TOC
{:toc}
---

# 1.GLFW库

这里通过`homebrew`来安装

```shell
$ brew install glfw
```

注意看安装完成后的提示，可能需要手动 `brew link'`

# 2.下载GLAD库

打开`GLAD`的[在线服务](http://glad.dav1d.de/)，将语言(Language)设置为**C/C++**，在`API`选项中，选择`3.3`或以上的`OpenGL`版本。之后将模式(`Profile`)设置为**Core**，并且保证生成加载器**(Generate a loader)**的选项是选中的。都选择完之后，点击生成(Generate)按钮来生成库文件。

`GLAD`现在应该提供给你了一个zip压缩文件，解压缩后。文件目录应是这样:

```
./glad
├── include
│   ├── KHR
│   │   └── khrplatform.h
│   └── glad
│       └── glad.h
└── src
    └── glad.c
```

将两个头文件目录（glad和KHR）复制到`/usr/local/include`，并添加`glad.c`文件到工程中。

# 3.配置Xcode项目头文件和库路径

在xcode项目中

Header Search Paths 中添加

```
/usr/local/include
```

Library Search Paths 中添加

```
/usr/local/Cellar/glfw/3.2.1/lib
```

# 4.使用

```c++
#include <glad/glad.h>
#include <GLFW/glfw3.h>
```

# 5.注意

在Mac需要加上这样的代码

```c++
#ifdef __APPLE__
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE); // uncomment this statement to fix compilation on OS X
#endif
```



目前按照这个教程在学习[https://learnopengl-cn.github.io](https://learnopengl-cn.github.io)

