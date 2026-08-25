---
title: CPU Load View
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[Example Tracealyzer Views](Example_FreeRTOS_Plus_IO_Views)]


### Visualises

The processing load on the CPU with respect to time.


### Synopsis

Time is displayed on the horizontal axis. The CPU load is displayed on
the vertical axis.
Colours are used to indicate the
actors that were running at any particular time (in this case, actors are
both FreeRTOS tasks and interrupts).

Just as in the main trace view, dragging the mouse adjusts the zoom
level. The graph resolution (or granularity) is adjusted using the
"Resolution" menu. A higher resolution is more sensitive to spikes in
the CPU load, while a lower resolution makes overall trends easier to view.


### Click Events

The name of an actor is displayed when the corresponding colour is clicked
on the graph.

Double-clicking in the graph shows the corresponding interval in the trace view.

![A screen shot of the FreeRTOS-Plus-Trace CPU load view](/media/2020/3.-CPU-Load-Graph.png)
<br />
*The CPU load view showing the CPU usage against time. Click to enlarge.*
