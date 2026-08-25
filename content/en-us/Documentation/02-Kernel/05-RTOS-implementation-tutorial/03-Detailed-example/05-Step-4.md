---
title: "RTOS Context Switch - Step 4"
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

## Incrementing the Tick Count

The RTOS function vTaskIncrementTick() executes after the TaskA context has been saved. For the purposes of this example
assume that incrementing the tick count has caused TaskB to become ready to run. TaskB has a higher priority than TaskA
so vTaskSwitchContext() selects TaskB as the task to be given processing time when the ISR completes.

Next: [RTOS Implementation - Detailed Example Step 5](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/06-Step-5)
