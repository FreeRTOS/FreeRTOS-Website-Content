---
title: 用户事件和信号绘图视图
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[Tracealyzer 视图示例](Example_FreeRTOS_Plus_IO_Views)]

### 可视化

用户生成的事件及其与时间相关的关联值。


### 概要

跟踪记录器代码包括一些 API 函数，这些函数允许
从 FreeRTOS 应用程序生成和触发具有关联值的用户可定义事件。用户事件视图展示了用户事件值
随时间的变化情况。

用户事件通过类似传统 printf() 的调用来生成，最多允许传递 15 个数据实参，
这些实参可以是整数、浮点数或字符串。这比传统的控制台 printf() 快得多，
部分原因是数据不需要通过串行电缆或类似方式传输，
部分原因是格式化工作由 Tracealyzer PC 应用程序离线完成。用户事件的
存储时间仅为微秒级别，而 printf() 可能需要几毫秒。这意味着用户
事件可以在时间关键型代码中使用。

用户事件可用于绘制值或标记事件发生。


### 点击事件

在视图中点击用户事件时，将显示与点击时间相对应的[跟踪视图](Trace_View)。

[![FreeRTOS-Plus-Trace 用户事件值随时间变化的截图](/media/2020/7.-User-Event-Signal-Plot.png)](/media/2020/7.-User-Event-Signal-Plot.png)
**内核对象 ** **利用率****视图。点击放大。**
 **另一个事件视图，其中用户事件为焦点。点击放大。**
