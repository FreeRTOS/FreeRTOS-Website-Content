---
title: RTOS上下文切换 - 步骤 2
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

## RTOS 滴答中断发生

RTOS 滴答中断在 TaskA 即将执行 LDI 指令时发生。中断发生时，
AVR 微控制器会自动将当前程序计数器 (PC) 置于堆栈上，然后跳转到
RTOS 滴答 ISR 的开始。

![AtoB2.gif](/media/2018/AtoB2.gif)

下一节：[RTOS 实现 - 详细示例步骤 3](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/04-Step-3)
