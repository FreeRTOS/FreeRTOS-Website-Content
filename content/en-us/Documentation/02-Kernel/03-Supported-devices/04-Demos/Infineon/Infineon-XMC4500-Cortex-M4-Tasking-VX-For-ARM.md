---
title: "Infineon XMC4500 ARM Cortex-M4 Floating Point DemoUsing the Tasking VX-Toolset for ARM development tools"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![XMC4500 microcontroller development board programmed with the Tasking VX Toolset for ARM](/media/2018/Infineon-XMC4000-Cortex-M4-Hexagon-kit.jpg)

### Introduction

**The demo provided on this page is now obsolete and [replaced by a new demo
and documentation page](Infineon-ARM-Cortex-M4-XMC4000-RTOS)**

This page documents a FreeRTOS demo application for the
[XMC4500 ARM Cortex-M4 microcontroller](http://www.infineon.com/xmc)
from [Infineon](http://www.infineon.com/). The demo
uses the FreeRTOS Tasking VX-toolset ARM Cortex-M4F port, which requires the application
to enable the ARM Cortex-M4 hardware floating point unit, and the project options to
be configured to generate floating point instructions (the project described on this
page is already configured correctly).

---

#### *IMPORTANT! Notes on using the FreeRTOS/Tasking XMC4000 demo project*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-infineon-arm-cortex-m4-demo-application)
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

The Tasking VX-toolset Eclipse project file for the XMC4500 demo application is located in the
FreeRTOS/Demo/CORTEX\_M4F\_Infineon\_XMC4500\_Tasking
directory. The
[Preparing the Eclipse Project](#building-and-executing-the-demo-application) section of this page contains
important information on setting up the demo project directory, and importing
the demo project into the Tasking Eclipse IDE.

---

### The Infineon ARM Cortex-M4 Demo Application

Two configurations can be selected between using the mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY
constant, which is located near the top of main.c.

#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 1

When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 1, main() calls
main\_blinky(), which then creates a very simple demo, as
described below.

* **The main\_blinky() Function:**

 main\_blinky() creates one queue, and two tasks. It then starts the
 RTOS scheduler.
* **The Queue Send Task:**

 The queue send task is implemented by the prvQueueSendTask() function in main\_blinky.c.
 prvQueueSendTask() sits in a loop that causes it to repeatedly block for
 200 milliseconds, before sending the value 100 to the queue that was created
 within main\_blinky(). Once the value is sent, the task loops back around to block for
 another 200 milliseconds.
* **The Queue Receive Task:**

 The queue receive task is implemented by the prvQueueReceiveTask() function
 in main\_blinky.c. prvQueueReceiveTask() sits in a loop where it repeatedly blocks on
 attempts to read data from the queue that was created within main\_blinky(). When data
 is received, the task checks the value of the data, and if the value equals
 the expected 100, toggles the LED. The 'block time' parameter passed to
 the queue receive function specifies that the task should be held in the Blocked
 state indefinitely to wait for data to be available on the queue. The queue
 receive task will only leave the Blocked state when the queue send task writes
 to the queue. As the queue send task writes to the queue every 200
 milliseconds, the queue receive task leaves the Blocked state every 200
 milliseconds, and therefore toggles the LED every 200 milliseconds.

#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 0

When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0, main() calls
main\_full(), which then creates a comprehensive test and demo application, which
demonstrates:

* Floating point context switching.
* Malloc failed and stack overflow [hook functions](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions).
 main.c also contains Tick and Idle hook functions, but FreeRTOSConfig.h is not configured to
 use them. See the comments in the implementation of the functions in main.c.
* [Software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers).
* [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/).
* [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/).
* [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/).

Some of the created tasks are from the set of [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
tasks, while others are specific
to the XMC4500 Tasking demo. Standard demo tasks are used by all FreeRTOS ports and demo applications.
They have no specific functionality, and are created just to demonstrate how to use the FreeRTOS API,
and test the FreeRTOS port.

main() creates 43 tasks before
starting the RTOS scheduler. The demo then dynamically and continuously creates and
deletes a further two tasks while it is running.

Application specific "register test" tasks are created in addition to the standard demo tasks.
These start by filling all the generic, and all the floating point registers, with known
values. The tasks then repeatedly check that
each register maintains the value written to it for the lifetime of
the tasks. The register check tasks run at the idle priority, so will exit and re-enter
the Running state frequently. The two register check
tasks each fill the CPU registers with different values, and a register containing an
unexpected value is symptomatic of an error in the context switching
mechanism.

A 'check' software timer is created that periodically inspects the standard
demo tasks, and register test tasks, to ensure all the tasks are functioning
as expected. The check software timer's
callback function toggles the single user LED on the XMC4500 Hexagon development kit
CPU board. This gives a visual feedback of the
system health. **If the LED is toggling every 3 seconds, then the
check software timer has not discovered any problems. If the LED is
toggling every 200 milliseconds, then the check software timer has
discovered a problem in one or more tasks.**

#### Hardware set up

The demo uses the LED that is soldered directly onto the CPU board PCB, so no
hardware set up is required.

#### Preparing the Tasking VX-Toolset Eclipse project directory

Eclipse projects can be either standard makefile projects, or managed make projects.
The FreeRTOS Tasking ARM Cortex-M4F project uses a managed make project. This in
turn means that either:

1. All the source files needed to build the project must be located under
 the folder/directory that contains the project file itself, or
2. The Eclipse workspace (note workspace, not project) needs to be
 configured to locate the files elsewhere on the hard disk.

Option 1 is used for this demo. Therefore, the directory FreeRTOS/Demo/CORTEX\_M4F\_Infineon\_XMC4500\_Tasking
contains a batch file called CreateProjectDirectoryStructure.bat that
copies all the required FreeRTOS source files, and some standard demo application
files, into sub directories inside the demo project directory.

**CreateProjectDirectoryStructure.bat must be executed before the Tasking
project is imported into the Eclipse workspace**.

CreateProjectDirectoryStructure.bat cannot be
executed from within the Tasking IDE.

#### Importing the demo application into the Tasking Eclipse workspace

To import the necessary projects into an existing or new Eclipse Workspace:
1. Select "Import" from the Tasking "File" menu. The dialogue box shown below
 will appear. Select "Existing Projects into Workspace".

![Importing the ARM Cortex-M4 project into the Eclipse workspace](/media/2018/Importing-the-STM32-TrueStudio-project-into-the-Eclipse-workspace.jpg)

**The dialogue box that appears when "Import" is first clicked**
2. In the next dialogue box, select FreeRTOS/Demo/CORTEX\_M4F\_Infineon\_XMC4500\_Tasking
 as the root directory. Then, make sure the RTOSDemo (rather than
 "FreeRTOS-Simple-Demo", as depicted below)
 project is checked in the "Projects" area, **and that the Copy Projects Into
 Workspace box is not checked**, before clicking
 the Finish button (see the image below for the correct check box states).

![Selecting the ARM Cortex-M4 RTOSDemo for importing into Tasking Eclipse](/media/2018/selecting-the-FreeRTOS-STM32-project-to-import-into-Eclipse.jpg)

**Make sure the RTOSDemo project is checked (not FreeRTOS-Simple-Demo

 as depicted), and "Copy projects into workspace" is not checked**

#### Building and executing the demo application

1. Ensure the CreateProjectDirectoryStructure.bat batch file has been executed,
 that the project has been imported into the Tasking workspace, and that
 mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to generate the required
 demo functionality, as noted above.
2. Ensure the target hardware is connected to the host computer using a
 suitable interface. The project was created using a J-Link Lite.
3. Select 'Build All' from the IDE's 'Project' menu, the
 RTOSDemo project should build without any errors or warnings.
4. After the project has built, click the "Debug" speed button in the IDE to
 program the microcontroller flash memory, and start a debug session.

---

### RTOS Configuration and Usage Details

#### Cortex-M4F FreeRTOS port specific configuration

Configuration items specific to this demo are contained in FreeRTOS/Demo/CORTEX\_M4F\_Infineon\_XMC4500\_Tasking/FreeRTOSConfig.h.
[The constants defined in this file can be edited to suit your application](/Documentation/02-Kernel/03-Supported-devices/02-Customization). In particular -

* **configTICK\_RATE\_HZ**

 This sets the frequency of the RTOS tick interrupt. The supplied value of 1000Hz is useful for
 testing the RTOS kernel functionality but is faster than most applications need. Lowering the frequency will improve efficiency.
* **configKERNEL\_INTERRUPT\_PRIORITY and configMAX\_SYSCALL\_INTERRUPT\_PRIORITY**

 See the [RTOS kernel configuration](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) documentation for full information on these configuration constants.
* **configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY and configLIBRARY\_MAX\_SYSCALL\_INTERRUPT\_PRIORITY**

 Whereas configKERNEL\_INTERRUPT\_PRIORITY and configMAX\_SYSCALL\_INTERRUPT\_PRIORITY
 are full eight bit shifted values, defined to be used as raw numbers directly
 in the ARM Cortex-M4F NVIC registers, configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY
 and configLIBRARY\_MAX\_SYSCALL\_INTERRUPT\_PRIORITY
 are equivalents that are defined using just the 6 priority bits implemented in the XMC4000
 NVIC.
 These values are provided because the CMSIS library function NVIC\_SetPriority()
 requires the unshifted 6 bit format.

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
Cortex-M microcontroller manufacturers implement a different number of priority bits and supply library
functions that expect priorities to be specified in different ways. For example,
on Infineon XMC4000 ARM Cortex-M4 microcontrollers, the lowest priority you can specify is in fact 63 - this is defined by the constant
configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY in FreeRTOSConfig.h. The highest priority
that can be assigned is always zero.

It is also recommended to ensure that all six priority bits are assigned as
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

Source/Portable/MemMang/heap\_2.c is included in the ARM Cortex-M4F demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Miscellaneous

Note that vPortEndScheduler() has not been implemented.
