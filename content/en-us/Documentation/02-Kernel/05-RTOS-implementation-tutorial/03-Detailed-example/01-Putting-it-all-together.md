---
title: "Putting It All Together"
created: 2018-09-20
categories:
  - kernel
description: How to put the building blocks together.
relatedLinks:
  - title: Download FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FreeRTOS reference manual
    link: /Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book/
---

[[Detailed Example](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

The final part of section 2 shows how these building blocks and source code modules are used to achieve an RTOS context
switch on the AVR microcontroller. The example demonstrates in seven steps the process of switching from a lower priority
task, called TaskA, to a higher priority task, called TaskB. The source code is compatible with the WinAVR C development tools.

Next: [RTOS Implementation - Detailed Example Step 1](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/02-Step-1)
