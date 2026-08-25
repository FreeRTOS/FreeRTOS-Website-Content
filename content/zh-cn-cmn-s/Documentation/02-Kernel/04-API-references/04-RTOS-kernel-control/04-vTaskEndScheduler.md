---
title: vTaskEndScheduler
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[RTOS 内核控制](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control)]

task. h 

```c
void vTaskEndScheduler( void );
```

注意：此函数目前仅在 x86 实模式 PC 端口中实现。

停止 RTOS 内核滴答。所有已创建的任务将自动删除，多任务处理 
（无论是抢占式还是协作式）亦将停止。执行将从调用 `vTaskStartScheduler()` 的位置恢复， 
就像 `vTaskStartScheduler()` 刚刚返回一样。

有关使用 `vTaskEndScheduler()` 的示例，请参阅 demo/PC 目录中的演示应用程序文件 main.c。

`vTaskEndScheduler()` 要求在可移植层中定义退出函数（请参阅针对 PC 端口的 port. c 中的 `vPortEndScheduler()`） 
。该函数执行硬件特定的操作，例如停止 RTOS 内核滴答。

`vTaskEndScheduler()` 会释放所有由 RTOS 内核分配的资源，但不会 
释放由应用程序任务分配的资源。


**用法示例：** 

```c
void vTaskCode( void * pvParameters )
{
    for( ;; )
    {
        // Task code goes here.

        // At some point we want to end the real time kernel processing 
        // so call ...
        vTaskEndScheduler ();
    }
}

void vAFunction( void )
{
    // Create at least one task before starting the RTOS kernel.
    xTaskCreate( vTaskCode, "NAME", STACK_SIZE, NULL, tskIDLE_PRIORITY, NULL );

    // Start the real time kernel with preemption.
    vTaskStartScheduler();

    // Will only get here when the vTaskCode () task has called 
    // vTaskEndScheduler (). When we get here we are back to single task 
    // execution.
}
```
