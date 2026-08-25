---
title: FreeRTOS-Plus-POSIX unistd.h Implementation
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
    POSIX unistd.h - standard symbolic constants and types
```


## SYNOPSIS

```c
    #include "FreeRTOS_POSIX/unistd.h"
```


## DESCRIPTION

### Function Prototypes

| &nbsp; | &nbsp; |
| --- | --- |
| `unsigned` | `sleep( unsigned seconds );` |
| `int` | `usleep( useconds_t usec );` |
