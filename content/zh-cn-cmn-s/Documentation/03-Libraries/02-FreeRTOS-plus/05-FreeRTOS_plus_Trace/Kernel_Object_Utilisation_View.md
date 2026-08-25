---
title: 内核对象利用率视图
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[Tracealyzer 视图示例](Example_FreeRTOS_Plus_IO_Views)]


### 可视化

随着时间的推移，队列或信号量中存在的消息数。


### 概要

用于进程间通信 (IPC) 的内核对象包括 FreeRTOS 队列和各种类型的
信号量。每次成功写入队列时，队列中的项目数都会增加，
每次成功读取队列时会减少。同样，
每次成功“给予”一个信号量时，与该信号量相关的计数就会递增，
而每次成功“获取”一个信号量时，计数就会递减。内核对象利用率视图显示了一段时间内
与队列或信号量相关的计数。


### 点击事件

单击视图时，将显示与所单击时间相对应的[追踪视图](Trace_View)。

[![显示了队列或信号量中的消息数量随时间变化的 FreeRTOS-Plus-Trace 内核对象利用率视图的屏幕截图](/media/2020/6.-Object-Utilization.png)](/media/2020/6.-Object-Utilization.png)
*内核对象利用率视图。（点击放大）。*
