---
title: "RTOS 滴答"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 内核构建块
relatedLinks:
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FreeRTOS 参考手册
    link: /Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book/
---

[[RTOS 实现构建块](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/01-Building-blocks)]

休眠时，RTOS 任务将指定需要“唤醒”的时间。
阻塞时，RTOS 任务可以指定希望等待的最长时间。
FreeRTOS 实时内核通过**滴答**计数变量测量时间。定时器中断
（ RTOS **滴答中断**）以严格的时间精度增加滴答数，
因此实时内核可以测量时间，达到所选定时器中断频率的分辨率。

每次滴答数增加时，实时内核必须检查现在是否为解除阻塞或唤醒任务的时间。
在滴答 ISR 期间唤醒或解除阻塞的任务的优先级
可能高于被中断任务的优先级。在这种情况下，滴答 ISR 应该返回到新唤醒/未阻塞任务——有效地中断了一个任务，
但返回到另一个任务。如下图所示：

![TickISR.gif](/media/2018/TickISR.gif)

请参阅上图中的数字：

- 在 (1) 处，RTOS 空闲任务正在执行。
- 在 (2) 处，RTOS 滴答发生，控制权转移到滴答 ISR (3)。
- RTOS 滴答 ISR 使 vControlTask 准备就绪，并且由于 vControlTask 的优先级高于 RTOS 空闲任务，
  因此将上下文切换到 vControlTask 的上下文。
- 由于执行上下文现在是 vControlTask 的上下文，退出 ISR (4) 会将控制权返回给 vControlTask，
  后者开始执行 (5)。

以这种方式发生的上下文切换称为**抢占式**，因为中断的任务被抢占，
而不是主动挂起。

FreeRTOS 的 AVR 移植使用定时器 1 上的比较匹配事件来生成 RTOS 滴答。
以下页面介绍了如何使用 WinAVR 开发工具实现 RTOS 滴答 ISR。

下一节：[RTOS 实现 - GCC Signal 属性](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/05-GCC-signal-attribute)
