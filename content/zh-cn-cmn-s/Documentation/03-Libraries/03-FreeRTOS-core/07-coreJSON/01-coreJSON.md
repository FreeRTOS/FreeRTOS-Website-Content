---
title: "coreJSON"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: coreJSON 库简介
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/

external links:
  - title: coreJSON API 引用
    link: https://freertos.github.io/coreJSON/v3.2.0/
---


严格执行 ECMA-404 JSON 标准的解析器库


## 简介

JSON（JavaScript 对象表示法）是一种来自 JavaScript 的可供人阅读的数据序列化格式， 
广泛用于交换数据，例如与 [AWS IoT Device Shadow 服务](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow)交换数据， 
还是 [GitHub REST API](https://developer.github.com/v3/) 等众多 API 的一部分。JSON 是由 
Ecma International 维护的标准。

coreJSON 库提供了一个解析器，支持[密钥查找](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/02-coreJSON-terminology)， 
同时严格执行标准（[ECMA-404：JSON 数据交换标准](http://www.ecma-international.org/publications/files/ECMA-ST/ECMA-404.pdf)）。 
此库以 C 编写，设计符合 [ISO C90](https://en.wikipedia.org/wiki/ANSI_C#C90) 
和  [MISRA C: 2012](https://misra.org.uk/misra-c/) 标准。 
它[已被证明](https://www.cprover.org/cbmc/)  具有内存使用安全性，并且不分配堆， 
因此适用于 IoT 微控制器，也可以完全移植到其他平台。 


### 源代码组织和演示

coreJSON 库位于[主 FreeRTOS 下载](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)中， 
可在 [FreeRTOS/FreeRTOS-Plus/Source/coreJSON](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Source) 
目录中找到。coreJSON 库的演示可在 
[IoT Device Shadow 演示](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/04-Device-shadow-demo) 中查看。 


### 内存使用情况

coreJSON 库使用内部堆栈来跟踪 JSON 文档中的嵌套结构体。该堆栈 
存在于单个函数调用期间，不会被保存。可以通过 
定义宏 JSON_MAX_DEPTH 来指定堆栈大小，默认为 32 级。每个级别消耗一个字节。 


**coreJSON 的代码大小（通过 ARM Cortex-M 的 GCC 生成的示例）**

| 文件 | 使用 -O1 优化 | 使用 -Os 优化 |
| --- | --- | --- |
| core_json.c | 2.9K | 2.4K |
| 预计总大小 | 2.9K | 2.4K |
