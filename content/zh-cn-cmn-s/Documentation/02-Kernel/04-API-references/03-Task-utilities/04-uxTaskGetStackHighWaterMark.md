---
title: uxTaskGetStackHighWaterMark, uxTaskGetStackHighWaterMark2
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[任务控制 ](/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]

task. h

```c
UBaseType_t uxTaskGetStackHighWaterMark
 ( TaskHandle_t xTask );

configSTACK_DEPTH_TYPE uxTaskGetStackHighWaterMark2
 ( TaskHandle_t xTask );
```

`INCLUDE_uxTaskGetStackHighWaterMark` 必须定义为 1，`uxTaskGetStackHighWaterMark` 函数 
才可用，`INCLUDE_uxTaskGetStackHighWaterMark2` 必须定义为 1，`uxTaskGetStackHighWaterMark2` 
函数才可用。更多信息，请参阅 [RTOS 配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization)文档。

`uxTaskGetStackHighWaterMark2()` 是 `uxTaskGetStackHighWaterMark()` 的一个版本，
后者返回用户可定义的类型，以删除 8 位架构上 `UBaseType_t` 类型的数据类型宽度限制。

随着任务的执行和中断的处理，任务使用的堆栈会增加和缩小。 `uxTaskGetStackHighWaterMark()` 
返回任务开始执行后任务可用的最小剩余堆栈空间量—— 
即任务堆栈达到最大（最深）值时未使用的堆栈量。这就是 
所谓的堆栈“高水位线”。


**参数：**

- *xTask*

  正在查询的任务的句柄。任务可以通过传递 NULL 作为 xTask 参数来查询自己的高水位标记。 


**返回：**

返回的值是以字为单位的高水位标记（例如，在 32 位计算机上， 
返回值为 1 表示有 4 个字节的堆栈未使用）。如果返回值为零， 
则任务可能已溢出堆栈。如果返回值接近于零，则任务已接近堆栈溢出 
。


**用法示例：** 

```c
    void vTask1( void * pvParameters )
    {
        UBaseType_t uxHighWaterMark;

        /* Inspect our own high water mark on entering the task. */
        uxHighWaterMark = uxTaskGetStackHighWaterMark( NULL );

        for( ;; )
        {
            /* Call any function. */
            vTaskDelay( 1000 );

            /* Calling the function will have used some stack space, we would 
               therefore now expect uxTaskGetStackHighWaterMark() to return a 
               value lower than when it was called on entering the task. */
            uxHighWaterMark = uxTaskGetStackHighWaterMark( NULL );
        }
    }
```
   
