---
title: coreHTTP 基础 S3 上传演示
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---
## 单线程 VS 多线程

coreHTTP 有两种使用模式，一种是*单线程*，另一种是*多线程*（多任务）。虽然 
此页中演示在一个线程中运行 HTTP 库，但它实际上演示了如何在一个单线程环境中使用 coreHTTP 
（即在演示中仅有一个任务使用 HTTP API）。单线程 
应用程序必须重复调用 HTTP 库，而多线程应用程序可以在后台的代理（或守护进程）任务中执行发送  
HTTP 请求操作。
  

## 简介

此示例演示了向 AWS S3 HTTP 服务器发送 PUT 请求并上传小文件的过程。 
它还执行 GET 请求，以在文件上传后验证其大小。本示例采用了 
一个使用 mbedTLS 的[网络传输接口](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface)， 
用于在运行 coreHTTP 的 IoT 设备客户端和 AWS S3 HTTP 服务器之间建立相互验证的连接。

core HTTP S3 上传演示项目使用 
[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)， 
因此可以使用 
Windows 上的[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/) 进行构建和评估， 
无需任何特定 MCU 硬件。
  

## 源代码组织

演示项目名为 http_s3_download_demo.sln，位于 
FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Upload   目录中。 
该目录包含在[ FreeRTOS 主下载包](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) 
（也可在 GitHub 上的 [coreHTTP_Windows_Simulator](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator) 存储库中找到）
。
  

## 构建演示项目

演示项目使用[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/)。 
要构建演示，请执行如下操作：

1. 在 Visual Studio IDE 内 打开 '`http_s3_upload_demo_demo.sln`' Visual Studio 解决方案文件。

2. 从 IDE 的 '`Build`' 菜单中选择 '`Build Solution`'。

**注意**：如果您使用的是 Microsoft Visual Studio 2017 或更早版本，则必须选择与您的版本兼容的 '`Platform 
Toolset`'：'`Project -> RTOSDemos Properties -> Platform Toolset`'。
  

## 配置演示项目

此演示使用 [FreeRTOS-Plus-TCP TCP/IP 堆栈](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/index.md)，因此请按照 
为 [TCP/IP 入门项目](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md)提供的说明进行操作， 
以确保您：

1. [安装了必备组件](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#prerequisites)（例如 WinPCap）。

2. [设置了静态或动态 IP 地址、网关地址和网络掩码](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#static-dynamic)（可选）。

3. [设置了 MAC 地址](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#mac-addr)（可选）。

4. [在您的主机上选择以太网接口](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#network-interface)。

5. 而且**重要的是**[，在尝试运行 HTTP 演示之前，测试网络连接](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#connectivity-test)。

交付时， TCP/IP 堆栈被配置为使用动态 IP 地址。
  

## 配置 AWS S3 HTTP 服务器连接

此演示使用预签名 URL 连接 AWS S3 HTTP 服务器并授权访问要下载的对象 
。AWS S3 HTTP 服务器的 TLS 连接仅使用服务器验证。在应用程序 
级别，使用预签名 URL 查询中的参数来验证对对象的访问。请按照 
以下步骤配置与 AWS 的连接。

1. 设置一个 Amazon Web Services (AWS) 帐户：

   * 如果您还没有账户，[请创建并激活 AWS 账户](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) 
     （其中包括一个[免费层级](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=categories%23iot)）。

   * 使用 AWS 身份和访问管理 (IAM) 设置帐户和权限。IAM 让您 
     可以管理每个用户的权限。默认情况下，用户需要获得根所有者的授权才具有权限 
     。

     + 要将 IAM 用户添加到您的 AWS 帐户，请参阅 [IAM 用户指南](https://docs.aws.amazon.com/IAM/latest/UserGuide/)。

     + 通过添加下方策略，为您的 AWS 帐户设置访问 FreeRTOS 和 AWS IoT 的权限：

       - AmazonS3FullAccess

2. 按照 [AWS 文档](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html)中提供的步骤在 S3 中创建存储桶

3. 按照 [AWS 文档](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/upload-objects.html)中提供的步骤更新文件至 S3。

4. 使用位于 `FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/Common/presigned_url_generator/presigned_urls_gen.py` 的脚本生成预签名 URL。 
   请参阅 `FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/Common/presigned_url_generato/README.md` 了解使用说明。


## 功能

演示先使用 TLS 服务器身份验证连接到 AWS S3 HTTP 服务器。然后它创建 HTTP  
请求以上传 `democonfigDEMO_HTTP_UPLOAD_DATA` 中指定的数据。上传文件后， 
它会通过请求文件的大小来检查文件是否已成功上传。演示 
的结构 
可在 GitHub 上的 [S3UploadHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Upload/DemoTasks/S3UploadHTTPExample.c#L317-L480) 中找到 
。
  

## 连接到 AWS S3 HTTP 服务器

函数 `connectToServerWithBackoffRetries()` 尝试与 HTTP 服务器建立 TCP 连接。 
如果连接失败，则在超时后重试。超时值将呈指数增长， 
直到达到最大尝试次数或最大超时值。 `connectToServerWithBackoffRetries()` 
如果在配置的尝试次数用尽后仍无法建立与服务器的 TCP 连接，则返回失败状态 
。`connectToServerWithBackoffRetries()` 的源代码位于 
 GitHub 上的 [http_demo_utils.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/Common/http_demo_utils.c#L76-L129)
 。

函数 '`prvConnectToServer()`' 演示了如何仅使用服务器身份验证与 AWS S3 HTTP 服务器建立连接 
。它使用基于 mbedTLS 的传输接口，该接口在文件  
'`FreeRTOS-Plus/Source/Application-Protocols/network_transport/freertos_plus_tcp/using_mbedtls/using_mbedtls.c`' 上实现。 
'`prvConnectToServer()`' 的定义参阅 
 GitHub 上的 [S3UploadHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Upload/DemoTasks/S3UploadHTTPExample.c#L483-L536) 
。
  

## 上传数据

函数 '`prvUploadS3ObjectFile`' 演示了如何创建 PUT 请求并指定要上传的文件 
。在预签名 URL 中指定要上传的 AWS S3 存储桶以及上传时的文件名 
。为节省内存，将同一缓冲区用于请求标头和接收响应 
。使用 API 函数 '`HTTPClient_Send()`' 同步接收响应。一个 `200 OK` 
响应状态代码预计会从 AWS S3 HTTP 服务器返回；若返回任何其他状态代码，则均视为错误。 

'`prvUploadS3ObjectFile`' 的源代码位于 
 GitHub 上的 [S3UploadHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Upload/DemoTasks/S3UploadHTTPExample.c#L706-L800) 
。
  

## 验证上传

函数 '`prvVerifyS3ObjectFileSize`' 调用 '`prvGetS3ObjectFileSize`' 以检索 
 S3 存储桶中对象的大小。S3 HTTP 服务器当前不支持使用预签名 URL 的标头请求， 
因此请求第 0 个字节。文件的大小包含在响应的 `Content-Range`  
标头字段。预计服务器会返回一个 `206 Partial Content` 响应；若返回任何其他状态代码，则均视为错误 
。 

'`prvGetS3ObjectFileSize`' 的源代码位于 
 GitHub 上的 [S3DownloadHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download/DemoTasks/S3DownloadHTTPExample.c#L491-L657) 
。

