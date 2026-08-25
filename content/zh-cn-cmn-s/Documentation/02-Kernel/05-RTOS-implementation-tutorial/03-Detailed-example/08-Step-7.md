---
title: RTOS上下文切换 - 步骤 7
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

## RTOS 滴答

从 vPortYieldFromTick() 退出，返回到 SIG_OUTPUT_COMPARE1A()，其中最后一条指令返回自 interrupt (RETI)。
RETI 指令假设，堆栈上的下一个值是中断发生时存放在其上的返回地址。

![AtoB6.gif](/media/2018/AtoB6.gif)

发生 RTOS 滴答中断时，AVR 自动将 TaskA 返回地址存放在堆栈上，也即
**taskA** 中要执行的下一条指令的地址。RTOS 滴答处理程序更改了堆栈指针，因此该指针现在指向 **TaskB**
堆栈。因此，通过 RETI 指令从堆栈弹出的返回地址实际上是 **TaskB**
在挂起前即将执行的指令的地址。

RTOS 滴答中断发生，中断了 **taskA**，但正在返回 **tasKB** - 上下文切换完成！
