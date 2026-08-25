---
title: coreHTTP 基础 S3 下载演示
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---
## 单线程 VS 多线程

coreHTTP 有两种使用模式，一种是*单线程*，另一种是*多线程*（多任务）。虽然 
本页上的演示是在一个线程中运行 HTTP 库，但实际上演示的是如何在单线程环境中使用 coreHTTP 
（演示中只有一个任务使用 HTTP API）。单线程 
应用程序必须重复调用 HTTP 库，多线程应用程序可以在后台的代理任务（或守护进程）中执行发送  
HTTP 请求。
  

## 简介

本演示展示如何使用[范围请求](https://tools.ietf.org/html/rfc7233)从 
AWS S3 http 服务器下载文件。在以下情况下，coreHTTP API 原生支持范围请求：使用 `HTTPClient_AddRangeHeader()` 
创建 HTTP 请求。在微控制器环境中，非常鼓励使用范围请求—— 
通过在不同范围内下载（而不是在单个请求中）大文件， 
可以在不阻塞网络套接字的情况下处理文件的每个部分。范围请求降低了数据包丢失的风险， 
因为丢失的数据包需要在 TCP 连接上重新传输，因此范围请求可改善设备的功耗。

本示例使用了一个使用 mbedTLS 的[网络传输接口](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface)， 
用于在运行 coreHTTP 的 IoT 设备客户端和 AWS S3 HTTP 服务器之间建立相互验证的连接。

core HTTP S3 下载演示项目使用 
[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)， 
因此可以使用 
[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/) 进行构建和评估， 
无需任何特定 MCU 硬件。
  

## 源代码组织

演示项目名为 `http_s3_download_demo.sln`，可在 
`FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download` 目录中找到， 
该目录属于 [主 FreeRTOS 下载](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)的一部分 
（也可在 GitHub 上的 [coreHTTP_Windows_Simulator](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator) 存储库中找到） 
。


## 配置演示项目

此演示使用 
[FreeRTOS-Plus-TCP TCP/IP 堆栈](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/index.md)，因此请按照 
为 [TCP/IP 入门项目](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md)提供的说明进行操作， 
以确保您：

1. 安装了[必要组件](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#prerequisites)（例如 WinPCap）。

2. [设置了静态或动态 IP 地址、网关地址和网络掩码](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#static-dynamic)（可选）。

3. [设置了 MAC 地址](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#mac-addr)（可选）。

4. [在您的主机上选择以太网接口](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#network-interface)。

5. **最重要的是**，在尝试运行 HTTP 演示之前，[测试了网络连接](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#connectivity-test)。

交付时， TCP/IP 堆栈被配置为使用动态 IP 地址。
  

## 配置 AWS S3 HTTP 服务器连接

此演示使用预签名 URL 连接 AWS S3 HTTP 服务器并授权访问要下载的对象 
。AWS S3 HTTP 服务器的 TLS 连接仅使用服务器验证。在应用程序层面， 
使用预签名 URL 查询中的参数来验证对对象的访问。按照 
以下步骤配置您与 AWS 的连接。

1. 设置一个 Amazon Web Services (AWS) 账户：

   * 如果您还没有账户， 
     [请创建并激活 AWS 帐户](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) 
     （其中包括一个[免费层级](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=categories%23iot)）。

   * 使用 AWS 身份和访问管理 (IAM) 设置账户和权限。使用 IAM， 
     可管理账户中每个用户的权限。默认情况下，获得根所有者的授权 
     才具有权限。

     1. 要将 IAM 用户添加到您的 AWS 帐户，请参阅[《IAM 用户指南》](https://docs.aws.amazon.com/IAM/latest/UserGuide/)。

     2. 通过添加以下策略，授予您的 AWS 账户访问 FreeRTOS 和 AWS IoT 的权限：

        + AmazonS3FullAccess

2. 按照 
   [“我如何创建 S3 存储桶？”]中的步骤在 S3 中创建一个存储桶，(https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html) 
   请参阅*Amazon 简单存储服务控制台用户指南*。

3. 按照[“如何将文件和文件夹上传到 S3 存储桶？”中的步骤上传文件至 S3](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/upload-objects.html)。

4. 使用位于 
   `FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/Common/presigned_url_generator/presigned_urls_gen.py` 的脚本生成预签名 URL。 
   使用说明，请参阅 [FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/Common/presigned_url_generator/README.md](https://github.com/FreeRTOS/FreeRTOS/tree/p3_rel_wip/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/Common/presigned_url_generator)。

## 构建演示项目

演示项目使用[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/)。 
要构建演示，请执行如下操作：

1. 从 Visual Studio IDE 中打开 `http_s3_download_demo.sln` Visual Studio 解决方案文件。

2. 在 IDE 的 '**Build**' 菜单中选择 '**Build Solution**'。

**注意**：如果您使用的是 Microsoft Visual Studio 2017 或更早版本，则必须选择与您的版本兼容的“**平台
工具集**”：“**Project -> RTOSDemos Properties -> Platform Toolset**”（项目 -> 演示属性 -> 平台工具集）。
  

## 功能

演示首先检索文件的大小。然后，演示依次循环请求每个字节范围， 
范围大小为 `democonfigRANGE_REQUEST_LENGTH`。 

演示的源代码 
可在 GitHub 上的 [S3DownloadHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download/DemoTasks/S3DownloadHTTPExample.c#L269-L430) 中找到 
。
  

### 连接到 AWS S3 HTTP 服务器

函数 `connectToServerWithBackoffRetries()` 试图与 HTTP 服务器建立 TCP 连接。 
如果连接失败，则在超时后重试。超时值将呈指数增长， 
直到达到最大尝试次数或最大超时值。 `connectToServerWithBackoffRetries()` 
如果在配置的尝试次数后仍无法建立与服务器的 TCP 连接， 
则返回失败状态。 

`connectToServerWithBackoffRetries()` 的源代码 
可在 GitHub 上的 [http_demo_utils.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/Common/http_demo_utils.c#L71-L120) 中找到 
。

函数 `prvConnectToServer()` 演示了如何仅使用服务器身份验证与 AWS S3 HTTP 服务器建立连接 
。它使用基于 mbedTLS 的传输接口，该接口在 
文件 `FreeRTOS-Plus/Source/Application-Protocols/network_transport/freertos_plus_tcp/using_mbedtls/using_mbedtls.c` 中实现。 

prvConnectToServer() 可在 
GitHub 上的 [S3DownloadHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download/DemoTasks/S3DownloadHTTPExample.c#L433-L488) 中找到 
。
  

### 创建范围请求

API 函数 `HTTPClient_AddRangeHeader()` 支持将字节范围序列化到 HTTP 请求 
标头中以形成范围请求。在此演示中，使用范围请求来检索文件大小 
并请求文件的每个部分。

函数 `prvGetS3ObjectFileSize()` 用于检索 S3 存储桶中文件的大小。在向 S3 发送的第一个请求中添加了 “Connection: keep-alive” 标头， 
以便在发送响应后保持连接开启。S3 
HTTP 服务器当前不支持使用预签名 URL 的 HEAD 请求，因此请求第 0 个字节。 
文件的大小包含在响应的 `Content-Range` 标头字段中。预计服务器会返回一个 `206 Partial Content` 
响应；如收到其他响应状态代码，则均视为错误。 

`prvGetS3ObjectFileSize()` 的源代码 
可在 GitHub 上的 [S3DownloadHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download/DemoTasks/S3DownloadHTTPExample.c#L491) 中找到 
。

检索文件大小后，此演示将为要下载的文件的每个字节范围创建一个 
新的范围请求。对文件的每个部分使用 `HTTPClient_AddRangeHeader()`。 

源代码 
可在 GitHub 上的 [S3DownloadHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download/DemoTasks/S3DownloadHTTPExample.c#L732-L734) 中找到 
。
  

### 发送范围请求和接收响应

函数 `prvDownloadS3ObjectFile()` 循环发送范围请求，直到下载完整个文件。 
API 函数 `HTTPClient_Send()` 发送请求并同步接收响应。函数返回时， 
将在 `xResponse` 中接收响应。然后验证状态代码是否为 `206 Partial Content`， 
并通过 `Content-Length` 标头值递增目前下载的字节数。 

`prvDownloadS3ObjectFile()` 的源代码 
可在 GitHub 上的 [S3DownloadHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download/DemoTasks/S3DownloadHTTPExample.c#L660-L803) 中找到 
。

