---
title: FreeRTOS-Plus-POSIX pthread.h Implementation
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-POSIX Overview](/Documentation/03-Libraries/05-FreeRTOS-labs/03-FreeRTOS-plus-POSIX/00-FreeRTOS-Plus-POSIX)]


## NAME

```c
POSIX pthread.h - threads
```


## SYNOPSIS

```c
#include "FreeRTOS_POSIX/pthread.h"
```


## DESCRIPTION

### Symbolic Constants

+ `PTHREAD_BARRIER_SERIAL_THREAD`
+ `PTHREAD_CREATE_DETACHED`
+ `PTHREAD_CREATE_JOINABLE`
+ `PTHREAD_MUTEX_DEFAULT`
+ `PTHREAD_MUTEX_ERRORCHECK`
+ `PTHREAD_MUTEX_NORMAL`
+ `PTHREAD_MUTEX_RECURSIVE`


### Compile Time Constants

| Name                               | Initializer for Type |
| ---------------------------------- | -------------------- |
| `PTHREAD_COND_INITIALIZER`         | pthread\_cond\_t     |
| `FREERTOS_POSIX_MUTEX_INITIALIZER` | pthread\_mutex\_t    |


### Types

Below types are NOT defined in FreeRTOS-Plus-POSIX pthread.h, but used across function prototypes in
FreeRTOS-Plus-POSIX pthread.h. In our implementation, to ensure forward compatibility, below types are
exposed to user as `void *`. To use FreeRTOS-Plus-POSIX threading features, user shall only maintain
pointers which point to below structure types. `pthread_*()` functions shall take care of structure
memory allocating, deallocating and type casting internally. See sys/types.h for type definition.

+ `pthread_attr_t`
+ `pthread_barrier_t`
+ `pthread_barrierattr_t`
+ `pthread_cond_t`
+ `pthread_condattr_t`
+ `pthread_mutex_t`
+ `pthread_mutexattr_t`
+ `pthread_t`


### Function Prototypes

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

Inclusion of the "FreeRTOS_POSIX/pthread.h" header shall make symbols defined in the headers "FreeRTOS_POSIX/sched.h"
and "FreeRTOS_POSIX/time.h" visible.
