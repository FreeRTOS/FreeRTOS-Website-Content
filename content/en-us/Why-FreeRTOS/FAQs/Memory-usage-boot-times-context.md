---
title: FreeRTOS FAQ - Memory Usage, Boot Times & Context Switch Times
created: 2018-09-20
description: Information about FreeRTOS memory usage, boot times, and context switch times
---

## How much RAM does FreeRTOS use?

This depends on your application. Below is a guide based on:

- IAR STR71x ARM7 port.
- Full optimisation.
- Minimum configuration
- Four priorities.

| **Item**                       | **Bytes Used**                                                            |
| ------------------------------ | ------------------------------------------------------------------------- |
| Scheduler Itself               | 236 bytes (can easily be reduced by using smaller data types).            |
| For each queue you create, add | 76 bytes + queue storage area (see FAQ Why do queues use that much RAM?)  |
| For each task you create, add  | 64 bytes (includes 4 characters for the task name) + the task stack size. |


## How much ROM/Flash does FreeRTOS use?

This depends on your compiler, architecture, and RTOS kernel configuration.

The RTOS kernel itself required about 5 to 10 KBytes of ROM space when using the same configuration as
stated for the FAQ "How much RAM does FreeRTOS use?".


## How long does FreeRTOS take to boot?

FreeRTOS, OPENRTOS and in most cases SAFERTOS are supplied as source code for static linking into the
users application. The build process therefore results in a single executable binary image. Typically
such an image will include a C start up routine to set up the C run time environment, before calling
main() to execute the users application. The interrupt vector table will also be statically configured
and included at a predetermined location within the same binary.

The list below provides an indication of the sequence of processing booting such a system will require,
along with some guidance on the time required for this processing to complete. Note that any numbers
provided are indicative only and realistic. Actual times achievable will depend on the architecture
being used, the clock frequencies configured, and the configuration of the memory interface.

1. Configure the CPU clocks for the performance level required.

   Typically requires a few register writes, followed by a short delay for clocks to lock. This will take
   in the order of a few microseconds, depending on the architecture being used. This is an optional step.
   It could be performed later from C code but can boost the boot time if it is performed prior to initializing
   memory.

2. Initialize static and global variables that contain only the value zero (bss).

   Including FreeRTOS in an application would typically only add an extra couple of hundred write accesses
   to be performed within a very tight assembly loop. This will add in the region of a few microseconds to
   the time taken when compared to that taken were the RTOS kernel not included.

3. Initialize variables that contain a value other than zero.

   Including FreeRTOS in an application would typically not add any extra time to this step.

4. Perform any other hardware set up required.

   Often it is desirable to configure peripherals prior to starting the RTOS scheduler. How long this takes
   will depend on the complexity of the peripherals being used, but on the class of microcontroller targeted
   by FreeRTOS the total time would typically require a few milliseconds only.

5. Create application queues, semaphores and mutexes.

   Typically the majority of queues, semaphores and mutexes will be created prior to the RTOS scheduler being
   started. By way of example, on a ARM Cortex-M3 device, using the ARM RVDS compiler with optimization set
   to 1 (low), creating a queue, semaphore or mutex will take approximately 500 CPU cycles.

6. Create application tasks.

   Typically the majority of tasks will be created prior to the RTOS scheduler being started. By way of example,
   on a ARM Cortex-M3 device, using the ARM RVDS compiler with optimization set to 1 (low), creating each task
   will take approximately 1100 CPU cycles.

7. Start the RTOS scheduler.

   The RTOS scheduler is started by calling vTaskStartScheduler(). The start up process includes configuring
   the tick interrupt, creating the idle task, and then restoring the context of the first task to run. By
   way of example, on a ARM Cortex-M3 device, using the ARM RVDS compiler with optimization set to 1 (low),
   starting the RTOS scheduler will take approximately 1200 CPU cycles.


## What is the context switch time?

Context switch times are dependent on the port, compiler and configuration. A context switch time of 84
CPU cycles was obtained under the following test conditions:

- FreeRTOS ARM Cortex-M3 port for the Keil compiler
- Stack overflow checking turned off
- Trace features turned off
- Run-time stats feature turned off
- Compiler set to optimise for speed
- [configUSE\_PORT\_OPTIMISED\_TASK\_SELECTION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_port_optimised_task_selection) set
  to 1 in FreeRTOSConfig.h

