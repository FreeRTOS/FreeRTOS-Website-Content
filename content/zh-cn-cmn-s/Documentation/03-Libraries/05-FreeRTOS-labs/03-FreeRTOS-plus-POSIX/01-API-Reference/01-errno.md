---
title: FreeRTOS-Plus-POSIX errno.h 实现
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
    POSIX errno.h - System Error Numbers
```


## 概要

```c
    #include "FreeRTOS_POSIX/errno.h"
```


## 描述

### 系统变量

+ `errno`

  可以通过设置 configUSE_POSIX_errno 为 0 来禁用 errno。详见 FreeRTOS.h。


### 符号常数——可能的错误代码

+ `EPERM`

  操作不允许。

+ `ENOENT`

  文件或目录不存在。

+ `EBADF`

  文件描述符错误。

+ `EAGAIN`

  资源不可用，请重试。

+ `ENOMEM`

  空间不足。

+ `EEXIST`

  文件已存在。

+ `EBUSY`

  设备或资源忙。

+ `EINVAL`

  参数无效。

+ `ENOSPC`

  设备无剩余空间。

+ `ERANGE`

  结果过大。

+ `ENAMETOOLONG`

  文件名过长。

+ `EDEADLK`

  可能出现资源死锁。

+ `EOVERFLOW`

  数值过大，无法存储在数据类型中。

+ `ENOSYS`

  函数不被支持。

+ `EMSGSIZE`

  消息过长。

+ `ENOTSUP`

  不支持的操作。

+ `ETIMEDOUT`

  连接超时。
