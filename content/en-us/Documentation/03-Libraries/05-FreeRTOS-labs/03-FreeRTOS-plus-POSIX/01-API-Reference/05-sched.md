---
title: FreeRTOS-Plus-POSIX sched.h Implementation
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
    POSIX sched.h - execution scheduling
```


## SYNOPSIS

```c
    #include "FreeRTOS_POSIX/sched.h"
```


## DESCRIPTION

### Symbolic Constants

+ `SCHED_OTHER`


### struct sched\_param

| Structure Member | Comment |
| --- | --- |
| `int sched_priority` | Process or thread execution scheduling priority. |


### Function Prototypes

| &nbsp;  | &nbsp;  |
| --- | --- |
| `int` | `sched_get_priority_max( int policy );` |
| `int` | `sched_yield( void );` |
