---
title: FreeRTOS-Plus-POSIX semaphore.h 实现
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[FreeRTOS-Plus-POSIX 概览](/Documentation/03-Libraries/05-FreeRTOS-labs/03-FreeRTOS-plus-POSIX/00-FreeRTOS-Plus-POSIX)]


## 名称
----

```c
    POSIX semaphore.h - semaphores
```


## 概要

```c
    #include "FreeRTOS_POSIX/semaphore.h"
```


## 描述

### 类型

+ `sem_t`


### 函数原型

| &nbsp;  | &nbsp; |
| --- | --- |
| `int` | `sem_destroy( sem_t * sem );` |
| `int` | `sem_getvalue( sem_t * sem, int * sval );` |
| `int` | `sem_init( sem_t * sem, int pshared, unsigned value );` |
| `int` | `sem_post( sem_t * sem );` |
| `int` | `sem_timedwait( sem_t * sem, const struct timespec * abstime );` |
| `int` | `sem_trywait( sem_t * sem );` |
| `int` | `sem_wait( sem_t * sem );` |

包含 “FreeRTOS_POSIX/semaphore.h” 标头可能使 “FreeRTOS_POSIX/time.h” 中定义的符号可见。
