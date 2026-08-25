---
title: "taskENTER_CRITICAL_FROM_ISR(), taskEXIT_CRITICAL_FROM_ISR()"
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

UBaseType_t taskENTER_CRITICAL_FROM_ISR( void );
void taskEXIT_CRITICAL_FROM_ISR( UBaseType_t uxSavedInterruptStatus );
```

可用于中断服务程序 (ISR) 的 [taskENTER_CRITICAL() and taskEXIT_CRITICAL()](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/01-taskENTER_CRITICAL_taskEXIT_CRITICAL) 版本
。

在 ISR 中，通过调用 taskENTER_CRITICAL_FROM_ISR() 进入临界区，
然后通过调用 taskEXIT_CRITICAL_FROM_ISR() 退出。

taskENTER_CRITICAL_FROM_ISR() 和 taskEXIT_CRITICAL_FROM_ISR() 宏提供了
一种基本的临界区实现，工作原理是通过简单地禁用中断，
可以是全局禁用，也可以是禁用到特定的中断优先级。

如果使用的 FreeRTOS 移植支持中断嵌套，则调用
taskENTER_CRITICAL_FROM_ISR() 将禁用优先级等于或低于
由 [configMAX_SYSCALL_INTERRUPT_PRIORITY](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)
（或 configMAX_API_CALL_INTERRUPT_PRIORITY）内核配置常量设置的优先级的中断，
同时启用所有其他高于此优先级的中断。
如果使用的 FreeRTOS 移植不支持中断嵌套，则
taskENTER_CRITICAL_FROM_ISR() 和 taskEXIT_CRITICAL_FROM_ISR() 将不起作用。

taskENTER_CRITICAL_FROM_ISR() 和 taskEXIT_CRITICAL_FROM_ISR() 的调用
采用嵌套结构，但这些宏的使用方式的语义不同于
taskENTER_CRITICAL() 和 taskEXIT_CRITICAL()
等效宏。

临界区必须尽量简短，否则会对本来可以嵌套的
高优先级中断的响应时间产生不利影响。
每次调用 taskENTER_CRITICAL_FROM_ISR() 时，
都必须有对应的 taskEXIT_CRITICAL_FROM_ISR() 调用。

不得从临界区调用 FreeRTOS API 函数。


**参数：**


+ *uxSavedInterruptStatus*

  taskEXIT_CRITICAL_FROM_ISR() 将 uxSavedInterruptStatus 作为唯一参数。作为 uxSavedInterruptStatus 参数的值
  必须是与之匹配的
  taskENTER_CRITICAL_FROM_ISR() 调用返回的值。

  taskENTER_CRITICAL_FROM_ISR() 不接受任何参数。


**返回：**

 taskENTER_CRITICAL_FROM_ISR() 返回调用宏之前的中断掩码状态
 。taskENTER_CRITICAL_FROM_ISR() 返回的值
 必须作为 uxSavedInterruptStatus 参数用于匹配的
 taskEXIT_CRITICAL_FROM_ISR() 调用。

 taskEXIT_CRITICAL_FROM_ISR() 不返回任何值。


**用法示例：**

```c
/* A function called from an ISR. */
void vDemoFunction( void )
{
UBaseType_t uxSavedInterruptStatus;

    /* Enter the critical section. In this example, this function is itself called from
       within a critical section, so entering this critical section will result in a nesting
       depth of 2. Save the value returned by taskENTER_CRITICAL_FROM_ISR() into a local
       stack variable so it can be passed into taskEXIT_CRITICAL_FROM_ISR(). */
    uxSavedInterruptStatus = taskENTER_CRITICAL_FROM_ISR();

    /* Perform the action that is being protected by the critical section here. */

    /* Exit the critical section. In this example, this function is itself called from a
       critical section, so interrupts will have already been disabled before a value was
       stored in uxSavedInterruptStatus, and therefore passing uxSavedInterruptStatus into
       taskEXIT_CRITICAL_FROM_ISR() will not result in interrupts being re-enabled. */
    taskEXIT_CRITICAL_FROM_ISR( uxSavedInterruptStatus );
}

/* A task that calls vDemoFunction() from within an interrupt service routine. */
void vDemoISR( void )
{
UBaseType_t uxSavedInterruptStatus;

    /* Call taskENTER_CRITICAL_FROM_ISR() to create a critical section, saving the
       returned value into a local stack variable. */
    uxSavedInterruptStatus = taskENTER_CRITICAL_FROM_ISR();


    /* Execute the code that requires the critical section here. */


    /* Calls to taskENTER_CRITICAL_FROM_ISR() can be nested so it is safe to call a
       function that includes its own calls to taskENTER_CRITICAL_FROM_ISR() and
       taskEXIT_CRITICAL_FROM_ISR(). */
    vDemoFunction();

    /* The operation that required the critical section is complete so exit the
       critical section. Assuming interrupts were enabled on entry to this ISR, the value
       saved in uxSavedInterruptStatus will result in interrupts being re-enabled.*/
    taskEXIT_CRITICAL_FROM_ISR( uxSavedInterruptStatus );
}
```
