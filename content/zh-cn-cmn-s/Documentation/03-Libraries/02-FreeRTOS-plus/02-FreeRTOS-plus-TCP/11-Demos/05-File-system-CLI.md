---
title: 文件相关命令行接口
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT 示例](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_FAT_demo_projects#Free_TCPIP_FAT_examples)

UDP [命令行接口示例](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/UDP_CLI) 中
包含允许查看、访问和操作文件的命令，具体
请参阅下表。

这些命令在 /FreeRTOS-Plus/Demo/Common/FreeRTOS_Plus_CLI_Demos/File-releated-CLI-commands.c 中实现。

| 命令             | 描述                                                |
| ------------------- | ---------------------------------------------------------- |
| dir                 | 查看目录列表                                   |
| cd \<path>          | 将当前工作目录 (CWD) 更改为 \<path>      |
| del \<file>         | 删除 \<file>                                             |
| rmdir \<path>       | 移除目录 \<path>，目录必须为空 |
| type \<file>        | 显示 \<file> 的内容。                           |
| copy \<src> \<dest> | 将文件 \<src> 复制到文件 \<dest>                   |
| pwd                 | 打印工作目录                                |

![通过命令行接口访问嵌入的 FAT 文件系统](/media/2018/File_System_Commands.png)
*通过命令行接口访问文件系统*
