---
title: FreeRTOS-Plus-POSIX fcntl.h Implementation
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
    POSIX fcntl.h - File Control Options
```


## SYNOPSIS

```c
    #include "FreeRTOS_POSIX/fcntl.h"
```


## DESCRIPTION

### Symbolic Constants -- File Creation Flags

Symbolic constants as file creation flags for use in the oflag value to open() and openat().


+ `O_CLOEXEC`

  Close the file descriptor upon exec().

+ `O_CREAT`

  Create file if it does not exist.

+ `O_DIRECTORY`

  Fail if file is a non-directory file.

+ `O_EXCL/code>`

  Exclusive use flag.

+ `O_NOCTTY`

  Do not assign controlling terminal.

+ `O_NOFOLLOW`

  Do not follow symbolic links.

+ `O_TRUNC`

  Truncate flag.

+ `O_TTY_INIT`

  termios structure provides conforming behavior.


### Symbolic Constants -- File status flags

Symbolic constants for use as file status flags for open(), openat(), and fcntl().

todo -- O\_DSYNC and O\_SYNC are both 0x0200. Open Group does not require each to be different. However,
those functionally should be different http://man7.org/linux/man-pages/man2/open.2.html. Open Group also
does not require these to be "bitwise-distinct". What is our design of file system?

+ `O_APPEND`

  Set append mode.

+ `O_DSYNC`

  Write according to synchronized I/O data integrity completion.

+ `O_NONBLOCK`

  Non-blocking mode.

+ `O_RSYNC`

  Synchronized read I/O operations.

+ `O_SYNC`

  Write according to synchronized I/O file integrity completion.


### Symbolic Constants -- Mask for File Access Modes

+ `O_ACCMODE`

  Mask for file access modes.


### Symbolic Constants -- File Access Modes

+ `O_EXEC`

  Open for execute only (non-directory files).

+ `O_RDONLY`

  Open for reading only.

+ `O_RDWR`

  Open for reading and writing.

+ `O_SEARCH`

  Open directory for search only.

+ `O_WRONLY`

  Open for writing only.
