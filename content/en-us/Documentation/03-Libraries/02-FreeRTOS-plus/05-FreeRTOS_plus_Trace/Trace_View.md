---
title: Trace View
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[Example Tracealyzer Views](Example_FreeRTOS_Plus_IO_Views)]


### Visualises

The execution pattern of FreeRTOS tasks, interrupts and events with respect to time.


### Synopsis

The trace view shows task scheduling, interrupts and events against time.

Time is shown on the vertical axis. Tasks are shown in the left trace column. Interrupts are shown in
the right trace column. Indentation within a column shows task or interrupt pre-emption. Actor names
are shown on the left side (in this case, actors are both tasks and interrupts). Labels show kernel
calls and user events.


### Click Events

Mouse events are described on the [Trace with Zoom](Trace_With_Zoom_View) page.


[![A screen shot of the FreeRTOS-Plus-Trace trace view](/media/2020/1.-Trace-view.png)](/media/2020/1.-Trace-view.png)
*The Tracealyzer trace view, showing task scheduling, interrupts and events. Click to enlarge.*
