---
title: Communication Flow View
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[Example Tracealyzer Views](Example_FreeRTOS_Plus_IO_Views)]


### Visualises

Communication paths between actors (in this case, actors are both FreeRTOS
tasks and interrupts).


### Synopsis

Kernel objects used for inter-process communication (IPC) include
FreeRTOS queues and the various types of semaphore.
The communication flow view shows how
actors are linked through IPC objects. It displays the actors
that write to an IPC object, and the actors that read from an
IPC object.


### Click Events

Detailed information on an actor or IPC node is displayed
when the node is clicked in the view.

The history of an IPC object is displayed
when the object is double clicked in the view.

[![A screen shot of the FreeRTOS-Plus-Trace communication flow view](/media/2020/4.-Communication-Flow.png)](/media/2020/4.-Communication-Flow.png)
*The communication flow view. Click to enlarge*
