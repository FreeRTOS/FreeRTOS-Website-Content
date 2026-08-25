---
title: FreeRTOS FAQ - What is This All About?
created: 2018-09-20
description: General information about FreeRTOS
---

## What is a Real Time Operating System?

Reading the [FreeRTOS Tutorial Book](/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book) will go a
long way to answering this question.

See the page "[what is an RTOS](/Why-FreeRTOS/What-is-FreeRTOS)" for a more detailed
explanation than provided here.

A Real Time Operating System is an operating system that is optimised for use in embedded/real time
applications. Their primary objective is to ensure a timely and deterministic response to events. An
event can be external, like a limit switch being hit, or internal like a character being received.

Using a real time operating system allows a software application to be written as a set of independent
tasks. Each task is assigned a priority and it is the responsibility of the Real Time Operating System to
ensure that the task with the highest priority that is able to run is the task that is running. Examples
of when a task may not be able to run include when a task is waiting for an external event to occur,
or when a task is waiting for a fixed time period.


## What is a Real Time Kernel?

See the page "[what is an RTOS](/Why-FreeRTOS/What-is-FreeRTOS)" for a more detailed
explanation than provided here.

A Real Time Operating System can provide many resources to application writers - including TCP/IP stacks,
files systems, etc. The Kernel is the part of the operating system that is responsible for task management,
and intertask communication and synchronisation. FreeRTOS is a real time kernel.


## What is a Real Time Scheduler?

See the page "[what is an RTOS](/Why-FreeRTOS/What-is-FreeRTOS)" for a more detailed
explanation than provided here.

Real Time Scheduler and Real Time Kernel are sometimes used interchangeably. Specifically, the Real
Time Scheduler is the part of the RTOS kernel that is responsible for deciding which task should be
executing.


## How do I use FreeRTOS?

Reading one of the [FreeRTOS Tutorial Books](/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book) will go a long way to answering
this question.

FreeRTOS is supplied as source code. The source code should be included in your application project.
Doing so makes the public API interface available to your application source code.

When using FreeRTOS your application should be written as a set of independent tasks. This means your
main() function does not contain the application functionality, but instead creates the application tasks,
then starts the RTOS kernel. See the main.c and project files (makefile or equivalent) included with
each port for examples.

Much more information is provided on the [Creating a New FreeRTOS Application](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project/)
page.


## How do I get started?

See the [FreeRTOS Quick Start Guide](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/02-Quick-start-guide).


## Why use an RTOS?

You do not need to use an RTOS to write good embedded software. At some point though, as your application
grows in size or complexity, the services of an RTOS might become beneficial for one or more of the reasons
listed below. These are not absolutes, but opinion. As with everything else, selecting the right tools for
the job in hand is an important first step in any project.

In brief:

* Abstract out timing information

  The real time scheduler is effectively a piece of code that allows you to specify the timing
  characteristics of your application - permitting greatly simplified, smaller (and therefore easier
  to understand) application code.

* Maintainability/Extensibility

  Not having the timing information within your code allows for greater maintainability and extensibility
  as there will be fewer interdependencies between your software modules. Changing one module should not
  effect the temporal behaviour of another module (depending on the prioritisation of your tasks). The
  software will also be less susceptible to changes in the hardware. For example, code can be written
  such that it is temporally unaffected by a change in the processor frequency (within reasonable limits).

* Modularity

  Organising your application as a set of autonomous tasks permits more effective modularity. Tasks should
  be loosely coupled and functionally cohesive units that within themselves execute in a sequential manner.
  For example, there will be no need to break functions up into mini state machines to prevent them taking
  too long to execute to completion.

* Cleaner interfaces

  Well defined inter task communication interfaces facilitates design and team development.

* Easier testing (in some cases)

  Task interfaces can be exercised without the need to add instrumentation that may have changed the
  behaviour of the module under test.

* Code reuse

  Greater modularity and less module interdependencies facilitates code reuse across projects. The tasks
  themselves facilitate code reuse within a project. For an example of the latter, consider an application
  that receives connections from a TCP/IP stack - the same task code can be spawned to handle each connection -
  one task per connection.

* Improved efficiency?

  Using FreeRTOS permits a task to block on events - be they temporal or external to the system. This means
  that no time is wasted polling or checking timers when there are actually no events that require processing.
  This can result in huge savings in processor utilisation. Code only executes when it needs to. Counter to
  that however is the need to run the RTOS tick and the time taken to switch between tasks. Whether the saving
  outweighs the overhead or vice versa is dependent of the application. Most applications will run some form
  of tick anyway, so making use of this with a tick hook function removes any additional overhead.

* Idle time

  It is easy to measure the processor loading when using FreeRTOS.org. Whenever the idle task is running
  you know that the processor has nothing else to do. The idle task also provides a very simple and automatic
  method of placing the processor into a low power mode.

* Flexible interrupt handling

  Deferring the processing triggered by an interrupt to the task level permits the interrupt handler
  itself to be very short - and for interrupts to remain enabled while the task level processing completes.
  Also, processing at the task level permits flexible prioritisation - more so than might be achievable
  by using the priority assigned to each peripheral by the hardware itself (depending on the architecture
  being used).

* Mixed processing requirements

  Simple design patterns can be used to achieve a mix of periodic, continuous and event driven processing
  within your application. In addition, hard and soft real time requirements can be met though the use of
  interrupt and task prioritisation.

* Easier control over peripherals

  Gatekeeper tasks facilitate serialisation of access to peripherals - and provide a good mutual exclusion
  mechanism.

* Etcetera
