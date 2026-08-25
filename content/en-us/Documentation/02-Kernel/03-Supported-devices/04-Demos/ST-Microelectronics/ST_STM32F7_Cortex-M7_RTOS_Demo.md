---
title: "ST ARM Cortex-M7 STM32 F7 RTOS DemoWith projects for the IAR and ARM Keil Embedded Compilers"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[IAR](http://www.iar.com/ewarm)]
[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

### Introduction

This page provides documentation for the FreeRTOS demo that targets the
STM32756G-EVAL Evaluation Kit, which incorporates an
[STM32F7 ARM Cortex-M7 microcontroller](http://www.st.com/web/en/catalog/mmc/SC1169/SS1858)
from [STMicroelectronics](http://www.st.com/). Pre-configured build projects are provided for
both the [IAR](http://www.iar.com/ewarm)
and ARM Keil tools.

---

#### *IMPORTANT! Notes on using the STM32F7 Cortex-M7 RTOS demo*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-st-arm-cortex-m7-demo-application)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting),
noting in particular the recommendation to develop with
[configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert) defined
in FreeRTOSConfig.h.

---

### Source Code Organisation

The FreeRTOS distribution available from this site contains the source files for all the FreeRTOS
ports, and the projects for all the FreeRTOS demo applications. It therefore contains many
more files than are required to use the STM32 F7 microcontroller.
See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
section for a description of the directory structure and information on creating a
new FreeRTOS project.

The IAR Embedded Workbench for ARM workspace for the STM32F7 demo application is called
RTOSDemo.eww, and is located in the FreeRTOS/Demo/CORTEX\_M7\_STM32F7\_STM32756G-EVAL
directory.

The ARM Keil project for the STM32F7 demo application is called
RTOSDemo.uvprojx, and is located in the FreeRTOS/Demo/CORTEX\_M7\_STM32F7\_STM32756G-EVAL
directory.

---

### The ST ARM Cortex-M7 Demo Application

#### Hardware Setup

The demo uses an LED that is connected to port F pin 10 by positioning jumper
JP24 so the jumper is connecting pin 2 to pin 3.

![jumper setting to connect LED to Cortex-M7 device](/media/2018/STM32F7_Cortex_M7_Jumper_Setting.png)

**JP24 is used to connect pin F10 to the LED**

#### Functionality

The STM32 F7 demo application can be built to create either a simple blinky demo,
or a comprehensive test and demo application. The constant
mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY, which is defined at the top of main.c, is used
to switch between the two.

#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 1

To build the simple blinky demo set mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to 1, which
results in main() calling main\_blinky(). main\_blinky() creates a simple demo as follows:
* **The main\_blinky() Function:**
main\_blinky() creates two tasks and one queue before starting the RTOS
 scheduler.
* **The Queue Send Task:**

 The queue send task is implemented by prvQueueSendTask() in main\_blinky.c.
 It writes to the queue every 200 milliseconds.
* **The Queue Receive Task:**

 The queue receive task is implemented by prvQueueReceiveTask()
 in main\_blinky.c. It blocks on queue reads to wait for messages from
 the queue send task - toggling an LED each time a message is received.
 As the queue send task writes to the queue every 200 milliseconds the
 queue receive task receives a message and toggles the LED every 200
 milliseconds.

#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 0

To build the comprehensive test and demo set mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY
to 0, which results in main() calling main\_full(). The comprehensive test and
demo application demonstrates:

* [Task notifications](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
* [Event groups](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)
* [Software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)
* [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)
* [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)
* [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)

Most of the created tasks are from the set of [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
tasks, which have no specific purpose other than to demonstrate how to use the
FreeRTOS API, and to test the RTOS port.

A 'check' task is also created which periodically inspects the standard
demo tasks to ensure they are executing as expected. The check task also toggles
an LED. **The LED will toggle every 3 seconds if the check task has determined
the demo is executing as expected, and every 200ms if the check task has detected
a potential error in any of the standard demo tasks**.

#### Building and executing the demo application - IAR

1. Open FreeRTOS/Demo/CORTEX\_M7\_STM32F7\_STM32756G-EVAL/RTOSDemo.eww
 from within the IAR Embedded Workbench IDE.
2. Open main.c, and set mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to generate either
 the simply blinky demo, or the full test and demo application, as
 required.
3. Ensure the target hardware is connected to the host computer using a
 suitable debugger interface - the demo was developed and debugged using
 a J-Link.
4. Select '**Rebuild All**' from the IDE's '**Project**' menu, the
 RTOSDemo project should build without any errors or warnings.
5. After the build completes, select '**Download and Debug**' from the IDE's '**Project**'
 menu to program the Cortex-M7 microcontroller, start a debug
 session, and have the debugger break on entry into the main() function.

#### Building and executing the demo application - Keil

1. Open FreeRTOS/Demo/CORTEX\_M7\_STM32F7\_STM32756G-EVAL/RTOSDemo.uvprojx
 from within the Keil uVision IDE.
2. Open main.c, and set mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to generate either
 the simply blinky demo, or the full test and demo application, as
 required.
3. Ensure the target hardware is connected to the host computer using a
 suitable debugger interface - the demo was developed and debugged using
 a J-Link.
4. Select '**Build Target**' from the IDE's '**Project**' menu, the
 RTOSDemo project should build without any errors or warnings.
5. After the build completes, select "**Start/Stop Debug Session**" from the IDE's '**Debug**'
 menu to program the Cortex-M7 microcontroller, start a debug
 session, and have the debugger break on entry into the main() function.

---

### RTOS Configuration and Usage Details

#### ARM Cortex-M7 FreeRTOS port specific configuration

Configuration items specific to this demo are contained in FreeRTOS/Demo/CORTEX\_M7\_STM32F7\_STM32756G-EVAL/FreeRTOSConfig.h.
[The constants defined in this file can be edited to suit your application](/Documentation/02-Kernel/03-Supported-devices/02-Customization). In particular -

* **configTICK\_RATE\_HZ**

 This sets the frequency of the RTOS tick interrupt. The supplied value of 1000Hz is useful for
 testing the RTOS kernel functionality but is faster than most applications need.
 Lowering the frequency will improve efficiency.
* **configKERNEL\_INTERRUPT\_PRIORITY and configMAX\_SYSCALL\_INTERRUPT\_PRIORITY**

 See the [RTOS kernel configuration](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) documentation for full information on these configuration constants.
* **configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY and configLIBRARY\_MAX\_SYSCALL\_INTERRUPT\_PRIORITY**

 Whereas configKERNEL\_INTERRUPT\_PRIORITY and configMAX\_SYSCALL\_INTERRUPT\_PRIORITY
 are full eight bit un-shifted values, defined to be used as raw numbers directly
 in the ARM Cortex-M7 NVIC registers, configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY
 and configLIBRARY\_MAX\_SYSCALL\_INTERRUPT\_PRIORITY
 are equivalents that are defined using just the 4 priority bits implemented in the STM32F7
 NVIC.
 These values are provided because the CMSIS library function NVIC\_SetPriority()
 requires the un-shifted 4 bit format.

Attention please!: See the [page dedicated to setting interrupt priorities on ARM Cortex-M devices](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4). Remember that ARM Cortex-M cores use
numerically low priority numbers to represent HIGH priority interrupts. This
can seem counter-intuitive and is easy to forget! If you wish to assign an
interrupt a low priority do NOT assign it a priority of 0 (or other low numeric
value) as this will result in the interrupt actually having the highest priority
in the system - and therefore potentially make your system crash if this
priority is above configMAX\_SYSCALL\_INTERRUPT\_PRIORITY. Also, do not leave
interrupt priorities unassigned, as by default they will have a priority of 0
and therefore the highest priority possible.

The lowest priority on a ARM Cortex-M core is in fact 255 - however, different
ARM Cortex-M microcontroller manufacturers implement a different number of priority bits and supply library
functions that expect priorities to be specified in different ways. For example,
on ST STM32F7 ARM Cortex-M7 microcontrollers, the lowest priority you can specify is in fact 15 - this is defined by the constant
configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY in FreeRTOSConfig.h. The highest priority
that can be assigned is always zero.

It is also recommended to ensure that all priority bits are assigned as
being preemption priority bits, and none as sub priority bits as is done
in the demo project by the function call

```c
HAL_NVIC_SetPriorityGrouping( NVIC_PRIORITYGROUP_4 );
```

Each port #defines 'BaseType\_t' to equal the most efficient data type for that
processor. This port defines BaseType\_t to be of type long.

### Interrupt service routines

Unlike many FreeRTOS ports, interrupt service routines that cause a context switch have
no special requirements, and can be written as per the compiler documentation.
The macro portEND\_SWITCHING\_ISR() can be used to request a context switch from
within an interrupt service routine.

Note that portEND\_SWITCHING\_ISR() will leave interrupts enabled.

The following source code snippet is provided as an example. The interrupt
uses a [direct to task notification](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
to synchronise with a task (not shown), and calls portEND\_SWITCHING\_ISR
to ensure the interrupt returns directly to the task.

```c

void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A task notification is used for this purpose. Note
 lHigherPriorityTaskWoken is initialised to zero. */
    [vTaskNotifyGiveFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR)( xTaskToNotify, &lHigherPriorityTaskWoken );

    /* If the task with handle xTaskToNotify was blocked waiting for the notification
 then sending the notification will have removed the task from the Blocked
 state. If the task left the Blocked state, and if the priority of the task
 is higher than the current Running state task (the task that this interrupt
 interrupted), then lHigherPriorityTaskWoken will have been set to pdTRUE
 internally within vTaskNotifyGiveFromISR(). Passing pdTRUE into the
 portEND\_SWITCHING\_ISR() macro will result in a context switch being pended to
 ensure this interrupt returns directly to the unblocked, higher priority,
 task. Passing pdFALSE into portEND\_SWITCHING\_ISR() has no effect. */
    portEND_SWITCHING_ISR( lHigherPriorityTaskWoken );
}
```

Only FreeRTOS API functions that end in "FromISR" can be called from an
interrupt service routine - and then only if the priority of the interrupt
is less than or equal to that set by the configMAX\_SYSCALL\_INTERRUPT\_PRIORITY
configuration constant (or configLIBRARY\_MAX\_SYSCALL\_INTERRUPT\_PRIORITY).

#### Resources used by FreeRTOS

FreeRTOS requires exclusive use of the SysTick and PendSV interrupts. SVC number #0 is also used.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition of configUSE\_PREEMPTION within FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative. The full demo application may not execute correctly when the co-operative RTOS scheduler is
selected.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.

#### Memory allocation

Source/Portable/MemMang/heap\_4.c is included in the ARM Cortex-M7 demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Miscellaneous

Note that vPortEndScheduler() has not been implemented.
