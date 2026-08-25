---
title: Kernel Object Utilisation View
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[Example Tracealyzer Views](Example_FreeRTOS_Plus_IO_Views)]


### Visualises

The number of messages present in a queue or semaphore over time.


### Synopsis

Kernel objects used for inter-process communication (IPC) include FreeRTOS queues and the various types
of semaphore. The number of items in a queue is incremented each time the queue is successfully written
to, and decremented each time the queue is successfully read from. In the same way, the count associated
with a semaphore is incremented each time the semaphore is successfully 'given', and decremented each
time the semaphore is successfully 'taken'. The kernel object utilisation view shows the count associated
with a queue or semaphore over a period of time.


### Click Events

The [trace view](Trace_View) corresponding to the clicked time is displayed when the view is clicked.

[![A screen shot of the FreeRTOS-Plus-Trace kernel object utilisation view showing the number of messages in a queue or semaphore over time](/media/2020/6.-Object-Utilization.png)](/media/2020/6.-Object-Utilization.png)
*The kernel object utilisation view. (Click to enlarge).*
