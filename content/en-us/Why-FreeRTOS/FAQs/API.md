---
title: FreeRTOS FAQ - FreeRTOS API
created: 2018-09-20
description: Frequently asked questions about the FreeRTOS API.
---

## Why are there so many API functions?

There are several reasons for this:

1. FreeRTOS has been around since before 2004, has a huge user base, and its road map is driven by those
   users. If enough users request a capability that requires a new API, then we add the API.

1. We chose to separate the API used within tasks from that used within interrupts. See the
   FAQ "[Why is there a separate API for use in interrupts?](#why-is-there-a-separate-api-for-use-in-interrupts)" for the rationale.

1. We rarely (not for many years) break backward compatibility to ensure new FreeRTOS versions are
   backward compatible with older FreeRTOS versions. That means we will add a new API function instead
   of breaking backward compatibility by changing an existing API function. For example, earlier versions
   of FreeRTOS did not include an option to allocated RTOS objects statically, so when that
   capability was added, we added additional APIs for static allocation.


## Why is there a separate API for use in interrupts?

In summary, simplicity and efficiency. We do however understand there are trade offs to both having a
single API for use in interrupts and tasks, and having separate APIs for use in interrupts and tasks.

Having separate APIs means:

1. API functions designed for use in interrupts are optimized for that use case; they do not need to
   programmatically check if they are being called from an interrupt, they do not need to take different
   actions depending on whether they are being called from an interrupt or task context, and they do
   not need parameters (such as block times) that are required when they are called from a task context
   but are obsolete when they are called from an interrupt context.

1. There is no need to have special interrupt entry code (such as keeping count of the interrupt nesting
   depth, or setting a flag to indicate an interrupt context).

1. There is no need to have the application writer take any specific steps, or add any additional code,
   when implementing an interrupt service routine.


## Why do APIs for use in ISRs set xHigherPriorityTaskWoken rather than actually perform a context switch?

In summary, to empower the application writer to decide if a context switch is necessary, and in so
doing, enabling the application writer to prevent unnecessary context switch thrashing.

As an example, imagine a simple interrupt service routine that receives strings character by character.
Rather then performing a context switch after each character it might be more efficient to only perform
a context switch once the entire string has been received.


## Why are semaphores as large as queues? How do I use semaphores efficiently?

The original version of FreeRTOS was developed before 2004, at which time simplicity of use and minimizing
code size were two primary design objectives. At that time, [FreeRTOS queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/) were
the primary inter task communication method.  [FreeRTOS Semaphore](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores) functionality
was then added by defining macros that used the pre-existing queue functionality - achieving the objective of
minimising code size (semaphore functionality didn't increase the code size), but at the cost of semaphores
being larger and slower than might be expected.

While minimising code size is still important, it is no longer the primary objective. We therefore looked
at providing our users with smaller and faster options. However, rather then re-implementing semaphores,
we instead optimized for the primary semaphore use cases, and
introduced [direct to task notifications](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications). In most cases, a direct to task
notification can be used in place of a semaphore. As direct to task notifications do not use an intermediate
object (a semaphore, or whatever) they are much faster and use less RAM.

If your use case is outside of an interrupt[^1] then  [Event groups](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups) offer
another efficient alternative so semaphores because event groups are not only small, but a single event
group can be used as up to 24 different binary semaphores.

[^1]: To explain the caveat about only using event groups as an alternative to semaphores when outside
of an interrupt: FreeRTOS has a policy of not performing non deterministic operations from inside a
critical section or inside an interrupt. Event groups are a broadcast mechanism as they can unblock
more than one task - and as such are not deterministic as it is not known in advance how many tasks
will be unblocked. Therefore event group operations performed in interrupts are deferred to the RTOS
daemon task, requiring an additional context switch to the RTOS daemon task.


## Why can't a task delete itself by exiting its implementing function?

To save stack space.

The original version of FreeRTOS was developed before 2004, when microcontrollers had a lot less memory.
Enabling a task to delete itself by simply running of the end of its implementing function, or exiting,
required the task to return to a function that would then clean up the memory used by the task, and a
pointer to that function along with associated parameters would need to be on the task's stack.

Recent versions of FreeRTOS will hit an assert() if a task exits incorrectly.

## Why does my delay of N ticks not result in exactly N periods of delay?

Please see [Tick Resolution](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/11-Tick-Resolution).
