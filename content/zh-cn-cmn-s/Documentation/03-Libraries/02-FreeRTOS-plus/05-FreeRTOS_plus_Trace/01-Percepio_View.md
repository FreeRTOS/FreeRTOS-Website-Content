---
title: 适用于 FreeRTOS 的 Percepio View
created: 2025-01-20
categories:
  - 内核
relatedLinks:
  - title: Tracealyzer™
    link: /Documentation/03-Libraries/02-FreeRTOS-plus/05-FreeRTOS_plus_Trace/00-FreeRTOS_Plus_Trace
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

基于 Percepio Tracealyzer 的 FreeRTOS 应用程序免费追踪工具。
<br />

[![](/media/2025/percepio-view-freertos-2.png)](/media/2025/percepio-view-freertos-2.png)

```jsx
<TraceButton link="https://traceviewer.io/get-view/?target=freertos" text="下载 Percepio View"/>
```

## 引言

FreeRTOS 内核提供实时多线程，这带来了许多优势，
但开发人员还需要考虑另一个层面——任务及其运行时交互的概念。

Percepio View 是一款基于 Percepio Tracealyzer 的免费追踪工具，用作
FreeRTOS 应用程序的监控摄像头，便于调试和验证。

Percepio View 可以与传统调试器结合使用，通过任务和 ISR 实时执行情况
可视化的方式对调试器加以补充。这些任务包括 FreeRTOS API 调用和您自己的“用户事件”。
它不需要任何特殊的追踪硬件。
<br />

[![](/media/2025/FreeRTOS-View-User-Events.png)](/media/2025/FreeRTOS-View-User-Events.png)


如需了解 Percepio View 及其入门方法和升级选项相关的更多信息，请查阅 [Percepio's product page](https://traceviewer.io/get-view/?target=freertos).

## 工作原理

FreeRTOS 内核在代码的关键位置拥有大约 100 个 “[追踪钩子](/Documentation/02-Kernel/02-Kernel-features/09-RTOS-trace-feature)”。
Percepio View 中包含通过上述追踪钩子记录重要的内核事件的 TraceRecorder 库
。FreeRTOS 源代码无需修改，只需更改并重建配置即可
启用追踪钩子。追踪开销通常不明显，
不过这取决于应用程序和处理器的速度。

Percepio View 只能用于快照追踪，这意味着数据存储于
目标 RAM 中的一个环形缓冲区里。Percepio View 在 Windows 和 Linux 主机上运行。

## Demo

[CORTEX\_MPS2\_QEMU\_IAR\_GCC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/QEMU/freertos-on-qemu-mps2-an385-model) 演示已通过 Percepio TraceRecorder 扩展，以演示 Percepio View。
它在 QEMU 模拟器中运行，因此不需要开发板。请参阅 [readme.md in the CORTEX\_MPS2\_QEMU\_IAR\_GCC demo folder](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS/Demo/CORTEX_MPS2_QEMU_IAR_GCC) 了解相关说明。

