---
title: xTaskAbortDelay()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[任务控制 ](/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]

task. h

```c
BaseType_t xTaskAbortDelay( TaskHandle_t xTask );
```

强制任务离开[阻塞状态](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states)，并
进入“准备就绪”状态，即使任务在阻塞状态下等待的事件没有发生，
并且任何指定的超时没有过期。

INCLUDE_xTaskAbortDelay 必须定义为 1，此函数才可用。有关详细信息，请参阅 
[RTOS 配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization)文档。


**参数：** 

+ *xTask* 

  将被强制退出阻塞状态的任务的句柄。 

  要获取任务句柄，请使用 [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) 创建任务并使用 pxCreatedTask 参数， 
  或使用 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) 创建任务并存储返回值， 
  或在 [xTaskGetHandle()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgethandle) 的调用中使用任务名称。


**返回：** 

如果 xTask 引用的任务不在“阻塞”状态，则返回 pdFAIL。否则返回 pdPASS。