Notes:

- Under these test conditions the context switch time is not dependent on whether a different task
  was selected to run or the same task was selected to continue running.

- The ARM Cortex-M port performs all task context switches in the PendSV interrupt. The quoted time
  does not include interrupt entry time.

- The quoted time includes a short section of C code. It has been determined that 12 CPU cycles could
  have been saved by providing the entire implementation in assembly code. It is considered that the
  benefit of maintaining a short section of generic C code (for reasons of maintenance, support, robustness,
  automatic inclusion of features such as tracing, etc.) outweighs the benefit of removing 12 CPU cycles
  from the context switch time.

- The Cortex-M CPU registers that are not automatically saved on interrupt entry can be saved with a
  single assembly instruction, then restored again with a further single assembly instruction. These
  two instructions on their own consume 12 CPU cycles.


## Why does my compiler tell me FreeRTOS is consuming all the available RAM?

Three of the [example memory allocation schemes](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)
supplied with FreeRTOS allocate memory from a statically allocated array that is dimensioned by
the [configTOTAL\_HEAP\_SIZE](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configtotal_heap_size) constant in FreeRTOSConfig.h. These are just
normal statically allocated arrays, and therefore appear in the RAM usage figures provided by many tool
chains. The tool chain is in effect showing the heap as consumed RAM, even though at that point the heap
is completely free as no memory has actually been allocated.

C applications require some RAM for things like static variables, buffers, etc. but will rarely use
all the RAM available on a microcontroller. Many of the FreeRTOS demo applications dimension the heap to
use up all the RAM that is left over, making it appear as if the application is using all the RAM available.


## Why do queues use that much RAM?

Event management is built into the queue functionality. This means the queue data structures contain
all the RAM that other RTOS systems sometimes allocate separately. There is no concept of an event control
block within FreeRTOS.


## How can I reduce the amount of RAM used?

- [FreeRTOS-Plus-Trace](/Documentation/03-Libraries/02-FreeRTOS-plus/05-FreeRTOS_plus_Trace/00-FreeRTOS_Plus_Trace) can trace memory
  allocation and memory free events, and so be useful in analysing and therefore optimising memory usage.

- In most cases [direct to task notifications](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications) can be used in place of
  binary semaphores. Unlike binary semaphores, which are generic objects that have to be created, direct
  to task notifications are sent directly to a task and do not use any RAM.

- Each flag (bit) in an [event group](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups) can be used as
  a [binary semaphore](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/), so replace multiple binary semaphores with
  a single event group.

- Use the [uxTaskGetStackHighWaterMark()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/04-uxTaskGetStackHighWaterMark)   function to see which tasks can be allocated a smaller stack.

- Use the xPortGetFreeHeapSize() and (where available) the xPortGetMinimumEverFreeHeapSize() API functions
  to see how much FreeRTOS heap is being allocated but never used, and
  adjust [accordingly.](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configtotal_heap_size).

- If [heap\_1.c, heap\_2.c, heap\_4.c or heap\_5.c](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)
  are being used, and nothing in your application is ever calling malloc() directly (as opposed to pvPortMalloc()),
  then ensure the linker is not allocated a heap to the C library because it will never get used.

- Set configMAX\_PRIORITIES and configMINIMAL\_STACK\_SIZE (found in portmacro.h) to the minimum values
  acceptable to your application.

- Recover the stack used by main(). The stack used upon program entry is not required once the RTOS
  scheduler has been started (unless your application calls vTaskEndScheduler(), which is only supported
  directly in the distribution for the PC and Flashlite ports, or uses the stack as an interrupt stack
  as is done in the ARM Cortex-M and RX ports). Every task has its own stack allocated so the stack
  allocated to main() is available for reuse once the RTOS scheduler has started.

- Minimise the stack used by main(). The idle task is automatically created when you create the first
  application task. The stack used upon program entry (before the RTOS scheduler has started) must
  therefore be large enough for a nested call to
  xTaskCreate() (or [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)).
  Creating the idle task manually can half this stack requirement. To create the idle task manually:

  1. Locate the function prvInitialiseTaskLists() in Sourcetasks.c.
  2. The idle task is created at the bottom of the function by a call to xTaskCreate(). Cut this line
     from Sourcetasks.c and paste it into main().

