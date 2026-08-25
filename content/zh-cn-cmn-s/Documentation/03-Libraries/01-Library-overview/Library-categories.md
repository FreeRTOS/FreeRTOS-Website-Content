---
title: FreeRTOS 库类别
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


## 简介

本网站上记录的每个库都属于下述的某个类别。所有库 
均已获得 [MIT（开放源码）许可](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/04-Licensing/01-Licensing)， 
专为微控制器和小型微处理器等资源有限的设备而设计。FreeRTOS Core 和适用于 AWS 库的 FreeRTOS 除了标准 C 库之外， 
没有任何其他依赖项，它们甚至不依赖于 RTOS。


### 类别描述

** FreeRTOS 内核**   
FreeRTOS 内核本身。此库包括 RTOS 内核、任务间通信原语 
和任务间同步原语。  
[了解更多](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel)


**FreeRTOS Plus**   
与 Core 库（见下文）不同，实现附加功能的库依赖 
FreeRTOS RTOS 内核。  
[了解更多](../Documentation/03-Libraries/02-FreeRTOS-plus/01-Introduction)


**FreeRTOS Core **   
库可实现基于开放标准的连接、安全性和相关功能。这些 
库适用于构建连接到云端的基于微控制器的智能设备。与 
FreeRTOS-Plus 库（见上文）不同，FreeRTOS Core 库除了标准 C 库之外没有其他依赖项， 
因此 FreeRTOS Core 库不依赖 FreeRTOS RTOS 内核。  
[了解更多](../freertos-core)


适用于 AWS IoT**   
 的 **FreeRTOS 为 AWS IoT 特定的增值云服务实现客户端的库，包括 over the air 
更新 (OTA)。这些库适用于构建连接到 
AWS IoT 云端的基于微控制器的智能设备。与 FreeRTOS Core 库一样，它们除了标准 C 库之外没有其他依赖项， 
因此不依赖 FreeRTOS RTOS 内核。  
[了解更多](../iot-libraries.md)


**FreeRTOS Labs**   
FreeRTOS Labs 库具有实用性，但要么不完整，要么是实验性的， 
要么只是为了开放源社区提供。请参阅各个库的文档页面， 
了解各个库的适用标准。  
[了解更多](../Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction)

