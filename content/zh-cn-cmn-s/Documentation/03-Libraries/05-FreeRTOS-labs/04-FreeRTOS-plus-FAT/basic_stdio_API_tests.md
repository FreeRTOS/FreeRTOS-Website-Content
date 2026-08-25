---
title: 基础 stdio API 测试
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT 示例](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_FAT_demo_projects#Free_TCPIP_FAT_examples)


一些 [FreeRTOS-Plus-FAT 演示项目](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_FAT_demo_projects)
利用 vStdioWithCWDTest() 函数，
使用标准 stdio API 在嵌入式 FAT 文件系统上执行一些
基础健全性测试。

vStdioWithCWDTest() 已在
/FreeRTOS-Plus/Demo/Common/FreeRTOS_Plus_FAT_Demos/test/ff_stdio_tests_with_cwd.c 中实现，
其实现可作为有用的引用。
