---
title: xEventGroupSetBits()
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
EventBits_t xEventGroupSetBits( EventGroupHandle_t xEventGroup,
                                const EventBits_t uxBitsToSet );
```

在 RTOS [事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)中设置位（标志）。该函数不能从中断中调用。
[xEventGroupSetBitsFromISR()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/06-xEventGroupSetBitsFromISR) 是可从中断调用的
版本。

在事件组中设置位将自动解除阻塞以等待位的任务。

必须将 RTOS 源文件 FreeRTOS/source/event_groups.c 包含在构建中，`xEventGroupSetBits()`
函数才可用。


**参数：**

- *xEventGroup*

  要设置位的事件组。必须事先通过调用
  [xEventGroupCreate()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate) 创建事件组。

- *uxBitsToSet*

  指定要在事件组中设置的一个或多个位的按位值。例如，将 `uxBitsToSet`
  设置为 0x08，则只设置第 3 位。将 `uxBitsToSet` 设置为 0x09，即可设置第 3 位和第 0 位。


**返回：**

- 调用 `xEventGroupSetBits()` 返回**时事件组的值**。

  有两种原因导致返回值中 `uxBitsToSet`
  参数指定的位被清除：

  1. 如果设置某位导致等待该位的任务离开阻塞状态，
     那么该位有可能已被自动清除（请参阅 `xClearBitOnExit` 参数，
     该参数属于 [xEventGroupWaitBits()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/04-xEventGroupWaitBits)）。

  2. 任何优先级高于
     调用 `xEventGroupSetBits()` 的任务的未阻塞（或其他就绪状态）任务都将执行，
     并可能在调用 `xEventGroupSetBits()` 返回之前更改事件组值。


**用法示例：**

```c
#define BIT_0	( 1 << 0 )
#define BIT_4	( 1 << 4 )

void aFunction( EventGroupHandle_t xEventGroup )
{
    EventBits_t uxBits;

    /* Set bit 0 and bit 4 in xEventGroup. */
    uxBits = xEventGroupSetBits(
                                 xEventGroup,    /* The event group being updated. */
                                 BIT_0 | BIT_4 );/* The bits being set. */

    if( ( uxBits & ( BIT_0 | BIT_4 ) ) == ( BIT_0 | BIT_4 ) )
    {
        /* Both bit 0 and bit 4 remained set when the function returned. */
    }
    else if( ( uxBits & BIT_0 ) != 0 )
    {
        /* Bit 0 remained set when the function returned, but bit 4 was
           cleared. It might be that bit 4 was cleared automatically as a
           task that was waiting for bit 4 was removed from the Blocked
           state. */
    }
    else if( ( uxBits & BIT_4 ) != 0 )
    {
        /* Bit 4 remained set when the function returned, but bit 0 was
           cleared. It might be that bit 0 was cleared automatically as a
           task that was waiting for bit 0 was removed from the Blocked
           state. */
    }
    else
    {
        /* Neither bit 0 nor bit 4 remained set. It might be that a task
           was waiting for both of the bits to be set, and the bits were cleared
           as the task left the Blocked state. */
    }
}
```
