---
title: FreeRTOS-Plus-POSIX semaphore.h Implementation
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[FreeRTOS-Plus-POSIX Overview](/Documentation/03-Libraries/05-FreeRTOS-labs/03-FreeRTOS-plus-POSIX/00-FreeRTOS-Plus-POSIX)]


## NAME
----

```c
    POSIX semaphore.h - semaphores
```


## SYNOPSIS

```c
    #include "FreeRTOS_POSIX/semaphore.h"
```


## DESCRIPTION

### Types

+ `sem_t`


### Function Prototypes

| &nbsp;  | &nbsp; |
| --- | --- |
| `int` | `sem_destroy( sem_t * sem );` |
| `int` | `sem_getvalue( sem_t * sem, int * sval );` |
| `int` | `sem_init( sem_t * sem, int pshared, unsigned value );` |
| `int` | `sem_post( sem_t * sem );` |
| `int` | `sem_timedwait( sem_t * sem, const struct timespec * abstime );` |
| `int` | `sem_trywait( sem_t * sem );` |
| `int` | `sem_wait( sem_t * sem );` |

Inclusion of the "FreeRTOS\_POSIX/semaphore.h" header may make visible symbols defined in the "FreeRTOS\_POSIX/time.h".
