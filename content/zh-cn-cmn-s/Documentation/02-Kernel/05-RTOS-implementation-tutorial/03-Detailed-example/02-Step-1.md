---
title: RTOS上下文切换 - 步骤 1
created: 2018-09-20
categories:
- 内核
description: FreeRTOS 内核详细描述
relatedLinks:
- title: 免费下载RTOS
  link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
- title: FreeRTOS 参考手册
  link: /Documentation/02-Kernel/06-Books-and-mannual/01-RTOS_book/
---

[[详细示例](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

## 在 RTOS 滴答中断前

此示例从执行 TaskA 开始。TaskB 之前已被挂起，
因此其上下文已存储在 TaskB 堆栈中。

TaskA 拥有下图所示的上下文。

![AtoB1.gif](/media/2018/AtoB1.gif)

每个寄存器中的 (A) 标签都表明此寄存器包含 TaskA 上下文的正确值。

下一节：[RTOS 实现 - 详细示例步骤 2](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/03-Step-2)
