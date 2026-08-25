---
title: FreeRTOS-Plus-POSIX pthread.h 实现
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
POSIX pthread.h - threads
```


## 概要

```c
#include "FreeRTOS_POSIX/pthread.h"
```


## 描述

### 符号常数

+ `PTHREAD_BARRIER_SERIAL_THREAD`
+ `PTHREAD_CREATE_DETACHED`
+ `PTHREAD_CREATE_JOINABLE`
+ `PTHREAD_MUTEX_DEFAULT`
+ `PTHREAD_MUTEX_ERRORCHECK`
+ `PTHREAD_MUTEX_NORMAL`
+ `PTHREAD_MUTEX_RECURSIVE`


### 编译时间常数

| 名称                               | 类型初始化器 |
| ---------------------------------- | -------------------- |
| `PTHREAD_COND_INITIALIZER`         | pthread_cond_t     |
| `FREERTOS_POSIX_MUTEX_INITIALIZER` | pthread_mutex_t    |


### 类型

以下类型未在 FreeRTOS-Plus-POSIX pthread.h 中定义，但已用于
FreeRTOS-Plus-POSIX pthread.h 中的各种函数原型。在我们的实现中，为了确保前向兼容性，以下类型
针对用户显示为 `void *`。要使用 FreeRTOS-Plus-POSIX 线程功能，用户应仅维护
指向以下结构体类型的指针。`pthread_*()` 函数应在内部处理
结构体内存分配、取消分配和类型转换。类型定义相关内容请参阅 sys/types.h。

+ `pthread_attr_t`
+ `pthread_barrier_t`
+ `pthread_barrierattr_t`
+ `pthread_cond_t`
+ `pthread_condattr_t`
+ `pthread_mutex_t`
+ `pthread_mutexattr_t`
+ `pthread_t`


### 函数原型

| &nbsp;      | &nbsp;                                                                                                              |
| ----------- | ------------------------------------------------------------------------------------------------------------------- |
| `int`       | `pthread_attr_destroy( pthread_attr_t * attr );`                                                                    |
| `int`       | `pthread_attr_getdetachstate( const pthread_attr_t * attr, int * detachstate );`                                    |
| `int`       | `pthread_attr_getschedparam( const pthread_attr_t * attr, struct sched_param * param );`                            |
| `int`       | `pthread_attr_getstacksize( const pthread_attr_t * attr, size_t * stacksize );`                                     |
| `int`       | `pthread_attr_init( pthread_attr_t * attr );`                                                                       |
| `int`       | `pthread_attr_setdetachstate( pthread_attr_t * attr, int detachstate );`                                            |
| `int`       | `pthread_attr_setschedparam( pthread_attr_t * attr, const struct sched_param * param );`                            |
| `int`       | `pthread_attr_setstacksize( pthread_attr_t * attr, size_t stacksize );`                                             |
| `int`       | `pthread_barrier_destroy( pthread_barrier_t * barrier );`                                                           |
| `int`       | `pthread_barrier_init( pthread_barrier_t * barrier, const pthread_barrierattr_t * attr, unsigned count );`          |
| `int`       | `pthread_barrier_wait( pthread_barrier_t * barrier );`                                                              |
| `int`       | `pthread_create( pthread_t * thread, const pthread_attr_t * attr, void *( *startroutine )( void * ), void * arg );` |
| `int`       | `pthread_cond_broadcast( pthread_cond_t * cond );`                                                                  |
| `int`       | `pthread_cond_destroy( pthread_cond_t * cond );`                                                                    |
| `int`       | `pthread_cond_init( pthread_cond_t * cond, const pthread_condattr_t * attr );`                                      |
| `int`       | `pthread_cond_signal( pthread_cond_t * cond );`                                                                     |
| `int`       | `pthread_cond_timedwait( pthread_cond_t * cond, pthread_mutex_t * mutex, const struct timespec * abstime );`        |
| `int`       | `pthread_cond_wait( pthread_cond_t * cond, pthread_mutex_t * mutex );`                                              |
| `int`       | `pthread_equal( pthread_t t1, pthread_t t2 );`                                                                      |
| `void`      | `pthread_exit( void * value_ptr );`                                                                                 |
| `int`       | `pthread_getschedparam( pthread_t thread, int * policy, struct sched_param * param );`                              |
| `int`       | `pthread_join( pthread_t thread, void ** retval );`                                                                 |
| `int`       | `pthread_mutex_destroy( pthread_mutex_t * mutex );`                                                                 |
| `int`       | `pthread_mutex_init( pthread_mutex_t * mutex, const pthread_mutexattr_t * attr );`                                  |
| `int`       | `pthread_mutex_timedlock( pthread_mutex_t * mutex, const struct timespec * abstime );`                              |
| `int`       | `pthread_mutex_trylock( pthread_mutex_t * mutex );`                                                                 |
| `int`       | `pthread_mutex_unlock( pthread_mutex_t * mutex );`                                                                  |
| `int`       | `pthread_mutexattr_destroy( pthread_mutexattr_t * attr );`                                                          |
| `int`       | `pthread_mutexattr_gettype( const pthread_mutexattr_t * attr, int * type );`                                        |
| `int`       | `pthread_mutexattr_init( pthread_mutexattr_t * attr );`                                                             |
| `int`       | `pthread_mutexattr_settype( pthread_mutexattr_t * attr, int type );`                                                |
| `pthread_t` | `pthread_self( void );`                                                                                             |
| `int`       | `pthread_setschedparam( pthread_t thread, int policy, const struct sched_param * param );`                          |

加入 "FreeRTOS_POSIX/pthread.h" 头文件后，"FreeRTOS_POSIX/schedule.h"
和 "FreeRTOS_POSIX/time.h" 等头文件中定义的符号应变为可见。
