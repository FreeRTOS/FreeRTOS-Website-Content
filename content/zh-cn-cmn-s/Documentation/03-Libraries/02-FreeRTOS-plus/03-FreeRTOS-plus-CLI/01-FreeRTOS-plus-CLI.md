---
title: FreeRTOS-Plus-CLI
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

**可扩展命令行接口框架**


## 简介

FreeRTOS-Plus-CLI （命令行接口）提供了一种简单、小巧、可扩展且 RAM 高效的方法， 
方便您的 FreeRTOS 应用程序处理命令行输入。添加命令所需的步骤如下图表（可点击）所示，
**可通过单击流程中的每个阶段**， 
了解具体实例。

[![提供一个实现 FreeRTOS-Plus-CLI 命令行为的函数](/media/2018/Creating-a-command-step-1.png)](FreeRTOS_Plus_CLI_Implementing_A_Command)

![FreeRTOS 命令行解释器序列分隔符](/media/2018/Creating-a-command-sequence-arrow.png)

[![提供常量结构体以将命令映射到实现此命令的函数](/media/2018/Creating-a-command-step-2.png)](FreeRTOS_Plus_CLI_Registering_A_Command)

![FreeRTOS 命令行解释器序列分隔符](/media/2018/Creating-a-command-sequence-arrow.png)

[![使用 FreeRTOS 命令解释器 FreeRTOS-Plus-CLI 注册常量结构体](/media/2018/Creating-a-command-step-3.png)](FreeRTOS_Plus_CLI_Registering_A_Command)

![FreeRTOS 命令行解释器序列分隔符](/media/2018/Creating-a-command-sequence-arrow.png)

[![提供字符输入和输出函数](/media/2018/Creating-a-command-step-4.png)](FreeRTOS_Plus_CLI_IO_Interfacing_and_Task)   
*向 FreeRTOS-Plus-CLI 添加一条命令。**此图表可点击**。*


FreeRTOS-Plus-CLI 可在 
官方 [FreeRTOS 压缩文件下载包的以下目录中找到](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)：`FreeRTOS-Plus/Source/FreeRTOS-Plus-CLI`。
本网站还提供了多个[示例项目](FreeRTOS_Plus_CLI_Demos)。

FreeRTOS V10.0.0 FreeRTOS-Plus-CLI 与 FreeRTOS 内核采用[相同的 MIT 许可。](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/04-Licensing/01-Licensing)

