---
title: FreeRTOS-Plus-FAT
---
DOS 兼容嵌入式 FAT 文件系统


**注意**：
FreeRTOS-Plus-FAT 是一个 [FreeRTOS Labs](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction) 项目。虽然功能齐全，
相当成熟，但它是收购过来的产品（不是我们自己编写的），因此不一定
符合我们的生产代码或测试标准。它可从
GitHub 上的 [Lab-Project-FreeRTOS-FAT](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-FAT) 存储库获得。


FreeRTOS-Plus-FAT 是一种开源、线程感知和可扩展的 FAT12/FAT16/FAT32 DOS/Windows 兼容
嵌入式 FAT 文件系统，最近被
[Real Time Engineers ltd.](/Why-FreeRTOS/Support-options) 并购，
以便与 RTOS 一同或分别使用。

FreeRTOS-Plus-FAT 已用于商业化产品，
它是 [FTP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/06-FTP-server)
和 [HTTP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/07-HTTP-web-server)
服务器示例使用的文件系统
（记录在 [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP) 页面上）。


[标准 C 库 API](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)
包括线程本地 errno 值，其较低级别的原生 API 提供了
丰富而详细的错误代码集。

我们目前正在努力改进嵌入式文件系统的
文档，添加其他可扩展性选项并更新
源代码，以确保其符合我们严格的编码标准。
您不妨下载 FreeRTOS-Plus-FAT，试用嵌入式 FAT 文件系统，
与此同时，我们会持续对其进行优化。

**为什么使用 FreeRTOS-Plus-FAT**

+ 全面线程感知
+ 可扩展
+ 支持长文件名（可选）
+ 快速哈希处理目录名称（可选）
+ 支持 FAT12、FAT16 和 FAT32
+ 明确到任务的工作目录
+ 明确到任务的 errno 支持
+ 额外综合错误报告
+ 标准、全面的 API
+ 技术支持
