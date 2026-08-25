---
title: xEventGroupCreate()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[事件组 API](00-Event-groups)]

[**提示：在许多情况下，“任务通知”可以提供事件组的轻量级替代方案**](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/04-As-event-group)

event_groups.h

```c
 EventGroupHandle_t xEventGroupCreate( void );
```

创建一个新的 RTOS [事件组](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups)，并返回
可以引用新创建的事件组的句柄。

要使此 RTOS API 函数可用：

1. [configSUPPORT_DYNAMIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_dynamic_allocation)
   必须在 FreeRTOSConfig.h 中设置为 1，或保留未定义状态（此时
   默认为 1）。

2. 必须将 RTOS 源文件 FreeRTOS/source/event_groups.c
   包含在构建中。

每个事件组都需要（非常）少量的 RAM 来保存
事件组的状态。如果使用 `xEventGroupCreate()` 创建事件组，
则所需的 RAM 将从 [FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)自动分配。
如果使用 [xEventGroupCreateStatic](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/02-xEventGroupCreateStatic)() 创建事件组
则 RAM 由应用程序编写器提供，这需要用到一个附加参数，
但允许在编译时静态分配 RAM
。有关详细信息，请参阅[静态分配与动态分配](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)页面。

事件组存储在 `EventBits_t` 类型的变量中。如果
[configUSE_16_BIT_TICKS](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_16_bit_ticks) 设置为 1，则事件组内实现的位数（或标志数）为 8；
如果 `configUSE_16_BIT_TICKS` 设置为 0，则事件组内实现的位数（或标志数）为 24。
对 `configUSE_16_BIT_TICKS` 的依赖
取决于 RTOS 任务内部实现中用于线程本地存储的数据类型。


**参数：**

*无*


**返回：**

- 如果创建了事件组，则返回事件组的句柄。
- 如果没有足够的 [FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)来创建事件组，则返回 NULL。


**用法示例：**

```c
    /* Declare a variable to hold the created event group. */
    EventGroupHandle_t xCreatedEventGroup;

    /* Attempt to create the event group. */
    xCreatedEventGroup = xEventGroupCreate();

    /* Was the event group created successfully? */
    if( xCreatedEventGroup == NULL )
    {
        /* The event group was not created because there was insufficient
           FreeRTOS heap available. */
    }
    else
    {
        /* The event group was created. */
    }
```
