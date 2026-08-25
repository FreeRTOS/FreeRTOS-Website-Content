---
title: "Atmel SAM4S RTOS Demo"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Atmel SAM4S RTOS Demo Using the free Atmel Studio 6 IDE, GCC, and the Atmel Software Framework

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]


![SAM4 microcontroller from Atmel](/media/2018/SAM4.jpg)


### Introduction

This page documents a FreeRTOS demo application for the
[SAM4S ARM Cortex-M4 microcontroller](https://www.microchip.com/design-centers/32-bit/sam-32-bit-mcus/sam-4s-mcus)
from Atmel. The demo
uses the FreeRTOS GCC ARM Cortex-M3/4 port, the free
[Atmel Studio 6 IDE](https://www.microchip.com/en-us/tools-resources/develop/microchip-studio), and components
of the comprehensive [Atmel Software Framework](https://www.microchip.com/avr-support/advanced-software-framework-(asf))
(ASF). The project is pre-configured to run on the SAM4S-EK evaluation kit.

---

#### *IMPORTANT! Notes on using the FreeRTOS SAM4S demo project*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-atmel-arm-cortex-m4-demo-application)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS zip file contains the source files for all the FreeRTOS
ports, and all the demo applications, only a few of which are needed by this
project.
See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
section for a description of the downloaded files and information on creating a
new project.

The Atmel Studio 6 Solution file for the ATSAM4S demo application is called
RTOSDemo.atsln, and is located in the FreeRTOS/Demo/CORTEX\_M4\_ATSAM4S\_Atmel\_Studio
directory.

The [Preparing the Project Directory Structure](#building-and-executing-the-demo-application) section
of this page contains important information on preparing this directory.


---

### The Atmel ARM Cortex-M4 Demo Application


#### Hardware set up

If mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0 (see the functionality section
below), then the demo will include the standard com test tasks. The standard
demo com test creates two tasks - a Tx task that sends characters to the USART,
and an Rx task that expects to receive every character sent by the Tx task. A
loopback connector is required on the USART port for this mechanism to work - simply
link pin 2 to pin 3 on the 9 way connector marked "USART" on the
SAM4S-EK.

It should be noted that the com test tasks are included to demonstrate queues
being used to communicate between tasks and interrupts, and to demonstrate a
context switch being performed from inside an interrupt service routine. The
serial driver used is **not** intended to represent an efficient implementation.
Real applications should make use of the USART's peripheral DMA channel (PDC).


#### Functionality

mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is defined in main.c. The behaviour of the
demo depends on its setting.
  

#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 1

If mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 1 then main() will
call main\_blinky(). main\_blinky() creates a very simple demo as follows:

* **The main\_blinky() Function:** 
 
 main\_blinky() creates one queue, and two tasks. It then starts the
 RTOS scheduler.
* **The Queue Send Task:** 
 
 The queue send task is implemented by the prvQueueSendTask() function in main\_blinky.c.
 It sends the value 100 to the queue every 200 milliseconds.
* **The Queue Receive Task:** 
 
 The queue receive task is implemented by the prvQueueReceiveTask() function
 in main\_blinky.c. It repeatedly reads from the queue with a block time
 specified, causing it to enter the [Blocked state](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states)
 if the queue is empty. The task toggles the red LED each time the value 100 is
 received from the queue, therefore, because the queue send task sends to
 the queue every 200 milliseconds, the queue receive task should exit
 the Blocked state and toggle the red LED every 200 milliseconds.


#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 0

If mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0 then main() will
call main\_full(). main\_full() creates a comprehensive test and demo application
that demonstrates:

* [Software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers).
* [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/).
* [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/).
* [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/).
* A simple interrupt service routine that causes an RTOS task context switch.

The created tasks are from the set of [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
tasks. Standard demo tasks are used by all FreeRTOS port demo applications.
They have no specific functionality, and are created just to demonstrate how to use the FreeRTOS API,
and test the RTOS port.

main() creates 34 tasks and three software timers before
starting the RTOS scheduler. The demo then dynamically and continuously creates and
deletes a further two tasks while it is running.

A 'check' software timer is created that periodically inspects the standard
demo tasks to ensure all the tasks are functioning
as expected. The check software timer's
callback function toggles the green LED on the SAM4S-EK hardware.
This gives visual feedback of the
system health. **If the green LED is toggling every 3 seconds, then the
check software timer has not discovered any problems. If the LED is
toggling every 200 milliseconds, then the check software timer has
discovered a problem in one or more tasks.** This mechanism can be tested by
removing the loopback connector, and in so doing, deliberately causing the
com test tasks to fail.


#### Preparing the Project Directory Structure

Atmel Studio requires all the source files built by a project to be located in, or
in subdirectories of, the directory that contains the Atmel Studio project itself.
It is therefore necessary to copy the FreeRTOS
and standard demo source files used by the demo applications from
their locations in the standard FreeRTOS directory structure into the demo
directory. A batch file called CreateProjectDirectoryStructure.bat is provided
for this purpose.

CreateProjectDirectoryStructure.bat is located in FreeRTOS/Demo/CORTEX\_M4\_ATSAM4S\_Atmel\_Studio,
**and must be executed before the demo application can be
built successfully**.


#### Building and executing the demo application

1. Ensure the CreateProjectDirectoryStructure.bat batch file has been executed.
2. Open FreeRTOS/Demo/CORTEX\_M4\_ATSAM4S\_Atmel\_Studio/RTOSDemo.atsln
 from within the Atmel Studio IDE.
3. Open main.c, and set mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to generate either
 the simply blinky demo, or the full test and demo application, as
 required.
4. Ensure the target hardware is connected to the host computer using a
 suitable J-Link or SAM-ICE interface. The project was created using a
 J-Link.
5. Select 'Build Solution' from the IDE's 'Build' menu, the
 RTOSDemo project should build without any errors or warnings.
6. After the build completes, select "Start Debug and Break" from the IDE's Debug
 menu to program the SAM4S microcontroller flash memory, start a debug
 session, and have the debugger break on entry into the main() function.


---

### RTOS Configuration and Usage Details


#### ARM Cortex-M4 FreeRTOS port specific configuration

Configuration items specific to this demo are contained in FreeRTOS/Demo/CORTEX\_M4\_ATSAM4S\_Atmel\_Studio/src/FreeRTOSConfig.h.
[The constants defined in this file can be edited to suit your application](/Documentation/02-Kernel/03-Supported-devices/02-Customization). In particular -

* **configTICK\_RATE\_HZ** 

 This sets the frequency of the RTOS tick interrupt. The supplied value of 1000Hz is useful for
 testing the RTOS kernel functionality but is faster than most applications need.
 Lowering the frequency will improve efficiency.
* **configKERNEL\_INTERRUPT\_PRIORITY and configMAX\_SYSCALL\_INTERRUPT\_PRIORITY** 

 See the [RTOS kernel configuration](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) documentation for full information on these configuration constants.
* **configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY and configLIBRARY\_MAX\_SYSCALL\_INTERRUPT\_PRIORITY** 

 Whereas configKERNEL\_INTERRUPT\_PRIORITY and configMAX\_SYSCALL\_INTERRUPT\_PRIORITY
 are full eight bit shifted values, defined to be used as raw numbers directly
 in the ARM Cortex-M4 NVIC registers, configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY
 and configLIBRARY\_MAX\_SYSCALL\_INTERRUPT\_PRIORITY
 are equivalents that are defined using just the 4 priority bits implemented in the SAM4
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

The lowest priority on a ARM Cortex-M core is in fact 255 - however different
ARM Cortex-M microcontroller manufacturers implement a different number of priority bits and supply library
functions that expect priorities to be specified in different ways. For example,
on Atmel SAM4 ARM Cortex-M4 microcontrollers, the lowest priority you can specify is in fact 15 - this is defined by the constant
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
uses a semaphore to synchronise with a task (not shown), and calls portEND\_SWITCHING\_ISR
to ensure the interrupt returns directly to the task. See the function
USART1\_Handler() in the file serial.c included in this demo project for another
example.

```c

void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A semaphore is used for this purpose. Note
 lHigherPriorityTaskWoken is initialised to zero. */
    xSemaphoreGiveFromISR( xTestSemaphore, &lHigherPriorityTaskWoken );

    /* If there was a task that was blocked on the semaphore, and giving the
 semaphore caused the task to unblock, and the unblocked task has a priority
 higher than the current Running state task (the task that this interrupt
 interrupted), then lHigherPriorityTaskWoken will have been set to pdTRUE
 internally within xSemaphoreGiveFromISR(). Passing pdTRUE into the
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

Set the definition configUSE\_PREEMPTION within FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative. The full demo application may not execute correctly when the co-operative RTOS scheduler is
selected.


#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.


#### Memory allocation

Source/Portable/MemMang/heap\_4.c is included in the ARM Cortex-M4 demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.


#### Miscellaneous

Note that vPortEndScheduler() has not been implemented.


  


 
