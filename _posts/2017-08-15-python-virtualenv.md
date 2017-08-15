---
layout: post
title: Python虚拟环境virtualenv
excerpt: "virtualenv可以搭建虚拟且独立的python运行环境, 使得单个项目的运行环境与其它项目独立起来."
categories: [Python]
tags: [Python]
date: 2017-08-15
comments: true
---

* TOC
{:toc}
---

virtualenv可以搭建虚拟且独立的python运行环境, 使得单个项目的运行环境与其它项目独立起来.

virtualenv本质上是个python包, 使用pip安装:

```python
pip3 install virtualenv
```

在工作目录下创建虚拟环境:

```
➜  virtualenvTest virtualenv test
Using base prefix '/usr/local/Cellar/python3/3.6.2/Frameworks/Python.framework/Versions/3.6'
New python executable in /Users/cyrill/virtualenvTest/test/bin/python3.6
Also creating executable in /Users/cyrill/virtualenvTest/test/bin/python
Installing setuptools, pip, wheel...done.
```

默认情况下, 虚拟环境中不包括系统的site-packages, 若要使用请添加参数:

```
virtualenv --system-site-packages test
```

进入虚拟环境目录, 执行`source ./bin/activate`进入虚拟环境:

```zsh
➜  virtualenvTest cd test
➜  test source ./bin/activate
(test) ➜  test python -V
Python 3.6.2
(test) ➜  test pip list
DEPRECATION: The default format will switch to columns in the future. You can use --format=(legacy|columns) (or define a format=(legacy|columns) in your pip.conf under the [list] section) to disable this warning.
pip (9.0.1)
setuptools (36.2.7)
wheel (0.29.0)
```

退出虚拟环境:

```
(test) ➜  test deactivate
➜  test
```