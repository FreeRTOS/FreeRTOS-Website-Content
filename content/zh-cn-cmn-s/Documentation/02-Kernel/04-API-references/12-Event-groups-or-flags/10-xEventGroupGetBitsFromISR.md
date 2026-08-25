---
title: xEventGroupGetBitsFromISR()
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
EventBits_t xEventGroupGetBitsFromISR(
                              EventGroupHandle_t xEventGroup );
```

可从中断调用的 [xEventGroupGetBits()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/09-xEventGroupGetBits) 版本。

必须将 RTOS 源文件 FreeRTOS/source/event_groups.c
包含在构建中，`xEventGroupGetBitsFrom()` 函数才可用。


**参数：**

- *xEventGroup*

  正在查询的事件组。必须事先通过调用
  [xEventGroupCreate()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate) 创建事件组。


**返回：**

- 调用 `xEventGroupGetBitsFromISR()` 时
  事件组中事件位的值。
