---
title: "滴答分辨率"
created: 2025-01-07 00:00:00.0 UTC
categories:
  - 内核
description: 节能状态简介
relatedLinks:
  - title: 构建块
    link: /Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/01-Building-blocks
  - title: RTOS 滴答
    link: /Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/03-The-RTOS-tick
---

## 滴答的分辨率

如 [RTOS 滴答文档页面](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/03-The-RTOS-tick)所述， 
RTOS 时间基于周期性的滴答中断。当 RTOS 任务希望等待特定时间过去（例如通过调用 [vTaskDelay()](/Documentation/02-Kernel/04-API-references/02-Task-control/01-vTaskDelay)）或者等待某个事件发生时（例如通过调用 
[xQueueReceive()](/Documentation/02-Kernel/04-API-references/06-Queues/09-xQueueReceive) 指定阻塞时间）， 
任务会指定最大阻塞（即[在不使用任何 CPU 周期的情况下等待](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states)）时间作为滴答计数。宏 pdMS_TO_TICKS() 将 
毫秒转换为滴答。请求的阻塞时间始于调用 API 的时间，介于两个滴答中断之间。滴答计数是 
一个整数，不计入部分滴答周期，因此从调用 API 到下一个滴答中断之间的时间计为 
延迟（阻塞）周期的第一个滴答。这将导致请求相同阻塞时间的不同 API 调用之间观察到的阻塞时间（挂钟时间）略有不同 
。

下列几张图以调用 vTaskDelay( 2 ) 为例加以演示，假设一个滴答周期为 1 毫秒。

第一张图显示滴答中断后立即调用 vTaskDelay() 的情况。观察到的阻塞时间将近 2 毫秒 
（即滴答 1 和滴答 2 之间的大部分时间，加上滴答 2 和滴答 3 之间的所有时间）。

[![](/media/2023/tick-diagram1.png)](/media/2023/tick-diagram1.png)

第二张图显示滴答中断马上发生之前调用 vTaskDelay() 的情况。观察到的阻塞时间 
刚刚超过 1 毫秒（即滴答 1 和滴答 2 之间的一小段时间，加上滴答 2 和滴答 3 之间的所有时间）。

[![](/media/2023/tick-diagram2.png)](/media/2023/tick-diagram2.png)

通过这些示例，我们可以看出，指定了 N 个滴答延迟时的实际延迟时间将始终介于 `(N-1 ticks * tick_period)` 
和 `(N * tick_period)` 之间。在这个特定示例中，这意味着延迟总时间介于 1.0000000001 毫秒和 1.99999999999 毫秒之间。

关于延迟时间的几个重要注意事项：
-  滴答分辨率始终取决于作为参数指定的滴答计数，但不会少于 `(N-1)` 个滴答。基本上其范围是 `N-1` 个滴答到 `N` 个滴答（不包括）。
-  为了保证最小延迟时间为 N，您需要延迟 `(N / (tick_period)) + 1` 个滴答。
-  延迟的持续周期（时间）依据的是调用延迟时 RTOS 个滴答之间的点——调用距离下一个滴答越近，延迟的时间就越短。