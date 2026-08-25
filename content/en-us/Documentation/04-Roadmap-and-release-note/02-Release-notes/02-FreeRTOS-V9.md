---
title: "FreeRTOS Version 9"
created: 2018-09-20
categories:
  - roadmap and release notes
description: Information on FreeRTOS Version 9
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: Beginner's guide to FreeRTOS
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: Download FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FAQs
    link: /Why-FreeRTOS/FAQs
---


### Preamble

See the [change history](/Documentation/04-Roadmap-and-release-note/02-Release-notes/00-Release-history) for full information on the differences between the final FreeRTOS
V9.0.0 release and its preceding release candidates - especially relating to the prototype of the
new [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)
API function.


### FreeRTOS V9 Highlights

#### Backward Compatibility

FreeRTOS V9.x.x is a drop-in compatible replacement for FreeRTOS V8.x.x that contains
new features, enhancements, and new ports.


#### Completely Statically Allocated Systems

Two new configuration constants that allow FreeRTOS to optionally be
used [without the necessity for any dynamic memory allocation](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)
have been introduced. See the description of
the [configSUPPORT\_STATIC\_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_static_allocation)
and [configSUPPORT\_DYNAMIC\_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_dynamic_allocation) constants for more
information - noting in particular the two callback functions that need to be provided by the application
writer when configSUPPORT\_STATIC\_ALLOCATION is set to 1.

The [Win32 demo located in the /FreeRTOS/demo/WIN32-MSVC-Static-Allocation-Only directory](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/04-Static-allocation-demo)
is provided as a reference of how to create a project that does not include
a [FreeRTOS heap](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)
at all, and therefore guarantee no dynamic memory allocation is being performed.


#### Creating Tasks and Other RTOS Objects Using Statically Allocated RAM

Also see the [Static Vs Dynamic Memory Allocation](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation) page]

Each [object]Create() RTOS API function now has a new [object]CreateStatic()
equivalent. The simpler Create() function will use dynamic
memory allocation, and the more powerful CreateStatic() function will
use memory passed into the function by the application writer. This allows
tasks, queues, semaphores, software timers, mutexes and event groups to be created
using either statically allocated or dynamically allocated memory.
For example:


* [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate)
  will [dynamically allocate](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)
  the memory necessary to create a
  task. [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)
  will not perform any dynamic memory allocation, and will instead use the memory passed into the function
  using the function's parameters.

* [xQueueCreate()](/Documentation/02-Kernel/04-API-references/06-Queues/01-xQueueCreate) will dynamically
  allocate the memory necessary to create a
  queue. [xQueueCreateStatic()](/Documentation/02-Kernel/04-API-references/06-Queues/02-xQueueCreateStatic)
  will not perform any dynamic memory allocation, and will instead use the memory passed into the function
  using the function's parameters.

* Likewise, an event group can be created using either
  [xEventGroupCreate()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate)
  or [xEventGroupCreateStatic()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/02-xEventGroupCreateStatic),
  a software timer can be created using either [xTimerCreate()](/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate/)
  or [xTimerCreateStatic()](/Documentation/02-Kernel/04-API-references/06-Queues/02-xQueueCreateStatic),
  binary semaphores can be created
  using [xSemaphoreCreateBinary()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/01-xSemaphoreCreateBinary)
  or [xSemaphoreCreateBinaryStatic()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/02-xSemaphoreCreateBinaryStatic),
  counting semaphores can be created using either [xSemaphoreCreateCounting()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/04-xSemaphoreCreateCounting)
  or [xSemaphoreCreateCountingStatic()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/05-xSemaphoreCreateCountingStatic),
  and mutexes can be created using either [xSemaphoreCreateMutex()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/06-xSemaphoreCreateMutex)
  or [xSemaphoreCreateMutexStatic()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/07-xSemaphoreCreateMutexStatic).

configSUPPORT\_DYNAMIC\_ALLOCATION must be set to 1 in FreeRTOSConfig.h (or left
undefined, as it defaults to 1) for the "dynamic" versions of the create functions
to be available.

configSUPPORT\_STATIC\_ALLOCATION must be set to 1 in FreeRTOSConfig.h for the "static"
versions of the create functions to be available - also note the requirement for
the application writer to provide two callback functions
when [configSUPPORT\_STATIC\_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_static_allocation)
is set to 1.

