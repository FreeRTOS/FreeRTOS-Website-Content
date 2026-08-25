---
title: HTTP Web 服务器示例
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
mainCREATE_HTTP_SERVER 设置为 1（它位于
项目的 main.c 源文件顶部）以将示例包含在
构建中。

此示例使用 FreeRTOS-Plus-TCP 实现基本 web (HTTP) 服务器，
通过由 FreeRTOS-Plus-FAT 实现的文件系统存取文件。一些演示项目
将文件存储在 RAM 磁盘上，而其他演示项目将文件存储在非易失性媒体上，
例如 SD 卡。

Web 服务器使用的基目录由常量 configHTTP_ROOT
（位于 FreeRTOSConfig.h 中）设置。
如果使用了 RAM 磁盘，则装载该磁盘后，会在基目录中创建一个名为 “freertos.html” 的
默认且非常基本的 HTML 文件。
[FTP 服务器](FTP_Server.md)可用于覆盖
具有不同 web 内容的默认 HTML 文件。

**注意**：使用 FreeRTOS Windows 移植时，性能将受到限制。

[\![](/media/2018/viewing_the_default_web_page.png)](/media/2018/viewing_the_default_web_page.png)  
_查看由 FreeRTOS-Plus-TCP Web 服务器提供的默认网页（点击放大）_
