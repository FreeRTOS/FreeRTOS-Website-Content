---
title: FreeRTOS-Plus-POSIX sched.h 实现
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
    POSIX sched.h - execution scheduling
```


## 概要

```c
    #include "FreeRTOS_POSIX/sched.h"
```


## 描述

### 符号常数

+ `SCHED_OTHER`


### struct sched_param

| 结构体成员 | 注释 |
| --- | --- |
| `int sched_priority` | 进程或线程执行调度优先级。 |


### 函数原型

| &nbsp;  | &nbsp;  |
| --- | --- |
| `int` | `sched_get_priority_max( int policy );` |
| `int` | `sched_yield( void );` |
