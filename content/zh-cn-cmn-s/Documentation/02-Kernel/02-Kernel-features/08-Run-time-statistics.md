---
title: "运行时间统计"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 节能状态简介
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS 初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---

*点击放大*
[\![](/media/2018/rtos-run-time-stats.jpg)](/media/2018/rtos-run-time-stats.jpg)


### 描述

FreeRTOS 可以选择性收集关于每个任务所用处理时间量的信息。
然后可以用 [vTaskGetRunTimeStats()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#vtaskgetruntimestats) API 函数以表格形式显示此信息，
如右图所示。

每个任务有两个值：

1. Abs 时间（绝对时间）

    指实际执行任务所耗费的总时间，即任务处于
    “正在运行”状态的总时间。由用户为其应用程序选择合适的时间基数。

2. % 时间（时间百分比）

    实质上，这里显示的是相同的信息，只不过是以占总处理时间的百分比形式显示，
    而不是绝对时间。


### 配置和使用

需要三个宏。这些宏可以在 FreeRTOSConfig.h 中定义。

1. configGENERATE_RUN_TIME_STATS

    通过将 configGENERATE_RUN_TIME_STATS 定义为 1，启用收集运行时统计信息。
    一旦完成此设置，还必须定义另外两个宏，以确保能成功
    编译。

2. portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()

    运行时统计信息的时间基数需要比 tick 中断具有更高的分辨率——
    否则统计信息可能会不准确，无法真正发挥作用。建议将
    此时间基数设置为比 tick 中断快 10 到 100 倍。时间基数越快，
    统计数据就越准确——但定时器值也会越早溢出。

    如果将 configGENERATE_RUN_TIME_STATS 定义为 1，那么 RTOS 内核会
    在启动时自动调用 portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()
    （从 vTaskStartScheduler() API 中进行调用）。应用程序设计人员希望
    使用宏来配置合适的时间基数。下面举例说明。
3. portGET_RUN_TIME_COUNTER_VALUE()

    此宏应只返回当前的时间，正如 portCONFIGURE_TIMER_FOR_RUN_TIME_STATS() 所配置的那样。
    下面提供了一些示例。

[vTaskGetRunTimeStats()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#vtaskgetruntimestats) API 函数用于检索收集的统计数据。
