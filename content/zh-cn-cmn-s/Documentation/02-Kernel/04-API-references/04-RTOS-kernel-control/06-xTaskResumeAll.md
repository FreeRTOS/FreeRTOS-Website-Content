---
title: xTaskResumeAll
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
BaseType_t xTaskResumeAll( void );
```

恢复通过调用 vTaskSuspendAll() 挂起的调度器。

xTaskResumeAll() 仅恢复调度器，不会恢复
之前通过调用 vTaskSuspend() 而挂起的任务。

**返回：**

如果恢复调度器导致了上下文切换，则返回 pdTRUE，否则返回 pdFALSE。


**用法示例：**

```c
 void vTask1( void * pvParameters )
 {
     for( ;; )
     {
         /* Task code goes here. */

         /* ... */

         /* At some point the task wants to perform a long operation
            during which it does not want to get swapped out. It cannot
            use taskENTER_CRITICAL()/taskEXIT_CRITICAL() as the length
            of the operation may cause interrupts to be missed -
            including the ticks.

            Prevent the RTOS kernel swapping out the task. */
         vTaskSuspendAll();

         /* Perform the operation here. There is no need to use critical
            sections as we have all the microcontroller processing time.
            During this time interrupts will still operate and the real
            time RTOS kernel tick count will be maintained. */

         /* ... */

         /* The operation is complete. Restart the RTOS kernel. We want to force
            a context switch - but there is no point if resuming the scheduler
            caused a context switch already. */
         if( !xTaskResumeAll () )
         {
              taskYIELD ();
         }
     }
 }
```
