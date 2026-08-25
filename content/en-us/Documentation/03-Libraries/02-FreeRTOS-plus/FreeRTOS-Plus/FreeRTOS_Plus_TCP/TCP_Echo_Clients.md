---
title: A TCP Echo Client Example (using a single RTOS task)
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
mainCREATE\_TCP\_ECHO\_TASKS\_SINGLE to 1 at the top of
the project's main.c source file to include the example in the
build.

The example creates two RTOS tasks that send TCP echo requests to an
external [echo server](https://en.wikipedia.org/wiki/Echo_Protocol)
using the standard echo port (port 7), then wait to receive the echo
reply within the same RTOS task. A [separate TCP echo example](TCP_Echo_Clients_Separate)
uses the same TCP socket from two different RTOS tasks - one RTOS task sends
the echo request and another RTOS tasks receives the echo reply.


The IP address of the echo server must be configured using the
configECHO\_SERVER\_ADDR0 to configECHO\_SERVER\_ADDR3 constants in FreeRTOSConfig.h,
and the echo server must (stating the obvious) be enabled and not blocked by a
firewall. [Windows ships with an echo server](https://technet.microsoft.com/library/cc740058(v=ws.10).aspx)
but it is not enabled by default. [Third party echo servers](http://bansky.net/echotool/)
are also available.
