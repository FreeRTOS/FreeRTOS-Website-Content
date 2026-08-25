---
title: "从 FreeRTOS V10.2.1 升级到 V10.3.0"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 路线图和版本说明
description: 关于从 FreeRTOS V10.2.1 升级到 V10.3.0 的信息
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS 简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---


### 向后兼容性

FreeRTOS 10.3.0 包含下文描述的全新配置选项。未被定义的
新选项将保持一个默认值来确保能够
向后兼容 FreeRTOS V10.2.x。因此，FreeRTOS 10.3.0 是
在 FreeRTOS V10.2.1 基础上增加了向后兼容性的替代品，更加便利。


### ARM Cortex-M 内存保护单元 (MPU) 移植

ARMv7-M（ARM Cortex-M3、ARM Cortex-M4F 和 ARM Cortex-M7）移植
配备了内存保护单元 (MPU)，具有以下新配置选项：

* configENFORCE_SYSTEM_CALLS_FROM_KERNEL_ONLY

当 configENFORCE_SYSTEM_CALLS_FROM_KERNEL_ONLY
在 FreeRTOSConfig.h 中定义为 1 时，只有 FreeRTOS 内核代码能够提升特权
（进入中断时硬件自行提升特权
除外）。这要求所有具有
freertos_system_calls 属性的函数放置在单独的部分中，
并且从链接器脚本中导出以下两个附加变量，用于告知
此部分的位置：

* \_\_syscalls_flash_start\_\_
* \_\_syscalls_flash_end\_\_

针对 GCC、Keil uVision 和 IAR Embedded Workbench 的预配置示例
分别位于 FreeRTOS/Demo/CORTEX_MPU_STM32L4_Discovery_GCC_IAR_Keil
和 FreeRTOS/Demo/CORTEX_MPU_M3_NUCLEO_L152RE_GCC 目录中。
请参阅 [FreeRTOS 内存保护单元 (MPU) 支持](/Security/04-FreeRTOS-MPU-memory-protection-unit)，详细了解
如何使用 FreeRTOS-MPU 移植。


### RISC-V 移植

configCLINT_BASE_ADDRESS 配置设置已弃用，
由 configMTIME_BASE_ADDRESS 和 configMTIMECMP_BASE_ADDRESS 取而代之。
有关新设置的信息，请参阅[“在 RISC-V 微控制器上使用 FreeRTOS”](/Using-FreeRTOS-on-RISC-V)
文档页面。  如果旧版应用程序仍然使用 configCLINT_BASE_ADDRESS，
会出现编译器警告，但应用程序还是会照旧
继续构建和运行。


### 其他变更

有关新移植和其他增强功能的详细信息，请参阅[变更历史记录](/Documentation/04-Roadmap-and-release-note/02-Release-notes/00-Release-history)。
