---
title: "RTOS 上下文切换 - 第 6 步"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 内核详细描述
relatedLinks:
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FreeRTOS 参考手册
    link: /Documentation/02-Kernel/06-Books-and-mannual/01-RTOS_book/
---

[[详细示例](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

## 恢复 TaskB 上下文

![AtoB5.gif](/media/2018/AtoB5.gif)

portRESTORE_CONTEXT() 通过将 TaskB 的上下文从其堆栈中恢复到相应的处理器寄存器中来完成其操作。

只有程序计数器仍保留在堆栈上。

下一篇：[RTOS 实现 - 详细示例第 7 步](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/08-Step-7)
