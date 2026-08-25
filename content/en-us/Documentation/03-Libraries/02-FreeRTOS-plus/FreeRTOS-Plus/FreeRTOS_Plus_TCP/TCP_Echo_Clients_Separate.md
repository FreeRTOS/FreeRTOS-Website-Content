---
title: A TCP Echo Client Example (using a multiple RTOS tasks)
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
mainCREATE\_TCP\_ECHO\_TASKS\_SEPARATE to 1 at the top of
the project's main.c source file to include the example in the
build.

The example creates two RTOS tasks that use the same TCP socket. One
RTOS task sends TCP echo requests to an external [echo server](https://en.wikipedia.org/wiki/Echo_Protocol)
using the standard echo port (port 7), the other RTOS task listens for
the echo replies. A [separate example](TCP_Echo_Clients)
uses the same RTOS task to both send echo requests and listen for echo
replies.

The IP address of the echo server must be configured using the
configECHO\_SERVER\_ADDR0 to configECHO\_SERVER\_ADDR3 constants in FreeRTOSConfig.h,
and the echo server must (stating the obvious) be enabled and not blocked by a
firewall. [Windows ships with an echo server](https://technet.microsoft.com/library/cc740058(v=ws.10).aspx)
but it is not enabled by default. [Third party echo servers](http://bansky.net/echotool/)
are also available.
