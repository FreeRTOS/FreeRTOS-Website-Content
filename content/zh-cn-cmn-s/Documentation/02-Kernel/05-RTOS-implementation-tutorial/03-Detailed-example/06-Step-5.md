---
title: RTOS上下文切换 - 步骤 5
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

## 检索到 TaskB 的堆栈指针

![AtoB4.gif](/media/2018/AtoB4.gif)

必须恢复 TaskB 上下文。RTOS 宏 portRESTORE_CONTEXT 做的第一件事就是
从 TaskB 挂起时获取的拷贝中检索 TaskB 堆栈指针。TaskB 堆栈指针被加载到处理器堆栈指针中，
因此现在 AVR 堆栈指向 TaskB 上下文的顶部。

下一节：[RTOS 实现 - 详细示例步骤 6](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/07-Step-6)
