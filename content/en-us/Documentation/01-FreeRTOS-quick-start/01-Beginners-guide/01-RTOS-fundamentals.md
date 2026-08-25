---
title: "RTOS Fundamentals"
created: 2018-09-20
categories:
  - kernel
description: Links to RTOS concept pages
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS implementation tutorial
    link: /Documentation/02-Kernel/05-RTOS-implementation-tutorial/01-RTOS-implementation/
  - title: Download FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FreeRTOS reference manual
    link: /Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book/

next:
  title: Build your first FreeRTOS project
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project
---

**An overview of real-time operating systems**

## Introduction

A Real-Time Operating System (RTOS) is a type of computer operating system designed to be small and deterministic.
RTOSes are commonly used in embedded systems such as medical devices and automotive ECUs that need to react to external events within strict time constraints.  Typically this class of embedded system only has one or two requirements demanding that level of deterministic timing, and using an RTOS has benefits even when the embedded system has no hard real-time requirement at all.  See the FAQ "[Why use an RTOS?](/Why-FreeRTOS/FAQs/What-is-this-all-about/#why-use-an-rtos)".

An RTOS is typically smaller and lighter weight than a general purpose operating system, making RTOSes suitable
for memory, compute and power constrained devices.


## Multitasking

The **kernel** is the core component within an operating system. General purpose operating systems, such as Linux, employ kernels that allow
multiple users to access the computer's processor seemingly simultaneously. These multiple users can each execute multiple programs apparently concurrently.

Each executing program is implemented by one or more **threads** under control of the operating system. If an operating system can execute multiple threads in this manner it is said to be **multitasking**.  Small RTOSes, like FreeRTOS, normally call threads **tasks** because they don't support virtual memory, so there is no distinction between processes and threads.

The use of a multitasking operating system can simplify the design of what would otherwise be a complex software application:

- The multitasking and inter-task communications features of the operating system allow the complex application to be
  partitioned into a set of smaller and more manageable tasks.
- The partitioning can result in easier software testing, dividing work within teams, and code reuse.
- Complex timing and sequencing details become the responsibility of the RTOS kernel, removing that burden from the application code.

The FAQ "[Why use an RTOS?](/Why-FreeRTOS/FAQs/What-is-this-all-about/#why-use-an-rtos)" provides a more comprehensive list.

## Multitasking Vs Concurrency

A conventional single core processor can only execute a single task at a time - but by rapidly switching between tasks a multitasking operating
system can make it **appear** as if each task is executing concurrently. This is depicted by the diagram below which shows the
execution pattern of three tasks with respect to time. The task names are color coded and written down the left hand side. Time moves
from left to right, with the colored lines showing which task is executing at any particular time. The upper diagram demonstrates
the perceived concurrent execution pattern, and the lower the actual multitasking execution pattern.

![Multitasking execution pattern diagram](/media/2018/TaskExecution.gif)

## Scheduling

The **scheduler** is the part of the kernel responsible for deciding which task should be executing at any particular time. The kernel
can pause and later resume a task many times during the task's lifetime.  If task B replaces task A as the executing task
(task A is paused and task B resumed) then task A is said to have been swapped (or switched) out, and task B swapped (or switched) in.

The **scheduling policy** is the algorithm used by the scheduler to decide which task to execute at any point in time. The policy of
a (non real-time) multi-user system will most likely allow each task a "fair" proportion of processor time. The policy used in real-time embedded systems is described later.

A task will only be swapped out if the scheduling algorithm decides to execute a different task. This can happen without the currently
executing task being aware of it, such as when the scheduling algorithm responds to an external event or timer expiration.  It can also
happen if the executing task explicitly calls an API function that results in it **yielding**, **sleeping** (also called **delaying**), or **blocking**.

If a task yields, the scheduling algorithm could select the same task to execute again. If a task sleeps, it becomes
unavailable for selection until the specified delay period elapses.  Similarly, if a task blocks, it becomes unavailable for selection
until either a specific event occurs (e.g., data arrives on a UART) or a timeout period expires.

The operating system kernel is responsible for managing these task states and transitions, ensuring that the appropriate task is
selected for execution at any given time according to the scheduling algorithm and the current state of each task.


![Task state transitions diagram](/media/2018/suspending.gif)

Referring to the numbers in the diagram above:

- At marker (1), task 1 is executing.
- At marker (2), the kernel swaps task 1 out ...
- ... and at marker (3), swaps task 2 in.
- While it is executing, at marker (4), task 2 locks a processor peripheral for its own exclusive access (not visible in the diagram).
- At marker (5), the kernel swaps task 2 out ...
- ... and at marker (6), swaps task 3 in.
- Task 3 tries to access the processor peripheral previously locked by task 2, and finding it locked, blocks at marker (7) to wait for the peripheral to be unlocked.
- At marker (8), the kernel swaps task 1 in.
- Etc.
- At marker (9), task 2 is executing again, finishes with the peripheral, and unlocks it.
- At marker (10), task 3 is executing again, finds the peripheral accessible, so continues executing until it is swapped out again.

