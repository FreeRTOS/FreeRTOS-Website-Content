---
title: FreeRTOS-Plus-POSIX sys/types.h 实现
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
    POSIX sys/types.h - data types
```


## 概要

```c
    #include "FreeRTOS_POSIX/sys/types.h"
```


## 描述

下面的多数数据类型可以通过重写 FreeRTOS_POSIX_portable_default.h 启用或禁用。
默认为“启用全部”。我们建议只有在数据类型与系统类型冲突时才禁用该数据类型
。


### 数据类型

| 数据类型 | 注释 |
| --- | --- |
| `clock_t` | 用于以时钟滴答或 CLOCKS_PER_SEC 为单位的系统时间。设置或清除 posixconfigENABLE_CLOCK_T。 |
| `clockid_t` | 用于时钟和定时器函数中的时钟 ID 类型。设置或清除 posixconfigENABLE_CLOCKID_T。 |
| `mode_t` | 用于某些文件属性。设置或清除 posixconfigENABLE_MODE_T。 |
| `pid_t` | 用于进程 ID 和进程组 ID。设置或清除 posixconfigENABLE_PID_T。 |
| `pthread_attr_t` | 用于识别线程属性对象。设置或清除 posixconfigENABLE_PTHREAD_ATTR_T。 |
| `pthread_barrier_t` | 用于标识屏障。 |
| `pthread_barrierattr_t` | 用于定义障碍属性对象。 |
| `pthread_cond_t` | 用于条件变量。设置或清除 posixconfigENABLE_PTHREAD_COND_T。 |
| `pthread_condattr_t` | 用于标识条件属性对象。设置或清除 posixconfigENABLE_PTHREAD_CONDATTR_T。 |
| `pthread_mutex_t` | 用于互斥锁。设置或清除 posixconfigENABLE_PTHREAD_MUTEX_T。 |
| `pthread_mutexattr_t` | 用于标识互斥锁属性对象。设置或清除 POSIXCONFIGEENABLE_PTHREAD_MUTEXATTR_T。 |
| `pthread_t` | 用于识别线程。设置或清除 posixconfigENABLE_PTHREAD_T。 |
| `ssize_t` | 用于字节计数或错误指示。设置或清除 POSIXCONFIGEENABLE_SSIZE_T。 |
| `time_t` | 用于以秒为单位的时间。设置或清除 posixconfigENABLE_TIME_T。 |
| `timer_t` | 用于 timer_create() 返回的计时器 ID。设置或清除 posixconfigENABLE_TIMER_T。 |
| `useconds_t` | 用于以微秒为单位的时间。设置或清除 posixconfigENABLE_USECONDS_T。 |
