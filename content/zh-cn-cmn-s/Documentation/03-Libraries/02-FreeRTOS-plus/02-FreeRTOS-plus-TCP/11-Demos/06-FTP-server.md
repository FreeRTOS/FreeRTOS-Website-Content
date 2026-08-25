---
title: FTP 服务器示例
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT 示例](TCP_FAT_demo_projects.md#Free_TCPIP_FAT_examples)

**注意：**此演示依赖于 FreeRTOS-Plus-FAT 代码库，
因此目前仅在 FreeRTOS Lab 下载中可以获得。

并非所有演示项目都包含此示例。如果此示例
包含在演示项目中，则可能需要将
mainCREATE_FTP_SERVER 设置为 1（它位于
项目的 main.c 源文件顶部）以将示例包含在
构建中。

此示例使用 FreeRTOS-Plus-TCP 实现
从 FreeRTOS-Plus-FAT 实现的文件系统中存取文件的 FTP 服务器。一些演示项目
将文件存储在 RAM 磁盘上，而其他演示项目将文件存储在非易失性媒体上，
例如 SD 卡。有些项目甚至在同一虚拟文件系统内同时装载 RAM 磁盘
和 SD 卡。

如果示例使用 RAM 磁盘，则在
装载 RAM 磁盘后会于其中创建一组示例文件。

**注意**：使用 FreeRTOS Windows 移植时，性能将受到限制。

可以使用标准 FTP 客户端访问 FTP 服务器，例如 [FileZilla](https://filezilla-project.org/)。如需连接：

- 输入 FTP 服务器的 IP 地址或主机名作为主机
  FTP 服务器是运行 FreeRTOS-Plus-TCP 的目标）。
- 输入 "anonymous" （匿名）作为用户名。
- 将密码留空。

![](/media/2018/viewing_the_ram_disk_in_FileZilla_FTP_client.png)  
_查看 FileZilla FTP 客户端中 RAM 磁盘上的示例文件_
