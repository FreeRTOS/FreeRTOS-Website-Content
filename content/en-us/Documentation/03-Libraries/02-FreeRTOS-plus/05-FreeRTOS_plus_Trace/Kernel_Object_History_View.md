---
title: Kernel Object History View
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[Example Tracealyzer Views](Example_FreeRTOS_Plus_IO_Views)]


### Visualises

The events affecting a queue or semaphore over a period of time.


### Synopsis

Kernel objects used for inter-process communication (IPC) include
FreeRTOS queues and the various types of semaphore.
An IPC event is an event that changes
the state of an IPC object, such as a queue read, queue write, queue peek,
semaphore give or semaphore take. The kernel object history view shows
the IPC events that affect a particular IPC object over a period of time.


### Click Events


The [trace view](Trace_View) corresponding to the time at which an event occurred is
displayed when the event is clicked in the kernel object history view.

Send events that correspond to a receive event, or receive events that
correspond to a send event, are located using the buttons on the right
side of the view.

[![A screen shot of the FreeRTOS-Plus-Trace kernel object history view showing queue and semaphore use over time](/media/2020/5.-Object-History.png)](/media/2020/5.-Object-History.png)
*The kernel object history view. (Click to enlarge)*
