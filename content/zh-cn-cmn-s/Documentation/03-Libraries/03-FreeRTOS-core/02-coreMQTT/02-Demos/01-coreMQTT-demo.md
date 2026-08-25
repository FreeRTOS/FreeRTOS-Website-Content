---
title: coreMQTT 演示（无 TLS）
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
description: 关于 coreMQTT 的演示和信息（无 TLS）
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
- title: FreeRTOS 初学者指南
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
- title: 下载 FreeRTOS
  link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
- title: 常见问题
  link: /Why-FreeRTOS/FAQs
---

coreMQTT 是一个 MIT 授权的开源 MQTT C 库，适用于基于微控制器和小型微处理器的 IoT 设备。
* 本页内容：
	+ [源代码组织](#源代码组织)
	+ [配置演示项目](#配置演示项目)
	+ [构建说明](#构建演示项目)
	+ [功能](#功能)
		- [连接到 MQTT 代理](#连接到-mqtt-代理)
		- [订阅 MQTT 主题](#订阅-mqtt-主题)
		- [发布到主题](#发布到主题)
		- [接收传入消息](#接收传入消息)
		- [处理传入的 MQTT 发布数据包](#处理传入的-mqtt-发布数据包)
		- [取消订阅主题](#取消订阅主题)

  
**注意：我们建议在任何物联网（ IoT ）应用程序中使用相互身份验证。此页面上的
演示在引入加密和身份验证
之前演示了 MQTT 通信，仅用于教育目的。不适用于生产。** 


## 单线程 VS 多线程

coreMQTT 有两种使用模式，*单线程*和*多线程*（多任务）。在多线程应用程序中 
仅在一个线程上使用 MQTT 库（如本页记录的演示那样） 
等同于单线程用例。单线程用例要求应用程序写入器 
对 MQTT 库进行重复的显式调用。多线程用例可以 
在后台的[代理（或守护进程）任务中执行 MQTT 协议](mqtt-agent-demo)。在代理任务中执行 MQTT 协议 
使应用程序写入器无需显式托管任何 MQTT 状态或调用 `MQTT_ProcessLoop()` 
API 函数。使用代理任务还能让多个应用程序任务共享单个 MQTT 连接， 
而无需使用互斥锁等同步原语。
  

## 演示简介

共有三个示例项目介绍 [“TLS 简介”](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/02-TLS-introduction)页面上描述的概念， 
此示例项目是其中之一。第一个示例 （本页）演示了未加密的 MQTT 通信。 
[第二个示例](server-authentication-mqtt-example)在第一个示例的基础上引入服务器身份验证 
（其中 IoT 客户端对其连接的 MQTT 服务器进行验证）。 
[第三个示例](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication)在第二个示例的基础上引入了强力相互身份验证 
（其中 IoT 客户端也对其连接的 MQTT 服务器进行验证）。

该系列中的第一个项目仅演示了基本 MQTT 用例，即如何连接到 MQTT 代理 
和 MQTT 在 [QoS 0](mqtt_terminology) 等级的订阅-发布工作流程。在其订阅了一个单一的主题过滤器后， 
它会向该主题发布消息，然后等待从服务器上接收同一消息。这种向代理发布消息， 
然后又从代理那里接收同一消息的循环会无限重复。由于它使用 QoS 0， 
它没有实现发布消息的任何重传机制。

此演示**未**创建安全连接，因此不适合在生产中使用， 
请勿在未加密的网络连接上发送任何机密信息。此演示的确演示了如何 
在连接失败的情况下，使用指数退避时间（包括定时抖动）进行连接。指数级增加连接尝试之间的时间间隔， 
并加入一些随机的时间抖动，对于大规模 IoT 设备机群而言是最佳实践， 
因为它可以防止所有 IoT 设备在同时断开连接时尝试同时重新连接。

此基础 MQTT 演示项目使用 
[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)， 
因此，它可以在 Windows 上使用 [Visual Studio 免费社区版](https://visualstudio.microsoft.com/vs/community/)进行构建和评估， 
而无需任何特定 MCU 硬件。 


## 源代码组织

演示项目名为 mqtt_plain_text_demo.sln，可在 
FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Plain_Text 目录中找到，  详见[主 FreeRTOS 下载内容](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)， 
（也可在下载页面链接的 Github 中找到）。


## 配置演示项目

此演示使用 [FreeRTOS-Plus-TCP TCP/IP 堆栈](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/index)，因此请按照 
为 [TCP/IP 入门项目](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)提供的说明进行操作， 
以确保您：

1. [安装了必备组件](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites) 
   （例如 WinPCap）。
2. [设置了静态或动态 IP 地址、网关地址和网络掩码](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic)（可选）。
3. [设置了 MAC 地址](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr)（可选）。
4. 在您的主机上[选择了以太网接口](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface) 
   。
5. ......**重要的是**，在尝试运行 MQTT 演示之前，[请先测试网络连接](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#connectivity-test) 
   。

每个演示项目都有自己的配置设置。当你按照网络配置说明进行操作时，
确保应用 MQTT 演示项目中的设置，而不是
TCP/IP 入门项目中的设置。默认情况下，TCP/IP 堆栈被配置为使用动态 IP 地址。


## 配置 MQTT 代理连接

### 备选方案 1：使用公共托管的 Mosquitto MQTT 代理（web 托管）

该演示项目可在 "test.mosquitto.org" 中与 Mosquitto 的公共托管消息代理进行通信。如果 
演示连接到具有 DHCP 服务和互联网接入的网络，则此操作应有效。请注意，FreeRTOSWindows 
端口仅适用于有线以太网网络适配器，该适配器可以是虚拟以太网适配器。您应使用 
单独的 MQTT 客户端，如 [MQTT.fx](https://mqttfx.jensd.de/)，测试从主机到公共 MQTT 代理的 
MQTT 连接。要使用托管的 Mosquitto 服务器：

1. 打开 `/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Plain_Text/demo_config.h` 的本地副本
2. 增加以下行：
   * #define democonfigMQTT_BROKER_ENDPOINT "test.mosquitto.org"
   * #define democonfigMQTT_BROKER_PORT ( 1883 )

**注意**：Mosquitto 是一个开源 MQTT 消息代理，支持 MQTT 5.0、3.1.1 和 3.1 版本。  
它是 Eclipse 基金会的一部分，是一个 [Eclipse IoT](https://iot.eclipse.org/) 项目。test.mosquitto.org 
MQTT 代理不隶属于 FreeRTOS，也不由其维护， 
可能随时无法使用。


### 备选方案 2：使用本地托管的 Mosquitto MQTT 消息代理（主机）

Mosquitto 代理也可以在本地运行，无论是在您的主机上（用于构建演示应用程序的机器），还是在 
您本地网络的另一台计算机上。请按以下步骤操作：

1. 请按照 https://mosquitto.org/download/上的说明在本地下载和安装 Mosquitto。
2. 打开位于 Mosquitto 安装目录下的 "mosquitto.conf"，将 “bind_address” 
   设置为 Mosquitto 将在您的系统上监听连接的网络。
3. 找到您主机的 IP 地址（在 Windows 上运行 `ipconfig` 命令，或在 Linux 或 MAC OS 上运行 `ifconfig` 命令）。请注意， 
   FreeRTOS Windows 移植仅适用于有线以太网适配器（可以是虚拟以太网适配器）。
   * **NOTE:** 从 Mosquitto 版本 2.0.0 开始，当 Mosquitto 代理在没有配置任何 [`listener`](https://mosquitto.org/man/mosquitto-conf-5.html) 的情况下运行时，它现在将绑定到环回接口 ` 127.0.0.1` 和/或 `::1`，将入站连接限制为仅来自本地主机。此外，所有侦听器现在默认为 [`allow_anonymous`](https://mosquitto.org/man/mosquitto-conf-5.html) false, 防止客户端在不提供用户名的情况下进行连接。因此，需要在`mosquitto.conf`配置文件中显式指定`listener`和`allow_anonymous`:
        ``` sh
        listener 1883
        allow_anonymous true
        ```
    * 要使用自定义配置文件启动 Mosquitto，请使用: `mosquitto -v -c <path/to/config/file>`
4. 打开 `FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Plain_Text/demo_config.h`。
5. 添加以下行，将 democonfigMQTT_BROKER_ENDPOINT 设置为运行 Mosquitto 的机器的 IP 地址， 
   该 IP 地址必须与演示所连接的网络位于同一子网：
   * `#define democonfigMQTT_BROKER_ENDPOINT "w.x.y.z"`
   * `#define democonfigMQTT_BROKER_PORT ( 1883 )`

您应使用单独的 MQTT 客户端，如 [MQTT.fx](https://mqttfx.jensd.de/)， 
测试从主机到安装的 MQTT 代理的 MQTT 连接。

**注意：**端口号 1883 是未加密 MQTT 的默认端口号。如果您无法使用该端口 
（例如，如果它被您的 IT 安全策略阻止），请把 Mosquitto 使用的端口更改为更高的端口号 
（例如，50000 到 55000 范围内的端口号），并相应地设置 `mqttexampleMQTT_BROKER_PORT`。


### 备选方案 3：您选择的任何其他未加密 MQTT 代理：

支持未加密 TCP/IP 通信的任何 MQTT 代理也可与此演示一起使用。请按以下步骤操作：

1. 打开 `/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Plain_Text/demo_config.h` 的本地副本
2. 添加下列行，并设置您所选择的代理：
   * #define democonfigMQTT_BROKER_ENDPOINT "your-desired-endpoint"
   * #define democonfigMQTT_BROKER_PORT ( 1883 )


## 构建演示项目

此演示项目使用的是   [Visual Studio 免费社区版](https://visualstudio.microsoft.com/vs/community/)。

要构建演示，请执行如下操作：
1. 从 Visual Studio IDE 中打开 `/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Plain_Text/mqt_plain_text_demo.sln` Visual Studio 
   Visual Studio 解决方案文件
2. 在 IDE 的 ‘build’ 菜单中选择 ‘build solution’


## 功能

该演示创建了一个单个应用程序任务，该任务通过一系列示例循环，演示如何连接到 
代理、订阅代理上的主题、在代理上发布主题以及再次断开与代理的连接。演示应用程序 
同时订阅和发布同一主题，因此演示程序每次向 MQTT 代理发布消息时， 
代理都会将同一消息发回给演示应用程序。演示的结构体如下：

```c
static void prvMQTTDemoTask( void * pvParameters )  
{  

    uint32_t ulPublishCount = 0U, ulTopicCount = 0U;  
    const uint32_t ulMaxPublishCount = 5UL;  
    NetworkContext_t xNetworkContext = { 0 };  
    MQTTContext_t xMQTTContext;  
    MQTTStatus_t xMQTTStatus;  
    PlaintextTransportStatus_t xNetworkStatus;  

    /***  
    * For readability, error handling in this function is restricted to  
    * the use of asserts().  
    ***/  

    for( ; ; )  
    {  
        /*************************** Connect. *********************************/  

        /* Attempt to connect to the MQTT broker. The socket is returned in  
         * the network context structure. */  
        xNetworkStatus = prvConnectToServerWithBackoffRetries( &xNetworkContext );  
        configASSERT( xNetworkStatus == PLAINTEXT_TRANSPORT_SUCCESS );  

        /* Connect to the MQTT broker using the already connected TCP socket. */  
        prvCreateMQTTConnectionWithBroker( &xMQTTContext, &xNetworkContext );  

        /**************************** Subscribe. ******************************/  

        /* Subscribe to the test topic. */  
        prvMQTTSubscribeWithBackoffRetries( &xMQTTContext );  

        /******************* Publish and Keep Alive Loop. *********************/  

        /* Publish messages with QoS0, then send and process Keep Alive  
         * messages. */  
        for( ulPublishCount = 0; ulPublishCount < ulMaxPublishCount; ulPublishCount++ )  
        {  
            prvMQTTPublishToTopic( &xMQTTContext );  

            /* Process the incoming publish echo. Since the application subscribed  
             * to the same topic, the broker will send the same publish message  
             * back to the application. Note there is a separate demo that  
             * shows how to use coreMQTT in a thread safe way - in which case the  
             * MQTT protocol runs in the background and this call is not  
             * required. */  
            xMQTTStatus = MQTT_ProcessLoop( &xMQTTContext, mqttexamplePROCESS_LOOP_TIMEOUT_MS );  
            configASSERT( xMQTTStatus == MQTTSuccess );  

            /* Leave the connection idle for some time. */  
            vTaskDelay( mqttexampleDELAY_BETWEEN_PUBLISHES );  
        }  

        /******************** Unsubscribe from the topic. *********************/  

        prvMQTTUnsubscribeFromTopic( &xMQTTContext );  

        /* Process the incoming packet from the broker. Note there is a separate  
         * demo that shows how to use coreMQTT in a thread safe way - in which case  
         * the MQTT protocol runs in the background and this call is not required. */  
        xMQTTStatus = MQTT_ProcessLoop( &xMQTTContext, mqttexamplePROCESS_LOOP_TIMEOUT_MS );  
        configASSERT( xMQTTStatus == MQTTSuccess );  

        /**************************** Disconnect. *****************************/  

        xMQTTStatus = MQTT_Disconnect( &xMQTTContext );  
        
        /* Close the network connection. */  
        xNetworkStatus = Plaintext_FreeRTOS_Disconnect( &xNetworkContext );  
        configASSERT( xNetworkStatus == PLAINTEXT_TRANSPORT_SUCCESS );  

        /* Wait for some time between two iterations to ensure that we do not  
         * bombard the MQTT broker. */  
        vTaskDelay( mqttexampleDELAY_BETWEEN_DEMO_ITERATIONS );  
    }  
}  
```

### 连接到 MQTT 代理

在上述函数中，`prvConnectToServerWithBackoffRetries()` 试图与 MQTT 代理建立 TCP 连接。 
如果连接失败，则在超时后重试。超时值将会呈指数级增长， 
也包括一些随机抖动，直到达到最大尝试次数或最大超时值。生产设备中 
使用这种类型的退避，可确保同时断开连接的 IoT 设备群不会同时尝试重新连接， 
以免服务器不堪重负。如果连接成功， 
则在 xNetworkContext 中返回连接的 TCP 套接字。

函数 `prvCreateMQTTConnectionWithBroker()` 演示了如何 
通过[清除会话](mqtt_terminology)与 MQTT 代理建立未加密连接。它使用 FreeRTOS-Plus-TCP [传输接口](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface)， 
该接口在文件 `FreeRTOS-Plus/Source/Application-Protocols/platform/freertos/transport/src/plaintext_freertos.c` 中实现。 
`prvCreateMQTTConnectionWithBroker()` 的定义如下。代理的存活秒数在 
`xConnectInfo` 中设置。 

以下函数显示了如何使用 MQTT_Init() 在 MQTT 上下文中设置 FreeRTOS-Plus-TCP 传输接口和时间函数， 
还显示了如何设置事件回调函数指针 (`prvEventCallback`)。此回调用于报告传入 
消息。 

```c
static void prvCreateMQTTConnectionWithBroker( MQTTContext_t * pxMQTTContext, NetworkContext_t * pxNetworkContext )  
{  
    MQTTStatus_t xResult;  
    MQTTConnectInfo_t xConnectInfo;  
    bool xSessionPresent;  
    TransportInterface_t xTransport;  

    /***  
     * For readability, error handling in this function is restricted to  
     * the use of asserts().  
     ***/  

    /* Fill in [Transport Interface](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface) send and receive function pointers. */  
    xTransport.pNetworkContext = pxNetworkContext;  
    xTransport.send = Plaintext_FreeRTOS_send;  
    xTransport.recv = Plaintext_FreeRTOS_recv;  

    /* Initialize MQTT library. */  
    xResult = MQTT_Init( 
        pxMQTTContext,   
        &xTransport,   
        prvGetTimeMs,  
        prvEventCallback,   
        &xBuffer );  
    configASSERT( xResult == MQTTSuccess );  

    /* Many fields not used in this demo so start with everything at 0. */  
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
    xConnectInfo.clientIdentifierLength = ( uint16_t ) strlen( democonfigCLIENT_IDENTIFIER );  

    /* Set MQTT keep-alive period. It is the responsibility of the application  
    * to ensure that the interval between Control Packets being sent does not  
    * exceed the Keep Alive value. In the absence of sending any other  
    * Control Packets, the Client MUST send a PINGREQ Packet. */  
    xConnectInfo.keepAliveSeconds = mqttexampleKEEP_ALIVE_TIMEOUT_SECONDS;  

    /* Send MQTT CONNECT packet to broker. LWT is not used in this demo, so it  
    * is passed as NULL. */  
    xResult = MQTT_Connect( 
        pxMQTTContext,  
        &xConnectInfo,  
        NULL,  
        mqttexampleCONNACK_RECV_TIMEOUT_MS,  
        &xSessionPresent );  
    configASSERT( xResult == MQTTSuccess );  
}  

```

### 订阅 MQTT 主题

函数 `prvMQTTSubscribeWithBackoffRetries()` 演示了如何在 MQTT 代理上订阅主题过滤器。 
该示例演示了如何订阅一个主题过滤器，但也可以在同一个订阅 API 调用中传递一个主题过滤器列表， 
以订阅一个以上的主题过滤器。此外，如果 MQTT 代理拒绝订阅请求，
则订阅将重试 MAX_RETRY_ATTEMPTS。该函数的定义如下：

```c
static const char *const pcExampleTopic = "/example/topic";  

static void prvMQTTSubscribeWithBackoffRetries( MQTTContext_t * pxMQTTContext )  
{  
    MQTTStatus_t xResult = MQTTSuccess;  
    RetryUtilsStatus_t xRetryUtilsStatus = RetryUtilsSuccess;  
    RetryUtilsParams_t xRetryParams;  
    MQTTSubscribeInfo_t xMQTTSubscription[ mqttexampleTOPIC_COUNT ];  
    bool xFailedSubscribeToTopic = false;      

    /***  
     * For readability, error handling in this function is restricted to  
     * the use of asserts().  
     ***/  

    /* Some fields not used by this demo so start with everything at 0. */  
    ( void ) memset( ( void * ) &xMQTTSubscription, 0x00, sizeof( xMQTTSubscription ) );  

    /* Each packet requires a unique ID. */  
    usSubscribePacketIdentifier = MQTT_GetPacketId( pxMQTTContext );  

    /* Subscribe to the pcExampleTopic topic filter. This example subscribes  
     * to only one topic and uses QoS0. */  
    xMQTTSubscription[ 0 ].qos = MQTTQoS0;  
    xMQTTSubscription[ 0 ].pTopicFilter = pcExampleTopic;  
    xMQTTSubscription[ 0 ].topicFilterLength = strlen( pcExampleTopic );  

    /* Initialize retry attempts and interval. */  
    RetryUtils_ParamsReset( &xRetryParams );  
    xRetryParams.maxRetryAttempts = MAX_RETRY_ATTEMPTS;  

    do  
    {  

        /* The client is already connected to the broker. Subscribe to the topic  
         * as specified in pcExampleTopic by sending a subscribe packet then  
         * waiting for a subscribe acknowledgment (SUBACK). */  
        xResult = MQTT_Subscribe( 
            pxMQTTContext,  
            xMQTTSubscription,  
            1, /* Only subscribing to one topic. */  
            usSubscribePacketIdentifier );  
        configASSERT( xResult == MQTTSuccess );  

        /* Process incoming packet from the broker. After sending the  
         * subscribe, the client may receive a publish before it receives a  
         * subscribe ack. Therefore, call generic incoming packet processing  
         * function. Since this demo is subscribing to the topic to which no  
         * one is publishing, probability of receiving Publish message before  
         * subscribe ack is zero; but application must be ready to receive any  
         * packet. This demo uses the generic packet processing function  
         * everywhere to highlight this fact. Note there is a separate demo that  
         * shows how to use coreMQTT in a thread safe way – in which case the  
         * MQTT protocol runs in the background and this call is not required. */  
        xResult = MQTT_ProcessLoop( pxMQTTContext, mqttexamplePROCESS_LOOP_TIMEOUT_MS );  
        configASSERT( xResult == MQTTSuccess );  

        /* Reset flag before checking suback responses. */  
        xFailedSubscribeToTopic = false;  

        /* Check if recent subscription request has been rejected.  
         * #xTopicFilterContext is updated in the event callback (shown in a  
         * code block below) to reflect the status of the SUBACK sent by the  
         * broker. It represents either the QoS level granted by the server upon  
         * subscription, or acknowledgment of server rejection of the  
         * subscription request. */  
        if( xTopicFilterContext.xSubAckStatus == MQTTSubAckFailure )  
        {  
            xFailedSubscribeToTopic = true;  
            xRetryUtilsStatus = RetryUtils_BackoffAndSleep( &xRetryParams );  
            break;  
        }  
        configASSERT( xRetryUtilsStatus != RetryUtilsRetriesExhausted );  
    } 
    while( ( xFailedSubscribeToTopic == true ) &&  ( xRetryUtilsStatus == RetryUtilsSuccess ) );  
}  
```

### 发布到主题

函数 `prvMQTTPublishToTopic()` 演示了如何在 MQTT 代理上发布主题过滤器。该 
函数的定义如下：

```c
static const char *const pcExampleTopic = "/example/topic";  

static void prvMQTTPublishToTopic( MQTTContext_t * pxMQTTContext )  
{  
    MQTTStatus_t xResult;  
    MQTTPublishInfo_t xMQTTPublishInfo;  

    /***  
     * For readability, error handling in this function is restricted to the   
     * use of asserts().   
     ***/  

    /* Some fields are not used by this demo so start with everything at 0. */  
    ( void ) memset( ( void * ) &xMQTTPublishInfo, 0x00, sizeof( xMQTTPublishInfo ) );  

    /* This demo uses QoS0. */  
    xMQTTPublishInfo.qos = MQTTQoS0;  
    xMQTTPublishInfo.retain = false;  
    xMQTTPublishInfo.pTopicName = pcExampleTopic;  
    xMQTTPublishInfo.topicNameLength = ( uint16_t ) strlen( pcExampleTopic );  
    xMQTTPublishInfo.pPayload = mqttexampleMESSAGE;  
    xMQTTPublishInfo.payloadLength = strlen( mqttexampleMESSAGE );  

    /* Send PUBLISH packet. Packet ID is not used for a QoS0 publish. */  
    xResult = MQTT_Publish( 
        pxMQTTContext, 
        &xMQTTPublishInfo, 
        0U );  
    configASSERT( xResult == MQTTSuccess );  

}  
```

### 接收传入消息

如前所述，应用程序在连接到代理之前注册事件回调函数。函数  
`prvMQTTDemoTask()` 通过调用 `MQTT_ProcessLoop()` 来接收传入消息。当接收到传入的 MQTT 消息时， 
它会调用应用程序注册的事件回调函数。函数 `prvEventCallback()` 
是这种事件回调函数的示例；它检查传入的数据包类型并调用合适的处理程序。在下面的示例中， 
该函数要么调用 `prvMQTTProcessIncomingPublish()` 来处理传入的发布信息， 
要么调用 `prvMQTTProcessResponse()` 来处理确认。请注意，有一个单独的演示展示了如何以线程安全的方式使用 coreMQTT 
——在这种情况下，MQTT 协议在后台运行，无需调用 MQTT_ProcessLoop()。

```c
static void prvEventCallback( MQTTContext_t * pxMQTTContext, MQTTPacketInfo_t * pxPacketInfo, MQTTDeserializedInfo_t * pxDeserializedInfo )  
{  
    /* The MQTT context is not used for this demo. */  
    ( void ) pxMQTTContext;  

    if( ( pxPacketInfo->type & 0xF0U ) == MQTT_PACKET_TYPE_PUBLISH )  
    {  
        prvMQTTProcessIncomingPublish( pxDeserializedInfo->pPublishInfo );  
    }  
    else  
    {  
        prvMQTTProcessResponse( pxPacketInfo, pxDeserializedInfo->packetIdentifier );  
    }  
}  
```

### 处理传入的 MQTT 发布数据包

函数 `prvMQTTProcessIncomingPublish()` 演示了如何处理来自 MQTT 代理的传入 PUBLISH 数据包。 
`prvMQTTProcessResonse()` 演示了如何处理确认数据包。这些函数 
的定义如下：


```c
static const char *const pcExampleTopic = "/example/topic";  

static void prvMQTTProcessIncomingPublish( MQTTPublishInfo_t * pxPublishInfo )  
{  
    /* Verify the received publish is for the we have subscribed to. */  
    if( ( pxPublishInfo->topicNameLength == strlen( pcExampleTopic ) ) &&  
        ( 0 == strcmp( pcExampleTopic, pxPublishInfo->pTopicName ) ) )  
    {  
        LogInfo( ( "Incoming Publish Topic Name: %.*s matches subscribed topic.&bsol;r&bsol;n"  
                   "Incoming Publish Message : %.*s",  
                   pxPublishInfo->topicNameLength,  
                   pxPublishInfo->pTopicName,  
                   pxPublishInfo->payloadLength,  
                   pxPublishInfo->pPayload ) );  
    }  

    else  
    {  
        LogInfo( ( "Incoming Publish Topic Name: %.*s does not match subscribed topic.",  
                   pxPublishInfo->topicNameLength,  
                   pxPublishInfo->pTopicName ) );  
    }  
}  

static void prvMQTTProcessResponse( MQTTPacketInfo_t * pxIncomingPacket, uint16_t usPacketId )  
{  
    MQTTStatus_t xResult = MQTTSuccess;  
    uint8_t * pucPayload = NULL;  
    size_t ulSize = 0;  

    switch( pxIncomingPacket->type )  
    {  
        case MQTT_PACKET_TYPE_SUBACK:  
            /* A SUBACK from the broker, containing the server response to our  
             * subscription request, has been received. It contains the status  
             * code indicating server approval/rejection for the subscription to  
             * the single topic requested. The SUBACK will be parsed to obtain  
             * the status code, and this status code will be stored in  
             * #xTopicFilterContext. */  
            xResult = MQTT_GetSubAckStatusCodes( pxIncomingPacket, &pucPayload, &ulSize );  

            /* MQTT_GetSubAckStatusCodes always returns success if called with  
             * packet info from the event callback and non-NULL parameters. */  
            configASSERT( xResult == MQTTSuccess );  

            /* This should be the QOS leve, 0 in this case. */  
            xTopicFilterContext.xSubAckStatus = *pucPayload;  

            /* Make sure ACK packet identifier matches with Request packet  
             * identifier. */  
            configASSERT( usSubscribePacketIdentifier == usPacketId );  
            break;  

        case MQTT_PACKET_TYPE_UNSUBACK:  
            LogInfo( ( "Unsubscribed from the topic %s.", mqttexampleTOPIC ) );  

            /* Make sure ACK packet identifier matches with Request packet  
             * identifier. */  
            configASSERT( usUnsubscribePacketIdentifier == usPacketId );  
            break;  

        case MQTT_PACKET_TYPE_PINGRESP:  

            /* Nothing to be done from application as library handles  
             * PINGRESP with the use of MQTT_ProcessLoop API function. */  
            LogWarn( ( "PINGRESP should not be handled by the application "  
                "callback when using MQTT_ProcessLoop.&bsol;n" ) );  
            break;  

        /* Any other packet type is invalid. */  
        default:  
            LogWarn( ( "prvMQTTProcessResponse() called with unknown packet type:(%02X).", pxIncomingPacket->type ) );  
    }  
}  
```

### 取消订阅主题

工作流中的最后一步是取消订阅主题，这样代理就不会再 
从 `pcExampleTopic` 发送任何发布信息。该函数的定义如下：

```c
static const char *const pcExampleTopic = "/example/topic";  

static void prvMQTTUnsubscribeFromTopic( MQTTContext_t * pxMQTTContext )  
{  
    MQTTStatus_t xResult;  
    MQTTSubscribeInfo_t xMQTTSubscription[ mqttexampleTOPIC_COUNT ];  

    /* Some fields not used by this demo so start with everything at 0. */  
    ( void ) memset( ( void * ) &xMQTTSubscription, 0x00, sizeof( xMQTTSubscription ) );  

    /* Subscribe to the pcExampleTopic topic filter. This example subscribes   
    * to only one topic and uses QoS0. */  
    xMQTTSubscription[ 0 ].qos = MQTTQoS0;  
    xMQTTSubscription[ 0 ].pTopicFilter = pcExampleTopic;  
    xMQTTSubscription[ 0 ].topicFilterLength = ( uint16_t ) strlen( pcExampleTopic);  

    /* Each packet requires a unique ID. */  
    usUnsubscribePacketIdentifier = MQTT_GetPacketId( pxMQTTContext );  

    /* Send UNSUBSCRIBE packet. */  
    xResult = MQTT_Unsubscribe( 
        pxMQTTContext,  
        xMQTTSubscription,  
        sizeof( xMQTTSubscription ) / sizeof( MQTTSubscribeInfo_t ),  
        usUnsubscribePacketIdentifier );  
    configASSERT( xResult == MQTTSuccess );  
}  
```

