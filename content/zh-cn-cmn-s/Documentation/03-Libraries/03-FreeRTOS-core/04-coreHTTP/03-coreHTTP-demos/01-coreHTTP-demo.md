---
title: coreHTTP 演示（无 TLS）
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


* 本页内容：
	+ [简介](#引言)
		- [单线程 vs. 多线程](#单线程-vs-多线程)
	+ [源代码组织](#源代码组织)
	+ [配置演示项目](#配置演示项目)
	+ [配置 HTTP 服务器连接](#配置-http-服务器连接)
		- [选项 1：使用公共托管的 HTTP 服务器](#选项-1-使用公共托管的-http-服务器)
		- [选项 2：使用本地托管的 HTTP 服务器](#选项-2-使用本地托管的-http-服务器)
		- [选项 3：您选择的任何其他未加密 HTTP 服务器：](#选项-3-您选择的任何其他未加密-http-服务器)
	+ [构建演示项目](#构建演示项目)
	+ [功能](#功能)
		- [连接到 HTTP 服务器](#连接到-http-服务器)
		- [发送 HTTP 请求并接收响应](#发送-http-请求并接收响应)


**注意：我们建议在任何物联
网 (IoT) 应用程序中使用相互身份验证。此页面上的演示在引入加密和身份验证之前演示了 
HTTP 通信，仅用于教育目的，不适用于
生产。**


## 引言

此演示程序展示了如何使用 coreHTTP 库与 HTTP 服务器建立连接，
以演示简单的请求/响应工作流程。在请求创建后，请求会被发送出去，
演示将同步等待接收响应。

此示例项目逐一介绍[“TLS 简介”](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/02-TLS-introduction)页面中所阐述的概念
。第一个示例 （本页）演示了未加密 HTTP 通信。
[第二个示例](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/03-coreHTTP-demos/02-Mutual-authentication)在此基础上引入了强力相互身份验证
（其中 HTTP 服务器也会对其所连接的 IoT 客户端进行身份验证）。

此演示**未**创建安全的连接，因此不适合生产使用——
请勿在未加密的网络连接上发送任何机密信息。演示展示了如何
在连接失败的情况下，使用指数退避时间（包括定时抖动）进行连接。指数级
增加连接尝试之间的时间，并包括一些随机的定时抖动，是
大型 IoT 设备群的最佳做法，因为它可以防止在所有 IoT 设备在同一时间断开连接的情况下
同时尝试重新连接。


此基础 HTTP 演示项目使用
[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)，
因此可以在 Windows 上使用
[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/) 进行构建和评估，
无需任何特定 MCU 硬件。

coreHTTP 库是一个 [MIT 授权](/Documentation/03-Libraries/01-Library-overview/04-Licensing)的开源 HTTP 客户端 C 库，
专为基于微控制器和小型微处理器的 IoT 设备打造。


### 单线程 VS 多线程

coreHTTP 有两种使用模式，一种是*单线程*，另一种是*多线程*（多任务）。尽管
此页演示了在一个线程中运行 HTTP 库，它实际上演示了如何在一个单线程环境中使用 coreHTTP
（即在演示中仅有一个任务使用 HTTP API）。尽管单线程
应用程序必须重复调用 HTTP 库，多线程应用程序可以在后台的代理任务（或守护进程）中发送 HTTP
请求。


## 源代码组织

演示项目名为 `http_plain_text_demo.sln`，可在
`FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_Plaintext` 目录下（此为
[FreeRTOS 主下载文件的目录](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)）（也可在下载页面链接的 Github 中找到）
。


## 配置演示项目

此演示使用 [FreeRTOS-Plus-TCP TCP/IP 堆栈](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)，因此
请按照
[TCP/IP 入门项目](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)的说明操作，以确保您：


1. [安装了必备组件](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites)（例如 WinPCap）。

2. [设置了静态或动态 IP 地址、网关地址和网络掩码](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic)（可选）。

3. [设置了 MAC 地址](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr)（可选）。

4. [在您的主机上选择以太网接口](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface)。

5. ……**最重要的是**，在尝试运行 HTTP 演示之前，[测试了网络连接](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#connectivity-test)。

每个演示项目都有自己的配置设置。因此，当您遵循这些网络配置说明时，
确保仅在 HTTP 演示项目中应用设置，而不要在 TCP/IP 入门项目中应用
。默认情况下，TCP/IP 堆栈被配置为使用动态 IP 地址。


## 配置 HTTP 服务器连接

### 选项 1 ：使用公共托管的 HTTP 服务器

演示项目可以在 “httpbin.org” 上与公共托管的 HTTP 服务器通信。如果
演示连接到具有 DHCP 服务和互联网接入的网络，则此操作应有效。请注意，FreeRTOS
 Windows 移植仅适用于有线以太网适配器（可以是虚拟以太网适配器）。
您应该使用单独的 HTTP 客户端，如您的 Web 浏览器，来测试 HTTP 连接
（从您的主机到公共 HTTP 服务器的连接）。要使用托管 HTTP 服务器：

1. 打开 `/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_Plaintext/demo_config.h`的本地副本。

2. 增加以下行：

   ```c
   #define democonfigSERVER_HOSTNAME "httpbin.org"
   #define democonfigHTTP_PORT ( 80 )
   ```

**注意**：httpbin 是支持 HTTP/1.1 的开源 HTTP 服务器。它是 Postmanlabs 的一部分，
其链接在[这里](https://github.com/postmanlabs/httpbin)。httpbin.org 服务器不隶属于
FreeRTOS，也不由其维护，可能随时不可用。


### 选项 2 ：使用本地托管的 HTTP 服务器

httpbin 服务器也可以在本地运行，或在本地网络的另一台机器上运行。请按以下步骤操作：

1. 安装 [Docker](https://docs.docker.com/docker-for-windows/install/)。

2. 使用以下命令通过端口 80 运行 httpbin：

   ```c
   docker pull kennethreitz/httpbin
   docker run -p 80:80 kennethreitz/httpbin
   ```

3. 通过以下步骤验证 httpbin 服务器是否在本地运行并监听8080端口：

   1. 打开 PowerShell。
   2. 要检查在 80 端口上是否有一个监听的活动连接，请输入指令

      ```c
      netstat -a -p TCP | findstr 80
      ```
   3. 确认你看到的输出是这样的：

      ```c
      TCP    0.0.0.0:80           <HOST-NAME>:0       LISTENING
      ```

4. 打开 `FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_Plaintext/demo_config.h`。

5. 增加以下行：

   ```c
   #define democonfigSERVER_HOSTNAME "ipv4_address_of_your_machine"
   #define democonfigHTTP_PORT ( 80 )
   ```

   您应该使用单独的 HTTP 客户端，如您的 Web 浏览器，来测试 HTTP 连接
   （从您的主机到已安装的 HTTP 客户端的连接）。

   **注意：**端口号 80 是未加密的 HTTP 默认端口号。如果您无法使用那个
   端口（例如，它被你的 IT 安全策略所阻止，或者端口被 Windows 中的另一个系统进程所使用），
   将 docekr 容器所使用的端口更改为高端口号（例如，在50000到55000范围内），
   并相应设置 `democonfigHTTP_PORT` 。欲进行此更改，您可以运行

   ```c
   docker run -p *<HIGH_PORT_NUMBER>*:80 kennethreitz/httpbin
   ```


### 选项 3 ：您选择的任何其他未加密 HTTP 服务器：

任何支持未加密 HTTP /IP 通信的 TCP服务器都可与此演示一起使用。请按以下步骤操作：

1. 打开 `/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_Plaintext/demo_config.h`的本地副本。

2. 添加下列行，并设置您所选择的服务器：

   ```c
   #define democonfigSERVER_HOSTNAME "your-desired-endpoint"
   #define democonfigHTTP_PORT ( 80 )
   ```


## 构建演示项目

演示项目使用[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/)。
要构建演示，请执行如下操作：

1. 从 Visual Studio IDE 中打开 `/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_Plaintext/http_plain_text_demo.sln`
   Visual Studio 解决方案文件

2. 在 IDE 的 '**build**'（构建）菜单中选择 '**build solution**' （构建解决方案）。


## 功能

演示创建了一个单一的应用程序任务，演示了如何：

* 连接到 AWS IoT HTTP 服务器，
* 创建 HTTP 请求，
* 发送 HTTP 请求，
* 接收 HTTP 响应，最后，
* 断开与服务器的连接。

演示的结构体为：

```c
static void prvHTTPDemoTask( void * pvParameters )
{
    /* The transport layer interface used by the HTTP Client library. */
    TransportInterface_t xTransportInterface;
    /* The network context for the transport layer interface. */
    NetworkContext_t xNetworkContext = { 0 };
    PlaintextTransportParams_t xPlaintextTransportParams = { 0 };
    /* An array of HTTP paths to request. */
    const httpPathStrings_t xHttpMethodPaths[] =
    {
        { democonfigGET_PATH,  httpexampleGET_PATH_LENGTH  },
        { democonfigHEAD_PATH, httpexampleHEAD_PATH_LENGTH },
        { democonfigPUT_PATH,  httpexamplePUT_PATH_LENGTH  },
        { democonfigPOST_PATH, httpexamplePOST_PATH_LENGTH }
    };
    /* The respective method for the HTTP paths listed in #httpMethodPaths. */
    const httpMethodStrings_t xHttpMethods[] =
    {
        { HTTP_METHOD_GET,  httpexampleHTTP_METHOD_GET_LENGTH  },
        { HTTP_METHOD_HEAD, httpexampleHTTP_METHOD_HEAD_LENGTH },
        { HTTP_METHOD_PUT,  httpexampleHTTP_METHOD_PUT_LENGTH  },
        { HTTP_METHOD_POST, httpexampleHTTP_METHOD_POST_LENGTH }
    };
    BaseType_t xIsConnectionEstablished = pdFALSE;
    UBaseType_t uxHttpPathCount = 0U;

    /* The user of this demo must check the logs for any failure codes. */
    BaseType_t xDemoStatus = pdPASS;

    /* Remove compiler warnings about unused parameters. */
    ( void ) pvParameters;

    /* Set the pParams member of the network context with desired transport. */
    xNetworkContext.pParams = &xPlaintextTransportParams;


    /**************************** Connect. ******************************/


    /* Attempt to connect to the HTTP server. If connection fails, retry after a
     * timeout. The timeout value will be exponentially increased until either the
     * maximum number of attempts or the maximum timeout value is reached. The
     * function returns pdFAIL if the TCP connection cannot be established with
     * the server after the number of attempts. */
    xDemoStatus = connectToServerWithBackoffRetries( prvConnectToServer,
                                                     &xNetworkContext );

    if( xDemoStatus == pdPASS )
    {
        /* Set a flag indicating that a TCP connection has been established. */
        xIsConnectionEstablished = pdTRUE;

        /* Define the transport interface. */
        xTransportInterface.pNetworkContext = &xNetworkContext;
        xTransportInterface.send = Plaintext_FreeRTOS_send;
        xTransportInterface.recv = Plaintext_FreeRTOS_recv;
    }
    else
    {
        /* Log error to indicate connection failure after all
         * reconnect attempts are over. */
        LogError( ( "Failed to connect to HTTP server %.*s.",
                    ( int32_t ) httpexampleSERVER_HOSTNAME_LENGTH,
                    democonfigSERVER_HOSTNAME ) );
    }


    /*********************** Send HTTP request.************************/


    for( uxHttpPathCount = 0;
         uxHttpPathCount < httpexampleNUMBER_HTTP_PATHS;
         ++uxHttpPathCount )
    {
        if( xDemoStatus == pdPASS )
        {
            xDemoStatus = prvSendHttpRequest(
                              &xTransportInterface,
                              xHttpMethods[ uxHttpPathCount ].pcHttpMethod,
                              xHttpMethods[ uxHttpPathCount ].ulHttpMethodLength,
                              xHttpMethodPaths[ uxHttpPathCount ].pcHttpPath,
                              xHttpMethodPaths[ uxHttpPathCount ].ulHttpPathLength );
        }
        else
        {
            break;
        }
    }


    /**************************** Disconnect. ******************************/


    /* Close the network connection to clean up any system resources that the
     * demo may have consumed. */
    if( xIsConnectionEstablished == pdTRUE )
    {
        /* Close the network connection. */
        Plaintext_FreeRTOS_Disconnect( &xNetworkContext );
    }


    if( xDemoStatus == pdPASS )
    {
        LogInfo( ( "prvHTTPDemoTask() completed successfully. "
                   "Total free heap is %u.\r\n",
                   xPortGetFreeHeapSize() ) );
        LogInfo( ( "Demo completed successfully.\r\n" ) );
    }
}
```


### 连接到 HTTP 服务器

在上述函数中， `connectToServerWithBackoffRetries()` 试图建立 TCP 连接到
HTTP 服务器。如果连接失败，则在超时后重试。超时值将呈指数增长，
并包括一些随机抖动，直到达到最大的尝试次数
或达到最大的超时值。在生产设备中使用这种类型的退避算法，
可确保如果一组 IoT 设备同时断开连接，它们不会同时尝试重新连接，
从而导致服务器不堪重负。如果连接成功，则连接的
TCP 套接字将在 `xNetworkContext` 参数中返回。

`prvConnectToServer()` 函数演示了如何与 HTTP服务器建立
未加密的连接。它使用 FreeRTOS-Plus-TCP [传输接口](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface)，
该接口在文件 `FreeRTOS-Plus/Source/Application-Protocols/network_transport/freertos_plus_tcp/using_plaintext/using_plaintext.c`中实现。
`prvConnectToServer()` 的定义如下：

```c
static BaseType_t prvConnectToServer( NetworkContext_t * pxNetworkContext )
{
    BaseType_t xStatus = pdPASS;

    PlaintextTransportStatus_t xNetworkStatus;

    configASSERT( pxNetworkContext != NULL );

    /* Establish a TCP connection with the HTTP server. This example connects
     * to the HTTP server as specified in democonfigSERVER_HOSTNAME and
     * democonfigHTTP_PORT in demo_config.h. */
    LogInfo( ( "Establishing a TCP connection to %.*s:%d.",
               ( int32_t ) httpexampleSERVER_HOSTNAME_LENGTH,
               democonfigSERVER_HOSTNAME,
               democonfigHTTP_PORT ) );
    xNetworkStatus = Plaintext_FreeRTOS_Connect(
                         pxNetworkContext,
                         democonfigSERVER_HOSTNAME,
                         democonfigHTTP_PORT,
                         democonfigTRANSPORT_SEND_RECV_TIMEOUT_MS,
                         democonfigTRANSPORT_SEND_RECV_TIMEOUT_MS );

    if( xNetworkStatus != PLAINTEXT_TRANSPORT_SUCCESS )
    {
        xStatus = pdFAIL;
    }

    return xStatus;
}

```


### 发送 HTTP 请求并接收响应

函数 `prvSendHttpRequest()` 演示了如何创建 HTTP 请求，然后将其发送到
服务器。在 `HTTPClient_Send()`的同一个 API 调用中同步接收响应。

```c
static BaseType_t prvSendHttpRequest(
                      const TransportInterface_t * pxTransportInterface,
                      const char * pcMethod,
                      size_t xMethodLen,
                      const char * pcPath,
                      size_t xPathLen )
{
    /* Return value of this method. */
    BaseType_t xStatus = pdPASS;

    /* Configurations of the initial request headers that are passed to
     * #HTTPClient_InitializeRequestHeaders. */
    HTTPRequestInfo_t xRequestInfo;
    /* Represents a response returned from an HTTP server. */
    HTTPResponse_t xResponse;
    /* Represents header data that will be sent in an HTTP request. */
    HTTPRequestHeaders_t xRequestHeaders;

    /* Return value of all methods from the HTTP Client library API. */
    HTTPStatus_t xHTTPStatus = HTTPSuccess;

    configASSERT( pcMethod != NULL );
    configASSERT( pcPath != NULL );

    /* Initialize all HTTP Client library API structs to 0. */
    ( void ) memset( &xRequestInfo, 0, sizeof( xRequestInfo ) );
    ( void ) memset( &xResponse, 0, sizeof( xResponse ) );
    ( void ) memset( &xRequestHeaders, 0, sizeof( xRequestHeaders ) );

    /* Initialize the request object. */
    xRequestInfo.pHost = democonfigSERVER_HOSTNAME;
    xRequestInfo.hostLen = httpexampleSERVER_HOSTNAME_LENGTH;
    xRequestInfo.pMethod = pcMethod;
    xRequestInfo.methodLen = xMethodLen;
    xRequestInfo.pPath = pcPath;
    xRequestInfo.pathLen = xPathLen;

    /* Set "Connection" HTTP header to "keep-alive" so that multiple requests
     * can be sent over the same established TCP connection. */
    xRequestInfo.reqFlags = HTTP_REQUEST_KEEP_ALIVE_FLAG;

    /* Set the buffer used for storing request headers. */
    xRequestHeaders.pBuffer = ucUserBuffer;
    xRequestHeaders.bufferLen = democonfigUSER_BUFFER_LENGTH;

    xHTTPStatus = HTTPClient_InitializeRequestHeaders( &xRequestHeaders,
                                                       &xRequestInfo );

    if( xHTTPStatus == HTTPSuccess )
    {
        /* Initialize the response object. The same buffer used for storing
         * request headers is reused here. */
        xResponse.pBuffer = ucUserBuffer;
        xResponse.bufferLen = democonfigUSER_BUFFER_LENGTH;

        LogInfo( ( "Sending HTTP %.*s request to %.*s%.*s...",
                   ( int32_t ) xRequestInfo.methodLen, xRequestInfo.pMethod,
                   ( int32_t ) httpexampleSERVER_HOSTNAME_LENGTH, democonfigSERVER_HOSTNAME,
                   ( int32_t ) xRequestInfo.pathLen, xRequestInfo.pPath ) );
        LogInfo( ( "Request Headers:\n%.*s\n"
                   "Request Body:\n%.*s\n",
                   ( int32_t ) xRequestHeaders.headersLen,
                   ( char * ) xRequestHeaders.pBuffer,
                   ( int32_t ) httpexampleREQUEST_BODY_LENGTH, democonfigREQUEST_BODY ) );

        /* Send the request and receive the response. */
        xHTTPStatus = HTTPClient_Send( pxTransportInterface,
                                       &xRequestHeaders,
                                       ( uint8_t * ) democonfigREQUEST_BODY,
                                       httpexampleREQUEST_BODY_LENGTH,
                                       &xResponse,
                                       0 );
    }
    else
    {
        LogError( ( "Failed to initialize HTTP request headers: Error=%s.",
                    HTTPClient_strerror( xHTTPStatus ) ) );
    }

    if( xHTTPStatus == HTTPSuccess )
    {
        LogInfo( ( "Received HTTP response from %.*s%.*s...\n",
                   ( int32_t ) httpexampleSERVER_HOSTNAME_LENGTH,
                   democonfigSERVER_HOSTNAME,
                   ( int32_t ) xRequestInfo.pathLen, xRequestInfo.pPath ) );
        LogDebug( ( "Response Headers:\n%.*s\n",
                    ( int32_t ) xResponse.headersLen, xResponse.pHeaders ) );
        LogDebug( ( "Status Code:\n%u\n",
                    xResponse.statusCode ) );
        LogDebug( ( "Response Body:\n%.*s\n",
                    ( int32_t ) xResponse.bodyLen, xResponse.pBody ) );
    }
    else
    {
        LogError( ( "Failed to send HTTP %.*s request to %.*s%.*s: Error=%s.",
                    ( int32_t ) xRequestInfo.methodLen,
                    xRequestInfo.pMethod,
                    ( int32_t ) httpexampleSERVER_HOSTNAME_LENGTH,
                    democonfigSERVER_HOSTNAME,
                    ( int32_t ) xRequestInfo.pathLen,
                    xRequestInfo.pPath,
                    HTTPClient_strerror( xHTTPStatus ) ) );
    }

    if( xHTTPStatus != HTTPSuccess )
    {
        xStatus = pdFAIL;
    }

    return xStatus;
}

```
