---
title: "coreMQTT 演示（相互身份验证）"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

**注意：我们建议在构建任何物联网 (IoT) 应用程序时始终使用相互身份验证。**

本页所述的 [coreMQTT 演示（相互身份验证）](https://github.com/FreeRTOS/FreeRTOS/tree/202012.00/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth)
使用 MBEDTLS 来执行加密函数。另一个使用
WolfSSL 的演示位于
[Github](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth_wolfSSL)，其中还包括
将演示从 MBEDTLS 转换为 WolfSSL [的说明](https://github.com/FreeRTOS/FreeRTOS-SESIP/blob/main/docs/wolfSSL-migration-guide/migrating_to_wolfssl.md)
。此新演示将在即将发布的 FreeRTOS 中提供。

## 单线程 VS 多线程

coreMQTT 有两种使用模式，_单线程_和_多线程_（多任务）。在多线程应用程序中，
仅在一个线程上使用 MQTT 库（如本页记录的演示那样）
等同于单线程用例。单线程
用例要求应用程序写入器对 MQTT 库进行重复的显式调用。与此不同的是，
多线程用例可以从一个[ agent（或守护进程任务）任务中在后台执行 MQTT 协议](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo)。
在 agent 任务中执行 MQTT 协议使应用程序写入器无需
显式托管任何 MQTT 状态或调用 `MQTT_ProcessLoop()` API 函数。使用 agent 任务还可以
让多个应用程序任务共享单个 MQTT 连接，无需互斥锁之类的同步基元
。

## 演示简介

共有三个示例项目逐一介绍
[“TLS 简介”](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/02-TLS-introduction)页面上描述的概念，此示例项目是其中之一。[第一个示例](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/01-coreMQTT-demo)
演示未加密的 MQTT 通信，[第二个示例](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/02-coreMQTT-demo-LTS)建立在第一个示例的基础上，但引入了服务器身份验证（IoT 客户端对其连接到的 MQTT 服务器进行身份验证）
。第三个示例（即本页面上的示例）在第二个示例的基础上引入了强相互身份验证（其中
MQTT 服务器也验证其所连接的客户端）。

此演示使用了一个[网络传输接口](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface)，此接口使用 mbedTLS，
在运行 coreMQTT 的 IoT 设备客户端和 MQTT 代理之间建立相互验证身份的连接。
它可以与任何具备相互身份验证连接功能的 MQTT 代理一起使用。
下文的说明介绍了如何连接到 [Amazon Web Services (AWS) IoT 消息代理](https://aws.amazon.com/iot-core/)
或者到主机上本地运行的 MQTT 服务器。

连接后，演示会订阅一个 MQTT 主题，接着发布到相同的 MQTT 主题，然后等待
从 MQTT 服务器返回的消息（由于 MQTT 客户端已订阅与其所发布主题相同的主题，
因此会接收回消息）。它会无限期重复发布和接收循环。

该演示使用 [QoS 1](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/01-MQTT-terminology) 来发布和订阅，这意味着每个 MQTT 消息至少接收一次。

coreMQTT（相互身份验证）演示项目使用
[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)，
因此可以在 Windows 上使用
[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/)
构建和评估，无需任何特定 MCU 硬件。

## 源代码组织

该演示项目名为 mqtt_mutual_auth_demo.sln，位于
`FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth` 目录中（此为 [FreeRTOS 主下载文件中的目录](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)）
（下载页面上也有指向 Github 的链接）。

源代码的组织方式与[基本 MQTT 演示（未使用 TLS ）相同。](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/01-coreMQTT-demo)

## 配置 MQTT 代理连接

### 选项 1：使用 AWS IoT 消息代理（Web 托管）：

相互身份验证 MQTT 演示需要客户端身份验证以及
[带有 TLS （服务器身份验证）演示的 MQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/02-coreMQTT-demo-LTS) 要求的服务器身份验证。由于大多数公共
 代理不对客户端进行身份验证，此演示将介绍与 AWS (Amazon Web Services)
 IoT 的连接。还需要采取其他步骤，以利用
 AWS 提供的现有工具获取和设置凭据。完成以下设置步骤后，其他 AWS IoT 相关的演示中也可复用此配置，
 例如 [AWS IoT Device Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/04-Device-shadow-demo)。为了增强安全性，AWS IoT
 不支持纯文本身份验证和仅服务器端的身份验证。
 请参阅 [AWS 中的安全性](https://docs.aws.amazon.com/freertos/latest/userguide/security.html)，了解更多详细信息。

请按照以下步骤配置与 AWS的连接。

1. 设置一个 Amazon Web Services (AWS) 帐户：

   - 如果您还没有账户，[请创建并激活 AWS 账户](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)
     （其中包括一个[免费层级](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=categories%23iot)）。

2. 使用 AWS 身份和访问管理 (IAM) 设置帐户和权限。IAM 让您
   可以管理每个用户的权限。默认情况下，用户需要获得根用户的授权才具有权限
   。

   - 要将 IAM 用户添加到您的 AWS 帐户，请参阅 [IAM 用户指南](https://docs.aws.amazon.com/IAM/latest/UserGuide/)。
   - 通过添加下方策略，为您的 AWS 帐户设置访问 FreeRTOS 和 AWS IoT 的权限：

     - `AmazonFreeRTOSFullAccess`
     - `AWSIoTFullAccess`

     要将 AmazonFreeRTOSFullAccess 策略附加到您的 IAM 用户：

     1. 打开 [IAM 控制台](https://console.aws.amazon.com/iam/home)，然后在导航窗格中选择 **Users**。
     2. 在搜索框中输入您的用户名，然后在搜索结果列表中选择它。
     3. 选择 **Add permissions**。
     4. 选择 **Attach existing policies directly**。
     5. 在搜索框中输入 **`AmazonFreeRTOSFullAccess`**，将其从列表中选中，然后选择 **Next: Review**。
     6. 选择 **Add permissions**。

     要将 AWSIoTFullAccess 策略附加到您的 IAM 用户：

     1. 打开 [IAM 控制台](https://console.aws.amazon.com/iam/home)，然后在导航窗格中选择 **Users**。
     2. 在搜索框中输入您的用户名，然后在搜索结果列表中选择它。
     3. 选择 **Add permissions**。
     4. 选择 **Attach existing policies directly**。
     5. 在搜索框中输入 **`AWSIoTFullAccess`**，将其从列表中选中，然后选择 **Next: Review**。
     6. 选择 **Add permissions**。

3. 使用 AWS Command Line Interface (CLI) 或 AWS IoT 控制台将设备注册为 AWS IoT thing。 
   使用 AWS CLI，可通过命令行而不是 AWS IoT 控制台接口执行配置
   。有关设置 CLI 的更多信息，请在此处查看其他文档。 
   AWS IoT 控制台提供一个用户界面用于手动设置设备。

   - **选项 1（推荐）：**通过 AWS 命令行接口 (CLI) 设置：

     1. 在您的计算机上[下载并安装](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
        AWS CLI。
     2. 使用 pip 安装 boto3：`pip install boto3`
     3. 继续执行[快速配置 AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration) 中的步骤
        以使用您的 AWS 帐户信息进将其设置完成
     4. 使用提供的 python 脚本注册设备。脚本设置 MQTT 代理（使用
        您输入的 “thing” 名称），下载私钥，并将凭据写入
        `FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth/demo_config.h.`。

        1. 在文件 `{FreeRTOS-root-directory}/tools/aws_config_quick_start/configure.json` 中，将 `"$thing_name"` 更改为您的
           MQTT 客户端 ID。您输入的 thing 名称应附上双引号 (`""`)，且只能组合使用
           字母、数字、分号 (`:`)、下划线 (`_`) 和连字符 (`-`)。

        2. 要完成设置，请打开终端，导航到 `{FreeRTOS-root-directory}/tools/aws_config_quick_start` 目录并
           运行：`python SetupAWS.py setup`

        3. 如果您使用 python3 安装 AWS CLI，则运行：`python3 SetupAWS.py setup`

   - **选项 2：**通过 AWS IoT 控制台手动设置 thing：

     1. 将一个设备添加到 AWS IoT 控制台

        请按照以下[步骤](https://docs.aws.amazon.com/iot/latest/developerguide/create-iot-resources.html)
        创建 IoT thing、私钥和证书，从而为设备注册 AWS IoT。记下
        您的 thing 名称和 AWS IoT 端点，并下载与您的 thing 相关的证书和密钥
        。要查找您的 AWS IoT 端点：

        1. 打开 [AWS IoT 控制台](https://console.aws.amazon.com/iotv2/)。
        2. 在导航窗格中，选择 **Settings**。

        您的 AWS IoT 端点将显示为 **Endpoint**。其格式应该是：
        `*`\<account-number>`*-ats.iot.*`\<us-east-1>`*.amazonaws.com`。

     2. 在服务端完成设置后，您需要为客户端上的 AWS 
        IoT 凭据配置凭据。文件 `aws_iot_demo_profile.h` 包含
        将您的 FreeRTOS 项目连接到 AWS IoT 所需的信息，包括端点、凭据和设置为适当值的密钥
        。请按照以下步骤使用 Certificate Configurator 设置凭据
        ：

        1. 在浏览器窗口中，打开 `{FreeRTOS-root-directory}/tools/aws_config_offline/CertificateConfigurator.html`。
        2. 在 **Thing 名称**下，输入您在 AWS IoT 上注册的 Thing 名称。
        3. 在 **AWS IoT Thing 端点**下，输入您的 AWS IoT 端点。 
        4. 在 **Certificate PEM 文件**中，选择您从下列位置下载的 `*`\<ID>`*-certificate.pem.crt`：
           AWS IoT 控制台。
        5. 在 **Private Key PEM 文件**中，选择您从下列位置下载的 `*`\<ID>`*-private.pem.key`：
           AWS IoT 控制台。
        6. 选择 **Generate** 并保存 `demo_config.h`，然后将文件保存在
           `FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth/demo_config.h` 中。这会覆写
           目录中的现有文件。

#### 使用 MQTT 用户名和密码与 AWS IoT 进行客户端身份验证（附加选项）

除了基于证书和私钥的客户端身份验证之外，AWS IoT 消息代理还支持
通过 MQTT 用户名和密码进行的[自定义客户端身份验证](https://docs.aws.amazon.com/iot/latest/developerguide/custom-authentication.html)法
。客户端身份验证只需要这两种客户端身份验证方法中的一种
。如果对于您的配置来说，基于证书和私钥的客户端身份验证已经足够，
那么**您可以忽略此部分**。如果使用基于用户名和密码的身份验证，
则演示应用程序将忽略按照上述步骤配置的 Thing 证书和私钥。

请按照以下步骤在 AWS IoT 中配置自定义身份验证并配置演示。

1. 按照下列文档中的说明在 AWS IoT 中创建一个自定义授权器：
   [AWS 文档](https://docs.aws.amazon.com/iot/latest/developerguide/config-custom-auth.html)。
2. 将 `demo_config.h` 文件中的配置 `democonfigCLIENT_USERNAME` 更新为以下用户名：
   第 1 步里 AWS IoT 授权器中配置的用户名。
3. 将 `demo_config.h` 文件中的 `config democonfigCLIENT_PASSWORD` 更新为以下密码：
   第 1 步里 AWS IoT 授权器中配置的密码。
4. 仅 AWS IoT 消息代理中的移植 443 才支持自定义身份验证，
   如 [AWS 文档](https://docs.aws.amazon.com/iot/latest/developerguide/custom-auth.html)所述。将
   `demo_config.h` 文件中的配置 `democonfigMQTT_BROKER_PORT` 更新为 ( 443 )。

**注意：确保使用的最终“demo_config”文件包含设置为“1”的宏“democonfigUSE_TLS”以启用 TLS**

### 选项 2：使用本地托管的 Mosquitto MQTT 消息代理（主机）：

Mosquitto MQTT 代理可以在本地运行，并且此演示可通过相互验证身份的连接加以连接
。此代理可在您的主机（用于构建演示应用程序的计算机）
或者您本地网络的另一台计算机上运行。为此，请按照
[mqtt_broker_setup.txt](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth/mqtt_broker_setup.txt) 中列出的步骤
在本地配置 Mosquitto MQTT 消息代理，并配置与该代理配合使用的演示。

### 构建演示项目

构建此演示项目的方式与[基本 MQTT 演示（未使用 LTS）](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/01-coreMQTT-demo#source_code)相同。
演示项目使用社区免费版 [Visual Studio](https://visualstudio.microsoft.com/vs/community/)。
要构建此演示：

- 从 Visual Studio IDE 中打开 `FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth/mqtt_mutual_auth_demo.sln` Visual
  Studio 解决方案文件
- 在 IDE 的 "Build" 菜单中选择 "Build Solution"

**注意：**如果您使用的是 Microsoft Visual Studio 2017 或更早版本，则必须选择与您的版本兼容的 Platform
Toolset：Project -> RTOSDemos Properties -> Platform Toolset


### 功能

该演示提供的功能与基本 MQTT 演示相同，但添加了到 AWS IoT 的安全连接。  如需了解添加功能的详情（订阅 MQTT 主题、发布到 MQTT 主题、接收传入消息、处理传入的 MQTT 发布包、取消订阅主题），请查看[基本 MQTT 演示（未使用 TLS）。](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/01-coreMQTT-demo#functionality)

演示创建一个应用程序任务，循环一组示例演示如何连接到代理、订阅一个代理上的主题、发布到一个代理上的主题，然后断开与代理的连接。演示应用程序订阅一个主题，并向同一个主题发布。每次演示向 MQTT 代理发布消息时，代理都向演示应用程序发回相同的消息。演示的结构体如下：

```c
static void prvMQTTDemoTask( void * pvParameters )
{
    uint32_t ulPublishCount = 0U, ulTopicCount = 0U;
    const uint32_t ulMaxPublishCount = 5UL;
    NetworkContext_t xNetworkContext = { 0 };
    NetworkCredentials_t xNetworkCredentials = { 0 };
    MQTTContext_t xMQTTContext = { 0 };
    MQTTStatus_t xMQTTStatus;
    TlsTransportStatus_t xNetworkStatus;

    /* Remove compiler warnings about unused parameters. */
    ( void ) pvParameters;

    /* Set the entry time of the demo application. This entry time will be used
     * to calculate relative time elapsed in the execution of the demo
     * application, by the timer utility function that is provided to the MQTT
     * library. */
    ulGlobalEntryTimeMs = prvGetTimeMs();

    for( ; ; )
    {
        /************************** Connect. ****************************/

        /* Attempt to establish TLS session with MQTT broker. If connection
         * fails, retry after a timeout. Timeout value will be exponentially
         * increased until  the maximum number of attempts are reached or the
         * maximum timeout value is reached. The function returns a failure
         * status if the TCP connection cannot be established to the broker
         * after the configured number of attempts. */
        xNetworkStatus = prvConnectToServerWithBackoffRetries(
                                                     &xNetworkCredentials,
                                                     &xNetworkContext );
        configASSERT( xNetworkStatus == TLS_TRANSPORT_SUCCESS );
ƒ
        /* Sends an MQTT Connect packet over the already established TLS
        connection and waits for connection acknowledgment (CONNACK) packet. */

        LogInfo( ( "Creating an MQTT connection to %s.\r\n", democonfigMQTT_BROKER_ENDPOINT ) );
        prvCreateMQTTConnectionWithBroker( &xMQTTContext, &xNetworkContext );

        /************************* Subscribe. ***************************/

        /* If server rejected the subscription request, attempt to resubscribe
         * to topic. Attempts are made according to the exponential backoff
         * retry strategy implemented in retryUtils. */
        prvMQTTSubscribeWithBackoffRetries( &xMQTTContext );

        /*************** Publish and Keep Alive Loop ********************/
        /* Publish messages with QoS1, send and process Keep alive messages. */
        for( ulPublishCount = 0; ulPublishCount < ulMaxPublishCount;
            ulPublishCount++ )
        {
            LogInfo( ( "Publish to the MQTT topic %s.\r\n",
                        mqttexampleTOPIC ) );
            prvMQTTPublishToTopic( &xMQTTContext );

            /* Process incoming publish echo, since application subscribed to
             * the same topic, the broker will send publish message back to the
             * application. */
            LogInfo( ( "Attempt to receive publish message from broker.\r\n" )
            );
            xMQTTStatus = MQTT_ProcessLoop( &xMQTTContext,
            mqttexamplePROCESS_LOOP_TIMEOUT_MS );
            configASSERT( xMQTTStatus == MQTTSuccess );

            /* Leave Connection Idle for some time. */
            LogInfo( ( "Keeping Connection Idle...\r\n\r\n" ) );
            vTaskDelay( mqttexampleDELAY_BETWEEN_PUBLISHES_TICKS );
        }

        /***************** Unsubscribe from the topic. ******************/
        LogInfo( ( "Unsubscribe from the MQTT topic %s.\r\n", mqttexampleTOPIC
        ) );
        prvMQTTUnsubscribeFromTopic( &xMQTTContext );

        /* Process incoming UNSUBACK packet from the broker. */
        xMQTTStatus = MQTT_ProcessLoop( &xMQTTContext,
                                        mqttexamplePROCESS_LOOP_TIMEOUT_MS );
        configASSERT( xMQTTStatus == MQTTSuccess );

        /************************* Disconnect. **************************/

        /* Send an MQTT Disconnect packet over the already connected TLS over
         * TCP connection. There is no corresponding response for the
         * disconnect packet. After sending disconnect, client must close the
         * network connection. */
        LogInfo( ( "Disconnecting the MQTT connection with %s.\r\n",
                    democonfigMQTT_BROKER_ENDPOINT ) );
        xMQTTStatus = MQTT_Disconnect( &xMQTTContext );
        configASSERT( xMQTTStatus == MQTTSuccess );

        /* Close the network connection.  */
        TLS_FreeRTOS_Disconnect( &xNetworkContext );

        /* Reset SUBACK status for each topic filter after completion of
         * subscription request cycle. */
        for( ulTopicCount = 0; ulTopicCount < mqttexampleTOPIC_COUNT;
        ulTopicCount++ )
        {
            xTopicFilterContext[ ulTopicCount ].xSubAckStatus =
            MQTTSubAckFailure;
        }

        /* Wait for some time between two iterations to ensure that we do not
         * bombard the broker. */
        LogInfo( ( "prvMQTTDemoTask() completed an iteration successfully. "
                   "Total free heap is %u.\r\n",
                    xPortGetFreeHeapSize() ) );
        LogInfo( ( "Demo completed successfully.\r\n" ) );
        LogInfo( ( "Short delay before starting the next iteration....
                    \r\n\r\n" ) );
        vTaskDelay( mqttexampleDELAY_BETWEEN_DEMO_ITERATIONS_TICKS );
    }
}

```

### 连接到 MQTT 代理（通过相互身份验证）

函数 `prvConnectToServerWithBackoffRetries()` 试图与 MQTT 代理建立相互身份验证 TLS 连接。如果连接失败，函数会在超时后重试。超时值将呈指数增长，直到达到最大尝试次数或最大超时值。函数 `RetryUtils_BackoffAndSleep()` 提供呈指数增长的超时值，并在达到最大尝试次数时返回 `RetryUtilsRetriesExhausted`。如果在达到配置的尝试次数后仍无法将 TLS 连接到此代理，则 `prvConnectToServerWithBackoffRetries()` 返回失败状态。

```c
static TlsTransportStatus_t prvConnectToServerWithBackoffRetries(
                                NetworkCredentials_t * pxNetworkCredentials,
                                NetworkContext_t * pxNetworkContext )
{
    TlsTransportStatus_t xNetworkStatus;
    RetryUtilsStatus_t xRetryUtilsStatus = RetryUtilsSuccess;
    RetryUtilsParams_t xReconnectParams;

    #ifdef democonfigUSE_AWS_IOT_CORE_BROKER

        /* ALPN protocols must be a NULL-terminated list of strings. Therefore,
         * the first entry will contain the actual ALPN protocol string while
         * the second entry must remain NULL. */
        char * pcAlpnProtocols[] = { NULL, NULL };

        /* The ALPN string changes depending on whether username/password
        authentication is used. */
        #ifdef democonfigCLIENT_USERNAME
            pcAlpnProtocols[ 0 ] = AWS_IOT_CUSTOM_AUTH_ALPN;
        #else
            pcAlpnProtocols[ 0 ] = AWS_IOT_MQTT_ALPN;
        #endif
        pxNetworkCredentials->pAlpnProtos = pcAlpnProtocols;
    #endif /* ifdef democonfigUSE_AWS_IOT_CORE_BROKER */

    pxNetworkCredentials->disableSni = democonfigDISABLE_SNI;
    /* Set the credentials for establishing a TLS connection. */
    pxNetworkCredentials->pRootCa = ( const unsigned char * )
    democonfigROOT_CA_PEM;
    pxNetworkCredentials->rootCaSize = sizeof( democonfigROOT_CA_PEM );
    #ifdef democonfigCLIENT_CERTIFICATE_PEM
        pxNetworkCredentials->pClientCert = ( const unsigned char * )
                                    democonfigCLIENT_CERTIFICATE_PEM;
        pxNetworkCredentials->clientCertSize = sizeof(
                                    democonfigCLIENT_CERTIFICATE_PEM );
        pxNetworkCredentials->pPrivateKey = ( const unsigned char * )
        democonfigCLIENT_PRIVATE_KEY_PEM;
        pxNetworkCredentials->privateKeySize = sizeof(
        democonfigCLIENT_PRIVATE_KEY_PEM );
    #endif
    /* Initialize reconnect attempts and interval. */
    RetryUtils_ParamsReset( &xReconnectParams );
    xReconnectParams.maxRetryAttempts = MAX_RETRY_ATTEMPTS;

    /* Attempt to connect to MQTT broker. If connection fails, retry after
     * a timeout. Timeout value will exponentially increase till maximum
     * attempts are reached.*/
    do
    {
        /* Establish a TLS session with the MQTT broker. This example connects
         * to the MQTT broker as specified in democonfigMQTT_BROKER_ENDPOINT
         * and democonfigMQTT_BROKER_PORT at the top of this file. */
        LogInfo( ( "Creating a TLS connection to %s:%u.\r\n",
                   democonfigMQTT_BROKER_ENDPOINT,
                   democonfigMQTT_BROKER_PORT ) );
        /* Attempt to create a mutually authenticated TLS connection. */
        xNetworkStatus = TLS_FreeRTOS_Connect(
                                    pxNetworkContext,
                                    democonfigMQTT_BROKER_ENDPOINT,
                                    democonfigMQTT_BROKER_PORT,
                                    pxNetworkCredentials,
                                    mqttexampleTRANSPORT_SEND_RECV_TIMEOUT_MS,
                                    mqttexampleTRANSPORT_SEND_RECV_TIMEOUT_MS
                                              );

        if( xNetworkStatus != TLS_TRANSPORT_SUCCESS )
        {
            LogWarn( ( "Connection to the broker failed. Retrying connection
            with backoff and jitter." ) );
            xRetryUtilsStatus = RetryUtils_BackoffAndSleep( &xReconnectParams
            );
        }

        if( xRetryUtilsStatus == RetryUtilsRetriesExhausted )
        {
            LogError( ( "Connection to the broker failed, all attempts
            exhausted." ) );
            xNetworkStatus = TLS_TRANSPORT_CONNECT_FAILURE;
        }
    } while( ( xNetworkStatus != TLS_TRANSPORT_SUCCESS ) &&
             ( xRetryUtilsStatus == RetryUtilsSuccess ) );

    return xNetworkStatus;
}

```

函数 `prvCreateMQTTConnectionWithBroker()` 演示了如何使用清除对话与一个 MQTT 代理建立 MQTT 连接。它使用 TLS 传输接口，此接口在文件 `FreeRTOS-Plus/Source/Application-Protocols/platform/freertos/transport/src/tls_freertos.c` 中实现。`prvCreateMQTTConnectionWithBroker()` 的定义如下。请记住，我们在 `xConnectInfo` 中设置代理的存活秒数。

下面的函数显示了如何使用 `MQTT_Init()` 在 MQTT 上下文中设置 TLS 传输接口和时间函数。还显示了如何设置事件回调函数指针 `( prvEventCallback )`。此回调用于报告传入消息。

```c
static void prvCreateMQTTConnectionWithBroker(
                                    MQTTContext_t * pxMQTTContext,
                                    NetworkContext_t * pxNetworkContext )
{
    MQTTStatus_t xResult;
    MQTTConnectInfo_t xConnectInfo;
    bool xSessionPresent;
    TransportInterface_t xTransport;

    /***
     * For readability, error handling in this function is restricted to the
     * use of asserts().
     ***/

    /* Fill in Transport Interface send and receive function pointers. */
    xTransport.pNetworkContext = pxNetworkContext;
    xTransport.send = TLS_FreeRTOS_send;
    xTransport.recv = TLS_FreeRTOS_recv;

    /* Initialize MQTT library. */
    xResult = MQTT_Init( pxMQTTContext, &xTransport, prvGetTimeMs,
                         prvEventCallback, &xBuffer );
    configASSERT( xResult == MQTTSuccess );

    /* Some fields are not used in this demo so start with everything at 0. */
    ( void ) memset( ( void * ) &xConnectInfo, 0x00, sizeof( xConnectInfo ) );

    /* Start with a clean session i.e. direct the MQTT broker to discard any
     * previous session data. Also, establishing a connection with clean
     * session will ensure that the broker does not store any data when this
     * client gets disconnected. */
    xConnectInfo.cleanSession = true;

    /* The client identifier is used to uniquely identify this MQTT client to
     * the MQTT broker. In a production device the identifier can be something
     * unique, such as a device serial number. */
    xConnectInfo.pClientIdentifier = democonfigCLIENT_IDENTIFIER;
    xConnectInfo.clientIdentifierLength = ( uint16_t ) strlen(
                                                democonfigCLIENT_IDENTIFIER );

    /* Set MQTT keep-alive period. If the application does not send packets at
     * an interval less than the keep-alive period, the MQTT library will send
     * PINGREQ packets. */
    xConnectInfo.keepAliveSeconds = mqttexampleKEEP_ALIVE_TIMEOUT_SECONDS;

    /* Append metrics when connecting to the AWS IoT Core broker. */
    #ifdef democonfigUSE_AWS_IOT_CORE_BROKER
        #ifdef democonfigCLIENT_USERNAME
            xConnectInfo.pUserName = CLIENT_USERNAME_WITH_METRICS;
            xConnectInfo.userNameLength = ( uint16_t ) strlen(
                                        CLIENT_USERNAME_WITH_METRICS );
            xConnectInfo.pPassword = democonfigCLIENT_PASSWORD;
            xConnectInfo.passwordLength = ( uint16_t ) strlen(
            democonfigCLIENT_PASSWORD );
        #else
            xConnectInfo.pUserName = AWS_IOT_METRICS_STRING;
            xConnectInfo.userNameLength = AWS_IOT_METRICS_STRING_LENGTH;
            /* Password for authentication is not used. */
            xConnectInfo.pPassword = NULL;
            xConnectInfo.passwordLength = 0U;
        #endif
    #else /* ifdef democonfigUSE_AWS_IOT_CORE_BROKER */
        #ifdef democonfigCLIENT_USERNAME
            xConnectInfo.pUserName = democonfigCLIENT_USERNAME;
            xConnectInfo.userNameLength = ( uint16_t ) strlen(
                                            democonfigCLIENT_USERNAME );
            xConnectInfo.pPassword = democonfigCLIENT_PASSWORD;
            xConnectInfo.passwordLength = ( uint16_t ) strlen(
                                            democonfigCLIENT_PASSWORD );
        #endif /* ifdef democonfigCLIENT_USERNAME */
    #endif /* ifdef democonfigUSE_AWS_IOT_CORE_BROKER */

    /* Send MQTT CONNECT packet to broker. LWT is not used in this demo, so it
     * is passed as NULL. */
    xResult = MQTT_Connect( pxMQTTContext,
                            &xConnectInfo,
                            NULL,
                            mqttexampleCONNACK_RECV_TIMEOUT_MS,
                            &xSessionPresent );
    configASSERT( xResult == MQTTSuccess );

    /* Successfully established and MQTT connection with the broker. */
    LogInfo( ( "An MQTT connection is established with %s.",
                democonfigMQTT_BROKER_ENDPOINT ) );
}

```
