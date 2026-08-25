---
title: 内核控制
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## 模块

* [taskYIELD](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control/#taskyield)
* [taskENTER_CRITICAL](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/01-taskENTER_CRITICAL_taskEXIT_CRITICAL/)
* [taskEXIT_CRITICAL](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/01-taskENTER_CRITICAL_taskEXIT_CRITICAL/)
* [taskENTER_CRITICAL_FROM_ISR](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/02-taskENTER_CRITICAL_FROM_ISR_taskEXIT_CRITICAL_FROM_ISR/)
* [taskEXIT_CRITICAL_FROM_ISR](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/02-taskENTER_CRITICAL_FROM_ISR_taskEXIT_CRITICAL_FROM_ISR/)
* [taskDISABLE_INTERRUPTS](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control/#taskdisable_interrupts)
* [taskENABLE_INTERRUPTS](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control/#taskenable_interrupts)
* [vTaskStartScheduler](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/03-vTaskStartScheduler)
* [vTaskEndScheduler](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/04-vTaskEndScheduler)
* [vTaskSuspendAll](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/05-vTaskSuspendAll)
* [xTaskResumeAll](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/06-xTaskResumeAll)
* [vTaskStepTick](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/07-vTaskStepTick)

---

## 详细描述


### taskYIELD

task. h

taskYIELD() 用于请求切换上下文到另一个任务。但是，如果没有其他任务的优先级高于或等于 
调用 taskYIELD () 的任务，则 RTOS 调度器将只 
选择调用 taskYIELD() 的任务，使其再次运行。

如果 [configUSE_PREEMPTION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_preemption) 
设置为 1，则 RTOS 调度器将始终运行能够运行的最高优先级任务， 
因此调用 taskYIELD() 始终不会切换到更高优先级的任务。

---

### taskDISABLE_INTERRUPTS()

task. h

如果使用的移植支持 [configMAX_SYSCALL_INTERRUPT_PRIORITY](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)（
或 configMAX_API_CALL_INTERRUPT_PRIORITY）常量，那么 taskDISABLE_INTERRUPTS 将
禁用所有中断，或在 configMAX_SYSCALL_INTRUPT_PROJECT 设置之前屏蔽（禁用）中断。
为在用移植检查 taskDISABLE_INTERRUPTS 的实现。

如果使用的移植不支持 configMAX_SYSCALL_INTERRUPT_PRIORITY 常量，
那么 taskDISABLE_INTERRUPTS() 将对所有可屏蔽的中断进行全局禁用。

通常情况下不会直接调用该宏， 
而应使用 [taskENTER_CRITICAL() and taskEXIT_CRITICAL()](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/01-taskENTER_CRITICAL_taskEXIT_CRITICAL/) 
。

---

### taskENABLE_INTERRUPTS()

task. h

启用微控制器中断的宏。

通常情况下不会直接调用该宏， 
而应使用 [taskENTER_CRITICAL() and taskEXIT_CRITICAL()](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/01-taskENTER_CRITICAL_taskEXIT_CRITICAL/) 
。

---
