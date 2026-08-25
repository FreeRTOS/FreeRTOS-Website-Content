---
title: "FreeRTOS 计数信号量"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 计数信号量
relatedLinks:
  - title: API 引用——信号量
    link: /Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores/
---

[另请参阅[阻塞多个 RTOS 对象](/Documentation/02-Kernel/04-API-references/07-Queue-sets/00-RTOS-queue-sets)]

[FreeRTOS 教程书籍](/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book)
提供更多信息，包括队列、二进制信号量、互斥锁、计数信号量、
递归信号量，以及包含在配套的示例项目中的简单示例。

### FreeRTOS 计数信号量

[**提示：在许多情况下， “任务通知”可以提供计数信号量的轻量级替代方案**](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/03-As-counting-semaphore)

正如二进制信号量可以被认为是长度为 1 的队列那样，
计数信号量也可以被认为是长度大于 1 的队列。同样，信号量的使用者对存储在队列中的数据并不感兴趣，
他们只关心队列是否为空。

计数信号量通常用于两种情况：

1. 盘点事件。

   在此使用场景中，事件处理程序将在每次事件发生时“提供”信号量（递增信号量计数值），
   而处理程序任务将在每次处理事件时“获取”信号量
   （递减信号量计数值）。因此，计数值是
   已发生的事件数与已处理的事件数之间的差值。在这种情况下，
   创建信号量时希望计数值为零。

1. 资源管理。

   在此使用情景中，计数值表示可用资源的数量。为了获得
   对资源的控制，任务必须首先获得信号量——递减信号量计数值。当计数值达到零时，
   表示没有空闲资源可用。当任务结束使用资源时，
   它会“返还”一个信号量——同时递增信号量计数值。在这种情况下，
   创建信号量时希望计数值等于最大计数值。

信号量相关 API 函数的列表，请参阅用户文档的[信号量/互斥锁](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)章节
。请搜索 FreeRTOS/Demo/Common/Minimal 目录下的文件，您将会看到它们的多个用法示例。
请注意，中断只能使用以 "FromISR" 结尾的 API 函数。
