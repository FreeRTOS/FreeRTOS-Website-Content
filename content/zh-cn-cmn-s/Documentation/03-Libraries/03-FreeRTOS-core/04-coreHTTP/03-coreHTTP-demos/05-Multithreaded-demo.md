---
title: coreHTTP 基础多线程演示
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---
## 简介

本演示使用 [FreeRTOS 线程安全队列](..//Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)保存等待处理的请求和响应 
。在该演示中，有三项任务值得注意：

* 主任务等待请求队列中的请求。通过网络发送这些请求，然后
  将响应放入响应队列。

* 请求任务创建要发送到服务器的 HTTP 库请求对象，然后将它们放入请求队列。每个
  请求对象均可指定应用程序配置用于下载的 S3 文件的字节范围。

* 响应任务等待响应队列中的响应，并会记录收到的所有响应。

此基础多线程演示配置为仅使用带有服务器身份验证的 TLS 连接， 
这是出于 S3 HTTP 服务器的要求。应用层身份验证是通过 
[签名版本 4](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html) 参数完成的 
（该参数位于[预签名 URL 查询中](https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-query-string-auth.html)）。

coreHTTP 基础多线程演示项目使用 
[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)， 
因此可以在 Windows 上使用 
[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/) 进行构建和评估， 
无需任何特定 MCU 硬件。
  

## 源代码组织

多线程 HTTP S3 演示的 Visual Studio 解决方案被称为 
[`http_s3_download_multithreaded_demo.sln`](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download_Multithreaded/http_s3_download_multithreaded_demo.sln)， 
可在 [/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download_Multithreaded](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download_Multithreaded) 
目录中找到（位于[主 FreeRTOS](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) 下载包中）。
  

## 构建演示项目

演示项目使用[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/)。 
要构建演示，请执行如下操作：

1. 在 Visual Studio IDE 内打开 '`mqtt_multitask_demo.sln`' Visual Studio 解决方案文件。

2. 从 IDE 的 '`Build`' 菜单中选择 '`Build Solution`'。

**注意**：如果您使用的是 Microsoft Visual Studio 2017 或更早版本，则必须选择与您的版本兼容的 '`Platform 
Toolset`'：'`Project -> RTOSDemos Properties -> Platform Toolset`'。
  

## 配置演示项目

此演示使用 
[FreeRTOS-Plus-TCP TCP/IP 堆栈](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/index.md)，因此请按照 
为 [TCP/IP 入门项目](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md)提供的说明进行操作， 
以确保您：

1. [安装了必备组件](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#prerequisites)（例如 WinPCap）。

2. [设置了静态或动态 IP 地址、网关地址和网络掩码](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#static-dynamic)（可选）。

3. [设置了 MAC 地址](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#mac-addr)（可选）。

4. [在您的主机上选择以太网接口](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#network-interface)。

5. 而且**重要的是**[，在尝试运行 HTTP 演示之前，测试网络连接](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#connectivity-test)。


## 配置 AWS S3 HTTP 服务器连接

此演示支持与 
[coreHTTP 基本 S3 下载](s3-download-demo.md#configuring-http-server)演示相同的配置选项。请参阅演示 
文档中关于配置 AWS S3 HTTP 服务器连接的说明。


## 功能

该演示共创建了三项任务： 

* 通过网络发送请求和接收响应
* 创建要发送的请求
* 处理收到的响应

在此演示中，主任务创建请求队列和响应队列，创建与服务器的连接， 
创建请求任务和响应任务，在请求队列中等待通过网络发送请求， 
并将通过网络收到的响应放入响应队列。请求任务创建每个范围请求， 
响应任务处理收到的每个响应。


## Typedef

此演示定义了如下支持多线程的结构体：

**请求项**   
以下结构体定义了要放入请求队列的请求项。请求任务 
创建 HTTP 请求之后，请求项会复制到队列中。

```c
/**  
 * @brief Data type for the request queue.  
 *  
 * Contains the request header struct and its corresponding buffer, to be  
 * populated and enqueued by the request task, and read by the main task. The  
 * buffer is included to avoid pointer inaccuracy during queue copy operations.  
 */  
typedef struct RequestItem  
{  
    HTTPRequestHeaders_t xRequestHeaders;  
    uint8_t ucHeaderBuffer[ democonfigUSER_BUFFER_LENGTH ];  
} RequestItem_t;  

```

**响应项**   
以下结构体定义了要放入响应队列的响应项。主 
HTTP 任务通过网络接收到响应之后，响应项会复制到队列中。

```c
/**  
 * @brief Data type for the response queue.  
 *  
 * Contains the response data type and its corresponding buffer, to be enqueued  
 * by the main task, and interpreted by the response task. The buffer is  
 * included to avoid pointer inaccuracy during queue copy operations.  
 */  
typedef struct ResponseItem  
{  
    HTTPResponse_t xResponse;  
    uint8_t ucResponseBuffer[ democonfigUSER_BUFFER_LENGTH ];  
} ResponseItem_t;  

```

## 主 HTTP 发送任务

主应用程序任务首先解析主机地址的预签名 URL，以建立与 
AWS S3 HTTP 服务器的连接。该任务还会解析 S3 存储桶中 
对象路径的预签名 URL。然后，它使用 TLS 和服务器身份验证连接到 AWS HTTP S3 服务器。 
接下来，创建请求和响应队列以及请求和响应任务。 
函数 "`prvHTTPDemoTask()`" 执行此设置并提供演示状态。 

此函数的源代码可以在 
Github 上的 [S3DownloadMultithreadedHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download_Multithreaded/DemoTasks/S3DownloadMultithreadedHTTPExample.c#L471-L650) 
文件中找到。

在函数 "`prvDownloadLoop()`" 中，主任务阻塞并等待来自请求队列的请求。 
收到请求后，它会使用 API 函数 “`HTTPClient_Send()`” 发送该请求。如果 API 函数成功执行， 
则会将响应放入响应队列。 

“`prvDownloadLoop()`” 的源代码可在 
Github 上的 [S3DownloadMultithreadedHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download_Multithreaded/DemoTasks/S3DownloadMultithreadedHTTPExample.c#L1071-L1174) 
文件中找到。
  

## HTTP 请求任务

响应任务在函数 "`prvRequestTask`" 中指定。 

此函数的源代码可以在 
Github 上的 [S3DownloadMultithreadedHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download_Multithreaded/DemoTasks/S3DownloadMultithreadedHTTPExample.c#L777-L878) 
文件中找到。

请求任务首先检索 S3 中对象的大小。该检索在 
函数 “`prvGetS3ObjectFileSize`”中完成。请求任务还会检索 S3 存储桶中文件的大小。在对 S3 的请求中 
添加 "Connection: keep-alive" 标头，即可在发送响应后保持连接开启。S3 HTTP 
服务器当前不支持使用预签名 URL 的 HEAD 请求，因此请求第 0 个字节。文件的大小 
包含在响应的 `Content-Range` 标头字段中。预计服务器会返回一个 `206 Partial Content` 
响应；如收到其他响应状态代码，则均视为错误。 

“`prvGetS3ObjectFileSize`” 的源代码可在 
Github 上的 [S3DownloadMultithreadedHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download_Multithreaded/DemoTasks/S3DownloadMultithreadedHTTPExample.c#L757-L775) 
文件中找到。

检索到文件大小后，请求任务会持续请求文件的每个范围。每个范围 
请求会放入请求队列中，等待主任务发送。文件范围 
由演示用户在宏 `democonfigRANGE_REQUEST_LENGTH` 中配置。范围请求在 HTTP 客户端库 API 中 
通过函数 “`HTTPClient_AddRangeHeader()`” 得到原生支持。函数 “`prvRequestS3ObjectRange()`” 
演示了 "`HTTPClient_AddRangeHeader()`" 的用法。 

“`prvRequestS3ObjectRange()`” 的源代码可在 
Github 上的 [S3DownloadMultithreadedHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download_Multithreaded/DemoTasks/S3DownloadMultithreadedHTTPExample.c#L757-L775) 
文件中找到。
  

## HTTP 响应任务

响应任务在响应队列中等待通过网络接收到的响应。成功接收到 
HTTP 响应后，主任务会填充响应队列。该任务通过 
记录状态代码、标头和正文来处理响应。例如，现实世界中的应用程序 
可以通过将响应体写入闪存来处理响应。如果响应状态代码不是 `206 partial content`， 
则该任务会通知主任务演示失败。响应任务 
在函数 "`prvResponseTask()`" 中指定。 

此函数的源代码可以在 
Github 上的 [S3DownloadMultithreadedHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download_Multithreaded/DemoTasks/S3DownloadMultithreadedHTTPExample.c#L961-L1048) 
文件中找到。

