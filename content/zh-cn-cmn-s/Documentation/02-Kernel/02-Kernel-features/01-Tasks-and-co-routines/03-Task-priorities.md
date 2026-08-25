---
title: "任务"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 任务状态的概念
relatedLinks:
  - title: API 引用——任务创建
    link: /Documentation/02-Kernel/04-API-references/01-Task-creation/00-TaskHandle/
  - title: API 引用——任务控制
    link: /Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control/
  - title: API 引用——任务实用程序
    link: /Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/
---

[[有关任务的更多信息……](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/00-Tasks-and-co-routines/)]

[FreeRTOS 教程书籍](/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book)提供任务及其行为
的更多详细信息。


### 任务优先级

每个任务均被分配了从 0 到 ( configMAX_PRIORITIES - 1 ) 的优先级，其中 configMAX_PRIORITIES
定义为 FreeRTOSConfig.h。

如果正在使用的移植实现了使用“前导零计数”类指令的移植优化任务选择机制
（针对单一指令中的任务选择）而且 configUSE_PORT_OPTIMISED_TASK_SELECTION
在 FreeRTOSConfig.h 中设置为 1，则 configMAX_PRIORITIES 无法高于 32。在其他所有情况下，
configMAX_PRIORITIES 可以取任何合理数值——但为了保证 RAM 的使用效率，应取
实际需要的最小值。

优先级数字小表示任务优先级低。[空闲任务](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/15-Idle-task)的优先级为零 (tskIDLE_PRIORITY)。

FreeRTOS 调度器可确保在就绪或运行[状态](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states)下的任务始终
比同样处于就绪状态下的更低优先级任务先获得处理器  (CPU) 时间。
换句话来说，处于运行状态的任务始终是能够运行的最高优先级任务。

处于相同优先级的任务数量不限。如果 configUSE_TIME_SLICING 未经定义，或者如果
configUSE_TIME_SLICING 设置为 1，则具有相同优先级的若干就绪状态任务将
通过时间切片轮询调度方案共享可用的处理时间。
