---
title: FreeRTOS-Plus-POSIX fcntl.h 实现
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[FreeRTOS-Plus-POSIX 概览](/Documentation/03-Libraries/05-FreeRTOS-labs/03-FreeRTOS-plus-POSIX/00-FreeRTOS-Plus-POSIX)]


## 名称

```c
    POSIX fcntl.h - File Control Options
```


## 概要

```c
    #include "FreeRTOS_POSIX/fcntl.h"
```


## 描述

### 符号常量 -- 文件创建标志

在 open() 和 openat() 的 oflag 值中使用的符号常量创建标志。


+ `O_CLOEXEC`

  在exec() 时关闭文件描述符。

+ `O_CREAT`

  如果文件不存在，创建文件。

+ `O_DIRECTORY`

  如果文件为非目录文件，则失败。

+ `O_EXCL/code>`

  专用标志。

+ `O_NOCTTY`

  不指定控制终端。

+ `O_NOFOLLOW`

  不跟随符号链接。

+ `O_TRUNC`

  截断标志。

+ `O_TTY_INIT`

  termios 结构体提供一致性行为。


### 符号常量 -- 文件状态标志

用作 open()、openat() 和 fcntl() 的文件状态标志的符号常量

todo -- O_DSYNC 和 O_SYNC 均为 0x0200。开放组不要求二者各不相同。但是，
它们在功能上应有所区分 http://man7.org/linux/man-pages/man2/open.2.html。开放组也
不要求它们"按位区分"。我们的文件系统是如何设计的？

+ `O_APPEND`

  设置追加模式。

+ `O_DSYNC`

  按同步 I/O 数据完整性完成写入。

+ `O_NONBLOCK`

  非阻塞模式。

+ `O_RSYNC`

  同步读取 I/O 操作。

+ `O_SYNC`

  按同步 I/O 文件完整性完成写入。


### 符号常量 -- 用于文件访问模式的掩码。

+ `O_ACCMODE`

  用于文件访问模式的掩码。


### 符号常量 -- 文件访问模式

+ `O_EXEC`

  以只执行方式打开（非目录文件）。

+ `O_RDONLY`

  以只读方式打开。

+ `O_RDWR`

  以可读写方式打开。

+ `O_SEARCH`

  以只搜索方式打开。

+ `O_WRONLY`

  以只写方式打开。
