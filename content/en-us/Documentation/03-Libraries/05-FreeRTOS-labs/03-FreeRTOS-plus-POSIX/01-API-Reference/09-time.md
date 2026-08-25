---
title: FreeRTOS-Plus-POSIX time.h Implementation
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
    POSIX time.h - time types
```


## SYNOPSIS

```c
    #include "FreeRTOS_POSIX/time.h"
```


## DESCRIPTION

The FreeRTOS real time kernel measures time using a tick count variable. POSIX time is implemented on
top of FreeRTOS tick. Refer to RTOS Tick concept on this site.


### Symbolic Constants

### Types

Below types are NOT defined in FreeRTOS-Plus-POSIX time.h, but in sys/types.h

+ `clock_t`
+ `time_t`
+ `clockid_t`
+ `timer_t`
+ `pid_t`
+ `pthread_mutex_t`
+ `pthread_mutexattr_t`
+ `pthread_t`

Also size\_t is NOT defined in FreeRTOS-Plus-POSIX. An application needs to take dependency on platform
specific stdlib.h.


### tm structure

| Structure Member | Comment |
| --- | --- |
| `time_t tm_tick` | FreeRTOS tick count |
| `int tm_sec` | Seconds [0,60]. Functionality is NOT supported. |
| `int tm_min` | Minutes [0,59]. Functionality is NOT supported. |
| `int tm_hour` | Minutes [0,23]. Functionality is NOT supported. |
| `int tm_mday` | Seconds [1,31]. Functionality is NOT supported. |
| `int tm_mon` | Seconds [0,11]. Functionality is NOT supported. |
| `int tm_year` | Years since 1900. Functionality is NOT supported. |
| `int tm_wday` | Day of week [0,6] (Sunday=0). Functionality is NOT supported. |
| `int tm_yday` | Day of year [0,365]. Functionality is NOT supported. |
| `int tm_isdst` | Daylight Savings flag. Functionality is NOT supported. |


### timespec structure

| Structure Member | Comment |
| --- | --- |
| `time_t tv_sec` | Seconds |
| `long tv_nsec` | Nanoseconds |


### itimerspec structure

| Structure Member | Comment |
| --- | --- |
| `struct timespec it_interval` | Timer period |
| `struct timespec it_value` | Timer expiration |


### Macro

| Macro Name | Comment |
| --- | --- |
| `CLOCKS_PER_SEC` | This macro is platform dependent. CLOCK\_PER\_SEC is provided by configTICK\_RATE\_HZ, and configurable via FreeRTOSConfig.h.  |


### Symbolic Constant

+ `CLOCK_REALTIME`
+ `CLOCK_MONOTONIC`
+ `TIMER_ABSTIME`


### Symbolic Constant -- Time Conversion

+ `MICROSECONDS_PER_SECOND`
+ `NANOSECONDS_PER_SECOND`
+ `NANOSECONDS_PER_TICK`


### Function Prototypes

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

Inclusion of the "FreeRTOS\_POSIX/time.h" header may make visible all symbols from the "FreeRTOS\_POSIX/sys/types.h"
and "FreeRTOS\_POSIX/signal.h" header.
