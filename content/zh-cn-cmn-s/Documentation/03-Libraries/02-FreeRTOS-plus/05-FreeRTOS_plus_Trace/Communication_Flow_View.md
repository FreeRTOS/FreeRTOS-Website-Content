---
title: 通信流视图
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[Tracealyzer 视图示例](Example_FreeRTOS_Plus_IO_Views)]


### 可视化

参与者之间的通信路径图（在本示例中，参与者包括 FreeRTOS
任务和中断）。


### 概要

用于进程间通信 (IPC) 的内核对象包括
FreeRTOS 队列和各类信号量。
通信流视图显示了
参与者如何通过 IPC 对象链接。还显示了写入 IPC 对象
的参与者，以及从 IPC 对象读取
的参与者。


### 点击事件

在视图中单击节点时，
将显示有关参与者或 IPC 节点的详细信息。

在视图中双击对象时
会显示 IPC 对象的历史记录。

[![FreeRTOS-Plus-Trace 通信流视图的屏幕截图](/media/2020/4.-Communication-Flow.png)](/media/2020/4.-Communication-Flow.png)
*通信流视图。点击放大*
