---
title: "静态分配的 FreeRTOS 参考项目"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 本页演示了静态分配的 FreeRTOS 项目
relatedLinks:
  - title: 静态分配演示
    link: /Documentation/02-Kernel/02-Kernel-features/09-Memory-management/04-Static-allocation-demo/
---


### 引言

任务、队列、信号量和软件定时器等 RTOS 对象都可
使用自动分配的 RAM 或预分配（静态分配）的 RAM 来创建。
详情请参阅以下页面：

* [静态和动态创建 RTOS 对象的优缺点](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)
* [configSUPPORT_STATIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_static_allocation) 
  和 [configSUPPORT_DYNAMIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_dynamic_allocation) 配置常量。

本页记录了一个参考项目，此项目演示了在 configSUPPORT_DYNAMIC_ALLOCATION 设置为 0 的情况下使用 FreeRTOS
的情况——在此设置下，所有 RTOS 对象
都使用预先分配的（可能是静态分配的）RAM 来创建，并且没有
构建任何 FreeRTOS 堆实现。此参考使用 
[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)，
因此，其构建和执行无需任何特定的嵌入式硬件。


### 构建参考项目

1. 如果尚未安装，请下载并安装 
   [Microsoft Visual Studio 社区免费版](https://visualstudio.microsoft.com/vs/express/)。
2. 请[下载](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)并解压缩 FreeRTOS 官方发行版（如尚未完成）。
3. 启动 Visual Studio，然后使用 "File|Open|Project/Solution" 菜单项打开 Win32.sln 解决方案文件， 
   该文件位于 FreeRTOS/Demo/WIN32-MSVC-Static-Allocation-Only 目录 
   （官方 FreeRTOS 发行版）。
4. 在编译之前阅读 main.c 中的注释，然后调试或运行应用程序。


![由静态分配的 RTOS 项目生成的输出结果](/media/2018/FreeRTOS_Static_Allocation.jpg)   
**由 100% 静态分配的 FreeRTOS 参考项目生成的输出结果** 
