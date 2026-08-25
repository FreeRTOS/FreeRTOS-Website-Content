---
title: "TI MSP430FR5969 (MSP430X) RTOS演示支持IAR和 TI (CCS) 编译器"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Texas Instruments MSP430 MSP-EXP430FR5969 Launchpad 开发工具包](/media/2018/MSP-EXP430FR5969.jpg)

**MSP-EXP430FR5969 LaunchPad 开发工具包** 

### 简介

此页面记录的 RTOS 演示应用程序面向
[Texas Instruments MSP430FR5969](http://www.ti.com/product/msp430fr5969)
低功率微控制器，该微控制器具有 16 位 MSP430X 核心。

我们提供了面向
[MSP-EXP430FR5969](http://www.ti.com/tool/msp-exp430fr5969#0) Launchpad
适用于 [IAR](https://www.iar.com/iar-embedded-workbench/texas-instruments/msp430/)
和 [Code Composer Studio](http://www.ti.com/ccs) (CCS) MSP430编译器：

每个项目都可进行编译，以创建简单的
blinky 演示或综合测试和演示应用程序，此类程序可包含
[FreeRTOS-Plus-CLI](/Documentation/03-Libraries/03-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
命令行接口。此外，
还提供了使用大小数据模型的构建配置。

#### 关于低功率支持的说明

[Idle 钩子](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions)用于将 MSP430 MCU 
设置为低功率模式，这是一种简单的省电方法。提供
[tickless idle](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)
的实现将大大提高节能性，
但未在此演示中配置。

|  |
| --- |
| [![FreeRTOS 内核感知调试器，可与 IAR 编译器结合使用](/media/2018/FreeRTOS-Kernel-Aware-Plug-In-Cortex-M0.jpg)](/media/2018/FreeRTOS-Kernel-Aware-Plug-In-Cortex-M0.jpg)<br/><br/><br/><br/>**状态查看器插件的截图，FreeRTOS该插件<br/> <br/>是IAR IDE 附带的。点击放大。** < br/> < br/> |
