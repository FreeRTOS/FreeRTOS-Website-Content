---
title: xEventGroupWaitBits()
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
EventBits_t xEventGroupWaitBits(
                      const EventGroupHandle_t xEventGroup,
                      const EventBits_t uxBitsToWaitFor,
                      const BaseType_t xClearOnExit,
                      const BaseType_t xWaitForAllBits,
                      TickType_t xTicksToWait );
```

读取 RTOS [ 事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)中的位，选择性地进入“阻塞”状态（已设置
超时值）以等待设置单个位或一组位。

无法从中断调用此函数。

必须将 RTOS 源文件 FreeRTOS/source/event_groups.c
包含在构建中，`xEventGroupWaitBits()` 函数才可用。


**参数：**

- *xEventGroup*

  正在测试位的事件组。必须事先通过调用
  [xEventGroupCreate()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate) 创建事件组。

- *uxBitsToWaitFor*

  指定要在事件组中测试的一个或多个位的按位值。例如，要等待
  第 0 位和/或第 2 位，将 `uxBitsToWaitFor` 设置为 0x05 即可。要等待第 0 位和/或第 1 位和/或第 2 位，
  将 `uxBitsToWaitFor` 设置为 0x07 即可。`uxBitsToWaitFor` **不得** 设置为 0。

- *xClearOnExit*

  如果 `xClearOnExit` 设置为 `pdTRUE`，那么在发生以下情况之前，作为 `uxBitsToWaitFor` 参数传递的值中设置的任何位
  都将在 `xEventGroupWaitBits()` 返回之前在事件组中清除：`xEventGroupWaitBits()`
  因超时以外的任何原因返回。超时值由 `xTicksToWait` 参数设置。
  如果 `xClearOnExit` 设置为 `pdFALSE`，
  那么当调用 `xEventGroupWaitBits()` 返回时，事件组中设置的位不会改变。

- *xWaitForAllBits*

  `xWaitForAllBits` 用于创建逻辑 AND 测试（必须设置所有位）
  或逻辑 OR 测试（必须设置一个或多个位），如下所示：

  如果 `xWaitForAllBits` 设置为 `pdTRUE`，那么 `xEventGroupWaitBits()` 在以下条件下将返回：****
  作为 `uxBitsToWaitFor` 参数传递的值中的所有位在事件组中被设置
  或指定的阻塞时间到期。

  如果 `xWaitForAllBits` 设置为 `pdFALSE` ，那么 `xEventGroupWaitBits()` 在以下条件下将返回： ****
  作为 `uxBitsToWaitFor` 参数传递的值中的任何位在事件组中被设置
  或指定的阻塞时间到期。

- *xTicksToWait*

  等待以下情况发生的最长时间（以“滴答”为单位，取决于 `xWaitForAllBits` 值）：
  `uxBitsToWaitFor` 指定的一个/所有位被设置。


**返回：**

- 事件位等待完成设置或阻塞时间过期时
  的事件组值。在以下情况下，
  事件组中事件位的当前值将与返回值不同：
  高优先级任务或中断在调用任务解除“阻塞”状态和退出
  `xEventGroupWaitBits()` 函数之间更改了事件位的值
  。

  测试返回值以确定
  哪些位已完成设置。如果 `xEventGroupWaitBits()` 因为超时过期而返回，
  则并非在等待的所有位都会进行设置。如果
  `xEventGroupWaitBits()` 返回因为其等待的位被设置而返回，
  则返回值是由于任何位因为
  `xClearOnExit` 参数被设置为 `pdTRUE` 而自动清除之前的事件组值。


**用法示例：**

```c
#define BIT_0	( 1 << 0 )
#define BIT_4	( 1 << 4 )

void aFunction( EventGroupHandle_t xEventGroup )
{
    EventBits_t uxBits;
    const TickType_t xTicksToWait = 100 / portTICK_PERIOD_MS;

    /* Wait a maximum of 100ms for either bit 0 or bit 4 to be set within
       the event group. Clear the bits before exiting. */
    uxBits = xEventGroupWaitBits(
               xEventGroup,   /* The event group being tested. */
               BIT_0 | BIT_4, /* The bits within the event group to wait for. */
               pdTRUE,        /* BIT_0 & BIT_4 should be cleared before returning. */
               pdFALSE,       /* Don't wait for both bits, either bit will do. */
               xTicksToWait );/* Wait a maximum of 100ms for either bit to be set. */

    if( ( uxBits & ( BIT_0 | BIT_4 ) ) == ( BIT_0 | BIT_4 ) )
    {
        /* xEventGroupWaitBits() returned because both bits were set. */
    }
    else if( ( uxBits & BIT_0 ) != 0 )
    {
        /* xEventGroupWaitBits() returned because just BIT_0 was set. */
    }
    else if( ( uxBits & BIT_4 ) != 0 )
    {
        /* xEventGroupWaitBits() returned because just BIT_4 was set. */
    }
    else
    {
        /* xEventGroupWaitBits() returned because xTicksToWait ticks passed
           without either BIT_0 or BIT_4 becoming set. */
    }
}
```
