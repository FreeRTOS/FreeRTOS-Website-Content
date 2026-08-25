---
title: User Event and Signal Plot View
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[Example Tracealyzer Views](Example_FreeRTOS_Plus_IO_Views)]


### Visualises

User generated events and their associated values with respect to time.


### Synopsis

The trace recorder code includes API functions that allow user definable events, with associated values,
to be generated and triggered from a FreeRTOS application. The user event view shows a plot of user event
values over time.

User events are generated with a call similar to a traditional printf(), allowing up to fifteen data
arguments which may be integers, floats or strings. This is many times faster than a traditional console
printf(), partly because the data does not need to be transferred over a serial cable or similar, and
partly because the formatting is performed offline by the Tracealyzer PC application. A user event is
stored in a matter of microseconds, while a printf() can take several milliseconds. This means user
events can be used in time critical code.

User events can be used to plot values, or mark event occurrences.


### Click Events

The [trace view](Trace_View) corresponding to the clicked time is displayed when a user event is clicked in the view.

[![A screen shot of the FreeRTOS-Plus-Trace user event values over time](/media/2020/7.-User-Event-Signal-Plot.png)](/media/2020/7.-User-Event-Signal-Plot.png)
**The kernel object utilization view. Click to enlarge.**
 **Another event view, with the user events in focus. Click to enlarge.**
