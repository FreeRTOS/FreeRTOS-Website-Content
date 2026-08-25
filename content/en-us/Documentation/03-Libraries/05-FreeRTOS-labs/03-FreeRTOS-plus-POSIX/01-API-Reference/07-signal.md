---
title: FreeRTOS-Plus-POSIX signal.h Implementation
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
    POSIX signal.h - signals
```

## SYNOPSIS

```c
    #include "FreeRTOS_POSIX/signal.h"
```


## DESCRIPTION

### struct sigevent

**Structure Members**

```c
int  sigev_notify
```
Notification type. The value of SIGEV\_SIGNAL is possible, but NOT supported.

```c
int  sigev_signo
```
Signal number. Functionality is NOT supported.

```c
union  sigval sigev_value
```
Signal value. The type of int is possible, but NOT supported.

```c
void  ( * sigev_notify_function ) ( union sigval )
```
Notification function.

```c
pthread_attr_t * sigev_notify_attributes
```
Notification attributes.


### struct member -- `int sigev_notify`

| Symbolic Constant value | Comment |
| --- | --- |
| `SIGEV_NONE` | No asynchronous notification is delivered when the event of interest occurs. |
| `SIGEV_SIGNAL` | A queued signal, with an application-defined value, is generated when the event of interest occurs. Functionality is NOT supported |
| `SIGEV_THREAD` | A notification function is called to perform notification. |


### struct member -- `sigval union`

| Data type | Comment |
| --- | --- |
| `int sival_int` | Integer signal value. Functionality is NOT supported. |
| `void * sival_ptr` | Pointer signal value. |
