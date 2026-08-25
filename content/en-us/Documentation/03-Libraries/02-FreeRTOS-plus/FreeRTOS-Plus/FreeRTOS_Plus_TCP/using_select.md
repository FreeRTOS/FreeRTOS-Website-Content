---
title: "Example that Uses FreeRTOS_select()"
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
mainCREATE\_SELECT\_UDP\_SERVER\_TASKS to 1 at the top of
the project's main.c source file to include the example in the
build.

The example creates two RTOS tasks that demonstrate how to use [FreeRTOS\_select()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/14-select).
One RTOS task creates numerous sockets which are added to a set using [FreeRTOS\_FD\_SET()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/16-FD_SET),
while the other RTOS task sends data to a random socket within that set
for the first RTOS task to receive and verify.

These RTOS tasks are self checking and will trigger a [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)
failure if they detect a difference in the data that is received from
that which was sent. As these RTOS tasks use UDP, which can legitimately loose
packets, they can cause configASSERT() failures if they are executed
in a less than perfect networking environment.
