---
title: "RTOS Context Switch - Step 1"
created: 2018-09-20
categories:
  - kernel
description: FreeRTOS kernel detailed description
relatedLinks:
  - title: Download FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FreeRTOS reference manual
    link: /Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book/
---

[[Detailed Example](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

## Prior to the RTOS tick interrupt

This example starts with TaskA executing. TaskB has previously been suspended so its context has already
been stored on the TaskB stack.

TaskA has the context demonstrated by the diagram below.

![AtoB1.gif](/media/2018/AtoB1.gif)

The (A) label within each register shows that the register contains the correct value for the context of task A.

Next: [RTOS Implementation - Detailed Example Step 2](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/03-Step-2)
