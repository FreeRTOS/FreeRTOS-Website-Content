---
title: xEventGroupSync()
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
EventBits_t xEventGroupSync( EventGroupHandle_t xEventGroup,
                             const EventBits_t uxBitsToSet,
                             const EventBits_t uxBitsToWaitFor,
                             TickType_t xTicksToWait );
```

以原子方式设置 RTOS [事件组](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups)中的位（标志），然后等待
在同一事件组中设置位的组合。此功能通常
用于同步多个任务（通常称为任务集合），其中每个
任务必须等待其他任务到达同步点后才能继续。

不能从中断使用此函数。

如果设置了
`uxBitsToWait` 参数指定的位，或者在该时间内设置了这些位，则该函数将在其阻塞时间到期之前返回。这种情况下，
`uxBitsToWait` 指定的所有位将在
函数返回之前自动清除。

必须将 RTOS 源文件 FreeRTOS/source/event_groups.c
包含在构建中，`xEventGroupSync()` 函数才可用。


**参数：**

- *xEventGroup*

  设置和测试位的事件组。必须事先通过调用
  [xEventGroupCreate()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate) 创建事件组。

- *uxBitsToSet*

  在确定
  `uxBitsToWait` 参数指定的所有位是否都已设置（可能还要等待）之前，要在事件组中设置的一个或多个位。例如，将 `uxBitsToSet` 设置为 0x04，
  即可设置事件组内的第 2 位。

- *uxBitsToWaitFor*

  指定要在事件组中测试的一个或多个位的按位值。例如，将 `uxBitsToWaitFor`
  设置为 0x05，即可等待第 0 位和第 2 位。将 `uxBitsToWaitFor` 设置为 0x07，即可等待第 0 位、第 1 位和第 2 位等。

- *xTicksToWait*

  等待 `uxBitsToWaitFor` 参数值指定的所有位被设置的最长时间（以滴答为单位）
  。


**返回：**

- 等待置位时或阻塞到期时
  事件组的值。测试返回值
  哪些位已完成设置。

  如果 `xEventGroupSync()` 因为超时过期而返回，
  则并非在等待的所有位都会进行设置。

  如果 `xEventGroupSync()` 因其所等待的所有位都被设置而返回，
  那么返回值是自动清除任何位**之前**的
  事件组值。


**用法示例：**

```c
/* Bits used by the three tasks. */
#define TASK_0_BIT        ( 1 << 0 )
#define TASK_1_BIT        ( 1 << 1 )
#define TASK_2_BIT        ( 1 << 2 )

#define ALL_SYNC_BITS ( TASK_0_BIT | TASK_1_BIT | TASK_2_BIT )

/* Use an event group to synchronise three tasks. It is assumed this event
   group has already been created elsewhere. */
EventGroupHandle_t xEventBits;

void vTask0( void *pvParameters )
{
    EventBits_t uxReturn;
    TickType_t xTicksToWait = 100 / portTICK_PERIOD_MS;

    for( ;; )
    {
        /* Perform task functionality here. */
        **. . .**

        /* Set bit 0 in the event group to note this task has reached the
           sync point. The other two tasks will set the other two bits defined
           by ALL_SYNC_BITS. All three tasks have reached the synchronisation
           point when all the ALL_SYNC_BITS are set. Wait a maximum of 100ms
           for this to happen. */
        uxReturn = xEventGroupSync( xEventBits,
                                    TASK_0_BIT,
                                    ALL_SYNC_BITS,
                                    xTicksToWait );

        if( ( uxReturn & ALL_SYNC_BITS ) == ALL_SYNC_BITS )
        {
            /* All three tasks reached the synchronisation point before the call
               to xEventGroupSync() timed out. */
        }
    }
}

void vTask1( void *pvParameters )
{
    for( ;; )
    {
        /* Perform task functionality here. */
        **. . .**

        /* Set bit 1 in the event group to note this task has reached the
           synchronisation point. The other two tasks will set the other two
           bits defined by ALL_SYNC_BITS. All three tasks have reached the
           synchronisation point when all the ALL_SYNC_BITS are set. Wait
           indefinitely for this to happen. */
        xEventGroupSync( xEventBits, TASK_1_BIT, ALL_SYNC_BITS, portMAX_DELAY );

        /* xEventGroupSync() was called with an indefinite block time, so
           this task will only reach here if the syncrhonisation was made by all
           three tasks, so there is no need to test the return value. */
    }
}

void vTask2( void *pvParameters )
{
    for( ;; )
    {
        /* Perform task functionality here. */
        **. . .**

        /* Set bit 2 in the event group to note this task has reached the
           synchronisation point. The other two tasks will set the other two
           bits defined by ALL_SYNC_BITS. All three tasks have reached the
           synchronisation point when all the ALL_SYNC_BITS are set. Wait
           indefinitely for this to happen. */
        xEventGroupSync( xEventBits, TASK_2_BIT, ALL_SYNC_BITS, portMAX_DELAY );

        /* xEventGroupSync() was called with an indefinite block time, so
           this task will only reach here if the syncrhonisation was made by all
           three tasks, so there is no need to test the return value. */
    }
}
```
