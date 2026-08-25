---
title: coreHTTP 演示（相互身份验证）
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---
**注意：我们建议在构建任何物联网 (IoT) 应用程序时始终使用相互身份验证。**

## 单线程 VS 多线程

coreHTTP 有两种使用模式，一种是_单线程_，另一种是_多线程_（多任务）。虽然
本页上的演示是在一个线程中运行 HTTP 库，但实际上演示的是如何在单线程环境中使用 coreHTTP
（演示中只有一个任务使用 HTTP API）。单线程
应用程序必须重复调用 HTTP 库，而多线程应用程序可以在后台的代理（或守护进程）任务中执行发送 
HTTP 请求操作。

## 演示简介

coreHTTP（相互身份验证）演示使用[网络传输接口](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface)，
该接口使用 mbedTLS 在 IoT 设备客户端
（此客户端运行 coreHTTP）和远程 HTTP 服务器之间建立相互身份验证的连接。此演示可以连接到任何能够进行相互身份验证连接的 HTTP 服务器
。连接后，演示创建 HTTP 请求，然后发送请求并接收响应。
下文介绍了如何连接到
[Amazon Web Services (AWS) IoT HTTP 服务器](https://aws.amazon.com/iot-core/)。

共有两个示例项目逐一介绍
[“TLS 简介”](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/02-TLS-introduction)页面上描述的概念，此示例项目是其中之一。
[第一个示例](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/03-coreHTTP-demos/01-coreHTTP-demo)演示了未加密的 HTTP 通信。第二个
示例（即本页面上的示例）在第一个示例的基础上引入强身份验证（其中 HTTP
服务器也验证其所连接的客户端）。

coreHTTP（相互身份验证）演示项目使用
[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)，
因此可以在 Windows 上使用
[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/)
构建和评估，无需任何特定 MCU 硬件。



## 源代码组织

该演示项目名为 http_mutual_auth_demo.sln，位于
`FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_Mutual_Auth` 目录下（此为
[FreeRTOS 主下载文件](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)的目录）（下载页面上也有指向 Github 的链接）。

源代码按照[基本 HTTP 演示（未使用 TLS）组织。](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/03-coreHTTP-demos/01-coreHTTP-demo)

## 配置 HTTP 服务器连接

相互身份验证 HTTP 演示需要客户端身份验证和服务器身份验证。由于大多数
公共 HTTP 服务器不对客户端进行身份验证，因此本演示将介绍与
[AWS (Amazon Web Services) IoT](https://aws.amazon.com/iot-core/)的连接。需要采取额外步骤
来使用 AWS 提供的现有工具获取和设置凭据。为了增强安全性，AWS IoT
不支持纯文本身份验证和仅服务器端的身份验证。
请参阅 [AWS 中的安全性](https://docs.aws.amazon.com/freertos/latest/userguide/security.html)，
了解更多详细信息。

请按照以下步骤配置与 AWS 的连接。

1. 设置一个 Amazon Web Services (AWS) 帐户：

   - 如果您还没有账户，[请创建并激活 AWS 账户](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)
     （其中包括一个[免费层级](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=categories%23iot)）。

2. 使用 [AWS 身份和访问管理 (IAM)](https://aws.amazon.com/iam/) 设置帐户和权限。
   IAM 允许您管理每个用户的权限。默认情况下，用户需要获得根所有者的授权才具有权限
   。

   - 要将 IAM 用户添加到您的 AWS 帐户，请参阅 [IAM 用户指南](https://docs.aws.amazon.com/IAM/latest/UserGuide/)。
   - 通过添加下方策略，为您的 AWS 帐户设置访问 FreeRTOS 和 AWS IoT 的权限：

     - `AmazonFreeRTOSFullAccess`
     - `AWSIoTFullAccess`

   * 要将 AmazonFreeRTOSFullAccess 策略附加到您的 IAM 用户：

     1. 打开 [IAM 控制台](https://console.aws.amazon.com/iam/home)，然后在导航窗格中选择 **Users**。
     2. 在搜索框中输入您的用户名，然后在搜索结果列表中选择它。
     3. 选择 **Add permissions**。
     4. 选择 **Attach existing policies directly**。
     5. 在搜索框中输入 **`AmazonFreeRTOSFullAccess`**，将其从列表中选中，然后选择 **Next: Review**。
     6. 选择 **Add permissions**。

   * 要将 AWSIoTFullAccess 策略附加到您的 IAM 用户：

     1. 打开 [IAM 控制台](https://console.aws.amazon.com/iam/home)，然后在导航窗格中选择 **Users**。
     2. 在搜索框中输入您的用户名，然后在搜索结果列表中选择它。
     3. 选择 **Add permissions**。
     4. 选择 **Attach existing policies directly**。
     5. 在搜索框中输入 **`AWSIoTFullAccess`**，将其从列表中选中，然后选择 **Next: Review**。
     6. 选择 **Add permissions**。

3. 使用 AWS IoT 核心控制台创建 AWS IoT 客户端证书。

   1. 将一个设备添加到 AWS IoT 控制台

      请按照以下[步骤](https://docs.aws.amazon.com/iot/latest/developerguide/device-certs-create.html#device-certs-create-console)操作
      以在 AWS IoT 中创建私钥和证书。立即下载创建的证书和私钥
      。您还需要通过以下步骤找到您的 AWS IoT 端点：

      1. 打开 [AWS IoT 控制台](https://console.aws.amazon.com/iotv2/)。

      2. 在导航窗格中，选择 **连接** 下的 **域配置**。

      您的 AWS IoT 端点将显示为**域名**。其格式应该是：
      **\<unique-identifier-for-your-AWS-IoT-account>`-ats.iot.`\<region>`.amazonaws.com`**。

   2. 在服务端完成设置后，您需要为客户端上的 AWS 
      IoT 凭据配置凭据。将端点和凭据
      粘贴入 `FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_Mutual_Auth/demo_config.h`：

      1. 将 **AWS IoT 自定义端点**复制到 `#define democonfigAWS_IOT_ENDPOINT `"\<Domain-Name>"。

      2. 将从 AWS IoT 控制台下载的根 CA 证书复制到
         `#define democonfigROOT_CA_PEM `"\<Root-CA>"。

      3. 将从 AWS IoT 控制台下载的客户端证书复制到
         `#define democonfigCLIENT_CERTIFICATE_PEM `"\<Client-Certificate>"。

      4. 将从 AWS IoT 控制台下载的客户端私钥复制到
         `#define democonfigCLIENT_PRIVATE_KEY_PEM `"\<Client-Private-Key>"。

### 构建演示项目

此演示项目的构建方式与[基本 HTTP 演示（未使用 TLS）](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/03-coreHTTP-demos/01-coreHTTP-demo#source_code)相同。
演示项目使用社区免费版 [Visual Studio](https://visualstudio.microsoft.com/vs/community/)。
要构建此演示：

- 从 Visual Studio IDE 中打开 `FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_Mutual_Auth/http_mutual_auth_demo.sln`
  Visual Studio 解决方案文件

- 在 IDE 的 "Build" 菜单中选择 "Build Solution"

**注意**：如果您使用的是 Microsoft Visual Studio 2017 或更早版本，则必须选择与您的版本兼容的 Platform Toolset：
Project -> RTOSDemos Properties -> Platform Toolset

### 功能

此演示提供与基本 HTTP 演示相同的功能，并增添了
到您的 AWS IoT 端点的安全连接。如需了解其他功能的详细信息（创建 HTTP 请求、发送
请求并接收响应），请查看[基本 HTTP 演示（未使用 TLS）。](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/03-coreHTTP-demos/01-coreHTTP-demo#functionality)

演示创建了一个单一的应用程序任务，演示了如何连接至 AWS IoT HTTP 服务器、
创建 HTTP 请求、发送 HTTP 请求并接收 HTTP 响应，最后与服务器断开连接
。此演示的结构体如下所示。

```c
static void prvHTTPDemoTask( void * pvParameters )
{
    /* The transport layer interface used by the HTTP Client library. */
    TransportInterface_t xTransportInterface;
    /* The network context for the transport layer interface. */
    NetworkContext_t xNetworkContext = { 0 };
    TlsTransportParams_t xTlsTransportParams = { 0 };
    BaseType_t xIsConnectionEstablished = pdFALSE;

    /* The user of this demo must check the logs for any failure codes. */
    BaseType_t xDemoStatus = pdPASS;

    /* Remove compiler warnings about unused parameters. */
    ( void ) pvParameters;

    /* Set the pParams member of the network context with desired transport. */
    xNetworkContext.pParams = &xTlsTransportParams;

    /**************************** Connect. ******************************/

    /* Attempt to connect to the HTTP server. If connection fails, retry after a
     * timeout. The timeout value will be exponentially increased until either the
     * maximum number of attempts or the maximum timeout value is reached. The
     * function returns pdFAIL if the TCP connection cannot be established with
     * the server after configured number of attempts. */
    xDemoStatus = connectToServerWithBackoffRetries( prvConnectToServer,
                                                     &xNetworkContext );

    if( xDemoStatus == pdPASS )
    {
        /* Set a flag indicating that a TLS connection exists. */
        xIsConnectionEstablished = pdTRUE;

        /* Define the transport interface. */
        xTransportInterface.pNetworkContext = &xNetworkContext;
        xTransportInterface.send = TLS_FreeRTOS_send;
        xTransportInterface.recv = TLS_FreeRTOS_recv;
    }
    else
    {
        /* Log error to indicate connection failure after all
         * reconnect attempts are over. */
        LogError( ( "Failed to connect to HTTP server %.*s.",
                    ( int32_t ) AWS_IOT_ENDPOINT_LENGTH,
                    democonfigAWS_IOT_ENDPOINT ) );
    }

    /*********************** Send HTTP request.************************/

    if( xDemoStatus == pdPASS )
    {
        xDemoStatus = prvSendHttpRequest( &xTransportInterface,
                                          HTTP_METHOD_POST,
                                          ( sizeof( HTTP_METHOD_POST ) - 1 ),
                                          democonfigPOST_PATH,
                                          ( sizeof( democonfigPOST_PATH ) - 1 ) );
    }

    /**************************** Disconnect. ******************************/

    /* Close the network connection to clean up any system resources that the
     * demo may have consumed. */
    if( xIsConnectionEstablished == pdTRUE )
    {
        /* Close the network connection. */
        TLS_FreeRTOS_Disconnect( &xNetworkContext );
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

### 连接到 HTTP 服务器（带相互身份验证）

函数 `connectToServerWithBackoffRetries()` 试图与
HTTP 服务器建立相互验证身份的 TLS 连接。如果连接失败，函数会在超时后重试。超时值将呈指数增长，
直到达到最大尝试次数或最大超时值。函数
`BackoffAlgorithm_GetNextBackoff()` 提供呈指数增长的超时值，
并在达到最大尝试次数时返回 `BackoffAlgorithmRetriesExhausted`。
如果在配置的尝试次数后仍无法与服务器建立 TLS 连接，则 `connectToServerWithBackoffRetries()` 将返回失败状态
。

```c
BaseType_t connectToServerWithBackoffRetries( TransportConnect_t connectFunction,
                                              NetworkContext_t * pxNetworkContext )
{
    BaseType_t xReturn = pdFAIL;
    /* Status returned by the retry utilities. */
    BackoffAlgorithmStatus_t xBackoffAlgStatus = BackoffAlgorithmSuccess;
    /* Struct containing the next backoff time. */
    BackoffAlgorithmContext_t xReconnectParams;
    uint16_t usNextBackoff = 0U;

    assert( connectFunction != NULL );

    /* Initialize reconnect attempts and interval */
    BackoffAlgorithm_InitializeParams( &xReconnectParams,
                                       RETRY_BACKOFF_BASE_MS,
                                       RETRY_MAX_BACKOFF_DELAY_MS,
                                       RETRY_MAX_ATTEMPTS );

    /* Attempt to connect to the HTTP server. If connection fails, retry after a
     * timeout. The timeout value will exponentially increase until either the
     * maximum timeout value is reached or the set number of attempts are
     * exhausted.*/
    do
    {
        xReturn = connectFunction( pxNetworkContext );

        if( xReturn != pdPASS )
        {
            LogWarn( ( "Connection to the HTTP server failed. "
                       "Retrying connection with backoff and jitter." ) );
            LogInfo( ( "Retry attempt %lu out of maximum retry attempts %lu.",
                       ( xReconnectParams.attemptsDone + 1 ),
                         RETRY_MAX_ATTEMPTS ) );

            /* Generate a random number and calculate backoff value (in milliseconds) for
             * the next connection retry.
             * Note: It is recommended to seed the random number generator with a device-specific
             * entropy source so that possibility of multiple devices retrying failed network operations
             * at similar intervals can be avoided. */
            xBackoffAlgStatus = BackoffAlgorithm_GetNextBackoff( &xReconnectParams, uxRand(), &usNextBackoff );
        }
    } while( ( xReturn == pdFAIL ) && ( xBackoffAlgStatus == BackoffAlgorithmSuccess ) );

    if( xReturn == pdFAIL )
    {
        LogError( ( "Connection to the server failed, all attempts exhausted." ) );
    }

    return xReturn;
}

```

函数 `prvConnectToServer()` 演示了如何与服务器建立 HTTP 连接。它
使用 TLS 传输接口，此接口在
文件 `FreeRTOS-Plus/Source/Application-Protocols/network_transport/freertos_plus_tcp/using_mbedtls/using_mbedtls.c` 中实现。
`prvConnectToServer()` 的定义如下。

```c
static BaseType_t prvConnectToServer( NetworkContext_t * pxNetworkContext )
{
    BaseType_t xStatus = pdPASS;

    TlsTransportStatus_t xNetworkStatus;
    NetworkCredentials_t xNetworkCredentials = { 0 };

    configASSERT( pxNetworkContext != NULL );

    if( democonfigAWS_HTTP_PORT == 443 )
    {
        /* ALPN protocols must be a NULL-terminated list of strings. Therefore,
         * the first entry will contain the actual ALPN protocol string while the
         * second entry must remain NULL. */
        static const char * pcAlpnProtocols[] = { IOT_CORE_ALPN_PROTOCOL_NAME, NULL };
        xNetworkCredentials.pAlpnProtos = pcAlpnProtocols;
    }

    xNetworkCredentials.disableSni = democonfigDISABLE_SNI;
    /* Set the credentials for establishing a TLS connection. */
    xNetworkCredentials.pRootCa = ( const unsigned char * ) democonfigROOT_CA_PEM;
    xNetworkCredentials.rootCaSize = sizeof( democonfigROOT_CA_PEM );
    xNetworkCredentials.pClientCert = ( const unsigned char * ) democonfigCLIENT_CERTIFICATE_PEM;
    xNetworkCredentials.clientCertSize = sizeof( democonfigCLIENT_CERTIFICATE_PEM );
    xNetworkCredentials.pPrivateKey = ( const unsigned char * ) democonfigCLIENT_PRIVATE_KEY_PEM;
    xNetworkCredentials.privateKeySize = sizeof( democonfigCLIENT_PRIVATE_KEY_PEM );

    /* Establish a TLS session with the HTTP server. This example connects to
     * the HTTP server as specified in democonfigAWS_IOT_ENDPOINT and
     * democonfigAWS_HTTP_PORT in demo_config.h. */
    LogInfo( ( "Establishing a TLS session to %.*s:%d.",
               ( int32_t ) AWS_IOT_ENDPOINT_LENGTH,
               democonfigAWS_IOT_ENDPOINT,
               democonfigAWS_HTTP_PORT ) );

    /* Attempt to create a mutually authenticated TLS connection. */
    xNetworkStatus = TLS_FreeRTOS_Connect( pxNetworkContext,
                                           democonfigAWS_IOT_ENDPOINT,
                                           democonfigAWS_HTTP_PORT,
                                           &xNetworkCredentials,
                                           democonfigTRANSPORT_SEND_RECV_TIMEOUT_MS,
                                           democonfigTRANSPORT_SEND_RECV_TIMEOUT_MS );

    if( xNetworkStatus != TLS_TRANSPORT_SUCCESS )
    {
        xStatus = pdFAIL;
    }

    return xStatus;
}
```
