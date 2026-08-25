---
title: "taskENTER_CRITICAL(), taskEXIT_CRITICAL()"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[RTOS 内核控制](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control)]


```c
task. h

void taskENTER_CRITICAL( void );
void taskEXIT_CRITICAL( void );
```

通过调用 taskENTER_CRITICAL() 进入临界区，随后
通过调用 taskEXIT_CRITICAL() 退出临界区。

宏 taskENTER_CRITICAL() 和 taskEXIT_CRITICAL() 提供了一个基本
临界区实现，只需禁用中断即可使其全局运作，
或在特定的中断优先级范围内运作。请参阅 [vTaskSuspendAll()](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/05-vTaskSuspendAll)
RTOS API 函数，获取有关在不禁用中断的情况下创建临界区的
信息。



如果所使用的 FreeRTOS 移植未使用
[configMAX_SYSCALL_INTERRUPT_PRIORITY](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) 内核配置常量
（也称为 configMAX_API_CALL_INTERRUPT_PRIORITY），则调用 taskENTER_CRITICAL()
会全局禁用中断。如果所使用的 FreeRTOS 移植使用了 configMAX_SYSCALL_INTERRUPT_PRIORITY
内核配置常量，则调用 taskENTER_CRITICAL()
会禁用优先级等于或低于 configMAX_SYSCALL_INTERRUPT_PRIORITY 设置的优先级的中断，
并启用所有高于此优先级的中断。

抢占式上下文切换仅在中断内发生， 在中断被禁用时不会发生。
因此，调用 taskENTER_CRITICAL() 的任务一定会保持在运行状态，
直到退出临界区，除非任务明确试图阻塞或让出
（任务不应在临界区内部进行该操作）。

taskENTER_CRITICAL() 和 taskEXIT_CRITICAL() 的调用采用嵌套结构。因此，只有在每次调用
taskENTER_CRITICAL() 后执行相应的 taskEXIT_CRITICAL() 调用时，
才会退出临界区。

临界区必须尽量简短，否则会对中断响应时间产生不利影响。
每次调用 taskENTER_CRITICAL() 时，都必须有对应的 taskEXIT_CRITICAL() 调用。

不得从临界区调用 FreeRTOS API 函数。

不得从中断服务程序 (ISR) 调用 taskENTER_CRITICAL() 和 taskEXIT_CRITICAL()，
请参阅 [taskENTER_CRITICAL_FROM_ISR()](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/02-taskENTER_CRITICAL_FROM_ISR_taskEXIT_CRITICAL_FROM_ISR) 和
taskEXIT_CRITICAL_FROM_ISR()，获取中断安全的等效函数。


**参数：**

*无*


**返回：**

*无*


**用法示例：**

```c
/* A function that makes use of a critical section. */
void vDemoFunction( void )
{
    /* Enter the critical section. In this example, this function is itself called
       from within a critical section, so entering this critical section will result
       in a nesting depth of 2. */
    taskENTER_CRITICAL();

    /* Perform the action that is being protected by the critical section here. */

    /* Exit the critical section. In this example, this function is itself called
       from a critical section, so this call to taskEXIT_CRITICAL() will decrement the
       nesting count by one, but not result in interrupts becoming enabled. */
    taskEXIT_CRITICAL();
}

/* A task that calls vDemoFunction() from within a critical section. */
void vTask1( void * pvParameters )
{
    for( ;; )
    {
        /* Perform some functionality here. */

        /* Call taskENTER_CRITICAL() to create a critical section. */
        taskENTER_CRITICAL();


        /* Execute the code that requires the critical section here. */

        /* Calls to taskENTER_CRITICAL() can be nested so it is safe to call a
           function that includes its own calls to taskENTER_CRITICAL() and
           taskEXIT_CRITICAL(). */
        vDemoFunction();

        /* The operation that required the critical section is complete so exit the
           critical section. After this call to taskEXIT_CRITICAL(), the nesting depth
           will be zero, so interrupts will have been re-enabled. */
        taskEXIT_CRITICAL();
    }
}
```
