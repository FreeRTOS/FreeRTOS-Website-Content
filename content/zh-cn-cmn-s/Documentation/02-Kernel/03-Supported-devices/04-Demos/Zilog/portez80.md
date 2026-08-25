---
title: "Zilog eZ80 Acclaim! 移植适用于 ZDS II 开发工具"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

Zilog eZ80 Acclaim! 移植由 Marcos A. Pereira 创建。

由于缺乏必要的开发工具和硬件，我无法测试该移植。这意味着它**不受支持**，
并与主 FreeRTOS 源代码下载分开提供。不久后将开始着手开发
支持的移植。

### Z80 移植作者的注释

请参阅支持的移植文档页面，获取有关目录结构、如何使用 FreeRTOS 等详细信息。

*“该移植是在 eZ80F91
  开发套件上使用 [ZDS II eZ80Acclaim! 开发工具](http://www.zilog.com/software/zds2.asp)
 (V4.9.1) 创建的。*

要将移植添加到现有的 FreeRTOS 下载中，需要定义一个新的常量，以在 portable.h 头文件中使用。 
我使用的是 ZDSII_EZ80_PORT。同一常量 (ZDSII_EZ80_PORT)
需在 project -> settings -> C -> Preprocessor -> Preprocessor definitions 中定义。所下载的 Z80 中包含的 portable.h 文件和演示项目文件
已有这些设置。

使用 heap_3.c 文件是因为该套件有大量 RAM。

我还需要更改 tasks.c 源文件，因为 ZDSII C 编译器无法理解 
\#if 和括号之间没有空格的 #if 子句。例如：

\#if( INCLUDE_vTaskDelete == 1 )

 会导致 
"ERROR (7) Illegal directive and ERROR (31) Extra "#endif" found" 错误。您需要更改所有 #if 子句， 
在 #if 和括号之间加上空格。同样，我已针对 Z80 下载文件中的文件进行这些修改。

[下载 FreeRTOS eZ80 源代码。](http://www.realtimeengineers.com/FreeRTOS_eZ80.zip)
