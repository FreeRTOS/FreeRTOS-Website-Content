---
title: FreeRTOS+POSIX
---

**NOTE**: FreeRTOS-Plus-POSIX is a [FreeRTOS Labs](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction) project provided in the hope that it is useful. It is not a complete pthreads implementation, and does not necessary meet our production code quality standard. FreeRTOS-Plus-POSIX is provided in the
[Lab-Project-FreeRTOS-POSIX](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-POSIX) repository on GitHub.

## Introduction
The Portable Operating System Interface (POSIX) is a family of standards specified by the IEEE Computer Society for maintaining compatibility between operating systems. FreeRTOS-Plus-POSIX implements a *small* subset of the [POSIX threading API](http://pubs.opengroup.org/onlinepubs/7908799/xsh/threads.html). This subset allows application developers familiar with POSIX API to develop a FreeRTOS application using POSIX like threading primitives. FreeRTOS-Plus-POSIX only implements about 20% of the POSIX API. Therefore, an existing POSIX compliant application or a POSIX compliant library cannot be ported to run on FreeRTOS Kernel using only this wrapper.

![FreeRTOS Architecture Description](/media/2019/POSIX.jpg)

**Location of FreeRTOS-Plus-POSIX when used with [FreeRTOS](/Why-FreeRTOS/FAQs/Amazon) libraries**

## Example Pre-configure Project

The FreeRTOS-Plus-POSIX pre-configured example is provided in a separate [zip file download](/media/2019/190820_FreeRTOS_plus_POSIX_demo.zip).

## Currently Supported Features

FreeRTOS-Plus-POSIX partially implements [IEEE Std 1003.1-2017 Edition The Open Group Technical Standard Base Specifications, Issue 7](http://pubs.opengroup.org/onlinepubs/9699919799/). FreeRTOS-Plus-POSIX includes implementations for the following POSIX threading header files - please refer to the [FreeRTOS-Plus-POSIX API documentation](/Documentation/03-Libraries/05-FreeRTOS-labs/03-FreeRTOS-plus-POSIX/01-API-Reference/00-API-Reference) for specifics on the features supported within each header file:

| * errno.h<br/>* fcntl.h<br/>* mqueue.h<br/>* pthread.h<br/>* sched.h<br/>* semaphore.h<br/> | * signal.h<br/>* sys/types.h<br/>* time.h<br/>* unistd.h<br/>* utils.h<br/> |
| --- | --- |

## FreeRTOS-Plus-POSIX Source Code Organisation
Porting related headers and implementation source code

```
/lib/FreeRTOS-Plus-POSIX
        |-- include
        |   |
        |   +- FreeRTOS_POSIX.h
        |   +- FreeRTOS_POSIX_internal.h
        |   +- FreeRTOS_POSIX_types.h
        |   +- portable
        |        |
        |        +- [target]
        |        |    |
        |        |    +- [development board]
        |        |            |
        |        |            +- FreeRTOS_POSIX_portable.h
        |        |
        |        +- FreeRTOS_POSIX_portable_default.h
        |
        +- source
            +- FreeRTOS_POSIX_clock.c
            +- FreeRTOS_POSIX_mqueue.c
            +- FreeRTOS_POSIX_pthread_barrier.c
            +- FreeRTOS_POSIX_pthread.c
            +- FreeRTOS_POSIX_pthread_cond.c
            +- FreeRTOS_POSIX_pthread_mutex.c
            +- FreeRTOS_POSIX_sched.c
            +- FreeRTOS_POSIX_semaphore.c
            +- FreeRTOS_POSIX_timer.c
            +- FreeRTOS_POSIX_unistd.c
            +- FreeRTOS_POSIX_utils.c
```

FreeRTOS-Plus-POSIX headers
```
	/lib/include/FreeRTOS_POSIX
                    +- errno.h
                    +- fcntl.h
                    +- mqueue.h
                    +- pthread.h
                    +- sched.h
                    +- semaphore.h
                    +- signal.h
                    +- sys
                    |    |
                    |    +- types.h
                    |
                    +- time.h
                    +- unistd.h
                    +- utils.h
```

## Dependencies

Both configUSE\_POSIX\_ERRNO and configUSE\_APPLICATION\_TASK\_TAG must be set to 1 in [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization).

## Developer References and API Documents
Please refer to the [API Reference](01-API-Reference/00-API-Reference).

## Porting
### Porting Related Header Files

| **FreeRTOS platform specific POSIX configuration** | **High Level Description** |
| --- | --- |
| include/FreeRTOS_POSIX.h | This header file brings in dependencies required by FreeRTOS-Plus-POSIX. This file must be included before all other FreeRTOS-Plus-POSIX includes. |
| include/FreeRTOS_POSIX_internal.h | FreeRTOS-Plus-POSIX internal structs and initializers. Users are not suggested to touch this file. |
| include/FreeRTOS_POSIX_portable_default.h | Defaults for FreeRTOS-Plus-POSIX port-specific configuration options. |
| include/portable/[vendor-directory]/FreeRTOS_POSIX_portable.h | Port-specific configuration overwrite of FreeRTOS-Plus-POSIX. As an example, include/portable/pc/windows/FreeRTOS_POSIX_portable.h, Windows simulator uses the defaults, thus does not need to overwrite anything. |

### FreeRTOS-Plus-POSIX Include Paths
* /lib/FreeRTOS-Plus-POSIX/include
* /lib/FreeRTOS-Plus-POSIX/source
* /lib/include/FreeRTOS_POSIX/

Note that a project only needs platform specific header from this path `/lib/FreeRTOS-Plus-POSIX/include/portable`.

## Code Size (in bytes)

| File | Optimisation off | Optimisation on |
| --- | --- | --- |
| FreeRTOS\_POSIX\_clock.c | 412 | 296 |
| FreeRTOS\_POSIX\_mqueue.c | 2016 | 1612 |
| FreeRTOS\_POSIX\_pthread\_barrier.c | 294 | 200 |
| FreeRTOS\_POSIX\_pthread.c | 980 | 660 |
| FreeRTOS\_POSIX\_pthread\_cond.c | 696 | 496 |
| FreeRTOS\_POSIX\_pthread\_mutex.c | 848 | 608 |
| FreeRTOS\_POSIX\_sched.c | 48 | 32 |
| FreeRTOS\_POSIX\_semaphore.c | 540 | 380 |
| FreeRTOS\_POSIX\_timer.c | 972 | 788 |
| FreeRTOS\_POSIX\_unistd.c | 92 | 68 |
| FreeRTOS\_POSIX\_utils.c | 1152 | 768 |
| Total | 8050 | 5908 |  |
