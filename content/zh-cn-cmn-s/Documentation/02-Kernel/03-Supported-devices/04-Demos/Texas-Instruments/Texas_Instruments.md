---
title: 适用于 TI 嵌入式 MCU 的 FreeRTOS
---

## 引言
此页面可链接到最新 RTOS 项目的文档页面，
这些项目面向 Texas Instruments 嵌入式处理器。旧 RTOS 项目的链接
位于主 [RTOS 移植页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#TI)。

## MSP432（ARM Cortex-M4F 核心）
支持 IAR、ARM (Keil) 和 TI (CCS) 编译器

![Texas Instruments MSP432 Launchpad 开发工具包](/media/2018/MSP432_Launchpad_Development_Kit.jpg)

MSP-EXP432P401R LaunchPad 开发工具包

[本页](TI_MSP432_Free_RTOS_Demo)记录的演示应用程序面向
[Texas Instruments MSP432 微控制器](http://www.ti.com/MSP432)，
 - 该微控制器是采用 ARM Cortex-M4F 核心的 MSP430
低功耗微控制器的变体。

我们为以下三种编译器提供了面向 MSP432P401R Launchpad 开发工具包的预配置 MSP432 项目：
IAR、ARM 和 TI (CCS) 编译器。

每个项目都可进行编译，以创建简单的 blinky
或综合测试和演示应用程序。

综合演示使用 [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/03-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
 通过 UART 创建一个简单的命令行接口。

blinky 演示使用 FreeRTOS 的无滴答空闲模式来降低功耗。

[阅读更多关于 MSP432 演示的信息......](TI_MSP432_Free_RTOS_Demo)


## MSP430FR5969（MSP430X 核心）
支持 IAR 和 TI (CCS) 编译器
![Texas Instruments MSP430 MSP-EXP430FR5969 Launchpad 开发工具包](/media/2018/MSP-EXP430FR5969.jpg)

### MSP-EXP430FR5969 LaunchPad 开发工具包
[本页](MSP430FR5969_Free_RTOS_Demo)记录的 RTOS 演示
应用程序面向
[Texas Instruments MSP430FR5969](http://www.ti.com/product/msp430fr5969)
低功率微控制器，该微控制器具有 16 位 MSP430X 核心。

我们提供了面向
[MSP-EXP430FR5969](http://www.ti.com/tool/msp-exp430fr5969#0) Launchpad 开发工具包的预配置项目，
适用于 [IAR](https://www.iar.com/iar-embedded-workbench/texas-instruments/msp430/)
和 [Code Composer Studio](http://www.ti.com/ccs) (CCS) MSP430编译器：

每个项目都可进行编译，以创建简单的
blinky 演示或综合测试和演示应用程序，此类程序可包含
[FreeRTOS-Plus-CLI](/Documentation/03-Libraries/03-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
 命令行接口。此外，
 还提供了同时使用大型和小型数据模型的构建配置。

[阅读更多关于 MSP430FR5969 演示的信息……](MSP430FR5969_Free_RTOS_Demo)
