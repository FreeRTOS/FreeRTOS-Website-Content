---
title: Tracealyzer™
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 适用于 FreeRTOS 的 Percepio View
    link: /Documentation/03-Libraries/02-FreeRTOS-plus/05-FreeRTOS_plus_Trace/01-Percepio_View
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---
 
针对 FreeRTOS 应用程序运行时行为提供前所未有的可视性
<br />

![](/media/2020/graphical-interconnected.gif)


**Tracealyzer 介绍视频**

```jsx
<div style={{ display: 'flex', gap: '10px' }}>
<TraceButton link="https://percepio.com/tracealyzer/download-tracealyzer/" text="Download Tracealyzer"/>
<TraceButton link="https://percepio.com/tracealyzer/freertostrace/" image="/media/2020/Logo_RGB_NEG.png"/>
</div>
```

## 引言

FreeRTOS 内核提供实时多线程，这带来了许多优势，
但开发人员还需要考虑另一个层面——任务及其运行时交互的概念。可视化跟踪
诊断可视为 FreeRTOS 应用程序的监控摄像头，
让您可以查看软件事件的时间线，在高级概览中发现问题，并深入了解排序细节。
在开展 FreeRTOS 应用程序调试、验证和优化等工作方面具有非常大的作用。

Percepio 的 Tracealyzer 是一款功能强大的运行时分析工具，
可与传统调试器并行使用，通过可视化任务和 ISR
（包括 FreeRTOS API 调用和您自己的“用户事件”）的实时执行情况，对调试器进行补充。
<br />

![](/media/2020/Picture-11.png)

Percepio Tracealyzer 可与传统源代码调试器同时使用，
并使用相同的调试探针。它不需要任何特殊的跟踪硬件。如需进一步了解可视化跟踪
诊断如何简化和加快 FreeRTOS 应用程序开发，
请查看 [Percepio RTOS 调试门户](https://percepio.com/rtos-debug-portal/)中的文章，
并阅读[快速入门指南](https://percepio.com/gettingstarted-freertos/)。


## 视图和数据示例

Tracealyzer 提供 30 多张不同抽象级的交互视图，包括概览和细节图。
这些视图相互关联，呈现出简化的工作流程，并且包括内核事件和用户事件的相关数据，
即应用程序代码中的可选日志记录调用。

* 任务执行、 ISR 、API 调用、用户事件等的时间表。
* 覆盖 CPU 负载、堆栈使用率和动态内存分配的图表。
* 任务时间（响应时间，执行时间等）统计图
* 用户事件图：可将记录为用户事件的任何数据可视化。
* 自定义间隔图：可供查看两个用户事件之间的时间间隔。
* 状态计图：从用户事件获取的状态图。


## 操作方式

FreeRTOS 内核在关键位置包含 100 多个“跟踪钩子”。

Tracealyzer 包括用于 FreeRTOS 的跟踪记录器库，该跟踪记录器库可通过上述跟踪钩子记录重要的内核事件
。无需修改 FreeRTOS 源代码，只需重新构建即可启用钩子
。跟踪记录器库设计时考虑了 32 位 MCU，因此非常节约内存。
每个事件的处理开销以微秒计算，通常不是很明显，
不过这取决于应用程序和处理器的速度。

跟踪记录器库还允许用户在应用程序代码中添加自己的自定义日志记录，
例如关于变量值、状态更改和寄存器值的日志记录。

跟踪数据可以连续传输到主机（流模式）
或存储到目标 RAM 的环形缓冲区（快照模式） ，以便根据需要随时上传。快照模式不需要特殊的跟踪硬件。
串流模式需要具有足够容量并能连接到主机的流通道，
如网络接线、USB 串行接线或 microSD 卡。

记录器允许进行灵活的配置，并且支持若干类预定义流。
Tracealyzer 主机应用程序可在 Windows 和 Linux上运行。


## 示例视图

点击以下链接，即可查看 Tracealyzer 屏幕截图精选示例。每张图像都附有简略说明。

**各类 Tracealyzer 图形视图的屏幕截图**

* [跟踪视图](Trace_View)
* [关于如何在不散焦的情况下缩放轨迹的演示图。](Trace_With_Zoom_View)
* [ CPU 负载图](CPU_Load)
* [任务（和中断）之间的通信路径图](Communication_Flow_View)
* [内核对象历史记录图](Kernel_Object_History_View)
* [内核对象使用历史记录图](Kernel_Object_Utilisation_View)
* [用户信号绘图](User_Signal_Plot_View)
