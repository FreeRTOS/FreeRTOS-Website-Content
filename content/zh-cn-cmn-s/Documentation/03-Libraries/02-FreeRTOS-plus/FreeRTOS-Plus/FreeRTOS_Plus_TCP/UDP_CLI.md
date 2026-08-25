---
title: 使用 UDP 套接字的 FreeRTOS-Plus-CLI 输入和输出
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT 示例](TCP_FAT_demo_projects#Free_TCPIP_FAT_examples)


并非所有演示项目都包含此示例。如果此示例
包含在演示项目中，则可能需要将
mainCREATE_UDP_CLI_TASKS 在项目
main.c 源文件的顶部设置为 1，以在构建中包含 CLI。

该示例创建了一个 [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI) 命令控制台，该控制台使用 UDP 端口进行输入和输出。

免费哑终端程序，适合
使用 UDP 连接到命令行接口，包括 [YAT](https://sourceforge.net/projects/y-a-terminal/)
和 [Hercules](http://www.hw-group.com/products/hercules/index_en.html)。

要连接到 CLI ，请将哑终端配置为连接到
目标的主机名（或 IP 地址）作为 IP 地址， 5001 作为远程端口， 5002
作为本地端口。默认主机名为 "RTOSDemo"。所需
配置如下图所示。

与 FreeRTOS-Plus-CLI 一样，在命令控制台中键入 "help" 以查看
已注册命令列表。

![免费 RTOS 命令行接口](/media/2018/yat-settings-for-udp-cli.png)
*使用 YAT 连接所需的配置*

![通过命令行接口访问嵌入式 FAT 文件系统](/media/2018/File_System_Commands.png)
*通过命令行接口访问文件系统*