The [StaticAllocation.c](https://sourceforge.net/p/freertos/code/HEAD/tree/trunk/FreeRTOS/Demo/Common/Minimal/StaticAllocation.c)
standard demo task is provided to demonstrate how the new CreateStatic() functions are used.


#### Forcing an RTOS Task To Leave the Blocked State

RTOS tasks enter the Blocked state to ensure they do not use any processing time
while they are waiting for a time to pass, or an event to occur. For example, if
a task calls [vTaskDelay](/Documentation/02-Kernel/04-API-references/02-Task-control/02-vTaskDelayUntil)( 100 ) it will
enter the Blocked state for 100 ticks. As
another example, if a task calls [xSemaphoreTake](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake)( xSemaphore, 50 )
then it will enter the Blocked state until either the semaphore becomes available,
or it times out because 50 ticks pass without the semaphore becoming available.
[Note: in a real application it is better to use the pdMS\_TO\_TICKS() macro to
specify time in millisconds rather than ticks].

The new [xTaskAbortDelay](/Documentation/02-Kernel/04-API-references/02-Task-control/10-xTaskAbortDelay)() RTOS API function makes it possible for one task to
force another task out of the Blocked state immediately. This is desirable in
situations where an event occurring elsewhere in the system means the task in
the Blocked state should stop waiting for an event, or the task in the Blocked
state has something more urgent to do.

INCLUDE\_xTaskAbortDelay must be set to 1 in FreeRTOSConfig.h for the
xTaskAbortDelay() function to be available.

The [AbortDelay.c](https://sourceforge.net/p/freertos/code/HEAD/tree/trunk/FreeRTOS/Demo/Common/Minimal/AbortDelay.c)
standard demo task is provided to demonstrate how xTaskAbortDelay() is used.


#### Deleting Tasks

In FreeRTOS versions prior to version 9, whenever a task was deleted, the memory
allocated by FreeRTOS to the task is freed by the Idle task. In FreeRTOS version 9,
if one task deletes another task, then the memory allocated by FreeRTOS to the
deleted task is freed immediately. However, if a task deletes itself, then the
memory allocated by FreeRTOS to the task is still freed by the Idle task.
Note that, in all cases, it is only the stack and task control block (TCB) allocated
to the task by the RTOS that get freed automatically.


#### Obtaining a Task Handle from the Task Name

The new [xTaskGetHandle](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgethandle)() API function
obtains a task handle from the task's human readable text name.

xTaskGetHandle() uses multiple string compare operations, so it is
recommended that it is called only once per task. The handle returned by
xTaskGetHandle() can then be stored locally for later re-use.


### Other Changes

See the [change history](/Documentation/04-Roadmap-and-release-note/02-Release-notes/00-Release-history) for more detailed information.

* Updates necessary to allow FreeRTOS to run on 64-bit architectures.

* Enhancements to the GCC ARM Cortex-A port layer relating to how the port
  uses the floating point unit.

* Update the ARM Cortex-M RTOS ports that use the memory protection using (MPU).

* Added vApplicationDaemonTaskStartupHook() which executes when the RTOS
  daemon task (which used to be called the timer service task) starts
  running. This is useful if the application includes initialisation code
  that would benefit from executing after the scheduler has been started.

* Added the pcQueueGetName() API function, which obtains the name of
  a queue from the queue's handle.

* Tickless idling (for low power applications) can now also be used when configUSE\_PREEMPTION is 0.

* If a task notification is used to unblock a task from an ISR, but the
  xHigherPriorityTaskWoken parameter is not used, then pend a context switch
  that will then occur during the next tick interrupt.

* Heap\_1.c and Heap\_2.c now use the [configAPPLICATION\_ALLOCATED\_HEAP](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configapplication_allocated_heap)
  settings, which previously was only used by heap\_4.c.
  configAPPLICATION\_ALLOCATED\_HEAP allows the application writer to declare
  the array that will be used as the FreeRTOS heap, and in-so-doing,
  place the heap at a specific memory location.

* The TaskStatus\_t structure, which is used to obtain details of a task, now includes the base address of the task's stack.

* Added the vTaskGetInfo() API function, which returns a TaskStatus\_t structure that contains information about a single task.
  Previously this information could only be obtained for all the tasks at once, as an array of TaskStatus\_t structures.

* Added the uxSemaphoreGetCount() API function.

* Replicate previous Cortex-M4F and Cortex-M7 optimisations in some Cortex-M3 port layers.

* General refactoring.

* Multiple additional devices supported.
