---
title: coreMQTT 存活演示
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

**注意：我们建议在构建任何物联网 (IoT) 应用程序时始终使用相互身份验证。
此页面上的演示在
引入加密和身份验证之前演示了 MQTT 通信，仅用于教育目的，不适用于生产。** 


## 简介

存活 MQTT 演示项目使用 
[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)， 
因此可以使用 
[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/)  
在 Windows 上进行构建和评估，无需任何特定 MCU 硬件。本项目提供了 
发送存活数据包的替代方法，以便在给定的存活间隔内未发送控制数据包的情况下， 
保持与 MQTT 代理的连接。

存活 MQTT 演示展示了如何建立一个与 MQTT 代理的明文 TCP 连接， 
如果连接失败，则采用指数退避逻辑。在建立 TCP 连接后，客户端也会发送一个 MQTT 连接数据包， 
其中包括关于所述代理存活间隔的信息。如果代理在 
此给定间隔的 1.5 倍时间内未收到控制数据包，代理将关闭连接。为了避免 
这个问题，自动重载软件定时器用于在间隔到期之前向代理发送 ping 请求。 
每当执行定时器以发送 ping 请求时，另一个定时器会被启动， 
等待来自代理的 ping 响应。接下来，客户端会订阅单个主题过滤器，然后等待足够长的时间来执行定时器。
之后，客户端以 [QoS 1](mqtt_terminology) 级别发布到该主题，并反复调用 
'`MQTT_ReceiveLoop`' 以接收来自代理的发布确认。'`MQTT_ReceiveLoop`' 
的超时为 0 时，只能运行一次迭代，每次迭代之间的任务会有延迟。请注意， 
如果在两次迭代中未收到发布确认，则将执行 ping 请求定时器。
整个周期无限期地重复。请记住，使用 '`MQTT_ProcessLoop`' 
代替 '`MQTT_ReceiveLoop`' 也可实现相同效果。不过，'`MQTT_ProcessLoop`' 需要一个定时器查询函数， 
返回当前时间（单位：毫秒）。

