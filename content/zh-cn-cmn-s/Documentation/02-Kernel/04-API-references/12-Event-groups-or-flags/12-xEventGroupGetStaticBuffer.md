---
title: xEventGroupGetStaticBuffer()
created: 2023-07-19 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[事件组 API](index)]

event_groups.h

```c
 BaseType_t xEventGroupGetStaticBuffer( EventGroupHandle_t xEventGroup,
                                        StaticEventGroup_t ** ppxEventGroupBuffer );
```

必须将 configSUPPORT_STATIC_ALLOCATION 定义为 1，此函数才可用。请参阅 
[RTOS 配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization)文档， 
了解更多信息。

检索指向静态创建的事件组数据结构体缓冲区的指针。该缓冲区 
与创建时提供的缓冲区相同。

**参数：**

+ `xEventGroup`     

  将检索其缓冲区的事件组。

+ `ppxEventGroupBuffer`     

  用于返回指向事件组的数据结构体缓冲区的指针。


**返回：**

+ 如果检索到缓冲区，则返回 pdTRUE， 
+ 否则返回 pdFALSE。 


