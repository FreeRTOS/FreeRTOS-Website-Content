---
title: "NXP LPC43xx ARM Cortex-M4F DemoUsing Keil MDK development tools"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![NXP LPC4300 family of microcontrollers](/media/2018/NXP-LPC4300-Hitex-Development-Board.jpg)

This page documents a FreeRTOS ARM Cortex-M4F demo application that targets an NXP
[LPC43xx microcontroller](http://ics.nxp.com/products/lpc4000/lpc43xx/).
A Keil project is provided that is pre-configured to run on the LPC4350 development board provided
by Hitex. The LPC4350 demo project will evolve over the coming weeks
to also include support for the LPC4350's ARM Cortex-M0 based co-processor.

The demo configures the LPC4350 to run at 204MHz. See the notes in the RTOS
configuration and usage section below.

The FreeRTOS ARM Cortex-M4F port supports a full interrupt nesting model, and never
completely disable interrupts. The port can only be used with hardware
floating point support turned on in the compile time options of the project
used to build the source files. ARM Cortex-M4 devices that don't include a floating
point unit should not use this port, but instead use the FreeRTOS ARM Cortex-M3 port layer.

Note that Keil MDK version 4.2.2 or above is required to ensure the no\_allow\_fpreg\_for\_nonfpdata
compiler option is available.

---

#### *IMPORTANT! Notes on using the FreeRTOS Keil LPC4300 demo project*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-nxp-lpc4350-demo-application)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS zip file download contains source code for all the FreeRTOS ports,
and every demo application project.
It therefore contains many more files than are required to build and run the NXP LPC4350 demo. See the
[Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description
of the downloaded files, and information on creating a new project.

The Keil MDK demo project for the ARM Cortex-M4F core on the LPC4350 is called M4.uvproj,
and is located in the FreeRTOS/Demo/CORTEX\_M4F\_M0\_LPC43xx\_Keil/M4 directory of the
official FreeRTOS .zip file download. The FreeRTOS/Demo/CORTEX\_M4F\_M0\_LPC43xx\_Keil/M0
directory is currently empty, and included as a placeholder for the near future addition of
support for the LPC4350's co-processor core.

---

### The NXP LPC4350 Demo Application

#### Functionality

This demo application demonstrates:

* Floating point context switching.
* Malloc failed, stack overflow, tick and idle [hook functions](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions).
* [Software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers).
* [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/).
* [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/).
* [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/).

The demo application can be configured to provide a very simply 'blinky' style
demonstration, or a full and comprehensive test and demonstration of the
FreeRTOS functionality. The configuration built is controlled by the constant
#define mainCREATE\_SIMPLE\_LED\_FLASHER\_DEMO\_ONLY, which is defined in
main.c.

Demo application tasks are split between standard demo tasks, and demo specific
tasks. Standard demo tasks are used by all FreeRTOS ports and demo applications.
They have no specific purpose, other than to demonstrate the FreeRTOS API, and test the port.

|  |  |
| --- | --- |
| <br />**mainCREATE\_SIMPLE\_LED\_FLASHER\_DEMO\_ONLY setting**<br /> | <br />**Description**<br /> |
| <br /> Set to 1<br />  | <br /> This creates a **very simple example** that creates three<br /> standard demo "flash" tasks. Each of the three tasks toggles an<br /> LED at a fixed but different frequency. LEDs LED3, LED2 and LED1<br /> are used.<br /> <br /> |
| <br /> Set to 0<br />  | <br /> This is a very comprehensive demo that creates 46 tasks before<br /> starting the RTOS scheduler. It then continuously creates and<br /> deletes a further two tasks while the application is executing.<br /> <br /> The demo includes a lot of queues, a software timer, and various different types of semaphore.<br /> The tasks consist mainly of the<br /> [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) tasks.<br /> <br /> Application specific "register test" tasks are also created.<br /> These start by filling all the generic, and all the floating point registers, with known<br /> values. The tasks then repeatedly check that<br /> each register maintains the value written to it for the lifetime of<br /> the task. The tasks run at the idle priority, so will exit and re-enter<br /> the Running state often. The two register check<br /> tasks each use different values, and a register containing an<br /> unexpected value is symptomatic of an error in the context switching<br /> mechanism.<br /> <br /> A 'check' software timer is created that periodically inspects the standard<br /> demo tasks, and register test tasks, to ensure all the tasks are functioning<br /> as expected. **The check software timer's<br /> callback function toggles LED LED0. This gives visual feedback of the<br /> system health. If LED LED0 is toggling every 3 seconds, then the<br /> check software timer has not discovered any problems. If LED LED0 is<br /> toggling every 200 milliseconds, then the check software timer has<br /> discovered a problem in one or more tasks.**<br /><br /> Like the simple flasher demo, the comprehensive demo<br /> creates the standard demo flash tasks, which toggle LEDs LED3, LED2 and LED1<br /> at fixed but different frequencies.<br />  |

#### Hardware set up

The demo uses the LEDs that are soldered directly onto the Hitex PCB, so no
hardware set up is required.

#### Building and executing the demo application

1. Ensure the target hardware is connected to the host computer using a
 suitable interface. The project has been tested with both a ULINK2 and a ULINK ME.
2. Open the [M4.uvproj](#source-code-organisation) Keil project from within
 the Keil IDE.
3. Select "Build" from the IDE's "Project" menu, or simply press F7. The project
 should build without any errors or warnings.
4. When the build completes, select "Start/Stop Debug Session" from the IDE's
 "Debug" menu (or just press CTRL+F5) to program the microcontroller flash memory,
 and start a debug session. The execution will break on entry to the main()
 function.

---

### RTOS Configuration and Usage Details

#### Cortex-M4F FreeRTOS port specific configuration

Configuration items specific to this demo are contained in FreeRTOS/Demo/CORTEX\_M4F\_M0\_LPC43xx\_Keil/M4/FreeRTOSConfig.h.
[The constants defined in this file can be edited to suit your application](/Documentation/02-Kernel/03-Supported-devices/02-Customization). In particular -

* **configTICK\_RATE\_HZ** 

 This sets the frequency of the RTOS tick interrupt. The supplied value of 1000Hz is useful for
 testing the RTOS kernel functionality but is faster than most applications require. Lowering this value will improve efficiency.
* **configKERNEL\_INTERRUPT\_PRIORITY and configMAX\_SYSCALL\_INTERRUPT\_PRIORITY** 

 See the [RTOS kernel configuration](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) documentation for full information on these configuration constants.
* **configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY and configLIBRARY\_MAX\_SYSCALL\_INTERRUPT\_PRIORITY** 

 Whereas configKERNEL\_INTERRUPT\_PRIORITY and configMAX\_SYSCALL\_INTERRUPT\_PRIORITY
 are full eight bit shifted values, defined to be used as raw numbers directly
 in the ARM Cortex-M4F NVIC registers, configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY
 and configLIBRARY\_MAX\_SYSCALL\_INTERRUPT\_PRIORITY
 are exact equivalents, but defined using just the 5 priority bits available on the LPC4300.
 The CMSIS library function NVIC\_SetPriority() requires the unshifted 5 bit format.

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
on LPC ARM Cortex-M microcontrollers, the lowest priority you can specify is in fact 31 - this is defined by the constant
configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY in FreeRTOSConfig.h. The highest priority
that can be assigned is always zero.

It is also recommended to ensure that all five priority bits are assigned as
being preemption priority bits, and none as sub priority bits, as they are in the provided
demo.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that
processor. This port defines BaseType\_t to be of type long.

#### Core clock configuration

The demo runs the LPC4350 clock at 204MHz. To achieve this it is necessary
for the functions that configure the parallel flash memory controller to execute out of
RAM. The mapping of these functions is performed within the linker script itself (scatter file),
and the code that steps the core clock up to 204MHz is contained in Hitex\_fast\_startup.c.

#### Interrupt service routines

Unlike most ports, interrupt service routines that cause a context switch have
no special requirements, and can be written as per the compiler documentation.
The macro portEND\_SWITCHING\_ISR() can be used to request a context switch from
within an interrupt service routine.

Note that portEND\_SWITCHING\_ISR() will leave interrupts enabled.

The following source code snippet is provided as an example. The interrupt
uses a semaphore to synchronise with a task (not shown), and calls portEND\_SWITCHING\_ISR
to ensure the interrupt returns directly to the task.

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
