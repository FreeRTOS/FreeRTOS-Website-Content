---
title: FreeRTOS-Plus-POSIX sys/types.h Implementation
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
    POSIX sys/types.h - data types
```


## SYNOPSIS

```c
    #include "FreeRTOS_POSIX/sys/types.h"
```


## DESCRIPTION

Most of the data types below can be enabled or disabled by overwriting FreeRTOS\_POSIX\_portable\_default.h.
Default is "everything is enabled". It is recommended to only disable a data type, if it conflicts with
your system types.


### Data Types

| Data Type | Comment |
| --- | --- |
| `clock_t` | Used for system times in clock ticks or CLOCKS\_PER\_SEC. Set/clear posixconfigENABLE\_CLOCK\_T. |
| `clockid_t` | Used for clock ID type in the clock and timer functions. Set/clear posixconfigENABLE\_CLOCKID\_T. |
| `mode_t` | Used for some file attributes. Set/clear posixconfigENABLE\_MODE\_T. |
| `pid_t` | Used for process IDs and process group IDs. Set/clear posixconfigENABLE\_PID\_T. |
| `pthread_attr_t` | Used to identify a thread attribute object. Set/clear posixconfigENABLE\_PTHREAD\_ATTR\_T. |
| `pthread_barrier_t` | Used to identify a barrier. |
| `pthread_barrierattr_t` | Used to define a barrier attributes object. |
| `pthread_cond_t` | Used for condition variables. Set/clear posixconfigENABLE\_PTHREAD\_COND\_T. |
| `pthread_condattr_t` | Used to identify a condition attribute object. Set/clear posixconfigENABLE\_PTHREAD\_CONDATTR\_T. |
| `pthread_mutex_t` | Used for mutexes. Set/clear posixconfigENABLE\_PTHREAD\_MUTEX\_T. |
| `pthread_mutexattr_t` | Used to identify a mutex attribute object. Set/clear posixconfigENABLE\_PTHREAD\_MUTEXATTR\_T |
| `pthread_t` | Used to identify a thread. Set/clear posixconfigENABLE\_PTHREAD\_T |
| `ssize_t` | Used for a count of bytes or an error indication. Set/clear posixconfigENABLE\_SSIZE\_T. |
| `time_t` | Used for time in seconds. Set/clear posixconfigENABLE\_TIME\_T. |
| `timer_t` | Used for timer ID returned by timer\_create(). Set/clear posixconfigENABLE\_TIMER\_T. |
| `useconds_t` | Used for time in microseconds. Set/clear posixconfigENABLE\_USECONDS\_T. |
