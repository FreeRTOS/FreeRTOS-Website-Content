---
title: "RTOS Context Switch - Step 6"
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

## Restore the TaskB context

![AtoB5.gif](/media/2018/AtoB5.gif)

portRESTORE_CONTEXT() completes by restoring the TaskB context from its stack into the appropriate processor registers.

Only the program counter remains on the stack.

Next: [RTOS Implementation - Detailed Example Step 7](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/08-Step-7)
