---
title: A UDP Echo Client Example
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[FreeRTOS-Plus-TCP and FreeRTOS-Plus-FAT Examples](TCP_FAT_demo_projects#Free_TCPIP_FAT_examples)


Not all demo projects will include this example. If this example is
included in a demo project then it may be necessary to set
mainCREATE\_UDP\_ECHO\_TASKS to 1 at the top of
the project's main.c source file to include the example in the
build.

The example creates two RTOS tasks that send UDP echo requests to an external
[echo server](https://en.wikipedia.org/wiki/Echo_Protocol)
using the standard echo port (port 7). One RTOS task uses
the standard socket interface, the other RTOS task uses the zero copy
socket interface.

The IP address of the echo server must be configured using the
configECHO\_SERVER\_ADDR0 to configECHO\_SERVER\_ADDR3 constants in FreeRTOSConfig.h,
and the echo server must (stating the obvious) be enabled and not blocked by a
firewall. [Windows ships with an echo server](https://technet.microsoft.com/library/cc740058(v=ws.10).aspx)
but it is not enabled by default. [Third party echo servers](http://bansky.net/echotool/)
are also available.

These RTOS tasks are self checking and will trigger a [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)
failure if they detect a difference in the data that is received from that which was sent.
As these RTOS tasks use UDP, which can legitimately loose packets, they can cause
configASSERT() failures when they are executed in a less than perfect networking
environment.
 
