---
title: uxTaskBasePriorityGet()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[任务控制](/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]

task. h

```c
UBaseType_t uxTaskBasePriorityGet( const TaskHandle_t xTask );
```

`INCLUDE_uxTaskPriorityGet` 和 `configUSE_MUTEXES` 必须定义为 1，才可使用此函数。请参阅 
[RTOS 配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization)文档， 
了解更多信息。

获取任意任务的基础优先级。任务的基础优先级是任务当前优先级被继承后 
将返回的优先级，旨在避免在获取互斥锁时 
出现无限制的优先级反转。 


**参数：**

+ `xTask`

  待查询任务的句柄。传递 NULL 句柄会返回调用任务的基础优先级。


**返回：**

+ `xTask` 的基础优先级。
