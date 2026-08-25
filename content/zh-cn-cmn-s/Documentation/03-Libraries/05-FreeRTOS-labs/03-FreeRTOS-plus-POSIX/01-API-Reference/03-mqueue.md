---
title: FreeRTOS-Plus-POSIX mqueue.h 实现
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
    POSIX mqueue.h - message queues
```


## 概要

```c
    #include "FreeRTOS_POSIX/mqueue.h"
```


## 描述

### 符号常数


### 类型

`mqd_t`

以下类型未在 FreeRTOS-Plus-POSIX sys/types.h 中定义，但在 sys/types.h 中定义

todo -- sys/types.h 不包含在此标头中。

+ `pthread_mutexattr_t`
+ `ssize_t`

以下类型未在 FreeRTOS-Plus-POSIX time.h 中定义，但在 sys/types.h 中定义

+ `struct timespec`

todo -- 为简化库依赖项，此处未定义 size_t，也未包含 stdlib.h。设置
演示，并了解如何将 stdlib.h 包含在特定平台中。然后更新此行。


### mq_attr 结构体

| 结构体成员 | 注释 |
| --- | --- |
| `long mq_flags` | 消息队列标志。 |
| `long mq_maxmsg` | 消息的最大数量。 |
| `long mq_msgsize` | 最大消息大小。 |
| `long mq_curmsgs` | 当前排队消息数。 |


### 函数原型

+ `int`

  `mq_close( mqd_t mqdes );`

+ `int`

  `mq_getattr( mqd_t mqdes, struct mq_attr * mqstat );`

+ `mqd_t`

  `mq_open( const char * name, int oflag, mode_t mode, struct mq_attr * attr );`

+ `ssize_t`

  `mq_receive( mqd_t mqdes, char * msg_ptr, size_t msg_len, unsigned int * msg_prio );`

+ `int`

  `mq_send( mqd_t mqdes, const char * msg_ptr, size_t msg_len, unsigned msg_prio );`

+ `ssize_t`

  `mq_timedreceive( mqd_t mqdes, char * msg_ptr, size_t msg_len, unsigned * msg_prio, const struct timespec * abstime );`

+ `int`

  `mq_timedsend( mqd_t mqdes, const char * msg_ptr, size_t msg_len, unsigned msg_prio, const struct timespec * abstime );`

+ `int`

  `mq_unlink( const char * name );`

包含 "FreeRTOS_POSIX/mqueue.h" 标头使 "FreeRTOS_POSIX/time.h" 标头中定义的符号可见。
