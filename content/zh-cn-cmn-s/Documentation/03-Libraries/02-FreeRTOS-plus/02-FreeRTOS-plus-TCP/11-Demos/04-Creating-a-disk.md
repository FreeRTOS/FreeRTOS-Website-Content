---
title: 创建磁盘
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT 示例](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_FAT_demo_projects#Free_TCPIP_FAT_examples)

所有 [FreeRTOS-Plus-FAT 演示项目](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_FAT_demo_projects)
都会至少创建一个磁盘，
但创建 RAM 磁盘的演示项目最受关注，因为这些项目
还演示了如何将磁盘[分区](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_Partition)、
将分区[格式化](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_Format)、
如何[挂载](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_Mount)
已格式化的分区并将[已挂载的分区](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_FS_Add)添加
到 FreeRTOS-Plus-FAT 虚拟文件系统。

具体示例参见
[使用 FreeRTOS Windows 移植的演示应用程序](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)。
此应用程序调用 RAM 磁盘媒体驱动程序的 FF_RAMDiskInit() 函数并执行上述所有操作。