## Real-Time Scheduling

Real-time operating systems (**RTOSes**) achieve multitasking using these same principles - but their objectives are very different
to those of general purpose (non real-time) systems. The different objective is reflected in the scheduling policy. Real-time embedded systems
are designed to provide a timely response to real world events. Events occurring in the real world can have deadlines before which
the real-time embedded system must respond and the RTOS scheduling policy must ensure these deadlines are met.

To achieve this objective using a small RTOS, such as FreeRTOS, the software engineer must assign a priority to each task. The scheduling policy of the RTOS is
then to simply ensure that the highest priority task that is able to execute is the task given processing time. This may optionally include sharing processing time "fairly" between tasks of equal priority if there is more than one task at the same highest priority that are able to run (are not delaying and are not blocked).

This basic form of real-time scheduling isn't magic - it can't slow down or speed up time - the application writer must ensure their timing constraints are feasible to meet with their selected task prioritisation.

### Example

The most basic example of this is a real-time system that incorporates a keypad, LCD and control algorithm.

A user must get visual feedback of each
key press within a reasonable period - if the user cannot see that the key press has been accepted within this period the software
product will at best be awkward to use (soft real-time). If the longest acceptable period was 100ms - any response between 0 and 100ms would be
acceptable. This functionality could be implemented as an autonomous task with the following structure:

```c
void vKeyHandlerTask( void *pvParameters )
{
    // Key handling is a continuous process and as such the task
    // is implemented using an infinite loop (as most real-time
    // tasks are).
    for( ;; )
    {
        [Block to wait for a key press event]
        [Process the key press]
    }
}
```

Now assume the real-time system is also performing a control function that relies on a digitally filtered input. The input must be
sampled, filtered and the control cycle executed every 2ms. For correct operation of the filter the regularity of the sample
must be accurate to 0.5ms. This functionality could be implemented as an autonomous task with the following structure:

```c
void vControlTask( void *pvParameters )
{
    for( ;; )
    {
        [Delay waiting for 2ms since the start of the previous cycle]
        [Sample the input]
        [Filter the sampled input]
        [Perform control algorithm]
        [Output result]
    }
}
```

The software engineer must assign the control task the highest priority as:

1. The deadline for the control task is stricter than that of the key handling task.
2. The consequence of a missed deadline is greater for the control task than for the key handler task.


The diagram below demonstrates how these tasks would be scheduled by a real-time operating system. The RTOS has itself created a task - the **idle** task - which
will execute only when there are no other tasks able to do so. The RTOS idle task is always in a state
where it is able to execute.

![Real-time scheduling example diagram](/media/2018/RTExample.gif)

Referring to the diagram above:

- At the start neither of our two tasks are able to run - vControlTask is waiting for the correct time to start a new control
  cycle and vKeyHandlerTask is waiting for a key to be pressed. Processor time is given to the RTOS idle task.
- At time t1, a key press occurs. vKeyHandlerTask is now able to execute - it has a higher priority than the RTOS idle task
  so is given processor time.
- At time t2 vKeyHandlerTask has completed processing the key and updating the LCD. It cannot continue until another key has
  been pressed so suspends itself and the RTOS idle task is again resumed.
- At time t3 a timer event indicates that it is time to perform the next control cycle. vControlTask can now execute and as
  the highest priority task is scheduled processor time immediately.
- Between time t3 and t4, while vControlTask is still executing, a key press occurs. vKeyHandlerTask is now able to execute,
  but as it has a lower priority than vControlTask it is not scheduled any processor time.
- At t4 vControlTask completes processing the control cycle and cannot restart until the next timer event - it suspends
  itself. vKeyHandlerTask is now the task with the highest priority that is able to run so is scheduled processor time in
  order to process the previous key press.
- At t5 the key press has been processed, and vKeyHandlerTask suspends itself to wait for the next key event. Again neither
  of our tasks are able to execute and the RTOS idle task is scheduled processor time.
- Between t5 and t6 a timer event is processed, but no further key presses occur.
- The next key press occurs at time t6, but before vKeyHandlerTask has completed processing the key a timer event occurs.
  Now both tasks are able to execute. As vControlTask has the higher priority vKeyHandlerTask is suspended before it has
  completed processing the key, and vControlTask is scheduled processor time.
- At t8 vControlTask completes processing the control cycle and suspends itself to wait for the next. vKeyHandlerTask is
  again the highest priority task that is able to run so is scheduled processor time so the key press processing can be
  completed.
