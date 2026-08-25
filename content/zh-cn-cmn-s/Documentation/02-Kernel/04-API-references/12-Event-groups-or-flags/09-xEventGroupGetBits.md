---
title: xEventGroupGetBits()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[事件组 API](00-Event-groups)]

event_groups.h

```c
EventBits_t xEventGroupGetBits( EventGroupHandle_t xEventGroup );
```

返回 RTOS [ 事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)中事件位（事件标志）的当前值。
不能从中断使用此函数。请参阅 [xEventGroupGetBitsFromISR()](10-xEventGroupGetBitsFromISR)
了解可在中断中使用的版本。

必须将 RTOS 源文件 FreeRTOS/source/event_groups.c
包含在构建中，`xEventGroupGetBits()` 函数才可用。


**参数：**

- *xEventGroup*

  正在查询的事件组。必须事先通过调用
  [xEventGroupCreate()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate) 创建事件组。


**返回：**

- 调用 `xEventGroupGetBits()` 时事件组中事件位的值。
