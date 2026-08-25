---
title: FreeRTOS-Plus-POSIX errno.h Implementation
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
    POSIX errno.h - System Error Numbers
```


## SYNOPSIS

```c
    #include "FreeRTOS_POSIX/errno.h"
```


## DESCRIPTION

### System Variable

+ `errno`

  errno can be suppressed by setting configUSE\_POSIX\_ERRNO to 0. See FreeRTOS.h.


### Symbolic Constants -- Possible Error Numbers

+ `EPERM`

  Operation not permitted.

+ `ENOENT`

  No such file or directory.

+ `EBADF`

  Bad file descriptor.

+ `EAGAIN`

  Resource unavailable, try again.

+ `ENOMEM`

  Not enough space.

+ `EEXIST`

  File exists.

+ `EBUSY`

  Device or resource busy.

+ `EINVAL`

  Invalid argument.

+ `ENOSPC`

  No space left on device.

+ `ERANGE`

  Result too large.

+ `ENAMETOOLONG`

  File name too long.

+ `EDEADLK`

  Resource deadlock would occur.

+ `EOVERFLOW`

  Value too large to be stored in data type.

+ `ENOSYS`

  Function not supported.

+ `EMSGSIZE`

  Message too long.

+ `ENOTSUP`

  Operation not supported.

+ `ETIMEDOUT`

  Connection timed out.
