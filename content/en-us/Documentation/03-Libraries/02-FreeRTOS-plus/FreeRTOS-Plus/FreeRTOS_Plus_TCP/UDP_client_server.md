---
title: Simple UDP Client and Server Examples
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
mainCREATE\_SIMPLE\_UDP\_CLIENT\_SERVER\_TASKS to 1 at the top of
the project's main.c source file to include the example in the build.

The example creates two UDP client RTOS tasks and two UDP server RTOS
tasks. The clients communicate with the servers. One set of RTOS tasks
use the standard sockets interface, and the other RTOS tasks use the
zero copy sockets interface.

These RTOS tasks are self checking and will trigger a [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert) failure if
they detect a difference in the data that is received from that which was sent.
As these RTOS tasks use UDP, which can legitimately loose packets, they can cause
configASSERT() failures if they are executed in a less than perfect networking
environment.