- Rationalise the number of tasks. The idle task is not required if:

  1. Your application has a task that never blocks, and ...
  2. Your application does not make any calls to vTaskDelete().

- Reduce the data size used by the definition BaseType\_t (this can increase execution time).

- There are other minor tweaks that can be performed (for example the task priority queues don't require
  event management), but if you get down to this level - you need more RAM!


## Why does my compiler tell me FreeRTOS is using much more ROM than you claim it requires?

The quoted ROM/Flash footprint figures are genuine. If you write a tiny FreeRTOS test program and it
appears to consume more ROM than expected then it is probably because of the libraries that are being
included in your build, not because of FreeRTOS. In particular, GCC string handling and any floating point
library is going to bloat your code.

FreeRTOS includes a very cut down open source implementation of many string handling functions in a file
called printf-stdarg.c. Including this in your project can greatly reduce both the amount of ROM used by
the build, and the size of the stack required to be allocated to any task making a string handling library
call (sprintf() for example). Note that printf-stdarg.c is open source, but not covered by the FreeRTOS
license. Ensure you are happy with the license conditions stated in the file itself before use.

Also, most linkers will remove unused code by default, but the GNU linker will only remove unused code
if you explicitly tell it to.

Check the output .map file to find exactly how ROM/Flash is being used.


## How is RAM allocated to tasks?

If a task is created using the [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)
API function then the RAM required by the task is provided by the application writer, and no memory
allocation occurs.

If a task is created using the [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate/)
API function then the RAM required by the task is allocated inside the xTaskCreate() API function from
the [FreeRTOS heap](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management).

The stack used by main() is not used by tasks, but (depending on the port) may be used by interrupts.


## How is RAM allocated to queues?

If a queue is created using the [xQueueCreateStatic()](/Documentation/02-Kernel/04-API-references/06-Queues/02-xQueueCreateStatic)
API function then the RAM required by the queue is provided by the application writer, and no memory
allocation occurs.

If a queue is created using the [xQueueCreate()](/Documentation/02-Kernel/04-API-references/06-Queues/01-xQueueCreate)
API function then the RAM required by the queue is allocated inside the xQueueCreate() API function from
the [FreeRTOS heap](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management).


## How big should the stack be?

Tasks can be created using either the [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate/)
or [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)
API function. The function's usStackDepth parameter specifies the size of the stack that will be allocated
to the task being created (in words, not bytes!). It is common for people to ask how to determine the
usStackDepth value, but, except in one way described below, there is little difference between determining
how much stack is required when using an RTOS than when writing a bare metal application (an application
that does not use an operating system).

Exactly as when writing a bare metal application, the amount of stack required is dependent on the
following application specific parameters:

- The function call nesting depth
- The number and size of function scope variable declarations
- The number of function parameters
- The processor architecture
- The compiler
- The compiler optimisation level
- The stack requirements of interrupt service routines - which for many RTOS ports is zero as the RTOS
  will switch to use a dedicated interrupt stack on entry to an interrupt service routine.

The processor context is saved onto a task's stack each time the scheduler temporarily stops running the
task in order to run a different task. The saved processor context is then popped off the task's stack the
next time the task runs. The stack space required to save the processor context is the only addition to
a task's stack requirement that comes from the RTOS itself.

While it is not easy to determine how much stack to allocate a task, the RTOS does provide functionality
that allows a task's stack size to be tuned taking a pragmatic trial and error approach;
the [uxTaskGetStackHighWaterMark()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/04-uxTaskGetStackHighWaterMark)
API function can be used to see how much stack has actually been used, allowing the stack size to be reduced
if more was allocated than necessary, and the [stack overflow detection](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking)
features can be used to determine if a stack is too small. In addition, the stack usages of all the RTOS
tasks can be viewed at once using
the [uxTaskGetSystemState()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/01-uxTaskGetSystemState)
API function, or one of the numerous FreeRTOS aware IDE plug-ins.

The FreeRTOS download contains a demo application for each port, and the FreeRTOSConfig.h file provided
with each demo application defines a constant called [configMINIMAL\_STACK\_SIZE](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configminimal_stack_size).
It is strongly recommended to never allocate a task a stack that is smaller than the
configMINIMAL\_STACK\_SIZE setting used in the port's demo application.

See also [Erich Styger's blog post on using the GNU stack analysis tool](http://mcuoneclipse.com/2015/08/21/gnu-static-stack-usage-analysis/).
