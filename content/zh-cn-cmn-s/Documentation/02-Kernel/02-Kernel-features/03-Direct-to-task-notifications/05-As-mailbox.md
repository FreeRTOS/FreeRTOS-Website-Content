---
title: "RTOS 任务通知"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 队列
relatedLinks:
  - title: API 引用——信号量与互斥锁
    link: /Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores/
  - title: RTOS 任务通知
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications/
  - title: 用作二进制信号量
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/02-As-binary-semaphore/
  - title: 用作轻量级计数信号量
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/03-As-counting-semaphore/
  - title: 用作轻量级事件组
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/04-As-event-group/
---

用作轻量级邮箱

RTOS 任务通知可用于向任务发送数据，
但相比使用 RTOS 队列实现有一些限制，因为：

1. 只能发送 32 位值
2. 该值保存为接收任务的[通知值](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)，然后
   在任何时间只能有一个通知值

因此，使用 “轻量级邮箱” 这个短语代替 “轻量级队列”。
任务的通知值就是邮箱值。

使用 [xTaskNotify()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify)（或 xTaskNotifyIndexed()）
和 [xTaskNotifyFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/07-xTaskNotifyFromISR)（或 xTaskNotifyIndexedFromISR ()）API
函数将数据发给任务，其中函数的 eAction 参数设置为 eSetValueWithOverwrite 或
eSetValueWithoutOrwrite。如果 eAction 设置为 eSetValueWithOverwrite，
则即使接收任务已有挂起的通知，
也会更新接收任务的通知值。如果 eAction 设置为 eSetValueWithoutOverwrite，
则只有在接收任务没有挂起通知时才会更新接收任务的通知值，
因为更新通知值会在
接收任务处理之前覆盖以前的值。

任务可以使用 [xTaskNotifyWait()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/08-xTaskNotifyWait)
（或 xTaskNotifyWaitIndexed()）读取自己的通知值。

有关示例，请参阅相关 API 函数的文档。
