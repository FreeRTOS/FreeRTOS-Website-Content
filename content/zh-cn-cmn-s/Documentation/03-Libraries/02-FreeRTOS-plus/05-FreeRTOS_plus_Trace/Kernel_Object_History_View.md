---
title: 内核对象历史视图
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[Tracealyzer 视图示例](Example_FreeRTOS_Plus_IO_Views)]


### 可视化

在一段时间内影响队列或信号量的事件。


### 概要

用于进程间通信 (IPC) 的内核对象包括
FreeRTOS 队列和各类信号量。
IPC 事件是指变更 IPC 对象状态的事件，
例如队列读取、队列写入、队列窥视、
信号量给定 (give) 或信号量获得 (take)。内核对象历史视图显示
在一段时间内影响特定 IPC 对象的 IPC 事件。


### 点击事件


在内核对象历史视图中单击某个事件时，将显示与该事件发生时间相对应的[跟踪视图](Trace_View)。
将在内核对象历史视图中点击事件时显示。

与接收事件对应的发送事件
或与发送事件对应的接收事件，
均可使用视图右侧的按钮定位。

[![FreeRTOS-Plus-Trace 内核对象历史视图的屏幕截图，显示随时间推移的队列和信号量使用情况](/media/2020/5.-Object-History.png)](/media/2020/5.-Object-History.png)
*内核对象历史视图。（点击放大）*
