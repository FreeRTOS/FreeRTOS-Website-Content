---
title: FreeRTOS-Plus-POSIX mqueue.h Implementation
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
    POSIX mqueue.h - message queues
```


## SYNOPSIS

```c
    #include "FreeRTOS_POSIX/mqueue.h"
```


## DESCRIPTION

### Symbolic Constants


### Types

`mqd_t`

Below types are NOT defined in FreeRTOS-Plus-POSIX sys/types.h, but in sys/types.h

todo -- sys/types.h is not included in this header.

+ `pthread_mutexattr_t`
+ `ssize_t`

Below types are NOT defined in FreeRTOS-Plus-POSIX time.h, but in sys/types.h

+ `struct timespec`

todo -- size\_t is not defined here, nor is stdlib.h included to simplify library dependency. Setup
demo, and see how to include stdlib.h in a specific platform. Then update this line.


### mq\_attr structure

| Structure Member | Comment |
| --- | --- |
| `long mq_flags` | Message queue flags. |
| `long mq_maxmsg` | Maximum number of messages. |
| `long mq_msgsize` | Maximum message size. |
| `long mq_curmsgs` | Number of messages currently queued. |


### Function Prototypes

+ `int`

  `mq_close( mqd_t mqdes );`

+ `int`

  `mq_getattr( mqd_t mqdes, struct mq_attr * mqstat );`

+ `mqd_t`

  `mq_open( const char * name, int oflag, mode_t mode, struct mq_attr * attr );`

+ `ssize_t`

  `mq_receive( mqd_t mqdes, char * msg_ptr, size_t msg_len, unsigned int * msg_prio );`

+ `int`

  `mq_send( mqd_t mqdes, const char * msg_ptr, size_t msg_len, unsigned msg_prio );`

+ `ssize_t`

  `mq_timedreceive( mqd_t mqdes, char * msg_ptr, size_t msg_len, unsigned * msg_prio, const struct timespec * abstime );`

+ `int`

  `mq_timedsend( mqd_t mqdes, const char * msg_ptr, size_t msg_len, unsigned msg_prio, const struct timespec * abstime );`

+ `int`

  `mq_unlink( const char * name );`

Inclusion of the "FreeRTOS\_POSIX/mqueue.h" header may make visible symbols defined in "FreeRTOS\_POSIX/time.h" header.
