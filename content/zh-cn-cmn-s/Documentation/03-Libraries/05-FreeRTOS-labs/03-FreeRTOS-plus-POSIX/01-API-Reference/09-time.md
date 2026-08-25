---
title: FreeRTOS-Plus-POSIX time.h 实现
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
    POSIX time.h - time types
```


## 概要

```c
    #include "FreeRTOS_POSIX/time.h"
```


## 描述

FreeRTOS 实时内核通过滴答计数变量测量时间。POSIX 时间
根据 FreeRTOS tick 来实现。请参阅本网站上的 RTOS Tick 概念。


### 符号常数

### 类型

以下类型未在 FreeRTOS-Plus-POSIX time.h 中定义，但在 sys/types.h 中定义

+ `clock_t`
+ `time_t`
+ `clockid_t`
+ `timer_t`
+ `pid_t`
+ `pthread_mutex_t`
+ `pthread_mutexattr_t`
+ `pthread_t`

size_t 也未在 FreeRTOS-Plus-POSIX 中定义 。应用程序需要依赖平台特定的
stdlib.h。


### tm 结构体

| 结构体成员 | 注释 |
| --- | --- |
| `time_t tm_tick` | FreeRTOS 滴答计数 |
| `int tm_sec` | [0,60] 秒。不支持此功能。 |
| `int tm_min` | [0,59] 分钟。不支持此功能。 |
| `int tm_hour` | [0,23] 分钟。不支持此功能。 |
| `int tm_mday` | [1,31] 秒。不支持此功能。 |
| `int tm_mon` | [0,11] 秒。不支持此功能。 |
| `int tm_year` | 1900 年以来的年份。不支持此功能。 |
| `int tm_wday` | 星期 [0,6]（星期日 = 0）。不支持此功能。 |
| `int tm_yday` | 一年中的第 [0,365] 天。不支持此功能。 |
| `int tm_isdst` | 夏令时标志。不支持此功能。 |


### timespec 结构体

| 结构体成员 | 注释 |
| --- | --- |
| `time_t tv_sec` | 秒 |
| `long tv_nsec` | 纳秒 |


### itimerspec 结构体

| 结构体成员 | 注释 |
| --- | --- |
| `struct timespec it_interval` | 计时器周期 |
| `struct timespec it_value` | 计时器过期 |


### 宏

| 宏名称 | 注释 |
| --- | --- |
| `CLOCKS_PER_SEC` | 此宏与平台相关。CLOCK_PER_SEC 由 configTICK_RATE_HZ 提供，可通过 FreeRTOSConfig.h 进行配置。  |


### 符号常量

+ `CLOCK_REALTIME`
+ `CLOCK_MONOTONIC`
+ `TIMER_ABSTIME`


### 符号常数—时间转换

+ `MICROSECONDS_PER_SECOND`
+ `NANOSECONDS_PER_SECOND`
+ `NANOSECONDS_PER_TICK`


### 函数原型

| &nbsp;  | &nbsp; |
| --- | --- |
| `clock_t` | `clock( void );` |
| `int` | `clock_getcpuclockid( pid_t pid, clockid_t * clock_id );` |
| `int` | `clock_getres( clockid_t clock_id, struct timespec * res );` |
| `int` | `clock_gettime( clockid_t clock_id, struct timespec * tp );` |
| `int` | `clock_nanosleep( clockid_t clock_id, int flags, const struct timespec * rqtp, struct timespec * rmtp );` |
| `int` | `clock_settime( clockid_t clock_id, const struct timespec * tp );` |
| `struct tm *` | `localtime_r( const time_t * timer, struct tm * result );` |
| `int` | `nanosleep( const struct timespec * rqtp, struct timespec * rmtp );` |
| `size_t` | `strftime( char * s, size_t maxsize, const char * format, const struct tm * timeptr );` |
| `time_t` | `time( time_t * tloc );` |
| `int` | `timer_create( clockid_t clockid, struct sigevent * evp, timer_t * timerid );` |
| `int` | `timer_delete( timer_t timerid );` |
| `int` | `timer_getoverrun( timer_t timerid );` |
| `int` | `timer_gettime( timer_t timerid, struct itimerspec * value );` |
| `int` | `timer_settime( timer_t timerid, int flags, const struct itimerspec * value, struct itimerspec * ovalue );` |

加入 "FreeRTOS_POSIX/time.h" 标头文件可能会使 "FreeRTOS_POSIX/sys/types.h"
和 "FreeRTOS_POSIX/signal.h" 头文件中的所有符号变得可见。
