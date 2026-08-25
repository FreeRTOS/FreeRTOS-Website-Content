---
title: FreeRTOS-Plus-POSIX Show Case with Actor Model
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-POSIX Overview](/Documentation/03-Libraries/05-FreeRTOS-labs/03-FreeRTOS-plus-POSIX/00-FreeRTOS-Plus-POSIX)]


## Overview

A common pain point for realtime application development is that learning curve for a specific platform
is often very steep for developers. While FreeRTOS has already taken care of the hardware facing interactions
for us, e.g. a FreeRTOS application could easily be ported from a supported platform to another, developers
still have to learn all FreeRTOS interfaces to start with. FreeRTOS-Plus-POSIX makes it even easier,
that an existing POSIX compliant application could be easily ported to onboard AWS IoT.

To show the concept of how porting can be easily done, this demo walks through the procedure of first
developing on a Linux box and then porting to FreeRTOS. This demo also contains a simple working implementation
of [actor model](https://en.wikipedia.org/wiki/Actor_model), which may be adopted in your application.


## What Does This Demo Do?

This demo creates two types of actors -- master and workers. Master notifies workers what to do, by
sending different types of messages. Upon receiving a message, a worker performs a predefined routine
associated to that message type. Once master finishes distributing work, master notifies workers "things
are done" and all actors terminate.

![](/media/2018/posix-demo-actor.png)

In this demo

+ An actor is really a thread, which is created with pthread\_create().

+ Messaging is done with queues, which are created with mq\_open() and messages are sent/received with
  mq\_send(), mq\_timedsend(), mq\_timedreceive().


## Writing Code on Linux, Compiling, and Running.

Just show me your code -- Download [posix\_demo.c](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Labs/main/FreeRTOS-Labs/Demo/FreeRTOS_Plus_POSIX_with_actor_Windows_Simulator/posix_demo.c)

Library dependencies

```c
/* Headers used in this demo, which are also defined in FreeRTOS-Plus-POSIX */
#include <pthread.h>
#include <mqueue.h>
#include <time.h>
#include <fcntl.h>
#include <errno.h>

/* Headers used in this demo, which are not defined by FreeRTOS-Plus-POSIX but defined by platform. */
#include <stdbool.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
```

To compile, open a command line window, and cd into the folder where you have downloaded posix\_demo.c to.

Compile with

```c
gcc -Wall posix_demo.c -lpthread -lrt -o posix_demo
```

Run with

```c
./posix_demo
```

Command line output

![](/media/2018/linux_compile_snapshot.png)


## Porting to FreeRTOS (Windows Simulator)

Just show me your code -- Clone [`aws/amazon-freertos-staging`](https://github.com/aws/amazon-freertos),
the source code for the same application is under `./demos/common/posix/aws_posix_demo.c`

Library dependencies are updated to port to FreeRTOS-Plus-POSIX

```c
/* Demo includes -- this is to run demo with aws_demo_runner.c. */
#include "aws_posix_demo.h"

/* FreeRTOS-Plus-POSIX */
#include "FreeRTOS_POSIX/pthread.h"
#include "FreeRTOS_POSIX/mqueue.h"
#include "FreeRTOS_POSIX/time.h"
#include "FreeRTOS_POSIX/fcntl.h"
#include "FreeRTOS_POSIX/errno.h"

/* FreeRTOS includes. */
#include "FreeRTOS.h"

/* System headers */
#include <stdbool.h>
```

Besides above header changes, `printf()` is also changed to `configPRINTF(()) to print to serial port.`

Though not related to porting, but two other changes are made

+ configASSERT(()) checks configuration before starting POSIX demo on Windows Simulator.
+ `int main( void )` function signature in Linux version of the demo is changed to `void vStartPOSIXDemo( void )`.
  As Windows Simulator already has a main entry point defined, which schedules demo tasks.

To compile and run

Load `aws_demos.sln` solution into Visual Studio (`aws_demos.sln` is under `./demo/pc/windows/visual_studio/`).
You may need to refer to the repo `README.md` for setting up Windows Simulator in general. Here assumes you
are already set up. `aws_demo.sln` provides various demo use cases. By default POSIX demo is not enabled.
To switch to POSIX demo, go to `aws_demo_runner.c`, and have these lines uncommented --

```c
/* some code ... */
extern void vStartMQTTEchoDemo( void );
/* some code ... */
vStartMQTTEchoDemo();
```

Then build and run as you would for the very first demo documented in `README.md`.

Command line output (This would have been serial port output, if running on a development board.)

 ![](/media/2018/windows_compile_snapshot.png)


## Summary

This demo shows how an existing POSIX compliant application can be easily ported to FreeRTOS. While
here only shows an example for doing such on Windows Simulator, porting to other platforms would be
similar. A platform might have its own implementation for a subset of POSIX interfaces. In this case,
one could selectively enable FreeRTOS-Plus-POSIX functionalities. Refer to `FreeRTOS_POSIX_portable_default.h` (for
defaults) and `FreeRTOS_POSIX_portable.h` (for overwrites) under `./lib/..` directory.
