---
title: xEventGroupClearBits()
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
EventBits_t xEventGroupClearBits(
                                  EventGroupHandle_t xEventGroup,
                                  const EventBits_t uxBitsToClear );
```

清除 RTOS [ 事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)中的位（标志）。无法从中断调用此函数
。有关可从中断调用的版本，请参阅 [xEventGroupClearBitsFromISR()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/08-xEventGroupClearBitsFromISR)
。

必须将 RTOS 源文件 FreeRTOS/source/event_groups.c
包含在构建中，`xEventGroupClearBits()` 函数才可用。


**参数：**

- *xEventGroup*

  要在其中清除位的事件组。必须事先通过调用
  [xEventGroupCreate()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate) 创建事件组。

- *uxBitsToClear*

  指定要在事件组中清除的一个或多个位的按位值。例如，将 `uxBitsToClear` 设置为 0x08，可清除第 3 位。
  将 `uxBitsToClear` 设置为 0x09，可清除第 3 位和第 0 位。


**返回：**

- 清除指定位**之前**的事件组的值。


**用法示例：**

```c
#define BIT_0	( 1 << 0 )
#define BIT_4	( 1 << 4 )

void aFunction( EventGroupHandle_t xEventGroup )
{
    EventBits_t uxBits;

    /* Clear bit 0 and bit 4 in xEventGroup. */
    uxBits = xEventGroupClearBits(
                                   xEventGroup,  /* The event group being updated. */
                                   BIT_0 | BIT_4 ); /* The bits being cleared. */

    if( ( uxBits & ( BIT_0 | BIT_4 ) ) == ( BIT_0 | BIT_4 ) )
    {
        /* Both bit 0 and bit 4 were set before xEventGroupClearBits()
           was called. Both will now be clear (not set). */
    }
    else if( ( uxBits & BIT_0 ) != 0 )
    {
        /* Bit 0 was set before xEventGroupClearBits() was called. It will
           now be clear. */
    }
    else if( ( uxBits & BIT_4 ) != 0 )
    {
        /* Bit 4 was set before xEventGroupClearBits() was called. It will
           now be clear. */
    }
    else
    {
        /* Neither bit 0 nor bit 4 were set in the first place. */
    }
}
```
