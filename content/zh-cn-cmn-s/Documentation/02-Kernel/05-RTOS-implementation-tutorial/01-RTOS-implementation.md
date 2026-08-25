---
title: "RTOS 实现"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 适用于 FreeRTOS 的 C 开发工具简介
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS 初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---

### 引言

本节旨在介绍 FreeRTOS 实现的部分内容。 

相关页面可为您提供以下方面的帮助：

* 修改 FreeRTOS 源代码。
* 将实时内核移植到另一个微控制器或原型板。
* 提供详细操作和实现情况（适用于 RTOS 初学者）。

FreeRTOS 实时内核已移植到 
许多不同的微控制器架构中。本示例选择 Atmel AVR 移植，原因如下：

* [AVR](http://www.microchip.com/wwwproducts/en/atmega32) 架构简单易懂。
* [WinAVR (GCC) 开发工具](http://winavr.sourceforge.net/)可免费使用。
* [STK500 原型板](http://www.microchip.com/developmenttools/productdetails.aspx?partno=atstk500)价格实惠。

本节最后将详细介绍一个完整的上下文切换。

### 构建模块

* [开发工具](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/02-C-development-tools)
* [RTOS 滴答](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/03-The-RTOS-tick)
* [GCC Signal 属性](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/05-GCC-signal-attribute)
* [GCC Naked 属性](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/06-GCC-naked-attributes)
* [FreeRTOS 滴答代码](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/07-FreeRTOS-tick-code)
* [AVR 上下文](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/08-The-AVR-context)
* [保存上下文](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/09-Saving-the-RTOS-task-context)
* [恢复上下文](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/10-Restoring-the-context)


### 详细示例

第 2 节的最后部分展示了如何使用这些构建块和源代码模块来实现 
AVR 微控制器上的上下文切换。该示例以七个步骤演示了 
从名为 TaskA 的低优先级任务切换到名为 TaskB 的高优先级任务的过程。

源代码与 WinAVR 开发工具兼容。 

* [整合所有部分](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/01-Putting-it-all-together)
* [第 1 步](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/02-Step-1)
* [第 2 步](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/03-Step-2)
* [第 3 步](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/04-Step-3)
* [第 4 步](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/05-Step-4)
* [第 5 步](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/06-Step-5)
* [第 6 步](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/07-Step-6)
* [第 7 步](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/08-Step-7)
