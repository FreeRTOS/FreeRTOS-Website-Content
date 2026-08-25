---
title: FreeRTOS-Plus-FAT 示例
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

下述 FreeRTOS-Plus-FAT 示例均包含于“全面”演示项目中，此项目的
[描述参见 FreeRTOS-Plus-TCP 页面](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)。
该演示项目可以使用免费开发工具
在 Windows 环境中进行构建和执行。

示例：

- [创建磁盘](#创建磁盘)
- [创建、写入和读取文件](#创建写入和读取文件)
- [与文件相关的 CLI 命令](#与文件相关的-cli-命令)
- [FTP 和 HTTP 服务器](#ftp-和-http-服务器)

---

#### 创建磁盘

[main.c](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)
源文件包含一个名为 prvCreateDiskAndExampleFiles() 的函数，
此函数调用 FF_RAMDiskInit()。

FF_RAMDiskInit() 是[初始化函数](File_System_Media_Driver/Media_Driver_Initialisation)，
此函数用于 FreeRTOS-Plus-FAT 的 RAM 磁盘媒体驱动程序。它演示了如何将磁盘[分区](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_Partition)、
如何将分区[格式化](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_Format)、
如何[挂载](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_Mount)
已格式化的分区并将[已挂载的分区](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_FS_Add)添加
到 FreeRTOS-Plus-FAT 虚拟文件系统。已挂载分区显示
为 /ram。


#### 创建、写入和读取文件

prvCreateDiskAndExampleFiles() 也调用 vCreateAndVerifyExampleFiles()，后者演示如何使用
[ff_fread()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_fread)、[ff_fwrite()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_fwrite)、[ff_fgetc()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_fgetc)
和 [ff_fputc()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_fputc)。

prvCreateDiskAndExampleFiles() 创建的文件和目录
可使用 FTP 服务器示例
和 UDP 命令行接口（两者的相关信息参见下文）来查看和操作。


#### 与文件相关的 CLI 命令

UDP [命令行接口示例](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/UDP_CLI) 中
包含允许查看、访问和操作文件的命令，如
下表所示：

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


#### FTP 和 HTTP 服务器

[FTP 示例](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/06-FTP-server)
和 [HTTP 示例](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/07-HTTP-web-server)
均使用 FreeRTOS-Plus-FAT 作为文件系统
。
