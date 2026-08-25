---
title: "ST STM32F4xx ARM Cortex-M4F DemoUsing IAR EWARM development tools"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![ST STM32F4 ARM Cortex-M4F starter kit](/media/2018/STM32F407ZG-SK.jpg)  
STM32F407ZG\_SK starter kit board

This page documents a FreeRTOS ARM Cortex-M4F demo application that targets an STMicroelectronics
[STM32F4xx microcontroller](http://www.st.com/internet/mcu/product/252136.jsp).
An IAR project is provided that is pre-configured to run on the development board provided
as part of the [STM32F407ZG-SK](https://www.iar.com/dev-dynamic-custom-objects/iar-systems-delivers-complete-starter-kit-for-high-performance-stm32f407zg-microcontroller-05b70486) starter kit.

The FreeRTOS ARM Cortex-M4F port supports a full interrupt nesting model, and never
completely disable interrupts. The port can only be used with hardware
floating point support turned on in the compile time options of the project
used to build the source files. ARM Cortex-M4 devices that don't include a floating
point unit should not use this port, but instead use the FreeRTOS ARM Cortex-M3 port layer.

**Note:** The demo presented on this page tests the FreeRTOS floating
point support by forcing interrupts that use the floating point unit to nest to
a level of three deep. The nesting starts from the tick hook function - which
is called from the FreeRTOS tick interrupt code. Removing this part of the test
will greatly improve the efficiency of the RTOS kernel, and can be achieved by setting
configUSE\_TICK\_HOOK to zero in FreeRTOSConfig.h.

**Note 2:** If this project fails to build then it is likely the version of IAR
Embedded Workbench being used is too old. If this is the case, then it is also
likely that the project file has been (silently) corrupted and will need to be
restored to its original state before it can be built even with an updated IAR version.

---

#### *IMPORTANT! Notes on using the FreeRTOS IAR STM32F4 demo project*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-stmicro-arm-cortex-m4f-demo-application)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS zip file download contains source code for all the FreeRTOS ports,
and every demo application project.
It therefore contains many more files than are required to build and run the ST STM32F407ZG demo. See the
[Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description
of the downloaded files, and information on creating a new project.

The IAR Embedded Workbench workspace for the STM32F4xx demo is called RTOSDemo.eww,
and is located in the FreeRTOS/Demo/CORTEX\_M4F\_STM32F407ZG-SK directory of the
official FreeRTOS .zip file download.

---

### The STMicro ARM Cortex-M4F Demo Application

#### Functionality

This demo application demonstrates:

* Floating point instructions being used from tasks.
* Floating point instructions being used from interrupts that nest 3 deep.
 **Note:** The nesting starts from the tick hook function - which
 is called from the FreeRTOS tick interrupt code. Removing this part of the test
 will greatly improve the efficiency of the RTOS kernel, and can be achieved by setting
 configUSE\_TICK\_HOOK to zero in FreeRTOSConfig.h.
* [Software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers).
* [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/).
* [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/).
* [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/).
* Malloc failed, stack overflow, tick and idle [hook functions](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions).

The demo application can be configured to provide very simply 'blinky' style
functionality, or a full and comprehensive test and demonstration of the
FreeRTOS functionality. The #define mainCREATE\_SIMPLE\_LED\_FLASHER\_DEMO\_ONLY constant,
which is defined in main.c, is used to switch between the two modes.

Demo application tasks are split between standard demo tasks, and demo specific
tasks. Standard demo tasks are used by all FreeRTOS ports and demo applications.
They have no purpose other than to demonstrate the FreeRTOS API, and test a port.

|  |  |
| --- | --- |
| <br />**mainCREATE\_SIMPLE\_LED\_FLASHER\_DEMO\_ONLY setting**<br /> | <br />**Description**<br /> |
| <br /> Set to 1<br />  | <br /> This creates a **very simple example** that creates three<br /> standard demo "flash" tasks. Each of the three tasks toggles an<br /> LED at a fixed but different frequency. LEDs STAT1, STAT2 and STAT3<br /> are used.<br /> <br /> |
| <br /> Set to 0<br />  | <br /> This is a very comprehensive demo that creates 46 tasks before<br /> starting the RTOS scheduler, then continuously dynamically creates and<br /> deletes another two tasks as the application executes.<br /> <br /> It creates a lot of queues, a software timer, and different types of semaphore.<br /> The tasks consist mainly of the<br /> [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) tasks.<br /> <br /> The demo includes application specific "register test" tasks.<br /> These are idle priority tasks that start by filling all the generic<br /> and floating point registers with known<br /> values. The tasks then repeatedly check that<br /> each register maintains the value written to it, as it enters and<br /> exits the Running state, for the lifetime of the task. Each of the two register check<br /> tasks uses a different set of known values, and a value being<br /> unexpectedly changed is symptomatic of an error in the context switching<br /> mechanism.<br /> <br /> The floating point interrupt nesting test starts in the tick hook<br /> function. The tick hook function is an optional application defined<br /> function that is called from the real time kernels tick interrupt<br /> if configUSE\_TICK\_HOOK is set to 1 in FreeRTOSConfig.h. The tick<br /> hook function fills the floating point registers with a known value,<br /> then forces a medium priority interrupt to interrupt it. The medium<br /> priority interrupt fills the floating point registers with a different<br /> value, before it too forces a high priority interrupt to interrupt it.<br /> The high priority interrupt fills the floating point registers with<br /> yet another value. As the interrupt nesting stack then unwinds, first<br /> the medium priority interrupt checks that the floating point registers<br /> contain the values that it wrote to them, and then the tick hook function<br /> (the lowest priority interrupt) checks that the floating point registers<br /> contain the values that it wrote to them.<br /> <br /> A 'check' software timer is created and started to periodically inspects the standard<br /> demo tasks and register test tasks, to ensure they are all operating<br /> as expected, and have never reported an error. **The check timer<br /> callback function toggles LED STAT4 to give visual feedback of the<br /> system status. If LED STAT4 toggles every 3 seconds, then the<br /> check software timer has not discovered any problems with the execution of the test and demo<br /> tasks. If the rate at which LED STAT4 toggles increases to every 200<br /> milliseconds, then the check software timer has discovered a problem<br /> in at least one task.**<br /><br /> Like the simple flasher demo, the comprehensive demo<br /> creates the standard demo flash tasks, which toggle LEDs STAT1, STAT2 and STAT3<br /> at fixed but different frequencies.<br />  |

#### Hardware set up

The demo uses the LEDs that are built onto the starter kit hardware, so no
hardware set up is required.

#### Building and executing the demo application

1. Ensure the target hardware is connected to the host computer using a
 suitable debugger interface. A J-Link lite is provided in the starter kit.
2. Open the [RTOSDemo.eww](#source-code-organisation) Embedded Workbench workspace
 from within the Embedded Workbench IDE.
3. Select "Build All" from the Embedded Workbench "Project" menu - the demo
 application should build without errors.
4. When the build completes, select "Download and Debug" from the Embedded Workbench
 "Project" menu (or just press CTRL+D) to program the microcontroller flash memory,
 and start a debug session. The application will start to run, and then
 break at the start of the function main().

---

### RTOS Configuration and Usage Details

#### Cortex-M4F FreeRTOS port specific configuration

Configuration items specific to this demo are contained in FreeRTOS/Demo/CORTEX\_M4F\_STM32F407ZG-SK/FreeRTOSConfig.h.
[The constants defined in this file can be edited to suit your application](/Documentation/02-Kernel/03-Supported-devices/02-Customization). In particular -

* **configTICK\_RATE\_HZ** 

 This sets the frequency of the RTOS tick interrupt. The supplied value of 1000Hz is useful for
 testing the RTOS kernel functionality but is faster than most applications require. Lowering this value will improve efficiency.
* **configKERNEL\_INTERRUPT\_PRIORITY and configMAX\_SYSCALL\_INTERRUPT\_PRIORITY** 

 See the [RTOS kernel configuration](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) documentation for full information on these configuration constants.
* **configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY and configLIBRARY\_MAX\_SYSCALL\_INTERRUPT\_PRIORITY** 

 Whereas configKERNEL\_INTERRUPT\_PRIORITY and configMAX\_SYSCALL\_INTERRUPT\_PRIORITY
 are full eight bit shifted raw values, defined to be used directly in the ARM Cortex-M4F NVIC registers,
 configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY and configLIBRARY\_MAX\_SYSCALL\_INTERRUPT\_PRIORITY
 are equivalents defined using just the 4 priority bits available on the STM32.
 The ST Standard Peripheral Library function NVIC\_Init(), and the CMSIS
 library function NVIC\_SetPriority(), both require the unshifted 4 bit format.

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
Cortex-M vendors implement a different number of priority bits and supply library
functions that expect priorities to be specified in different ways. For example,
on STM32 microcontrollers the lowest priority you can specify is in fact 15 - this is defined by the constant
configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY in FreeRTOSConfig.h. The highest priority
that can be assigned is always zero.

It is also recommended to ensure that all four priority bits are assigned as
being preemption priority bits, and none as sub priority bits, as they are in the provided
demo.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that
processor. This port defines BaseType\_t to be of type long.

#### Interrupt service routines

Unlike most ports, interrupt service routines that cause a context switch have
no special requirements, and can be written as per the compiler documentation.
The macro portEND\_SWITCHING\_ISR() can be used to request a context switch from
within an interrupt service routine.

Note that portEND\_SWITCHING\_ISR() will leave interrupts enabled.

As an example, this demo provides an interrupt service routine called
EXTI9\_5\_IRQHandler(), which is defined in main.c. This interrupt is triggered by
pressing the button marked "USER" on the starter kit hardware. The interrupt
uses a semaphore to synchronise with a task, and calls portEND\_SWITCHING\_ISR
to ensure the interrupt returns directly to the task. The function is shown below:

```c

void EXTI9_5_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Only line 6 is enabled, so there is no need to test which line generated
 the interrupt. */
    EXTI_ClearITPendingBit( EXTI_Line6 );

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. First the handler releases a semaphore.
 lHigherPriorityTaskWoken has been initialised to zero. */
    xSemaphoreGiveFromISR( xTestSemaphore, &lHigherPriorityTaskWoken );

    /* If there was a task that was blocked on the semaphore, and giving the
 semaphore caused the task to unblock, and the unblocked task has a priority
 higher than the currently executing task (the task that this interrupt
 interrupted), then lHigherPriorityTaskWoken will have been set to pdTRUE.
 Passing pdTRUE into the following macro call will cause this interrupt to
 return directly to the unblocked, higher priority, task. */
    portEND_SWITCHING_ISR( lHigherPriorityTaskWoken );
}
```

Only FreeRTOS API functions that end in "FromISR" can be called from an
interrupt service routine - and then only if the priority of the interrupt
is less than or equal to that set by the configMAX\_SYSCALL\_INTERRUPT\_PRIORITY
configuration constant.

#### Resources used by FreeRTOS

FreeRTOS requires exclusive use of the SysTick and PendSV interrupts. SVC number #0 is also used.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within RTOSDemo/FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative. The full demo application may not execute correctly when the co-operative RTOS scheduler is
selected.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.

#### Memory allocation

Source/Portable/MemMang/heap\_2.c is included in the ARM Cortex-M4F demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Miscellaneous

Note that vPortEndScheduler() has not been implemented.
