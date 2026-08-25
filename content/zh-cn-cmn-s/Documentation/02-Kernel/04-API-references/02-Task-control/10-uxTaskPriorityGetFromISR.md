---
title: uxTaskPriorityGetFromISR()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[任务控制 ](/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]


task.h

```c
UBaseType_t uxTaskPriorityGetFromISR( const TaskHandle_t xTask );
```

`INCLUDE_uxTaskPriorityGet` 必须定义为 1，才可使用此函数。请参阅 
[RTOS 配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 文档 
了解更多信息。

获取任何任务的优先级。在中断服务程序 (ISR) 中使用此函数是安全的。


**参数：**

+ `xTask`   

  待查询的任务句柄。传递 NULL 句柄会导致返回调用任务的优先级。


**返回：**

+ `xTask` 的优先级。 

