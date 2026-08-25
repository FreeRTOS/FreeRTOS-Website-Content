---
title: 创建和验证文件
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT 示例](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_FAT_demo_projects#Free_TCPIP_FAT_examples)


创建 RAM 磁盘时，磁盘为空，因此 [FreeRTOS-Plus-FAT 演示项目](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_FAT_demo_projects)
（使用 RAM 磁盘）
在被创建后，需要在磁盘上创建一组示例文件。
通过调用 vCreateAndVerifyExampleFiles() 函数，可创建并验证示例文件
。

vCreateAndVerifyExampleFiles() 在
/FreeRTOS-Plus/Demo/Common/FreeRTOS_Plus_FAT_Demos/CreateAndVerifyExampleFiles.c 中实现，
其实现可作为有用的引用。
