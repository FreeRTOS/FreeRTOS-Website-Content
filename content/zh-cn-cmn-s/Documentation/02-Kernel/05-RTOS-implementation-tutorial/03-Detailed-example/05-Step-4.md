---
title: RTOS上下文切换 - 步骤 4
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

## 滴答计数递增

RTOS 函数 vTaskIncrementTick() 在 TaskA 上下文保存后执行。本示例中，
假设滴答计数递增已经导致 TaskB 运行就绪。TaskB 的优先级高于 TaskA，
因此 vTaskSwitchContext() 选择 TaskB 作为 ISR 完成时要给予处理时间的任务。

下一节：[RTOS 实现 - 详细示例步骤 5](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/06-Step-5)
