---
title: 蜂窝接口
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
description: 蜂窝接口库简介
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
externalLinks:
- title: 蜂窝接口 API 引用
  link: https://freertos.github.io/FreeRTOS-Cellular-Interface/v1.3.0/
---

## 简介

蜂窝接口库实现了一个简单 
而统一的 [API](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/01-Cellular-interface)， 
它隐藏了蜂窝调制解调器专用 AT 命令的复杂性，并为 C 程序员提供了一个类似套接字的接口。

大多数蜂窝调制解调器都或多或少地执行 
[3GPP TS v27.007](https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=1515) 
标准所定义的 AT 命令。本项目在一个可重复使用的通用组件中[实现](https://github.com/FreeRTOS/FreeRTOS-Cellular-Interface/tree/main/source)了 
此类标准 AT 命令。[](../Documentation/api-ref/cellular/cellular_porting_module_guide) 
本项目的三个蜂窝接口库都利用了该通用代码。每个调制解调器的库 
仅实现供应商特定的 AT 命令，随后公开完整的蜂窝接口 API。 

实现 3GPP TS v27.007 标准的通用组件已按照 
以下代码质量标准进行编写：

* GNU 复杂性得分不超过 8
* MISRA C: 2012 编码标准。任何偏离标准的情况都被记录在用 "coverity" 标记的源代码注释中。


## 入门指南

###  下载源代码

源代码可以从 FreeRTOS 库下载，也可以自行下载。

使用 HTTPS 从 Github 进行克隆：

```c
git clone https://github.com/FreeRTOS/FreeRTOS-Cellular-Interface.git  

```

使用 SSH：

```c
git clone git@github.com:FreeRTOS/FreeRTOS-Cellular-Interface.git  

```


### 文件夹结构

此存储库的根目录包括以下文件夹：

* source：可重复使用的通用代码，实现经 3GPP TS v27.007 定义的标准 AT 命令
* docs：文档
* test：单元测试和 cbmc
* tools：用于 Coverity 静态分析和 CMock 的工具


### 配置和构建库

蜂窝接口库应作为应用程序的一部分进行构建。为此， 
必须提供某些配置。 
The [FreeRTOS 蜂窝演示](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator) 
项目提供了一个关于如何配置构建的[示例](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator/MQTT_Mutual_Auth_Demo_with_BG96/cellular_config.h) 
。想要了解更多信息，请参阅 
[蜂窝接口 API 引用](../Documentation/api-ref/cellular/cellular_config)。 


更多信息，请参[阅蜂窝接口演示（双向验证）](../cellular-demo)。 


## 将蜂窝接口库与 MCU 平台集成

蜂窝接口库在使用抽象接口 
（即[通信接口](https://github.com/FreeRTOS/FreeRTOS-Cellular-Interface/blob/main/source/interface/cellular_comm_interface.h)） 
与蜂窝调制解调器通信的 MCU 上运行。通信接口也必须在 MCU 平台上实现。 
通信接口的最常见的实现方式是使用 UART 硬件， 
但也可以通过其他物理接口（如 SPI）来实现。通信接口的文档可在 
[蜂窝 API 引用](../Documentation/api-ref/cellular/cellular_porting#cellular_porting_comm_if)中找到。 
以下为通信接口的实现示例：

* [FreeRTOSWindows 模拟器通信接口](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator/Common/comm_if_windows.c)
* [FreeRTOS通用 IO UART 通信接口](https://github.com/aws/amazon-freertos/blob/main/libraries/abstractions/common_io/include/iot_uart.h)
* [STM32 L475 探索板通信接口](https://github.com/aws/amazon-freertos/blob/feature/cellular/vendors/st/boards/stm32l475_discovery/ports/comm_if/comm_if_uart.c)
* [Sierra 传感器集线器板通信接口](https://github.com/aws/amazon-freertos/blob/feature/cellular/vendors/sierra/boards/sensorhub/ports/comm_if/comm_if_sierra.c)


