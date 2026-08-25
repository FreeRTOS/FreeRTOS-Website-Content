---
title: FreeRTOS-Plus-POSIX signal.h 实现
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
    POSIX signal.h - signals
```

## 概要

```c
    #include "FreeRTOS_POSIX/signal.h"
```


## 描述

### struct sigevent

**结构体成员**

```c
int  sigev_notify
```
通知类型。可以设置 SIGEV_SIGNAL 的值，但尚不支持。

```c
int  sigev_signo
```
信号编号。不支持此功能。

```c
union  sigval sigev_value
```
信号值。可以设置为整型，但尚不支持。

```c
void  ( * sigev_notify_function ) ( union sigval )
```
通知函数。

```c
pthread_attr_t * sigev_notify_attributes
```
通知属性。


### 结构体成员——`int sigev_notify`

| 符号常量值 | 注释 |
| --- | --- |
| `SIGEV_NONE` | 相关事件发生时，不会发送异步通知。 |
| `SIGEV_SIGNAL` | 相关事件发生时，生成排队信号，该信号具有应用程序定义的值。不支持此功能。 |
| `SIGEV_THREAD` | 调用通知函数执行通知。 |


### 结构体成员——`sigval union`

| 数据类型 | 注释 |
| --- | --- |
| `int sival_int` | 整数信号值。不支持此功能。 |
| `void * sival_ptr` | 指针信号值。 |
