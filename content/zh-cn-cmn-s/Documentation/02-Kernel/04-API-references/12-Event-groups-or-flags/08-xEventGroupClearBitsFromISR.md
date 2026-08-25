---
title: xEventGroupClearBitsFromISR()
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
BaseType_t xEventGroupClearBitsFromISR(
                               EventGroupHandle_t xEventGroup,
                               const EventBits_t uxBitsToClear );
```

可从中断调用的 [xEventGroupClearBits()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/07-xEventGroupClearBits) 版本。
清除操作推迟到 RTOS 守护进程任务，也称为定时器服务任务。
守护进程任务的优先级由 [configTIMER_TASK_PRIORITY](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configtimer_task_priority)
设置（在 FreeRTOSConfig.h 中）。

必须将 RTOS 源文件 FreeRTOS/source/event_groups.c
包含在构建中，`xEventGroupClearBitsFromISR()` 函数才可用。


**参数：**

- *xEventGroup*

  要在其中清除位的事件组。必须事先通过调用
  [xEventGroupCreate()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate) 创建事件组。

- *uxBitsToClear*

  指定要在事件组中清除的一个或多个位的按位值。例如，将 `uxBitsToClear` 设置为 0x08，可清除第 3 位。
  将 `uxBitsToClear` 设置为 0x09，可清除第 3 位和第 0 位。


**返回：**

- `pdPASS`如果操作已成功延迟到 RTOS 守护进程任务，则返回 pdPASS。

- 否则，返回 `pdFALSE`。只有满足以下条件，才返回 `pdFALSE`：
  [定时器命令队列](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/02-Timer-service-daemon-task)已满。


**用法示例：**

```c
#define BIT_0	( 1 << 0 )
#define BIT_4	( 1 << 4 )

/* This code assumes the event group referenced by the
   xEventGroup variable has already been created using a call to
   xEventGroupCreate(). */
void anInterruptHandler( void )
{
    BaseType_t xSuccess;

    /* Clear bit 0 and bit 4 in xEventGroup. */
    xSuccess = xEventGroupClearBitsFromISR(
                                xEventGroup, /* The event group being updated. */
                                BIT_0 | BIT_4 );/* The bits being cleared. */

    if( xSuccess == pdPASS )
    {
        /* The command was sent to the daemon task. */
    }
    else
    {
        /* The clear bits command was not sent to the daemon task. */
    }
}
```
