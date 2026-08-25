---
title: pcTimerGetName
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[定时器 API](/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions/)]

timers.h

```c
 const char * pcTimerGetName( TimerHandle_t xTimer );
```

返回[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)的人类可读文本名称。

文本名称是使用 `pcTimerName` 参数分配给定时器的 
（该参数在创建定时器时调用 [xTimerCreate()](/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate/)）。


**参数：** 

- *xTimer*

  被查询的定时器。

**返回：**

- 指向定时器文本名称的指针，该指针为以 NULL 结尾的标准 C 字符串。


**用法示例：**

```c
const char *pcTimerName = "ExampleTimer";

/* A function that creates a timer. */
static void prvCreateTimer( void )
{
TimerHandle_t xTimer;

    /* Create a timer. */
    xTimer = xTimerCreate( pcTimerName,           /* Text name. */
                           pdMS_TO_TICKS( 500 ),  /* Period. */
                           pdTRUE,                /* Autoreload. */
                           NULL,                  /* No ID. */
                           prvExampleCallback );  /* Callback function. */

    if( xTimer != NULL )
    {
        xTimerStart( xTimer, portMAX_DELAY );

        /* Just to demonstrate pcTimerGetName(), query the timer's name and
           assert if it does not equal pcTimerName. */
        configASSERT( strcmp( pcTimerGetName( xTimer ), pcTimerName ) == 0 );
    }
}
```
