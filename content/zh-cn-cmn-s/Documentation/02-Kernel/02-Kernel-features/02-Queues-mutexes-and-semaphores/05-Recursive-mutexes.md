---
title: "FreeRTOS 递归互斥锁"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 队列
relatedLinks:
  - title: API 引用——信号量与互斥锁
    link: /Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores/
---

[另请参阅[阻塞多个 RTOS 对象](/Documentation/02-Kernel/04-API-references/07-Queue-sets/00-RTOS-queue-sets)]


[FreeRTOS 教程书籍](/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book)提供了有关队列、
二进制信号量、互斥锁、计数信号量、递归信号量的信息，
以及一组简单工作示例的示例项目。

### FreeRTOS 递归互斥锁

用户可对一把递归互斥锁重复加锁。只有用户
为每个成功的 xSemaphoreTakeRecursive() 请求调用 xSemaphoreGiveRecursive() 后，互斥锁才会重新变为可用。例如，如果一个任务成功“加锁”相同的互斥锁 5 次，
那么任何其他任务都无法使用此互斥锁，直到任务也把这个互斥锁“解锁”5 次。

这种类型的信号量使用优先级继承机制，因此“加锁”一个信号量的任务必须在不需要此信号量时，
立即将信号量“解锁”。

不能从中断服务程序中使用类型是互斥锁的信号量。

不能从中断中使用互斥锁的原因是：

- 互斥锁使用的优先级继承机制要求
  从任务中（而不是从中断中）拿走和放入互斥锁。
- 中断无法保持阻塞来等待一个被互斥锁保护的资源
  变得可用。
