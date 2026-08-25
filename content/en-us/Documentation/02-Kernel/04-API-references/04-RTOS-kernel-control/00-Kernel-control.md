---
title: Kernel Control
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## Modules

* [taskYIELD](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control/#taskyield)
* [taskENTER\_CRITICAL](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/01-taskENTER_CRITICAL_taskEXIT_CRITICAL/)
* [taskEXIT\_CRITICAL](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/01-taskENTER_CRITICAL_taskEXIT_CRITICAL/)
* [taskENTER\_CRITICAL\_FROM\_ISR](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/02-taskENTER_CRITICAL_FROM_ISR_taskEXIT_CRITICAL_FROM_ISR/)
* [taskEXIT\_CRITICAL\_FROM\_ISR](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/02-taskENTER_CRITICAL_FROM_ISR_taskEXIT_CRITICAL_FROM_ISR/)
* [taskDISABLE\_INTERRUPTS](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control/#taskdisable_interrupts)
* [taskENABLE\_INTERRUPTS](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control/#taskenable_interrupts)
* [vTaskStartScheduler](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/03-vTaskStartScheduler)
* [vTaskEndScheduler](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/04-vTaskEndScheduler)
* [vTaskSuspendAll](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/05-vTaskSuspendAll)
* [xTaskResumeAll](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/06-xTaskResumeAll)
* [vTaskStepTick](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/07-vTaskStepTick)

---

## Detailed Description


### taskYIELD

task.h

taskYIELD() is used to request a context switch to another task. However, if there are no other tasks 
at a higher or equal priority to the task that calls taskYIELD() then the RTOS scheduler will simply 
select the task that called taskYIELD() to run again.

If [configUSE\_PREEMPTION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_preemption) 
is set to 1 then the RTOS scheduler will always be running the highest priority task that is able to 
run, so calling taskYIELD() will never result in a switch to a higher priority task.

---

### taskDISABLE\_INTERRUPTS()

task.h

If the port in use supports the [configMAX\_SYSCALL\_INTERRUPT\_PRIORITY](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) (or
configMAX\_API\_CALL\_INTERRUPT\_PRIORITY) constant, then taskDISABLE\_INTERRUPTS will either
disable all interrupts, or mask (disable) interrupts up to the configMAX\_SYSCALL\_INTERRUPT\_PRIORITY setting.
Check the implementation of taskDISABLE\_INTERRUPTS for the port in use.

If the port in use does not support the configMAX\_SYSCALL\_INTERRUPT\_PRIORITY constant
then taskDISABLE\_INTERRUPTS() will globally disable all maskable interrupts.

Normally this macro would not be called directly 
and [taskENTER\_CRITICAL() and taskEXIT\_CRITICAL()](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/01-taskENTER_CRITICAL_taskEXIT_CRITICAL/) should 
be used in its place.

---

### taskENABLE\_INTERRUPTS()

task.h

Macro to enable microcontroller interrupts.

Normally this macro would not be called directly 
and [taskENTER\_CRITICAL() and taskEXIT\_CRITICAL()](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/01-taskENTER_CRITICAL_taskEXIT_CRITICAL/) should 
be used in its place.

---
