---
title: vSemaphoreDelete
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[信号量](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)]

[**提示：在许多使用场景中，使用直达任务通知要比使用二进制信号量的速度更快，内存效率更高。**](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/02-As-binary-semaphore)


semphr.h

```c
void vSemaphoreDelete( SemaphoreHandle_t xSemaphore );
```

删除信号量，包括互斥锁型信号量和递归信号量。

请勿删除已有阻塞任务的信号量（正在
等待信号灯可用的阻塞状态任务)。

**参数：**

- *xSemaphore*

  被删除的信号量的句柄。