下面提供的说明将演示 
如何连接到托管在互联网上的 [Mosquitto 测试代理](https://test.mosquitto.org/) 
或在主机上本地运行的服务器。

本演示**仅**作为学习练习使用。本演示**未**创建
安全连接，但可以轻松修改以使用 TLS 连接。不过，所有 MQTT 信息 
都以明文形式发送，没有加密。**请勿**从您的 IoT 
设备向 MQTT 代理发送任何机密信息。MQTT 代理由不隶属于 
FreeRTOS 的第三方公开托管。此 MQTT 代理可能随时不可用，且不由 FreeRTOS 维护。 
生产 IoT 设备应使用相互身份验证和加密的网络连接， 
如 [MQTT TLS 演示](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication)中演示的那样。

**注意**：Mosquitto 是一个开源 MQTT 消息代理。更多详细信息请点击[此处](https://iot.eclipse.org/)。


## 源代码组织

用于存活 MQTT 演示的 Visual Studio 解决方案称为 
[`mqtt_keep_alive_demo.sln`](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Keep_Alive/mqtt_keep_alive_demo.sln)， 
可在 
[FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Keep_Alive](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Keep_Alive) 
目录中找到（位于[主 FreeRTOS](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) 下载包中）。

![](/media/2020/coreMQTT-keep-alive-2-217x300.png)


## 构建演示项目

演示项目使用[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/)。 
要构建演示，请执行如下操作：

1. 从 Visual Studio IDE 中打开 '`mqtt_keep_alive_demo.sln`' Visual Studio 解决方案文件。
2. 在 IDE 的 '**Build**' 菜单中选择 '**Build Solution**'。

**注意**：如果您使用的是 Microsoft Visual Studio 2017 或更早版本， 
则必须选择与您的版本兼容的 “平台工具集”：'`Project -> RTOSDemos Properties -> Platform Toolset`'。


## 配置演示项目

此演示使用 [FreeRTOS-Plus-TCP TCP/IP 堆栈](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/index)，因此请按照
为 [TCP/IP 入门项目](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)提供的说明进行操作， 
以确保您：

1. [安装了必备组件](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites)（例如 WinPCap）。

2. [设置了静态或动态 IP 地址、网关地址和网络掩码](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic)（可选）。

3. [设置了 MAC 地址](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr)（可选）。

4. 在您的主机上[选择以太网接口](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface) 
   。

5. ......**重要的是**，在尝试运行 MQTT 演示之前，[请先测试网络连接](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#connectivity-test) 
   。

所有这些设置都应在 MQTT LTS rc1 演示项目中更改，而不是在上面链接的页面中所提及的 TCP/IP Starter 项目中 
更改！交付时， TCP/IP 堆栈被配置为使用动态 IP  
地址。


## 配置 MQTT 代理连接

### 备选方案 1：使用公开托管的 Mosquitto MQTT 代理（web 托管）：

该演示项目预先配置为在 "test.mosquitto.org" 中与 Mosquitto 的公开托管消息代理进行通信 
。如果演示连接到具有 DHCP 服务和互联网接入的网络，则此操作应有效 
。请注意，FreeRTOS Windows 移植仅适用于有线以太网适配器 
（可以是虚拟以太网适配器）。

应使用单独的 MQTT 客户端（如 [MQTT.fx](https://mqttfx.jensd.de/)）测试 
从您的主机到公共 MQTT 代理的 MQTT 连接。


### 备选方案 2：使用本地托管的 Mosquitto MQTT 消息代理（主机）：

Mosquitto 代理也可以在本地运行，无论是在您的主机上（用于构建演示应用程序的机器），还是在 
您本地网络的另一台计算机上。请按以下步骤操作：

1. [下载 Mosquitto](https://mosquitto.org/download/)

2. 通过运行安装程序将 Mosquitto 安装为一个 Windows 服务。

3. 启动 Mosquitto 服务。有关将 Mosquitto 作为 Windows 服务运行的更多详细信息，请参阅其 
   [自述文件窗口](https://github.com/eclipse-mosquitto/mosquitto/blob/master/README-windows.txt) 
   和[自述文件](https://github.com/eclipse-mosquitto/mosquitto/blob/master/README.md)。

   * **NOTE:** 从 Mosquitto 版本 2.0.0 开始，当 Mosquitto 代理在没有配置任何 [`listener`](https://mosquitto.org/man/mosquitto-conf-5.html) 的情况下运行时，它现在将绑定到环回接口 ` 127.0.0.1` 和/或 `::1`，将入站连接限制为仅来自本地主机。此外，所有侦听器现在默认为 [`allow_anonymous`](https://mosquitto.org/man/mosquitto-conf-5.html) false, 防止客户端在不提供用户名的情况下进行连接。因此，需要在`mosquitto.conf`配置文件中显式指定`listener`和`allow_anonymous`:
        ``` sh
        listener 1883
        allow_anonymous true
        ```
    * 要使用自定义配置文件启动 Mosquitto，请使用: `mosquitto -v -c <path/to/config/file>`

4. 通过以下步骤验证 Mosquitto 服务器是否在本地运行并在端口 1883 上侦听：

    1. 打开 PowerShell。

    2. 键入命令
    
       ```c
       netstat -a -p TCP | findstr 1883
       ```

       已检查在端口 1883 上是否有侦听的活动连接。

    3. 验证命令是否输出如下内容：
    
       ```c
       TCP    0.0.0.0:1883           :0       LISTENING
       ```

    4. 如果没有前述步骤所述输出，请参阅上文列出的 Mosquitto 文档，
    检查您的设置是否正确。

5. 确保允许 Mosquitto 代理通过 Windows 防火墙进行通信。请按照 
   [](https://support.microsoft.com/help/4558235/windows-10-allow-an-app-through-microsoft-defender-firewall)Microsoft 的 
   指示，允许应用程序通过 Windows 10 Defender 防火墙进行通信。在 
   运行此 MQTT 示例后，最好通过 Windows 防火墙禁用 Mosquitto 代理通信， 
   以避免不必要的网络流量进入您的机器。

6. 验证 Mosquitto 代理运行成功后，更新配置 `democonfigMQTT_BROKER_ENDPOINT` 
   到 Windows 主机本地 IP 地址。请注意，"localhost" 或地址 "127.0.0.1" 将不起作用， 
   因为此示例在 Windows 模拟器上运行，而不是在 Windows 主机上运行。 
   另请注意，如果 Windows 主机使用虚拟专用网络 (VPN)， 
   与 Mosquitto 代理的连接可能无法正常工作。

应使用单独的 MQTT 客户端（如 [MQTT.fx](https://mqttfx.jensd.de/)）测试 
从您的主机到本地 MQTT 代理的 MQTT 连接。

**注意：**端口号 1883 是未加密 MQTT 的默认端口号。如果您无法使用那个 
端口（例如，如果它被您的 IT 安全策略阻止），请把 Mosquitto 使用的端口更改为更高的端口号 
请把 Mosquitto 使用的端口更改为更高的端口号（例如，50000 到 55000 范围内的端口号），并相应地设置 `democonfigMQTT_BROKER_PORT` 
。Mosquitto 使用的端口号是由位于 Mosquitto 安装目录下的 '`mosquitto.conf`' 中的 '`port`' 参数 
设置的。


### 备选方案 3：您选择的任何其他未加密 MQTT 代理：

支持未加密 TCP/IP 通信的任何 MQTT 代理也可与此演示一起使用。请按以下步骤 
操作：

1. 打开 [/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Keep_Alive/demo_config.h](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Keep_Alive/demo_config.h) 的本地副本。

2. 添加下列行，并设置您所选择的代理：

   ```c
   #define democonfigMQTT_BROKER_ENDPOINT "your-desired-endpoint"
   ```

   ```c
   #define democonfigMQTT_BROKER_PORT ( 1883 )
   ```


## 功能

该演示创建了一个单个应用程序任务，该任务通过一系列示例循环，演示如何连接到 
代理，使用自动重新加载定时器处理存活，订阅代理上的主题， 
在代理上发布主题，最后，断开与代理的连接。演示应用程序 
订阅一个主题，并向同一个主题发布。当演示向 MQTT 代理发布消息时， 
代理会向演示应用程序发送相同的消息。演示的结构体如下 
所示：

```c
static void prvMQTTDemoTask( void * pvParameters )  
{  
uint32_t ulTopicCount = 0U;  
NetworkContext_t xNetworkContext = { 0 };  
MQTTContext_t xMQTTContext;  
MQTTStatus_t xMQTTStatus;  
PlaintextTransportStatus_t xNetworkStatus;  
BaseType_t xTimerStatus;  
  
    /* Remove compiler warnings about unused parameters. */  
    ( void ) pvParameters;  
  
    /* Serialize a PINGREQ packet to send upon invoking the keep-alive timer  
     * callback. */  
    xMQTTStatus = MQTT_SerializePingreq( &xPingReqBuffer );  
    configASSERT( xMQTTStatus == MQTTSuccess );  
  
    for( ; ; )  
    {  
        /****************************** Connect. ******************************/  
  
        /* Attempt to connect to the MQTT broker. If connection fails, retry  
         * after a timeout. The timeout value will be exponentially increased  
         * until the maximum number of attempts are reached or the maximum  
         * timeout value is reached. The function below returns a failure status  
         * if the TCP connection cannot be established to the broker after  
         * the configured number of attempts. */  
        xNetworkStatus = prvConnectToServerWithBackoffRetries( &xNetworkContext );  
        configASSERT( xNetworkStatus == PLAINTEXT_TRANSPORT_SUCCESS );  
  
        /* Sends an MQTT Connect packet over the already connected TCP socket,  
         * and waits for connection acknowledgment (CONNACK) packet. */  
        LogInfo( ( "Creating an MQTT connection to %s.", democonfigMQTT_BROKER_ENDPOINT ) );  
        prvCreateMQTTConnectionWithBroker( &xMQTTContext, &xNetworkContext );  
  
        /* Create timers to handle keep-alive. */  
        xPingReqTimer = xTimerCreateStatic( "PingReqTimer",  
                                            mqttexamplePING_REQUEST_DELAY,  
                                            pdTRUE,  
                                            ( void * ) &xMQTTContext.transportInterface,  
                                            prvPingReqTimerCallback,  
                                            &xPingReqTimerBuffer );  
        configASSERT( xPingReqTimer );  
        xPingRespTimer = xTimerCreateStatic( "PingRespTimer",  
                                             mqttexamplePING_RESPONSE_DELAY,  
                                             pdFALSE,  
                                             NULL,  
                                             prvPingRespTimerCallback,  
                                             &xPingRespTimerBuffer );  
        configASSERT( xPingRespTimer );  
  
        /* Start the timer to send a PINGREQ. */  
        xTimerStatus = xTimerStart( xPingReqTimer, 0 );  
        configASSERT( xTimerStatus == pdPASS );  
  
        /**************************** Subscribe. ******************************/  
  
        /* If the server rejected the subscription request, attempt to resubscribe  
         * to the topic. Attempts are made according to the exponential backoff retry  
         * strategy declared in retry_utils.h. */  
        prvMQTTSubscribeWithBackoffRetries( &xMQTTContext );  
  
        /************************ Send PINGREQ packet. ************************/  
  
        /* Deliberately delay in order for the auto-reload timer to send a PINGREQ to the broker. */  
        vTaskDelay( mqttexamplePING_REQUEST_DELAY );  
  
        /********************* Publish and Receive Loop. **********************/  
        /* Publish messages with QOS1, send and process keep-alive messages. */  
        LogInfo( ( "Publish to the MQTT topic %s.", mqttexampleTOPIC ) );  
        prvMQTTPublishToTopic( &xMQTTContext );  
  
        /* Process the incoming publish echo. Since the application subscribed to  
         * the same topic, the broker will send the same publish message back  
         * to the application. */  
        LogInfo( ( "Attempt to receive publish message from broker." ) );  
        while( xReceivedPubAck == pdFALSE )  
        {  
            ulReceiveLoopIterations += 1U;  
            configASSERT( ulReceiveLoopIterations <= mqttexampleMAX_RECEIVE_LOOP_ITERATIONS );  
  
            vTaskDelay( mqttexampleRECEIVE_LOOP_ITERATION_DELAY );  
  
            xMQTTStatus = MQTT_ReceiveLoop( &xMQTTContext, 0U );  
            configASSERT( xMQTTStatus == MQTTSuccess );  
        }  
  
        /* Reset after loop. */  
        ulReceiveLoopIterations = 0U;  
        xReceivedPubAck = pdFALSE;  
  
        /******************** Unsubscribe from the topic. *********************/  
        LogInfo( ( "Unsubscribe from the MQTT topic %s.", mqttexampleTOPIC ) );  
        prvMQTTUnsubscribeFromTopic( &xMQTTContext );  
  
        /* Process an incoming packet from the broker. */  
        while( xReceivedUnsubAck == pdFALSE )  
        {  
            ulReceiveLoopIterations += 1U;  
            configASSERT( ulReceiveLoopIterations <= mqttexampleMAX_RECEIVE_LOOP_ITERATIONS );  
  
            vTaskDelay( mqttexampleRECEIVE_LOOP_ITERATION_DELAY );  
  
        }  
  
        /* Reset after loop. */  
        ulReceiveLoopIterations = 0U;  
        xReceivedUnsubAck = pdFALSE;  
  
        /**************************** Disconnect. *****************************/  
  
        /* Send an MQTT disconnect packet over the connected TCP socket.  
         * There is no corresponding response for the disconnect packet. After  
         * sending the disconnect, the client must close the network connection. */  
        LogInfo( ( "Disconnecting the MQTT connection with %s.",  
        democonfigMQTT_BROKER_ENDPOINT ) );  
        xMQTTStatus = MQTT_Disconnect( &xMQTTContext );  
        configASSERT( xMQTTStatus == MQTTSuccess );  
  
        /* Stop the keep-alive timers for the next iteration. */  
        xTimerStatus = xTimerStop( xPingReqTimer, 0 );  
        configASSERT( xTimerStatus == pdPASS );  
        xTimerStatus = xTimerStop( xPingRespTimer, 0 );  
        configASSERT( xTimerStatus == pdPASS );  
  
        /* Close the network connection. */  
        xNetworkStatus = Plaintext_FreeRTOS_Disconnect( &xNetworkContext );  
        configASSERT( xNetworkStatus == PLAINTEXT_TRANSPORT_SUCCESS );  
  
        /* Reset the SUBACK status for each topic filter after completion of the  
         * subscription request cycle. */  
        for( ulTopicCount = 0; ulTopicCount < mqttexampleTOPIC_COUNT; ulTopicCount++ )  
        {  
            xTopicFilterContext[ ulTopicCount ].xSubAckStatus = MQTTSubAckFailure;  
        }  
      
        /* Wait for some time between two iterations to ensure that we do not  
         * bombard the broker. */  
        LogInfo( ( "prvMQTTDemoTask() completed an iteration successfully. "  
                   "Total free heap is %u.",  
                   xPortGetFreeHeapSize() ) );  
        LogInfo( ( "Demo completed successfully." ) );  
        LogInfo( ( "Short delay before starting the next iteration.... &bsol;r&bsol;n" ) );  
        vTaskDelay( mqttexampleDELAY_BETWEEN_DEMO_ITERATIONS );  
    }  
}  
```

![](/media/2020/coreMQTT-keep-alive-1.png)


## 连接到 MQTT 代理

函数 `prvConnectToServerWithBackoffRetries()` 试图与 MQTT 代理建立 TCP 连接 
。如果连接失败，则在超时后重试。超时值将呈指数增长， 
直到达到最大尝试次数或最大超时值。 
如果在配置的尝试次数后仍无法与代理建立 TCP 连接，`prvConnectToServerWithBackoffRetries()` 
将返回失败状态。

```c
static PlaintextTransportStatus_t prvConnectToServerWithBackoffRetries( NetworkContext_t * pxNetworkContext )  
{  
PlaintextTransportStatus_t xNetworkStatus;  
RetryUtilsStatus_t xRetryUtilsStatus = RetryUtilsSuccess;  
RetryUtilsParams_t xReconnectParams;  
  
    /* Initialize reconnect attempts and interval. */  
    RetryUtils_ParamsReset( &xReconnectParams );  
    xReconnectParams.maxRetryAttempts = MAX_RETRY_ATTEMPTS;  
  
    /* Attempt to connect to MQTT broker. If connection fails, retry after  
     * a timeout. Timeout value will exponentially increase till maximum  
     * attempts are reached.  
     */  
    do  
    {  
        /* Establish a TCP connection with the MQTT broker. This example connects to  
         * the MQTT broker as specified in democonfigMQTT_BROKER_ENDPOINT and  
         * democonfigMQTT_BROKER_PORT at the top of this file. */  
        LogInfo( ( "Create a TCP connection to %s:%d.",  
        democonfigMQTT_BROKER_ENDPOINT,  
        democonfigMQTT_BROKER_PORT ) );  
        xNetworkStatus = Plaintext_FreeRTOS_Connect( pxNetworkContext,  
        democonfigMQTT_BROKER_ENDPOINT,  
        democonfigMQTT_BROKER_PORT,  
        mqttexampleTRANSPORT_SEND_RECV_TIMEOUT_MS,  
        mqttexampleTRANSPORT_SEND_RECV_TIMEOUT_MS );  
      
        if( xNetworkStatus != PLAINTEXT_TRANSPORT_SUCCESS )  
        {  
            LogWarn( ( "Connection to the broker failed. Retrying connection with backoff and jitter." ) );  
            xRetryUtilsStatus = RetryUtils_BackoffAndSleep( &xReconnectParams );  
        }  
      
        if( xRetryUtilsStatus == RetryUtilsRetriesExhausted )  
        {  
            LogError( ( "Connection to the broker failed, all attempts exhausted." ) );  
            xNetworkStatus = PLAINTEXT_TRANSPORT_CONNECT_FAILURE;  
        }  
    } while( ( xNetworkStatus != PLAINTEXT_TRANSPORT_SUCCESS ) && ( xRetryUtilsStatus == RetryUtilsSuccess ) );  
  
    return xNetworkStatus;  
}  
```

函数 '`prvCreateMQTTConnectionWithBroker()`' 演示了如何使用 
清除会话与 MQTT 代理建立未加密连接。它使用 FreeRTOS-Plus-TCP 传输接口， 
该接口在文件 `FreeRTOS-Plus/Source/Application-Protocols/platform/freertos/transport/src/plaintext_freertos.c'` 中实现。 
'`prvCreateMQTTConnectionWithBroker()`' 的定义如下所示。请记住，我们在
'`xConnectInfo.`' 中设置代理的存活秒数。

以下函数展示了如何使用 `MQTT_Init()` 在 MQTT 上下文中设置 FreeRTOS-Plus-TCP 传输接口。
它还展示了如何设置事件回调函数指针 (`prvEventCallback`)。此回调用于报告
传入消息。

```c
static void prvCreateMQTTConnectionWithBroker( MQTTContext_t * pxMQTTContext,  
NetworkContext_t * pxNetworkContext )  
{  
MQTTStatus_t xResult;  
MQTTConnectInfo_t xConnectInfo;  
bool xSessionPresent;  
TransportInterface_t xTransport;  
  
    /***  
     * For readability, error handling in this function is restricted to the use of  
     * asserts().  
     ***/  
  
    /* Fill in Transport Interface send and receive function pointers. */  
    xTransport.pNetworkContext = pxNetworkContext;  
    xTransport.send = Plaintext_FreeRTOS_send;  
    xTransport.recv = Plaintext_FreeRTOS_recv;  
  
    /* Initialize MQTT library. */  
    xResult = MQTT_Init( pxMQTTContext, &xTransport, prvGetTimeMs, prvEventCallback, &xBuffer );  
    configASSERT( xResult == MQTTSuccess );  
  
    /* Many fields not used in this demo so start with everything at 0. */  
    ( void ) memset( ( void * ) &xConnectInfo, 0x00, sizeof( xConnectInfo ) );  
  
    /* Start with a clean session i.e. direct the MQTT broker to discard any  
     * previous session data. Also, establishing a connection with a clean session  
     * will ensure that the broker does not store any data when this client  
     * gets disconnected. */  
    xConnectInfo.cleanSession = true;  

    /* The client identifier is used to uniquely identify this MQTT client to  
     * the MQTT broker. In a production device, the identifier can be something  
     * unique, such as a device serial number. */  
    xConnectInfo.pClientIdentifier = democonfigCLIENT_IDENTIFIER;  
    xConnectInfo.clientIdentifierLength = ( uint16_t ) strlen( democonfigCLIENT_IDENTIFIER );  

    /* Set MQTT keep-alive period. It is the responsibility of the application  
     * to ensure that the interval between control packets being sent does not  
     * exceed the keep-alive value. In the absence of sending any other control  
     * packets, the client MUST send a PINGREQ Packet. */  
    xConnectInfo.keepAliveSeconds = mqttexampleKEEP_ALIVE_TIMEOUT_SECONDS;  

    /* Send MQTT CONNECT packet to broker. LWT is not used in this demo, so it  
     * is passed as NULL. */  
    xResult = MQTT_Connect( pxMQTTContext,  
                            &xConnectInfo,  
                            NULL,  
                            mqttexampleCONNACK_RECV_TIMEOUT_MS,  
                            &xSessionPresent );  
                            configASSERT( xResult == MQTTSuccess );  
}  

```

`prvCreateMQTTConnectionWithBroker()` 演示了如何使用 
清除会话与 MQTT 代理建立未加密连接。


## 使用自动重新加载定时器处理存活

应用程序连接到代理后，它会创建一个自动重新加载定时器， 
负责在 '`mqttexampleKEEP_ALIVE_DELAY`' 滴答过后调用回调。此回调 
使用 coreMQTT 序列化器 API 序列化 ping 请求数据包，然后将其发送到 MQTT 代理。此回调函数的定义 
如下所示：

```c
static void prvPingReqTimerCallback( TimerHandle_t pxTimer )  
{  
    TransportInterface_t * pxTransport;  
    int32_t xTransportStatus;  
    BaseType_t xTimerStatus;  
  
    pxTransport = ( TransportInterface_t * ) pvTimerGetTimerID( pxTimer );  
  
    /* Do not resend if waiting on a PINGRESP. */  
    if( xWaitingForPingResp == false )  
    {  
        /* Send PINGREQ to broker */  
        LogInfo( ( "Ping the MQTT broker." ) );  
        xTransportStatus = pxTransport->send( pxTransport->pNetworkContext,  
                                              ( void * ) xPingReqBuffer.pBuffer,  
                                              xPingReqBuffer.size );  
        configASSERT( ( size_t ) xTransportStatus == xPingReqBuffer.size );  
  
        xWaitingForPingResp = true;  

        /* Start the timer to expect a PINGRESP. */  
        xTimerStatus = xTimerStart( xPingRespTimer, 0 );  
        configASSERT( xTimerStatus == pdPASS );  
    }  
}  

```

`prvKeepAliveTimerCallback()` 演示了如何向 MQTT 代理发送 ping 请求数据包。发送后， 
将启动另一个计时器，通过下面定义的另一个回调来处理 ping 响应：

```c
static void prvPingRespTimerCallback( TimerHandle_t pxTimer )  
{  
    ( void ) pxTimer;  
  
    /* Assert that a pending PINGRESP has been received. */  
    configASSERT( xWaitingForPingResp == false );  
}  

```

`prvKeepAliveTimerCallback()` 只断言已收到 ping 响应。


## 订阅 MQTT 主题

函数 '`prvMQTTSubscribeWithBackoffRetries()`' 演示了如何订阅 MQTT 代理上的主题过滤器 
。该示例演示了如何订阅一个主题过滤器，但也可以在同一个 API 调用中传递一个主题过滤器列表， 
以订阅一个以上的主题过滤器。此外，如果 
MQTT 代理拒绝了订阅请求，则订阅将重试 '`MAX_RETRY_ATTEMPTS`' 次。 
此函数的定义如下所示：

```c
static void prvMQTTSubscribeWithBackoffRetries( MQTTContext_t * pxMQTTContext )  
{  
MQTTStatus_t xResult = MQTTSuccess;  
RetryUtilsStatus_t xRetryUtilsStatus = RetryUtilsSuccess;  
RetryUtilsParams_t xRetryParams;  
MQTTSubscribeInfo_t xMQTTSubscription[ mqttexampleTOPIC_COUNT ];  
bool xFailedSubscribeToTopic = false;  
uint32_t ulTopicCount = 0U;  
  
    /* Some fields are not used by this demo so start with everything at 0. */  
    ( void ) memset( ( void * ) &xMQTTSubscription, 0x00, sizeof( xMQTTSubscription ) );  
  
    /* Get a unique packet id. */  
    usSubscribePacketIdentifier = MQTT_GetPacketId( pxMQTTContext );  
  
    /* Subscribe to the mqttexampleTOPIC topic filter. This example subscribes to  
     * only one topic and uses QoS0. */  
    xMQTTSubscription[ 0 ].qos = MQTTQoS0;  
    xMQTTSubscription[ 0 ].pTopicFilter = mqttexampleTOPIC;  
    xMQTTSubscription[ 0 ].topicFilterLength = ( uint16_t ) strlen( mqttexampleTOPIC );  
  
    /* Initialize retry attempts and interval. */  
    RetryUtils_ParamsReset( &xRetryParams );  
    xRetryParams.maxRetryAttempts = MAX_RETRY_ATTEMPTS;  
  
    do  
    {  
        /* The client is now connected to the broker. Subscribe to the topic  
         * as specified in mqttexampleTOPIC at the top of this file by sending a  
         * subscribe packet then waiting for a subscribe acknowledgment (SUBACK).  
         * This client will then publish to the same topic it subscribed to, so it  
         * will expect all the messages it sends to the broker to be sent back to it  
         * from the broker. This demo uses QOS0 in Subscribe. Therefore, the publish  
         * messages received from the broker will have QOS0. */  
        LogInfo( ( "Attempt to subscribe to the MQTT topic %s.", mqttexampleTOPIC ) );  
        xResult = MQTT_Subscribe( pxMQTTContext,  
        xMQTTSubscription,  
        sizeof( xMQTTSubscription ) / sizeof( MQTTSubscribeInfo_t ),  
        usSubscribePacketIdentifier );  
        configASSERT( xResult == MQTTSuccess );  
      
        LogInfo( ( "SUBSCRIBE sent for topic %s to broker.&bsol;n&bsol;n", mqttexampleTOPIC ) );  
  
        /* Process incoming packet from the broker. After sending the subscribe, the  
         * client may receive a publish before it receives a subscribe ack. Therefore,  
         * call the generic incoming packet processing function. Since this demo is  
         * subscribing to the topic to which no one is publishing, probability of  
         * receiving a publish message before a subscribe ack is zero; but the application  
         * must be ready to receive any packet. This demo uses the generic packet  
         * processing function everywhere to highlight this fact. */  
        while( xReceivedSubAck == pdFALSE )  
        {  
            ulReceiveLoopIterations += 1U;  
            configASSERT( ulReceiveLoopIterations <= mqttexampleMAX_RECEIVE_LOOP_ITERATIONS );  
          
            vTaskDelay( mqttexampleRECEIVE_LOOP_ITERATION_DELAY );  
          
            xResult = MQTT_ReceiveLoop( pxMQTTContext, 0U );  
            configASSERT( xResult == MQTTSuccess );  
        }  
  
        /* Reset in case another attempt to subscribe is needed. */  
        ulReceiveLoopIterations = 0U;  
        xReceivedSubAck = pdFALSE;  
      
        /* Reset flag before checking suback responses. */  
        xFailedSubscribeToTopic = false;  
  
        /* Check if the recent subscription request has been rejected. #xTopicFilterContext  
         * is updated in the event callback to reflect the status of the SUBACK  
         * sent by the broker. It represents either the QoS level granted by the  
         * server upon subscription or acknowledgement of server rejection of the  
         * subscription request. */  
        for( ulTopicCount = 0; ulTopicCount < mqttexampleTOPIC_COUNT; ulTopicCount++ )  
        {  
            if( xTopicFilterContext[ ulTopicCount ].xSubAckStatus == MQTTSubAckFailure )  
            {  
                LogWarn( ( "Server rejected subscription request. Attempting to re-subscribe to topic %s.",  
                xTopicFilterContext[ ulTopicCount ].pcTopicFilter ) );  
                xFailedSubscribeToTopic = true;  
                xRetryUtilsStatus = RetryUtils_BackoffAndSleep( &xRetryParams );  
                break;  
            }  
        }  
  
        configASSERT( xRetryUtilsStatus != RetryUtilsRetriesExhausted );  

    } while( ( xFailedSubscribeToTopic == true ) && ( xRetryUtilsStatus == RetryUtilsSuccess ) );  
}  

```


## 接收传入消息

如前所述，应用程序在连接到代理之前注册事件回调函数。 
函数 `'prvMQTTDemoTask()`' 通过调用 '`MQTT_ReceiveLoop()`' 来接收传入消息。当接收到传入的 MQTT 消息时， 
它会调用应用程序注册的事件回调函数。函数 
'`prvEventCallback()`' 是这种事件回调函数的示例；它检查传入的数据包类型， 
并调用适当的处理程序。在此处的示例中，函数要么 
调用 '`prvMQTTProcessIncomingPublish()`' 来处理传入的发布消息，要么调用 '`prvMQTTProcessResponse()`' 
来处理确认。

```c
static void prvEventCallback( MQTTContext_t * pxMQTTContext,  
                              MQTTPacketInfo_t * pxPacketInfo,  
                              MQTTDeserializedInfo_t * pxDeserializedInfo )  
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


## 发布到主题

函数 "`prvMQTTPublishToTopic()`" 演示了如何在 MQTT 代理上发布主题过滤器。 
此函数的定义如下所示：

```c
static void prvMQTTPublishToTopic( MQTTContext_t * pxMQTTContext )  
{  
MQTTStatus_t xResult;  
MQTTPublishInfo_t xMQTTPublishInfo;  
BaseType_t xTimerStatus;  

    /***  
     * For readability, error handling in this function is restricted to the use of  
     * asserts().  
     ***/  

    /* Some fields are not used by this demo so start with everything at 0. */  
    ( void ) memset( ( void * ) &xMQTTPublishInfo, 0x00, sizeof( xMQTTPublishInfo ) );  

    /* This demo uses QoS0. */  
    xMQTTPublishInfo.qos = MQTTQoS0;  
    xMQTTPublishInfo.retain = false;  
    xMQTTPublishInfo.pTopicName = mqttexampleTOPIC;  
    xMQTTPublishInfo.topicNameLength = ( uint16_t ) strlen( mqttexampleTOPIC );  
    xMQTTPublishInfo.pPayload = mqttexampleMESSAGE;  
    xMQTTPublishInfo.payloadLength = strlen( mqttexampleMESSAGE );  
  
    /* Send a PUBLISH packet. Packet ID is not used for a QoS0 publish. */  
    xResult = MQTT_Publish( pxMQTTContext, &xMQTTPublishInfo, 0U );  
    configASSERT( xResult == MQTTSuccess );  
  
    /* When a PUBLISH packet has been sent, the keep-alive timer can be reset. */  
    xTimerStatus = prvCheckTimeoutThenResetTimer( xKeepAliveTimer );  
    configASSERT( xTimerStatus == pdPASS );  
}  

```


## 处理传入的 MQTT 发布数据包

函数 "`prvMQTTProcessIncomingPublish()`" 演示了如何处理来自 MQTT 代理的 `PUBLISH` 数据包
。此函数的定义如下所示：

```c
static void prvMQTTProcessIncomingPublish( MQTTPublishInfo_t * pxPublishInfo )  
{  
    configASSERT( pxPublishInfo != NULL );  
  
    /* Process incoming Publish. */  
    LogInfo( ( "Incoming QoS : %d&bsol;n", pxPublishInfo->qos ) );  
  
    /* Verify the received publish is for the we have subscribed to. */  
    if( ( pxPublishInfo->topicNameLength == strlen( mqttexampleTOPIC ) ) &&  
        ( 0 == strncmp( mqttexampleTOPIC, pxPublishInfo->pTopicName, pxPublishInfo->topicNameLength ) ) )  
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

```


## 取消订阅主题

工作流中的最后一步是取消订阅主题，因此代理不再发送已在 
'`mqttexampleTOPIC`' 上发布的消息。此函数的定义如下所示：

```c
static void prvMQTTUnsubscribeFromTopic( MQTTContext_t * pxMQTTContext )  
{  
MQTTStatus_t xResult;  
MQTTSubscribeInfo_t xMQTTSubscription[ mqttexampleTOPIC_COUNT ];  
  
    /* Some fields are not used by this demo, so start with everything at 0. */  
    ( void ) memset( ( void * ) &xMQTTSubscription, 0x00, sizeof( xMQTTSubscription ) );  
  
    /* Get a unique packet id. */  
    usSubscribePacketIdentifier = MQTT_GetPacketId( pxMQTTContext );  
  
    /* Subscribe to the mqttexampleTOPIC topic filter. This example subscribes to  
     * only one topic and uses QoS0. */  
    xMQTTSubscription[ 0 ].qos = MQTTQoS0;  
    xMQTTSubscription[ 0 ].pTopicFilter = mqttexampleTOPIC;  
    xMQTTSubscription[ 0 ].topicFilterLength = ( uint16_t ) strlen( mqttexampleTOPIC );  
  
    /* Get the next unique packet identifier. */  
    usUnsubscribePacketIdentifier = MQTT_GetPacketId( pxMQTTContext );  
  
    /* Send the UNSUBSCRIBE packet. */  
    xResult = MQTT_Unsubscribe( pxMQTTContext,  
    xMQTTSubscription,  
    sizeof( xMQTTSubscription ) / sizeof( MQTTSubscribeInfo_t ),  
    usUnsubscribePacketIdentifier );  
  
    configASSERT( xResult == MQTTSuccess );  
}  

```

