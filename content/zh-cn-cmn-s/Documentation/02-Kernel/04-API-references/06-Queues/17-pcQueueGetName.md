---
title: pcQueueGetName
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[队列管理 ](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]


queue.h

```c
const char *pcQueueGetName( QueueHandle_t xQueue )
```

从队列的句柄中查找队列名称。

队列只有添加到[队列注册表](/Documentation/02-Kernel/04-API-references/06-Queues/15-vQueueAddToRegistry)时才有名称。


**参数：** 

+ *xQueue*  

  正在查询的队列的句柄。


**返回：** 

如果 xQueue 引用的队列在队列注册表中，
则返回队列的文本名称，否则返回 NULL。

