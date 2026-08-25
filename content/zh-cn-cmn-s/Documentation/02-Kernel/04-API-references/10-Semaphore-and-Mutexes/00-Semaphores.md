---
title: 信号量
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---



**提示**：[在许多情况下，“任务通知”](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)可以提供信号量的轻量级替代方案


## 模块

* [xSemaphoreCreateBinary](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/01-xSemaphoreCreateBinary)
* [xSemaphoreCreateBinaryStatic](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/02-xSemaphoreCreateBinaryStatic)
* [vSemaphoreCreateBinary](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/03-vSemaphoreCreateBinary) [使用 [用于新设计的 xSemaphoreCreateBinary()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/01-xSemaphoreCreateBinary)]
* [xSemaphoreCreateCounting](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/04-xSemaphoreCreateCounting/)
* [xSemaphoreCreateCountingStatic](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/05-xSemaphoreCreateCountingStatic)
* [xSemaphoreCreateMutex](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/06-xSemaphoreCreateMutex/)
* [xSemaphoreCreateMutexStatic](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/07-xSemaphoreCreateMutexStatic)
* [xSemaphoreCreateRecursiveMutex](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/08-xSemaphoreCreateRecursiveMutex)
* [xSemaphoreCreateRecursiveMutexStatic](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/09-xSemaphoreCreateRecursiveMutexStatic)
* [vSemaphoreDelete](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/18-vSemaphoreDelete/)
* [xSemaphoreGetMutexHolder](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/10-xSemaphoreGetMutexHolder)
* [xSemaphoreTake](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake)
* [xSemaphoreTakeFromISR](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/13-xSemaphoreTakeFromISR)
* [xSemaphoreTakeRecursive](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/14-xSemaphoreTakeRecursive)
* [xSemaphoreGive](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/15-xSemaphoreGive)
* [xSemaphoreGiveRecursive](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/16-xSemaphoreGiveRecursive)
* [xSemaphoreGiveFromISR](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR)
* [uxSemaphoreGetCount](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/11-uxSemaphoreGetCount)
