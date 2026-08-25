---
title: FreeRTOS-Plus-POSIX unistd.h 实现
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
    POSIX unistd.h - standard symbolic constants and types
```


## 概要

```c
    #include "FreeRTOS_POSIX/unistd.h"
```


## 描述

### 函数原型

| &nbsp; | &nbsp; |
| --- | --- |
| `unsigned` | `sleep( unsigned seconds );` |
| `int` | `usleep( useconds_t usec );` |
