---
title: "Microchip PIC32 MZ RTOS port with a MIPS M14K core"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

### Introduction

#### The PIC32MZ and PIC32MZ EF RTOS ports

This page presents the FreeRTOS port and demo application for the [PIC32MZ](http://www.microchip.com/PIC32)
and PIC32MZ EF 32bit microcontrollers from [Microchip](http://www.microchip.com/), which have a MIPS M14K core.

The FreeRTOS PIC32MZ port:

* Maintains a separate interrupt stack. Without a separate interrupt stack
 each task stack would have to allocated enough space to hold an entire
 (potentially nested) interrupt stack frame.
* Supports interrupt stack overflow detection in addition to the standard
 task stack overflow detection. Interrupt stack overflow detection is
 turned on by building with
 [configCHECK\_FOR\_STACK\_OVERFLOW](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking) set to 3 when
 [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert) is also defined.
* Provides a full interrupt nesting model that does not, itself, ever completely disable
 interrupts. Although the MIPS hardware disables interrupts on entry to an
 interrupt service routine the RTOS code quickly re-enables them before
 any application handler code is executed.

![RTOS on PIC32 starter kit](/media/2018/PIC32MZ-StarterKit.jpg)

**PIC32MZ Starter Kit**

#### The demo application

The demo application is pre-configured to use the
[MPLAB X](http://www.microchip.com/mplabx) IDE and the
[MPLAB XC32](http://www.microchip.com/XC32) GCC based
compiler. Three build configurations are provided; PIC32MZ2048\_SK which targets
the standard PIC32MZ Starter Kit, and PIC32MZ2048EF\_SK\_SOFT\_FLOAT and
PIC32MZ2048EF\_SK\_HARD\_FLOAT - both of which target the
[PIC32 Embedded Connectivity with FPU (EF) Starter Kit](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=DM320007).

The demo project can be configuration to build either a simple blinky demo or a
comprehensive test and demo application. The comprehensive application demonstrates
and tests the interrupt nesting behaviour. Build instructions are provided on this
page.

---

#### IMPORTANT! Notes on using the PIC32 MZ RTOS port

*Please read all the following points before using this RTOS port.*

1. [Source Code Organization](#source-code-organization)
2. [The Demo Application](#the-demo-application)
3. [Configuration and Usage Details](#configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organization

The FreeRTOS download contains the source code and demo application projects for
all the RTOS ports, so most of the files it contains are not relevant to the
PIC32MZ demo.
See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files, and information on creating a new project.

The MPLAB X project that builds the PIC32MZ RTOS demo is located in the
FreeRTOS/Demo/PIC32MZ\_MPLAB directory.

### The Demo Application

#### Functionality

The constant mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY, which is defined at the
top of main.c, is used to switch between a simple 'blinky' style starter project
and a more comprehensive test and demo application.

##### When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 1

When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 1 main() calls main\_blinky().
main\_blinky() creates a very simple example that uses two
tasks, one queue, and one software timer.
* The Blinky Software Timer:

 This demonstrates an auto-reload software timer. The timer callback
 function does nothing but toggle an LED.
* The Queue Send Task:

 The queue send task is implemented by the prvQueueSendTask() function.
 The task sits in a loop that sends the value 100 to the queue
 every 200 milliseconds.
* The Queue Receive Task:

 The queue receive task is implemented by the prvQueueReceiveTask()
 function. The task sits in a loop blocking on attempts to
 read from the queue (no CPU cycles are consumed while it is blocked),
 toggling an LED each time a value is received. As the queue send task
 writes to the queue very 200 milliseconds the queue receive task unblocks
 and toggles the LED every 200 milliseconds.

##### When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0

When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0 main() calls main\_full().
main\_full() creates a very comprehensive test and demo application that
creates numerous RTOS tasks and software timers.
* The first LED is under the control of a simple 'flash' software timer.
* The second LED is under the control of a task that is triggered by an
 interrupt. It is provided as an example of how to write a FreeRTOS
 compatible interrupt service routine (RTOS compatible interrupt service
 routines are also described on this page).
* Most of the RTOS tasks created by the demo do not update an LED so have
 no visible indication that they are operating correctly. Therefore the
 last LED is under the control of a 'Check' software timer. The software
 timer is used to monitor all the other tasks, and to toggle an LED. If
 all the other tasks are executing as expected the LED will toggle every
 3 seconds. If a suspected error has been found in any of the other tasks
 the toggle rate will increase to 200ms.
* Interrupt nesting is exercised using one task and two
 interrupts - all of which access the same two queues. The
 two interrupts run at different priorities, and both run
 above the RTOS kernel interrupt priority, meaning a maximum nesting
 depth of three is demonstrated by this particular test. The
 high frequency timer interrupt adds another nesting level. See the
 [RTOS Configuration and Usage](#important-notes-on-using-the-pic32-mz-rtos-port)
 section for a more complete explanation of the executing
 interrupts, and their respective priorities.

#### Building and debugging the demo application with MPLAB X

These instructions assume you have MPLAB X and the MPLAB XC32 compiler correctly
installed on your host computer.

1. Open the project from within the MPLAB X IDE (the location of
 the project is detailed in the Source Code Organization section
 near the top of this page).
2. Connect the debug USB connector of the PIC32MZ Starter Kit to
 your host computer (the computer running MPLAB X).
3. From the MPLAB X 'Debug' menu, select 'Debug Project'. The project
 should build without an errors or warnings, and the resultant
 binary programmed into the PIC32 flash memory.

### Configuration and Usage Details

#### RTOS port specific configuration

Configuration items specific to this demo are contained in FreeRTOS/Demo/PIC32MZ\_MPLAB/FreeRTOSConfig.h. The
constants defined in that file can be edited to suit your application. In particular -

* **configTICK\_RATE\_HZ**
 This sets the frequency of the RTOS tick. The supplied value of 1000Hz is
 useful for testing the RTOS kernel functionality but is faster
 than most applications require. Lowering this value will improve efficiency.
* **configKERNEL\_INTERRUPT\_PRIORITY** and **configMAX\_SYSCALL\_INTERRUPT\_PRIORITY**
See the [interrupt configuration](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)
 section of the RTOS kernel configuration documentation for full information on
 these options.

 configKERNEL\_INTERRUPT\_PRIORITY sets the interrupt priority used by the RTOS kernel
 itself, and will normally be set to the lowest possible interrupt priority.
 configMAX\_SYSCALL\_INTERRUPT\_PRIORITY sets the highest interrupt priority
 from which queue, software timer, and semaphore API functions can be called.
 Note that only API functions that end in FromISR() can be called from within
 an ISR. FreeRTOS maintains a separate API for use in an ISR to ensure interrupt
 entry is as quick and as standard as possible, and to ensure that the respective
 API versions used from tasks and from interrupts can both be optimised for their
 specific usage scenarios.

 configKERNEL\_INTERRUPT\_PRIORITY should be set to the lowest priority.

 Interrupts above configMAX\_SYSCALL\_INTERRUPT\_PRIORITY will not be masked
 by kernel critical sections and will therefore be unaffected
 by RTOS kernel activity - within the limitations imposed by the hardware itself.

 By way of demonstration, the demo application defines
 configMAX\_SYSCALL\_INTERRUPT\_PRIORITY to be 3, configKERNEL\_INTERRUPT\_PRIORITY to be 1,
 and all other interrupts as follows:

	+ The interrupt used to wake a task that toggles an LED is allocated
	 a priority of 3 - which equals the setting of configMAX\_SYSCALL\_INTERRUPT\_PRIORITY,
	 and is therefore the highest priority from which interrupt safe
	 FreeRTOS API functions can be called.
	+ The two timers used by the interrupt nesting test are allocated
	 priorities 2 and 3 respectively. Even though they both access the
	 same two queues, the priority 3 interrupt can safely interrupt the
	 priority 2 interrupt. Both can interrupt the RTOS tick.
	+ Finally, a high frequency timer interrupt is configured to use
	 priority 4 - which is higher than configMAX\_SYSCALL\_INTERRUPT\_PRIORITY
	 and therefore kernel activity will never prevent the high
	 frequency timer from executing immediately that the interrupt is
	 raised (within the limitations of the hardware itself). It is
	 not safe to access a queue from this interrupt, even using interrupt
	 safe RTOS API functions.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that
processor. This port defines BaseType\_t to be of type long.

Note that vPortEndScheduler() has not been implemented.

#### Interrupt service routines

Interrupt service routines that cannot nest have no special requirements and can
be written as per the compiler documentation. However interrupts written in this
manner will utilise the stack of whichever task was interrupted, rather than the
system stack, necessitating that adequate stack space be allocated to each
created task. It is therefore not recommended to write interrupt service routines
in this manner.

Interrupts service routines that can nest require a simple assembly wrapper, as
demonstrated below. It is recommended that all interrupts be written in this manner.

The T5 interrupt (the interrupt for the timer that is used to demonstrate a task
being unblocked from an interrupt) within the PIC32MZ demo can be used as an example - the assembly
code wrapper for which is replicated in Listing 1, and the C handler for which
is replicated in Listing 2.

---

```c

/* Prototype to be included in a C file to ensure the vector is
correctly installed. Note that because this ISR uses the FreeRTOS
assembly wrapper the IPL setting in the following prototype has no
effect. The interrupt priority is set using the Microchip provided
library functions. */
void __attribute__( (interrupt(ipl3), vector(_TIMER_5_VECTOR)))
                                                    vT5InterruptWrapper( void );

/* Header file in which portSAVE\_CONTEXT and portRESTORE\_CONTEXT are defined. */
#include "ISR_Support.h"

/* Ensure correct instructions is used. */
.set	nomips16
.set 	noreorder

/* Interrupt entry point. */
vT5InterruptWrapper:

  /* Save the current task context. This line MUST be included! */
  portSAVE_CONTEXT

  /* Call the C function to handle the interrupt. */
  jal vT5InterruptHandler
  nop

  /* Restore the context of the next task to execute. This line
 MUST be included! */
  portRESTORE_CONTEXT

  .end  vT5InterruptWrapper
```

**Listing 1: Assembly code wrapper for handling an interrupt that can cause a context switch**

---

Some notes on the assembly file wrapper:

* I have found that the assembly file in which the wrapper is placed must
 have a .S extension (with a capitol S). Using a lower case .s may
 result in the portSAVE\_CONTEXT and portRESTORE\_CONTEXT macros being
 incorrectly inlined.
* The portSAVE\_CONTEXT and portRESTORE\_CONTEXT macros must be used as the
 very first and very last executable lines in the function respectively.
* When the FreeRTOS assembly file wrapper is used as an entry point the
 IPL setting in the ISR function prototype has no effect.

Second, the C function called by the assembly file wrapper:

---

```c

void vT5InterruptHandler( void )
{
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* Give the semaphore. If giving the semaphore causes the task to leave the
 Blocked state, and the priority of the task is higher than the priority of
 the interrupted task, then xHigherPriorityTaskWoken will be set to pdTRUE
 inside the xSemaphoreGiveFromISR() function. xHigherPriorityTaskWoken is
 later passed into portEND\_SWITCHING\_ISR(), where a context switch is
 requested if it is pdTRUE. The context switch ensures the interrupt returns
 directly to the unblocked task. */
    xSemaphoreGiveFromISR( xBlockSemaphore, &xHigherPriorityTaskWoken );

    /* Clear the interrupt */
    IFS0CLR = _IFS0_T5IF_MASK;

    /* See comment above the call to xSemaphoreGiveFromISR(). */
    portEND_SWITCHING_ISR( xHigherPriorityTaskWoken );
}
```

**Listing 2: The C portion of an ISR that can cause a context switch**

---

Some notes on the C function:

* The parameter passed to portEND\_SWITCHING\_ISR() should be zero if no
 context switch is required, and non zero if a context switch is required.
 Performing a context switch from inside an interrupt can result in the
 interrupt returning to a task other than the task originally interrupted.
* The C function does not use any special qualifiers or attributes - it is
 just a standard C function.

#### Critical sections

Exiting a critical section will always set the interrupt priority such that all interrupts are enabled, no matter what its level when the critical section
was entered. FreeRTOS API functions themselves will use critical sections.

#### Execution context

In line with the conventions documented in the XC32 compiler manual, the RTOS
kernel assumes all access to the K0 and K1 registers will be atomic. Code generated
by the XC32 compiler conforms to this convention so if you are writing application purely in C then this is of no concern.
Care must be taken however if any hand written assembly code is used to ensure that too conforms to the same convention.

#### Shadow registers

The interrupt shadow registers are not used and are therefore available for use by the host application. Shadow registers should not be used within an interrupt
service routine that causes a context switch.

#### Software interrupts

The RTOS kernel makes use of the MIPS software interrupt 0. This interrupt is therefore not available for use by the application.

#### Memory allocation

Source/Portable/MemMang/heap\_4.c is included in the PIC32 demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.
