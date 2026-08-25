---
title: "FreeRTOS 直达任务通知"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 任务通知
relatedLinks:
  - title: API 引用 — RTOS 任务通知
    link: /Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/00-RTOS-task-notifications/
  - title: 用作二进制信号量
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/02-As-binary-semaphore/
  - title: 用作轻量级计数信号量
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/03-As-counting-semaphore/
  - title: 用作轻量级事件组
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/04-As-event-group/
  - title: 用作邮箱
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/05-As-mailbox/
---

[**从 FreeRTOS V8.2.0 开始可用 <br /> <br />  自 V10.4.0 起支持单任务多条通知**](/Documentation/04-Roadmap-and-release-note/02-Release-notes/01-FreeRTOS-V8)

### 描述

[另请参阅博客文章[“通过 FreeRTOS 通知减少 RAM 占用空间并加速执行”](/Community/Blogs/2020/decrease-ram-footprint-and-accelerate-execution-with-freertos-notifications)]

每个 RTOS 任务都有一个_任务通知_数组。每个任务__
都有“挂起”或“非挂起”的通知状态和一个 32 位的_通知值_。常量
[configTASK_NOTIFICATION_ARRAY_ENTRIES](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configtask_notification_array_entries) 设置
任务通知数组中的索引数量。在 FreeRTOS V10.4.0 版本前，任务只有单条任务通知，
而无通知数组。

_直达任务通知_是直接发送到任务的事件，而不是通过中间对象
（如队列、事件组或信号量）间接发送至任务的事件。向任务发送“直达任务通知”
会将目标任务通知设为“挂起”状态。正如任务可以阻塞中间对象
（如等待信号量可用的信号量），任务也可以阻塞任务通知，
以等待通知状态变为“挂起”。

向任务发送“直达任务通知”也可以
[使用下列任一方法更新目标通知的值（可选）](#用例)：

- 覆盖原值，无论接收任务是否读取被覆盖的值。
- 覆盖原值，但前提是接收任务已读取被覆盖的值。
- 在值中设置一个或多个位。
- 对值进行增量（添加 1）。

调用 [xTaskNotifyWait()/xTaskNotifyWaitIndexed()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/08-xTaskNotifyWait) 读取通知值
会将该通知的状态清除为“非挂起”。此外，也可以通过调用
[xTaskNotifyStateClear()/xTaskNotifyStateClearIndexed()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/09-xTaskNotifyStateClear) 将通知状态明确设置为“未挂起”。

**注意：**数组中的每条通知均独立运行
——任务一次只能阻塞数组中的一个通知，
并且不会被发送到任何其他数组索引的通知解除阻塞。

默认情况下，RTOS 任务通知功能处于启用状态，并且可以
通过将 [configUSE_TASK_NOTIFICATIONS](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_task_notifications)
在 [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 中设置为 0 从构建中排除（每个任务每个数组索引节省 8 个字节）。

**重要提示：**FreeRTOS [流和消息缓冲区 ](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers) 在数值索引为 0 时使用任务通知。
如需在调用流或消息缓冲区 API 函数时保持任务通知的状态，
请使用数组索引大于 0 的任务通知。

### 性能优势和使用限制

任务通知具有高度灵活性，
使得它们可以在
必须要创建单独[队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)、[二进制信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)、[计数信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/03-Counting-semaphores/)
或[事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)的情况下进行使用。与通过诸如二进制信号量等中间对象来解除任务阻塞状态相比，通过直接通知解除 RTOS 任务阻塞状态的速度快 **45%**，
**使用的 RAM** 也更少。不过
这些性能优势也有一些意料之内的使用限制：

1. RTOS 任务通知仅可在只有一个任务
   可以接收事件时使用。不过，这个条件在
   大多数真实世界情况下是满足的。比如，中断解除了一个任务的阻塞状态，该任务
   将处理由中断接收的数据。

2. 仅可在使用 RTOS 任务通知代替
   队列的情况下：当某个接收任务可在阻塞状态下等待通知
   （因而不花费任何 CPU 时间）时，发送任务不能
   在阻塞状态下等待发送完成（在发送不能立刻完成的情况下）
   。

### 用例

通知使用 [xTaskNotifyIndexed()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify)
和 [xTaskNotifyGiveIndexed()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/01-xTaskNotifyGive) API 函数（及其
[中断安全等效物](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/00-RTOS-task-notifications)）进行发送，
并保持挂起，直到接收到 RTOS 任务调用
由 [xTaskNotifyWaitIndexed()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/08-xTaskNotifyWait)
或 [ulTaskNotifyTakeIndexed()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/03-ulTaskNotifyTake) API 函数。

每个上述 API 函数都有一个无 "Indexed"
前缀的等效物。非“索引”版本始终在数组索引为 0 的任务通知上进行操作。
例如，xTaskNotifyGive( TargetTask ) 等同于
xTaskNotifyGiveIndexed( TargetTask, 0 )，两者都在任务索引 0 处
对由以 TargetTask 为句柄的任务所引用的任务进行增量。

#### 示例

- [使用 RTOS 任务通知作为轻量级二进制信号量](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/02-As-binary-semaphore)
- [使用 RTOS 任务通知作为轻量级计数信号量](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/03-As-counting-semaphore)
- [使用 RTOS 任务通知作为轻量级事件组](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/04-As-event-group)
- [使用 RTOS 任务通知作为轻量级邮箱](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/05-As-mailbox)

---

†_使用 
FreeRTOS V8.1.2 中的二进制信号量实现进行测量，使用 GCC 在 -O2 优化下编译，并且没有定义 
configASSERT()。使用 FreeRTOS V8.2.0 及更高版本中改进的
二进制信号量实现，仍然可以实现 35% 的改进。_

