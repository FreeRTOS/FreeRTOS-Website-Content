---
title: FreeRTOS 常见问题 - 移植
created: 2018-09-20 00:00:00.0 UTC
description: FreeRTOS 移植相关信息
---

## FreeRTOS 是否可以在 Windows 上运行？

可以，但无法实现真正的实时操作。

[FreeRTOS 主下载中提供了两个 FreeRTOS Windows 模拟器项目](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)。
第一个使用 Visual Studio 免费速成版，第二个使用 GCC/MingW 和 Eclipse 免费工具。

x86 移植可在 DOS 仿真盒中运行，ARM7 Keil 移植可以在 windows 中 
完全模拟（许多其他移植也可以）。

## FreeRTOS 能在任何 Cortex-M 端口上运行吗？
 
运行 FreeRTOS 所需的一切都包含在内核端口层中，因此 FreeRTOS 可以运行在任何 Cortex-M3/M4/M4F/M7/M23/M33/M55/M85 设备上。
由于不可能为每个设备都提供演示，因此你可能需要 
[自己创建一个项目](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)。
许多 MCU 厂商也提供了与其工具链兼容的 FreeRTOS 项目。

## 是否支持 NNN 开发工具？

支持多种不同的开发工具 
。[检查移植列表](/Documentation/02-Kernel/03-Supported-devices/00-Supported-devices)。


## 是否支持 NNN 微控制器？

支持多种不同的微控制器 
。[检查移植列表](/Documentation/02-Kernel/03-Supported-devices/00-Supported-devices)。


## 如何新建移植？

请参阅 [FreeRTOS 移植指南](/Documentation/02-Kernel/03-Supported-devices/01-FreeRTOS-porting-guide)。


## 官方移植和不受支持的移植之间有什么区别？

请参阅['官方支持'和'社区贡献' FreeRTOS 代码](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) 
的描述。
