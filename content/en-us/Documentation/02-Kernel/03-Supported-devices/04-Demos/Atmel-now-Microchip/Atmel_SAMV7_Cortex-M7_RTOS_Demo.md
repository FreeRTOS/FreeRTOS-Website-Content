---
title: "Atmel ARM Cortex-M7 SAMV71/SAME70 RTOS Demo Using the IAR, Atmel Studio (GCC), and ARM Keil Embedded Development Tools"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

 Using the [IAR](http://www.iar.com/ewarm),
 [Atmel Studio](https://www.microchip.com/en-us/tools-resources/develop/microchip-studio) (GCC),
 and ARM Keil Embedded Development Tools

 [[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![SAMV71 Cortex-M7 microcontroller from Atmel](/media/2018/SAMV71_Xplained_Ultra_Angle.png)

### Introduction

This page documents:
* A FreeRTOS demo application for the
 [SAMV7 ARM Cortex-M7 microcontroller](http://www.microchip.com/design-centers/32-bit/sam-32-bit-mcus/sam-v-mcus)
 from Atmel. The project
 can be built with either the [IAR](http://www.iar.com/ewarm),
 [Atmel Studio](https://www.microchip.com/en-us/tools-resources/develop/microchip-studio),
 or ARM Keil tools, and targets the
 [SAM V71 Xplained Ultra Evaluation Kit](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATSAMV71-XULT).
* A FreeRTOS demo application for the
 [SAME7 ARM Cortex-M7 microcontroller](http://www.microchip.com/design-centers/32-bit/sam-32-bit-mcus/sam-e-mcus)
 from Atmel. The project
 can be built with the
 [Atmel Studio](https://www.microchip.com/en-us/tools-resources/develop/microchip-studio)
 compiler (GCC) and IDE, and targets the
 [SAM E70 Xplained Ultra Evaluation Kit](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATSAME70-XPLD).

As the SAM V70 includes a superset of functionality, so the SAM V70 Xplained Ultra board can
also be used to evaluate running the RTOS on SAM V70,
[SAM S70](http://www.microchip.com/design-centers/32-bit/sam-32-bit-mcus/sam-s-mcus),
and [SAM E70](http://www.microchip.com/design-centers/32-bit/sam-32-bit-mcus/sam-e-mcus)
ARM Cortex-M7 devices.

|  |
| --- |
| <br />[![](/media/2018/Atmel_Cortex-M7_IDE_Plug_In.png)](/media/2018/Atmel_Cortex-M7_IDE_Plug_In.png)<br /><br />**Atmel Studio with the FreeRTOS Viewer window open.<br /> Click to enlarge.** <br /><br /> |

---

#### *IMPORTANT! Notes on using the SAMV7 and SAME7 ARM Cortex-M7 RTOS demo*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-atmel-arm-cortex-m7-demo-application)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting),
noting in particular the recommendation to develop with
[configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert) defined
in FreeRTOSConfig.h.

---

### Source Code Organisation

The FreeRTOS zip file download contains the source files for all the FreeRTOS
ports, and projects for all the demo applications. It therefore contains many
more files than are needed by this project.
See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
section for a description of the directory structure and information on creating a
new FreeRTOS project.

The Atmel Studio project for the SAMV7 demo application is called
RTOSDemo.atsln, and is located in the FreeRTOS/Demo/CORTEX\_M7\_SAMV71\_Xplained\_AtmelStudio
directory.

The Atmel Studio project for the SAME7 demo application is called
RTOSDemo.atsln, and is located in the FreeRTOS/Demo/CORTEX\_M7\_SAME70\_Xplained\_AtmelStudio
directory.

The IAR Embedded Workbench for ARM workspace for the SAMV7 demo application is called
RTOSDemo.eww, and is located in the FreeRTOS/Demo/CORTEX\_M7\_SAMV71\_Xplained\_IAR\_Keil
directory.

The ARM Keil project for the SAMV7 demo application is called
RTOSDemo.uvprojx, and is located in the FreeRTOS/Demo/CORTEX\_M7\_SAMV71\_Xplained\_IAR\_Keil
directory.

---

### The Atmel ARM Cortex-M7 Demo Application

#### Functionality

mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is defined in main.c. The behaviour of the
demo depends on its setting.

#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 1

If mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 1 then main()
calls main\_blinky(). main\_blinky() creates a very simple demo as follows:
* **The main\_blinky() Function:**
main\_blinky() creates one queue, and two tasks. It then starts the
 RTOS scheduler.
* **The Queue Send Task:**

 The queue send task is implemented by prvQueueSendTask() in main\_blinky.c.
 It sends the value 100 to the queue every 200 milliseconds.
* **The Queue Receive Task:**

 The queue receive task is implemented by prvQueueReceiveTask()
 in main\_blinky.c. It blocks on queue reads, unblocking and toggling an
 LED each time the message from the queue send task is received. The
 queue send task sends to the queue every 200 milliseconds, so the queue
 receive task leaves the Blocked state and toggles the LED
 every 200 milliseconds.

#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 0

If mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0 then main()
calls main\_full(). main\_full() creates a comprehensive test and demo application
that demonstrates:

* [Task notifications](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
* [Event groups](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)
* [Software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)
* [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)
* [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)
* [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)

The created tasks are from the set of [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
tasks. Standard demo tasks are used by all FreeRTOS port demo applications and
have no specific functionality. They are used to demonstrate how to use the FreeRTOS API,
and to test the RTOS port.

A 'check' task is created to periodically inspect the standard
demo tasks in order to ensure all the tasks are functioning
as expected. The check task also toggles an LED to give a visual feedback of the
system status. **If the LED is toggling every 3 seconds, then the
check task has not discovered any problems. If the LED is
toggling every 200 milliseconds, then the check task has
discovered a problem in one or more tasks.**.

#### Building and executing the demo application - Atmel Studio

1. Open the project file FreeRTOS/Demo/CORTEX\_M7\_SAMV71\_Xplained\_AtmelStudio/RTOSDemo.atsln
 or FreeRTOS/Demo/CORTEX\_M7\_SAME70\_Xplained\_AtmelStudio/RTOSDemo.atsln
 from within the Atmel Studio IDE.
2. Open main.c, and set mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to generate either
 the simply blinky demo, or the full test and demo application, as
 required.
3. Ensure the target hardware is connected to the host computer using a
 suitable debugger interface - the demo was developed and debugged using
 a J-Link; the Edge debug interface built onto the target hardware can
 also be used.
4. Select '**Build Solution**' from the IDE's '**Build**' menu, the
 RTOS demo project should build without any errors or warnings.
5. After the build completes, select '**Start Debugging and Break**' from the IDE's '**Debug**'
 menu to program the Cortex-M7 microcontroller, start a debug
 session, and have the debugger break on entry into the main() function.

#### Building and executing the demo application - IAR

1. Open FreeRTOS/Demo/CORTEX\_M7\_SAMV71\_Xplained\_IAR\_Keil/RTOSDemo.eww
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

1. Open the project file FreeRTOS/Demo/CORTEX\_M7\_SAMV71\_Xplained\_IAR\_Keil/RTOSDemo.uvprojx
 from within the Keil uVision IDE.
2. Open main.c, and set mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to generate either
 the simply blinky demo, or the full test and demo application, as
 required.
3. Ensure the target hardware is connected to the host computer using a
 suitable debugger interface - the demo was developed and debugged using
 a J-Link.
4. Select '**Build Target**' from the IDE's '**Project**' menu, the
 RTOSDemo project should build without any errors or warnings.
5. After the build completes, select '**Start/Stop Debug Session**' from the IDE's '**Debug**'
 menu to program the Cortex-M7 microcontroller, start a debug
 session, and have the debugger break on entry into the main() function.

---

### RTOS Configuration and Usage Details

#### ARM Cortex-M7 FreeRTOS port specific configuration

Configuration items specific to this demo are contained in the file FreeRTOS/Demo/CORTEX\_M7\_SAMV71\_Xplained\_IAR\_Keil/FreeRTOSConfig.h
or FreeRTOS/Demo/CORTEX\_M7\_SAME70\_Xplained\_IAR\_Keil/FreeRTOSConfig.h.
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
 are equivalents that are defined using just the 3 priority bits implemented in the SAMV7
 and SAME7 NVIC.
 These values are provided because the CMSIS library function NVIC\_SetPriority()
 requires the un-shifted 3 bit format.

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
on Atmel SAMV7/SAME7 ARM Cortex-M7 microcontrollers, the lowest priority you can specify is in fact 7 - this is defined by the constant
configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY in FreeRTOSConfig.h. The highest priority
that can be assigned is always zero.

It is also recommended to ensure that all priority bits are assigned as
being preemption priority bits, and none as sub priority bits, as they are in the provided
demo.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that
processor. This port defines BaseType\_t to be of type long.

#### Interrupt service routines

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
