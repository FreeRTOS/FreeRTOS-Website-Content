---
title: 整合所有部分
created: 2018-09-20
categories:
- 内核
description: 如何整合所有构建块。
relatedLinks:
- title: 免费下载RTOS
  link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
- title: FreeRTOS 参考手册
  link: /Documentation/02-Kernel/06-Books-and-mannual/01-RTOS_book/
---

[[详细示例](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

第 2 节的最后部分展示了如何使用这些构建块和源代码模块来实现 AVR 微控制器上的 RTOS 上下文切换
。该示例以七个步骤演示了
从名为 TaskA 的低优先级任务切换到名为 TaskB 的高优先级任务的过程。源代码与 WinAVR C 开发工具兼容。

下一节：[RTOS 实现 - 详细示例步骤 1](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/02-Step-1)
