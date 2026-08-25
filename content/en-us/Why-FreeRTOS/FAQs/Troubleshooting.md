---
title: Before the FAQ...
created: 2018-09-20
categories:
  - kernel
description: Troubleshoot your FreeRTOS based application
---

The FAQ ["My application does not run, what could be wrong?"](#freertos-faq---my-application-does-not-run-what-could-be-wrong)
follows below. Before that, a couple of helpful notes.


## A note for users of ARM Cortex-M MCUs

Most support requests on ARM Cortex-M microcontrollers result from issues attributed to incorrect interrupt
priority assignment. FreeRTOS V7.5.0 and on-wards includes configASSERT() calls to trap this common source
of user error. Please ensure [configASSERT() is defined](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert) during development.

In addition, the following two online resources are provided:

1. A [page dedicated](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)
   to explaining the ARM Cortex-M interrupt behaviour, and how it relates to the FreeRTOSConfig.h settings
   relevant to interrupt nesting.

2. A page that describes how to debug a ARM Cortex-M [hard fault exception](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Others/Debugging-Hard-Faults-On-Cortex-M-Microcontrollers).


## A note about configASSERT()

The [configASSERT() macro](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert) is provided to help trap user errors. Please ensure
configASSERT() is defined while developing or debugging your FreeRTOS application.


## Other help resources

After reading this FAQ, if you are still having issues, other support resources include
the [quick start guide](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/02-Quick-start-guide) (which includes links to useful pages within the
FreeRTOS.org web site), and the [official support system](https://forums.freertos.org/).


## FreeRTOS FAQ - My application does not run, what could be wrong?

I don't know - its your application - but here are some common solutions:


### The application I created compiles, but does not run

Each official FreeRTOS port comes with an official demo that (at least at the time of its creation)
compiles and executes on the hardware platform on which it was developed without any modification.
The demo projects are provided to ensure new users can get started with FreeRTOS in the quickest
possible time, and with the minimum of fuss. It is always recommended that a new FreeRTOS project
is created by starting with, and then adapting, one of the provided pre-configured demos. Doing this
ensures the new project includes all the necessary source and header files, and installs the necessary
interrupt service routines, with no effort on the part of the project's creator.

If the project you have created is compiling, and at least executing up to the point that the scheduler
is started, but only a single task is executing or no tasks are executing at all after the call
to [vTaskStartScheduler()](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/03-vTaskStartScheduler),
then it is likely that the interrupt vector table is incorrect.

All FreeRTOS ports use a timer interrupt, and some FreeRTOS ports use multiple interrupts. Use the
provided demo projects as an example.

**Special note to ARM Cortex-M users:** ARM Cortex-M3, ARM Cortex-M4 and ARM Cortex-M4F ports need
FreeRTOS handlers to be installed on the SysTick, PendSV and SVCCall interrupt vectors. The vector
table can be populated directly with the FreeRTOS defined xPortSysTickHandler(), xPortPendSVHandler()
and vPortSVCHandler() functions respectively, or, if the interrupt vector table is CMSIS compliant,
the following three lines can be added to FreeRTOSConfig.h to map the FreeRTOS function names to
their CMSIS equivalents:

```c
#define vPortSVCHandler SVC_Handler
#define xPortPendSVHandler PendSV_Handler
#define xPortSysTickHandler SysTick_Handler
```

Using #defines in this way will only work if the default handlers provided by your development tools
are defined as [weak symbols](http://en.wikipedia.org/wiki/Weak_symbol). If the default handlers are
not defined as week symbols they must be either commented out or deleted.


### Task stacks

[see also
the [uxTaskGetStackHighWaterMark()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/04-uxTaskGetStackHighWaterMark)
API function, and
the [stack overflow detection](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking) options]. Stack overflow is by
far the most common source of support requests. The size of the stack available to a task is set
using the usStackDepth parameter of the xTaskCreate()
or [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)
API function.

Try increasing the size of the stack allocated to the task that is causing the problem, or reducing
the amount of stack that the task utilises. Don't write interrupt service routines that require a
lot of stack.

Tasks that make calls to any string formatting functions are likely to require a lot of stack -
particularly when using the GCC compiler. Such tasks are particularly prone to stack overflow.

Each byte of the task stack is set to 0xa5 when the task is created, making it relatively simple to
see if a stack overflow has occurred. In addition - the function usTaskCheckFreeStackSpace() in tasks.c
demonstrates how the stack usage can be checked at run time (although this is a somewhat inefficient
function so should only be used for debugging).


### main() stack

The context of main() does not exist after the FreeRTOS scheduler has started as, from that point,
only RTOS tasks and interrupts have a context. To maximise the amount of RAM available to the FreeRTOS
application, and as allowed by the C standard as the context of main() no longer exists, some FreeRTOS
ports re-use the stack allocated to main as the system or interrupt stack. Therefore never allocate
variables or buffers that are needed or in any way accessed by the FreeRTOS application on the stack
used by main() because they are likely to get overwritten.


### Interrupts are not executing

First, be absolutely sure the issue is related to FreeRTOS by trying to use
the interrupt is a simple basic application that is not using FreeRTOS.

If a FreeRTOS API function is called before the scheduler has been started
then interrupts will deliberately be left disabled, and not re-enable again
until the first task starts to execute. This is done to protect the system
from crashes caused by interrupts attempting to use FreeRTOS API functions
during system initialisation, before the scheduler has been started, and
while the scheduler may be in an inconsistent state.

Do not alter the microcontroller interrupt enable bits or priority flags
using any method other than calls to taskENTER\_CRITICAL() and taskEXIT\_CRITICAL().
These macros keep a count of their call nesting depth to ensure interrupts
become enabled again only when the call nesting has unwound completely to
zero. Be aware that some library functions may themselves enable and disable
interrupts.


### I added a simple task to a demo, and now the demo crashes!

Creating a task requires memory to be obtained from
the [kernel heap](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management).
Many of the demo application projects dimension the heap to be just big enough to run the demo tasks - so
not big enough for any further tasks to be added to the project. The idle task is automatically created when
you start the RTOS scheduler. If there is insufficient heap available for the idle task to be created
then vTaskStartScheduler() will return - causing the application to never even start.

To rectify this, [increase the heap space](/Documentation/02-Kernel/03-Supported-devices/02-Customization), or
remove some of the demo application tasks.


### Using API functions within interrupts

Do not use API functions within interrupt service routines unless the name of the API function ends
with "...FromISR()".

**ARM Cortex-M3, ARM Cortex-M4 and ARM Cortex-M7 users - please note -
this is the cause of 95% of support requests on ARM Cortex-M devices:**

(A separate page [is also provided](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)
that explains ARM Cortex-M interrupt priorities, and gives full information on setting ARM Cortex-M interrupt
priorities for use with the powerful FreeRTOS interrupt nesting model.)

API functions must not be called from an interrupt if the interrupt has a priority above the priority
set by configMAX\_SYSCALL\_INTERRUPT\_PRIORITY. Note carefully the following points when setting an
interrupt priority:

* configMAX\_SYSCALL\_INTERRUPT\_PRIORITY is defined in FreeRTOSConfig.h. On ARM Cortex-M3 devices, a
  numerically low interrupt priority value represents a logically high interrupt priority. Do not leave
  an interrupt priority unassigned because it will use priority 0 by default. Priority 0 is the highest
  possible interrupt priority and will be above configMAX\_SYSCALL\_INTERRUPT\_PRIORITY.

* Take care when specifying a priority as different ARM Cortex-M3 implementations use a different number
  of priority bits.

* Internally the ARM Cortex-M3 uses the 'n' most significant bits of a byte to represent an interrupt
  priority, where 'n' is implementation defined as noted above. ARM and various ARM Cortex-M3 licensees
  provide library functions to allow interrupt priorities to be assigned, but some expect the priority
  to be shifted into the most significant bits before the library function is called, whereas others
  will perform the shift internally.

* The bits that define an interrupt priority are split between those that represent the preemption priority,
  and those that represent the sub priority. For greatest simplicity and compatibility, ensure that all the
  priority bits are assigned as 'preemption priority' bits.


### The RTOS scheduler crashes when attempting to start the first task

If you are using an ARM7 target then the processor must be in Supervisor mode when the RTOS scheduler is
started.


### The interrupt enable flag gets set incorrectly

Do not use any method for disabling and enabling interrupts other than calls to
portENTER\_CRITICAL() and portEXIT\_CRITICAL(). These macros keep a count of the call nesting depth
to ensure interrupts only become enabled again when the call nesting has unwound completely to zero.

If a FreeRTOS API function is called before the scheduler has been started then most FreeRTOS ports will
deliberately disable interrupts, and not re-enable them until the first task starts to execute. This is
done to protect the system from crashes caused by interrupts attempting to use FreeRTOS API functions
during system initialization, before the scheduler has been started.


### My application crashes before the RTOS scheduler is even started

A context switch cannot occur until after the RTOS scheduler has started. Any interrupt service routine
that could potentially cause a context switch must therefore not be permitted to execute prior to the
RTOS scheduler being started. The same is true of any interrupt service routine that attempts to send
to or receive from a queue or semaphore.

Many API functions cannot be called prior to the RTOS scheduler being started. It is best to restrict
such usage to the creation of the tasks, queues and semaphores that will be used once the RTOS scheduler
activity has commenced.


### Suspending the RTOS scheduler (calling vTaskSuspendAll()) causes me problems

Do not call API functions while the RTOS scheduler is suspended. Some functions can be used, but not
all. This is not the intended purpose of the suspension mechanism.


### I have created a new application - but it will not compile

Base new applications on the provided demo project file for the port you are using. This way you will
be sure that the correct files are included and the compiler is correctly configured.


### I get stuck on the line that starts for( pxIterator = ( ListItem\_t * ) &( pxList->xListEnd );

Likely causes include:

1. Stack overflow - see [/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking).

2. Incorrect interrupt priority assignment, especially on ARM Cortex-M3 parts where numerically high priority
   values denote low actual interrupt priories, which can seem counter intuitive. See configMAX\_SYSCALL\_INTERRUPT\_PRIORITY
   on [/Documentation/02-Kernel/03-Supported-devices/02-Customization/#kernel\_priority](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority).

3. Calling an API function from within a critical section or when the RTOS scheduler is suspended.


## What else can I do?

1. Check the [list of known issues](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)
   on the download page.
2. Post a description of your problem in the [monitored support forum](https://forums.freertos.org/).
