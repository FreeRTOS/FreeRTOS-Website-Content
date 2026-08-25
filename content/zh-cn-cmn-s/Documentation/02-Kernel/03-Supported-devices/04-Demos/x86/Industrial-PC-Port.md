---
title: "工业电脑移植"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

此 RTOS 移植是在非常老的笔记本电脑上开发的，利用并行端口驱动数字 IO。 
此后，它已被用于低端（使用 486 处理器）和高端（使用奔腾处理器）工业单板计算机中， 
用于使用 ISA CANBus 接口的电机控制应用程序。可以使用任何基于 x86 的 PC 单板计算机。
有关如何在 *Windows DOSBox 中测试此移植的信息，请参阅常见问题 “* FreeRTOS 可以在 Windows 下运行吗” 。 

[FreeDOS](http://www.freedos.org/)
 提供方便、可靠和免版税的启动系统，以及文件和控制台 IO。受常规的 16 位 DOS 
 限制影响，这对奔腾系统有点浪费！

如果您选择的目标单板计算机包含网络适配器，则可免费使用[数据包驱动程序](http://www.crynwr.com/) 
将驱动器从主机系统映射到目标上。然后可以在映射的驱动器中执行和调试正在开发的应用程序， 
每次编译后删除下载应用程序的要求。

如果有足够的空间，PC 兼容的架构允许 [Open Watcom 开发工具](http://www.openwatcom.org/)
 直接用在目标单板计算机上， 
或通过远程调试实用程序使用。虽然 Borland 开发工具不开源，但事实证明它 
很可靠。

从 V4.0.0 开始，PC 演示已更新，以演示如何使用协程。请参阅[协同程序文档](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/14-Standard-demo-examples) 
页面，了解更多信息。

---

### *重要提示！工业电脑 RTOS 移植*的使用说明

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和用法详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载内容包含所有 FreeRTOS 移植的源代码。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，获取
下载文件的描述和有关创建新项目的信息。

针对 PC 的项目文件（Open Watcom 和 Borland）包含在 
Demo/PC 目录下。

---

### 演示应用程序

FreeRTOS 源代码下载包含 PC RTOS 移植的完全抢占式多任务演示应用程序。

### 演示应用程序硬件设置

演示应用程序包括通过串行端口发送和接收字符的任务。一个任务发送的字符
需要另一个任务来接收：如果遗漏任何字符或字符接收顺序错误，则会标记错误状态。串行端口上
需要一个环回连接器才能让此机制正常运行（只需在串行端口连接器上将引脚 2 和 3 
连接在一起）。

演示应用程序使用标准并行端口来控制 8 个 LED。不使用这些 LED 不会导致 RTOS 演示应用程序失败， 
但告知用户一切运行正常的部分视觉反馈将无法提供。 

RTOS 内核不维护浮点寄存器的上下文。使用 Open Watcom 时，必须定义 NO87 环境变量 
以强制使用浮点仿真。

Borland 浮点仿真不是可重入的， 
但有大量证据证明，存在一些技巧可以使其可重入。

### 构建 RTOS 演示应用程序

支持 Borland V4.52 和 Open Watcom 开发工具。 
可在 Demo/PC 目录中找到可在相应 IDE 内打开的项目文件。

### 功能

演示应用程序创建所有标准演示应用程序实时任务和协程（请参阅 
 （有关各个任务的详细信息，请参阅[演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)部分）。

连接到并行端口的 LED 由 “flash” 协程控制。每个 LED 都会以不同的固定频率闪烁， 
如演示应用程序文档中所述。每个 LED 都由不同的协程控制。

其中包括一项检查任务，用于监控所有实时任务和协程。任何任务或协程中发生错误，都会唤醒“检查”任务，
并将错误消息输出到显示器。此外，“检查”任务
每 5 秒检查一次系统中的所有任务，以确保任务均在正确执行，没有错误， 
然后输出状态消息。“OK” 状态消息表示未检测到错误。可以通过将环回连接器 
从串行端口（如上所述）移除来检查此机制，
 因为这样做故意制造了一个错误。

---

### 配置和用法详情

### RTOS 移植特定配置

此移植的特定配置项位于 Demo/PC/FreeRTOSConfig.h
（如果使用的是 Borland 编译器，则位于 Demo/PC/FRConfig.h）。可以编辑此文件中定义的常量
确保适配您的应用程序。特别是，可以将定义 configTICK_RATE_HZ 用于设置
RTOS tick 的频率。演示项目提供的数值 1000 Hz 可用于测试 RTOS 内核功能，但
此速度超过了大部分应用程序的要求。降低此值将提高效率。

每个移植都会将 "BaseType_t" 定义为对处理器而言最有效的数据类型。此移植将
BaseType_t 定义为短整型。

### 在抢占式和协同式 RTOS 内核之间切换

将 Demo/PC/ 内FreeRTOSConfig.h
（如果使用的是 Borland 编译器，则位于 Demo/PC/FRConfig.h 内）的定义 configUSE_PREEMPTION 设置为 1，可使用抢占式，
设置为 0 可使用协同式。  

### 开发工具选项

与所有的移植一样，使用正确的编译器选项至关重要。若要确保这一点，最佳方法是基于
提供的 RTOS 演示应用程序项目来构建您的应用程序。

### RTOS 演示应用程序串行端口驱动程序

编写串行端口驱动程序是为了测试某些 RTOS 内核功能，它并非一个优化的 
解决方案。
