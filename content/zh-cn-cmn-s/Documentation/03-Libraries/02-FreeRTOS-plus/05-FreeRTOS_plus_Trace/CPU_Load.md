---
title: CPU 负载视图
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[Tracealyzer 视图示例](Example_FreeRTOS_Plus_IO_Views)]


### 可视化

CPU 上与时间有关的处理负载。


### 概要

时间在水平轴上显示。CPU 负载在
垂直轴上显示。
颜色用于指示
在任何特定时间运行的参与者（在本示例中，参与者
包括 FreeRTOS 任务和中断）。

如同在主跟踪视图中一样，拖动鼠标可调整缩放
级别。使用“分辨率”菜单
调整图形分辨率（或粒度）。分辨率越高，对 CPU 负载的峰值越敏感，
而分辨率越低，则更容易查看整体趋势。


### 点击事件

在图表中单击相应的颜色时，
会显示参与者的名称。

在图表中双击会显示跟踪视图中的相应间隔。

![A screen shot of the FreeRTOS-Plus-Trace CPU load view](/media/2020/3.-CPU-Load-Graph.png)
<br />
*CPU 负载视图显示 CPU 使用率与时间的关系。点击放大。*
