---
title: vEventGroupDelete()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[事件组 API](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups)]

event_groups.h

```c
 void vEventGroupDelete( EventGroupHandle_t xEventGroup );
```

删除先前的[事件组](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups)，
该事件组通过调用 [xEventGroupCreate()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate)创建。

在被删除的事件组上阻塞的任务将被取消阻塞，并且
报告事件组值为 0。

必须将 RTOS 源文件 FreeRTOS/source/event_groups.c
包含在构建中，vEventGroupDelete() 函数才可用。

无法从中断调用此函数。


**参数：**

- *xEventGroup*

  要删除的事件组。


**返回：**

*无。*
