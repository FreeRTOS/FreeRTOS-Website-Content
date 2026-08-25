---
title: coreMQTT 基本多线程演示
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


## 单线程 VS 多线程

coreMQTT 有两种使用模式，*单线程*和*多线程*（多任务）。您可以此页面上的演示为例， 
创建您自己的多线程方案。还有一个 
多线程示例， 
它在后台的[agent（或守护进程）任务中执行 MQTT 协议](mqtt-agent-demo.md)。在agent 任务中执行 MQTT 协议 
使应用程序写入器无需显式托管任何 MQTT 状态或调用 `MQTT_ProcessLoop()` 
API 函数。使用 agent 任务还可以让多个应用程序任务共享单个 MQTT 连接， 
而无需使用互斥锁等同步原语。


## 演示简介

coreMQTT 基本多线程演示项目使用 
[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)， 
因此可以使用 
[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/) 
在 Windows 上进行构建和评估，无需任何特定 MCU 硬件。

此演示使用线程安全队列来保存与 MQTT API 交互的命令。本演示中 
有四项任务需要注意：

* 命令（主）任务处理来自命令队列的命令，而其他任务则将它们放入队列 
  。该任务进入循环，并在循环期间处理来自命令队列的命令。如果收到终止命令， 
  就会跳出循环。

* 同步发布者任务创建一系列发布操作，并将其推送到命令队列， 
  然后由命令任务执行发布操作。此任务使用同步发布，这意味着它将等待每个发布 
  操作完成，然后再调度下一个操作。

* 异步发布者任务创建一系列发布操作，并将其推送到命令队列， 
  然后由命令任务执行发布操作。此任务与前一个任务的区别在于， 
  它不会等待一个发布操作完成后再安排下一个发布操作， 
  而是在所有发布操作排队后检查每个发布操作的状态。请注意， 
  同步发布和异步发布的区别仅在于任务的行为， 
  而不在于实际的发布命令。

* 订阅者任务创建一个主题过滤器 MQTT 订阅，该订阅与发布者任务发布的所有消息的主题相匹配 
  。它循环进行，等待接收其他任务发布的消息 
  。

任务可以有队列来保存收到的消息，命令任务将传入的消息推送到 
订阅了传入主题的每个任务的队列中。

可将基本多线程演示配置为使用带有相互身份验证的 TLS 连接 
或明文 TCP 连接。默认情况下，演示使用 TLS。如果在演示过程中网络意外断开， 
则客户端将尝试使用指数退避逻辑重新连接。此外， 
如果重新连接成功，但代理无法恢复先前的会话， 
则客户端将重新订阅先前订阅的主题。


## 源代码组织

多线程 MQTT 演示的 Visual Studio 解决方案称为 
[`mqtt_multitask_demo.sln`](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Multitask/mqtt_multitask_demo.sln)， 
可在 
[/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Multitask](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Multitask) 
目录中找到（位于[主 FreeRTOS](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) 下载包中）。


[\![](../fr-content-src/uploads/2020/10/coreMQTT-Source-Code-Organization.png)](../fr-content-src/uploads/2020/10/coreMQTT-Source-Code-Organization.png)   
*点击放大*


## 构建演示项目

演示项目使用[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/)。 
要构建演示，请执行如下操作：

1. 从 Visual Studio IDE 中打开 '`mqtt_multitask_demo.sln`' Visual Studio 解决方案文件。

2. 从 IDE 的 '`Build`' 菜单中选择 '`Build Solution`' 。

**注意**：如果您使用的是 Microsoft Visual Studio 2017 或更早版本，则必须选择与您的版本兼容的 '`Platform 
Toolset`'：'`Project -> RTOSDemos Properties -> Platform Toolset`'。


## 配置演示项目

此演示使用 [FreeRTOS-Plus-TCP TCP/IP 堆栈](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/index.md)，因此 
请按照 
[TCP/IP 入门项目](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md)的说明操作， 
以确保您：

1. [安装了必备组件](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#prerequisites) 
   （如 WinPCap）。

2. [设置了静态或动态 IP 地址、网关地址和网络掩码](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#static-dynamic)（可选）。

3. [设置了 MAC 地址](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#mac-addr)（可选）。

4. 在您的主机上[选择以太网接口](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#network-interface) 
   。

5. ......**重要的是**，在尝试运行 MQTT 演示之前，[请先测试网络连接](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#connectivity-test) 
   。

所有这些设置都应在 MQTT LTS rc1 演示项目中更改，而不是在上面链接的页面中所提及的 TCP/IP Starter 项目中 
更改！交付时， TCP/IP 堆栈被配置为使用动态 
IP 地址。


## 配置 MQTT 代理连接

### 备选方案 1：带有相互身份验证的 TLS（默认）：

此演示支持与 [MQTT Mutual Auth](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication) 演示相同的配置选项 
。请参阅演示文档，了解所有可用选项。


### 备选方案 2：明文：

为了启用无需证书配置的快速设置，基本多线程演示允许使用 
明文 TCP 连接来代替相互身份验证的 TLS 连接。要禁用 TLS， 
宏 '`democonfigUSE_TLS`' 应在 '`demo_config`' 中设置为 `0`，或者干脆不定义。然后， 
可以按照与明文演示相同的说明，将该演示用于任何未加密的 MQTT 代理（例如，Eclipse Mosquitto） 
[](basic-mqtt-example.md)。


## 功能

演示总共创建了四个任务：其中三个请求 MQTT API 调用，一个处理这些请求 
（主任务）。在本演示中，主任务通过创建三个子任务、调用处理循环 
并在之后进行清理实现循环。这个主任务创建一个与代理的单 MQTT 连接， 
然后由子任务共享。其中两个任务向代理发布消息， 
第三个任务通过与所有已发布消息匹配的主题过滤器的 MQTT 订阅 
来接收消息。 


## Typedef

演示定义了以下结构体、枚举和函数指针：


**命令**  

任务不是直接调用 MQTT API，而是使用 '`Command_t`' 结构体创建命令， 
指示主任务为它们调用适当的 API。命令类型可能为 '`PROCESSLOOP`'、 
'`PUBLISH`'、'`SUBSCRIBE`'、'`UNSUBSCRIBE`'、'`PING`'、'`DISCONNECT`'、'`RECONNECT`' 或 '`TERMINATE`'。 
'`TERMINATE`' 命令没有相应的 MQTT API； 
它在演示中用于指示主任务停止处理命令并开始清除操作。由于某些 
MQTT 命令（'`MQTT_Publish`'、'`MQTT_Subscribe`' 
和 '`MQTT_Unsubscribe`'）需要一些附加信息（如发布或订阅信息），因此我们使用 '`CommandContext_t`' 字段。该字段对刚才提到的三条命令是必须的， 
但对其他命令是可选的。 

由于这些命令需要此上下文，所以一旦命被排队后， 
在命令完成之前，一定不能改变该上下文。命令完成后，可调用可选回调。 
在这个演示中，我们使用回调来创建任务通知， 
通知调用任务命令已完成。对于需要确认的 MQTT 操作（订阅、 
取消订阅和以大于 0 的 QoS 发布），一旦收到确认，则认为命令已经完成。否则， 
一旦返回相应的 MQTT API 调用，就认为命令已经完成。

```c
/**  
 * @brief A command for interacting with the MQTT API.  
 */  
typedef struct Command  
{  
    CommandType_t xCommandType;  
    CommandContext_t * pxCmdContext;  
    CommandCallback_t vCallback;  
} Command_t;  

```

```c
/**  
 * @brief Struct containing context for a specific command.  
 *  
 * @note An instance of this struct and any variables it points to MUST stay  
 * in scope until the associated command is processed, and its callback called.  
 * The command callback will set the `xIsComplete` flag, and notify the calling task.  
 */  
typedef struct CommandContext  
{  
    MQTTPublishInfo_t * pxPublishInfo;  
    MQTTSubscribeInfo_t * pxSubscribeInfo;  
    size_t ulSubscriptionCount;  
    MQTTStatus_t xReturnStatus;  
    bool xIsComplete;  
  
    /* The below fields are specific to this FreeRTOS implementation. */  
    TaskHandle_t xTaskToNotify;  
    uint32_t ulNotificationBit;  
    QueueHandle_t pxResponseQueue;  
} CommandContext_t;  

```

```c
/**  
 * @brief A type of command for interacting with the MQTT API.  
 */  
typedef enum CommandType  
{  
    PROCESSLOOP, /**< @brief Call MQTT_ProcessLoop(). */  
    PUBLISH,     /**< @brief Call MQTT_Publish(). */  
    SUBSCRIBE,   /**< @brief Call MQTT_Subscribe(). */  
    UNSUBSCRIBE, /**< @brief Call MQTT_Unsubscribe(). */  
    PING,        /**< @brief Call MQTT_Ping(). */  
    DISCONNECT,  /**< @brief Call MQTT_Disconnect(). */  
    RECONNECT,   /**< @brief Reconnect a broken connection. */  
    TERMINATE    /**< @brief Exit the command loop and stop processing commands. */  
} CommandType_t;  

```

```c
/**  
 * @brief Callback function called when a command completes.  
 */  
typedef void (* CommandCallback_t )( CommandContext_t * );  

```

**致谢**  

由于某些 MQTT 操作需要确认，所以使用了一个 '`AckInfo_t`' 数组， 
其中包含了预期确认的数据包标识符，以及期待它的原始命令 
（这样就可以调用其完成回调）。 

```c
typedef struct ackInfo  
{  
    uint16_t usPacketId;  
    Command_t xOriginalCommand;  
} AckInfo_t;  

```

**订阅**  

本演示能够跟踪每个任务的订阅。为此，每个请求订阅的任务必须提供一个消息队列， 
在该队列中它将接收发布的消息。多个 
任务可以订阅同一个主题过滤器，因为它们要使用不同的响应队列。

```c
/**  
 * @brief An element in the list of subscriptions maintained in the demo.  
 *  
 * @note This demo allows multiple tasks to subscribe to the same topic.  
 * In this case, another element is added to the subscription list, differing  
 * in the destination response queue.  
 */  
typedef struct subscriptionElement  
{  
    char pcSubscriptionFilter[ mqttexampleDEMO_BUFFER_SIZE ];  
    uint16_t usFilterLength;  
    QueueHandle_t pxResponseQueue;  
} SubscriptionElement_t;  
```


**收到的已发布消息**  

由于任务与主任务并行执行，因此如果主任务必须等待每个订阅的任务读取收到的已发布消息， 
将十分困难且耗时。因此，收到的每条消息都会被复制到 
订阅了已发布消息主题的任何任务的响应队列中。由于从 MQTT 客户端收到的发布数据包 
包含指向客户端网络缓冲区的指针，在插入到响应队列之前， 
传入消息的有效载荷和主题名称将被复制到不同的缓冲区。这样，在 MQTT 客户端清除其网络缓冲区后， 
订阅的任务仍然可以读取收到的信息。

```c
/**  
 * @brief An element for a task's response queue for received publishes.  
 *  
 * @note Since elements are copied to queues, this struct needs to hold  
 * buffers for the payload and topic of incoming publishes, as the original  
 * pointers are out of scope. When processing a publish from this struct,  
 * the `pcTopicNameBuf` and `pcPayloadBuf` pointers need to be set to point to the  
 * static buffers in this struct.  
 */  
typedef struct publishElement  
{  
    MQTTPublishInfo_t xPublishInfo;  
    uint8_t pcPayloadBuf[ mqttexampleDEMO_BUFFER_SIZE ];  
    uint8_t pcTopicNameBuf[ mqttexampleDEMO_BUFFER_SIZE ];  
} PublishElement_t;  

```

## 主任务

主应用程序任务建立一个持久的 MQTT 会话，创建三个子任务，并执行处理循环， 
直到收到终止命令。由于使用了持久会话，所以如果网络意外断开， 
演示将在后台重新连接代理，而不会导致订阅或来自代理的任何传入已发布消息丢失 
。为了为每次运行创建一个新的持久会话，演示在设置了“清除会话”标志的情况下与代理相连， 
然后断开连接，并在未设置该标志的情况下重新连接。处理循环结束后，它将断开与代理的连接， 
并从网络重新连接中再次循环。主任务的结构体如下所示：

```c
static void prvMQTTDemoTask( void * pvParameters )  
{  
    BaseType_t xNetworkStatus = pdFAIL;  
    MQTTStatus_t xMQTTStatus;  
    BaseType_t xResult = pdFALSE;  
    uint32_t ulNotification = 0;  
    uint32_t ulExpectedNotifications = mqttexamplePUBLISHER_SYNC_COMPLETE_BIT |  
                                       mqttexampleSUBSCRIBE_TASK_COMPLETE_BIT |  
                                       mqttexamplePUBLISHER_ASYNC_COMPLETE_BIT;  
  
    ( void ) pvParameters;  
  
    ulGlobalEntryTimeMs = prvGetTimeMs();  
  
    /* Create command queue for processing MQTT commands. */  
    xCommandQueue = xQueueCreate( mqttexampleCOMMAND_QUEUE_SIZE, sizeof( Command_t ) );  
    /* Create response queues for each task. */  
    xSubscriberResponseQueue = xQueueCreate( mqttexamplePUBLISH_QUEUE_SIZE, sizeof( PublishElement_t ) );  
  
    /* In this demo, send publishes on non-subscribed topics to this queue.  
     * Note that this value is not meant to be changed after `prvCommandLoop` has  
     * been called, since access to this variable is not protected by thread  
     * synchronization primitives. */  
    xDefaultResponseQueue = xQueueCreate( 1, sizeof( PublishElement_t ) );  

    /* This demo uses a persistent session that can be re-connected if disconnected.  
     * Clean any lingering sessions that may exist from previous executions of the  
     * demo. */  
    prvCleanExistingPersistentSession();  

    for( ; ; )  
    {  
        /* Clear the lists of subscriptions and pending acknowledgments. */  
        memset( pxPendingAcks, 0x00, mqttexamplePENDING_ACKS_MAX_SIZE * sizeof( AckInfo_t ) );  
        memset( pxSubscriptions, 0x00, mqttexampleSUBSCRIPTIONS_MAX_COUNT * sizeof( SubscriptionElement_t ) );  
  
        /* Connect to the broker. */  
        xNetworkStatus = prvSocketConnect( &xNetworkContext );  
        configASSERT( xNetworkStatus == pdPASS );  
        /* Form an MQTT connection with a persistent session. */  
        xMQTTStatus = prvMQTTConnect( &globalMqttContext, false );  
        configASSERT( xMQTTStatus == MQTTSuccess );  
        configASSERT( globalMqttContext.connectStatus == MQTTConnected );  
  
        /* Give subscriber task higher priority so the subscribe will be processed before the first publish.  
         * This must be less than or equal to the priority of the main task. */  
        xResult = xTaskCreate( prvSubscribeTask, "Subscriber", democonfigDEMO_STACKSIZE, NULL, tskIDLE_PRIORITY + 1, &xSubscribeTask );  
        configASSERT( xResult == pdPASS );  
        xResult = xTaskCreate( prvSyncPublishTask, "SyncPublisher", democonfigDEMO_STACKSIZE, NULL, tskIDLE_PRIORITY, &xSyncPublisherTask );  
        configASSERT( xResult == pdPASS );  
        xResult = xTaskCreate( prvAsyncPublishTask, "AsyncPublisher", democonfigDEMO_STACKSIZE, NULL, tskIDLE_PRIORITY, &xAsyncPublisherTask );  
        configASSERT( xResult == pdPASS );  
  
        LogInfo( ( "Running command loop" ) );  
        prvCommandLoop();  
  
        /* Delete created queues. Wait for tasks to exit before cleaning up. */  
        LogInfo( ( "Waiting for tasks to exit." ) );  
        ( void ) prvNotificationWaitLoop( &ulNotification, ulExpectedNotifications, false );  
  
        configASSERT( ( ulNotification & ulExpectedNotifications ) == ulExpectedNotifications );  
  
        /* Reset queues. */  
        xQueueReset( xCommandQueue );  
        xQueueReset( xDefaultResponseQueue );  
        xQueueReset( xSubscriberResponseQueue );  
  
        /* Clear task notifications. */  
        ulNotification = ulTaskNotifyValueClear( NULL, ~( 0U ) );  
  
        /* Disconnect. */  
        xNetworkStatus = prvSocketDisconnect( &xNetworkContext );  
        configASSERT( xNetworkStatus == pdPASS );  
  
        LogInfo( ( "\r\n\r\nprvMQTTDemoTask() completed an iteration successfully. Total free heap is %u.\r\n", xPortGetFreeHeapSize() ) );  
        LogInfo( ( "Demo completed successfully.\r\n" ) );  
        LogInfo( ( "Short delay before starting the next iteration.... \r\n\r\n" ) );  
        vTaskDelay( mqttexampleDELAY_BETWEEN_DEMO_ITERATIONS );  
    }  
}  
```

[\![](../fr-content-src/uploads/2020/11/Screen-Shot-2020-10-30-at-5.51.54-AM.png)](../fr-content-src/uploads/2020/11/Screen-Shot-2020-10-30-at-5.51.54-AM.png)   
点击放大


**命令循环**  

命令循环等待命令排队，然后调用适当的 MQTT API。请注意，除了 
'`DISCONNECT`' 和 '`TERMINATE`' 外的所有命令都会导致 '`MQTT_ProcessLoop`' 被调用。 
此演示设置了一个套接字唤醒回调，当套接字上有数据可用时，将 '`PROCESSLOOP`' 命令添加到队列中 
。然而，这时队列中可能有许多命令排在它前面。因此，为了确保在处理其他命令时不会忽略传入的数据， 
在每条命令之后都会调用 '`MQTT_ProcessLoop`' 进行一次迭代 
。

```c
static void prvCommandLoop( void )  
{  
    Command_t xCommand;  
    Command_t xNewCommand;  
    MQTTStatus_t xStatus = MQTTSuccess;  
    static int lNumProcessed = 0;  
    bool xTerminateReceived = false;  
    BaseType_t xCommandAdded = pdTRUE;  
  
    /* Loop until we receive a terminate command. */  
    for( ; ; )  
    {  
        /* If there is no command in the queue, try again. */  
        if( xQueueReceive( xCommandQueue, &xCommand, mqttexampleDEMO_TICKS_TO_WAIT ) == pdFALSE )  
        {  
            LogInfo( ( "No commands in the queue. Trying again." ) );  
            continue;  
        }  
  
        xStatus = prvProcessCommand( &xCommand );  
  
        /* Add connect operation to front of queue if status was not successful. */  
        if( xStatus != MQTTSuccess )  
        {  
            LogError( ( "MQTT operation failed with status %s\n",  
                        MQTT_Status_strerror( xStatus ) ) );  
            prvCreateCommand( RECONNECT, NULL, NULL, &xNewCommand );  
            xCommandAdded = xQueueSendToFront( xCommandQueue, &xNewCommand, mqttexampleDEMO_TICKS_TO_WAIT );  
            /* Ensure the command was added to the queue. */  
            configASSERT( xCommandAdded == pdTRUE );  
        }  
  
        /* Keep a count of processed operations, for debug logs. */  
        lNumProcessed++;  
  
        /* Delay after sending a subscribe. This is to so that the broker  
         * creates a subscription for us before processing our next publish,  
         * which should be immediately after this. */  
        if( xCommand.xCommandType == SUBSCRIBE )  
        {  
            LogDebug( ( "Sleeping for %d ms after sending SUBSCRIBE packet.", mqttexampleSUBSCRIBE_TASK_DELAY_MS ) );  
            vTaskDelay( mqttexampleSUBSCRIBE_TASK_DELAY_MS );  
        }  
  
        /* Terminate the loop if we receive the termination command. */  
        if( xCommand.xCommandType == TERMINATE )  
        {  
            xTerminateReceived = true;  
            break;  
        }  
  
        LogDebug( ( "Processed %d operations.", lNumProcessed ) );  
    }  
  
    /* Make sure we exited the loop due to receiving a terminate command and not  
     * due to the queue being empty. */  
    configASSERT( xTerminateReceived == true );  
  
    LogInfo( ( "Creating Disconnect operation." ) );  
    MQTT_Disconnect( &globalMqttContext );  
    LogInfo( ( "Disconnected from broker." ) );  
}  

```


**处理命令**

```c
static MQTTStatus_t prvProcessCommand( Command_t * pxCommand )  
{  
    MQTTStatus_t xStatus = MQTTSuccess;  
    uint16_t usPacketId = MQTT_PACKET_ID_INVALID;  
    bool xAddAckToList = false, xAckAdded = false;  
    BaseType_t xNetworkResult = pdFAIL;  
    MQTTPublishInfo_t * pxPublishInfo;  
    MQTTSubscribeInfo_t * pxSubscribeInfo;  
  
    switch( pxCommand->xCommandType )  
    {  
        case PROCESSLOOP:  
  
            /* The process loop will run at the end of every command, so we don't  
             * need to call it again here. */  
            LogDebug( ( "Running Process Loop." ) );  
            break;  
  
        case PUBLISH:  
            configASSERT( pxCommand->pxCmdContext != NULL );  
            pxPublishInfo = pxCommand->pxCmdContext->pxPublishInfo;  
            configASSERT( pxPublishInfo != NULL );  
  
            if( pxPublishInfo->qos != MQTTQoS0 )  
            {  
                usPacketId = MQTT_GetPacketId( &globalMqttContext );  
            }  
  
            LogDebug( ( "Publishing message to %.*s.", ( int ) pxPublishInfo->topicNameLength, pxPublishInfo->pTopicName ) );  
            xStatus = MQTT_Publish( &globalMqttContext, pxPublishInfo, usPacketId );  
            pxCommand->pxCmdContext->xReturnStatus = xStatus;  

            /* Add to pending ack list, or call callback if QoS 0. */  
            xAddAckToList = ( pxPublishInfo->qos != MQTTQoS0 ) && ( xStatus == MQTTSuccess );  
            break;  

        case SUBSCRIBE:  
        case UNSUBSCRIBE:  
            configASSERT( pxCommand->pxCmdContext != NULL );  
            pxSubscribeInfo = pxCommand->pxCmdContext->pxSubscribeInfo;  
            configASSERT( pxSubscribeInfo != NULL );  
            configASSERT( pxSubscribeInfo->pTopicFilter != NULL );  
            usPacketId = MQTT_GetPacketId( &globalMqttContext );  
  
            if( pxCommand->xCommandType == SUBSCRIBE )  
            {  
                /* Even if some subscriptions already exist in the subscription list,  
                 * it is fine to send another subscription request. A valid use case  
                 * for this is changing the maximum QoS of the subscription. */  
                xStatus = MQTT_Subscribe( &globalMqttContext,  
                                          pxSubscribeInfo,  
                                          pxCommand->pxCmdContext->ulSubscriptionCount,  
                                          usPacketId );  
            }  
            else  
            {  
                xStatus = MQTT_Unsubscribe( &globalMqttContext,  
                                            pxSubscribeInfo,  
                                            pxCommand->pxCmdContext->ulSubscriptionCount,  
                                            usPacketId );  
            }  
  
            pxCommand->pxCmdContext->xReturnStatus = xStatus;  
            xAddAckToList = ( xStatus == MQTTSuccess );  
            break;  
  
        case PING:  
            xStatus = MQTT_Ping( &globalMqttContext );  
  
            if( pxCommand->pxCmdContext != NULL )  
            {  
                pxCommand->pxCmdContext->xReturnStatus = xStatus;  
            }  
            break;  
  
        case DISCONNECT:  
            xStatus = MQTT_Disconnect( &globalMqttContext );  
  
            if( pxCommand->pxCmdContext != NULL )  
            {  
                pxCommand->pxCmdContext->xReturnStatus = xStatus;  
            }  
            break;  
  
        case RECONNECT:  
            /* Reconnect TCP. */  
            xNetworkResult = prvSocketDisconnect( &xNetworkContext );  
            configASSERT( xNetworkResult == pdPASS );  
            xNetworkResult = prvSocketConnect( &xNetworkContext );  
            configASSERT( xNetworkResult == pdPASS );  

            /* MQTT Connect with a persistent session. */  
            xStatus = prvMQTTConnect( &globalMqttContext, false );  
            break;  
  
        case TERMINATE:  
            LogInfo( ( "Terminating command loop." ) );  
  
        default:  
            break;  
    }  
  
    if( xAddAckToList )  
    {  
        xAckAdded = prvAddAwaitingOperation( usPacketId, pxCommand );  
  
        /* Set the return status if no memory was available to store the operation  
         * information. */  
        if( !xAckAdded )  
        {  
            LogError( ( "No memory to wait for acknowledgment for packet %u\n", usPacketId ) );  
  
            /* All operations that can wait for acks (publish, subscribe, unsubscribe)  
             * require a context. */  
            configASSERT( pxCommand->pxCmdContext != NULL );  
            pxCommand->pxCmdContext->xReturnStatus = MQTTNoMemory;  
        }  
    }  
  
    if( !xAckAdded )  
    {  
        /* The command is complete, call the callback. */  
        if( pxCommand->vCallback != NULL )  
        {  
            pxCommand->vCallback( pxCommand->pxCmdContext );  
        }  
    }  
  
    /* Run a single iteration of the process loop if there were no errors and  
     * the MQTT connection still exists. */  
    if( ( xStatus == MQTTSuccess ) && ( globalMqttContext.connectStatus == MQTTConnected ) )  
    {  
        xStatus = MQTT_ProcessLoop( &globalMqttContext, mqttexamplePROCESS_LOOP_TIMEOUT_MS );  
    }  
  
    return xStatus;  
}  

```


## 同步发布者任务

同步发布者任务同步创建 '`PUBLISH`' 操作， 
在调度下一个操作之前等待每个操作完成。此演示使用 QoS 1 发布消息，这意味着在收到发布确认包之前， 
这些操作不被视为完成。 

```c
void prvSyncPublishTask( void * pvParameters )  
{  
    ( void ) pvParameters;  
    Command_t xCommand;  
    MQTTPublishInfo_t xPublishInfo = { 0 };  
    char payloadBuf[ mqttexampleDEMO_BUFFER_SIZE ];  
    char topicBuf[ mqttexampleDEMO_BUFFER_SIZE ];  
    CommandContext_t xContext;  
    uint32_t ulNotification = 0U;  
    BaseType_t xCommandAdded = pdTRUE;  

    /* We use QoS 1 so that the operation won't be counted as complete until we  
     * receive the publish acknowledgment. */  
    xPublishInfo.qos = MQTTQoS1;  
    xPublishInfo.pTopicName = topicBuf;  
    xPublishInfo.pPayload = payloadBuf;  
  
    /* Synchronous publishes. In case mqttexamplePUBLISH_COUNT is odd, round up. */  
    for( int i = 0; i < ( ( mqttexamplePUBLISH_COUNT + 1 ) / 2 ); i++ )  
    {  
        snprintf( payloadBuf, mqttexampleDEMO_BUFFER_SIZE, mqttexamplePUBLISH_PAYLOAD_FORMAT, "Sync", i + 1 );  
        xPublishInfo.payloadLength = ( uint16_t ) strlen( payloadBuf );  
        snprintf( topicBuf, mqttexampleDEMO_BUFFER_SIZE, mqttexamplePUBLISH_TOPIC_FORMAT_STRING, "sync", i + 1 );  
        xPublishInfo.topicNameLength = ( uint16_t ) strlen( topicBuf );  
  
        memset( ( void * ) &xContext, 0x00, sizeof( &xContext ) );  
        xContext.xTaskToNotify = xTaskGetCurrentTaskHandle();  
        xContext.ulNotificationBit = 1 << i;  
        xContext.pxPublishInfo = &xPublishInfo;  
        LogInfo( ( "Adding publish operation for message %s \non topic %.*s", payloadBuf, xPublishInfo.topicNameLength, xPublishInfo.pTopicName ) );  
        prvCreateCommand( PUBLISH, &xContext, prvCommandCallback, &xCommand );  
        xCommandAdded = prvAddCommandToQueue( &xCommand );  
        /* Ensure command was added to queue. */  
        configASSERT( xCommandAdded == pdTRUE );  
        LogInfo( ( "Waiting for publish %d to complete.", i + 1 ) );  
  
        if( prvNotificationWaitLoop( &ulNotification, ( 1U << i ), true ) != true )  
        {  
            LogError( ( "Synchronous publish loop iteration %d"  
                        " exceeded maximum wait time.\n", ( i + 1 ) ) );  
        }  
  
        configASSERT( ( ulNotification & ( 1U << i ) ) == ( 1U << i ) );  
  
        LogInfo( ( "Publish operation complete. Sleeping for %d ms.\n", mqttexamplePUBLISH_DELAY_SYNC_MS ) );  
        vTaskDelay( pdMS_TO_TICKS( mqttexamplePUBLISH_DELAY_SYNC_MS ) );  
    }  
  
    LogInfo( ( "Finished sync publishes.\n" ) );  
  
    /* Clear this task's notifications. */  
    xTaskNotifyStateClear( NULL );  
    ulNotification = ulTaskNotifyValueClear( NULL, ~( 0U ) );  
  
    /* Notify main task this task has completed. */  
    xTaskNotify( xMainTask, mqttexamplePUBLISHER_SYNC_COMPLETE_BIT, eSetBits );  
  
    /* Delete this task. */  
    LogInfo( ( "Deleting Sync Publisher task." ) );  
    vTaskDelete( NULL );  
}  

```


## 异步发布者任务

异步发布者不会等待一个发布完成再排队下一个发布。这意味着 
一个任务无需等待 MQTT 操作完成后再恢复执行。相反， 
它只在必要时等待。因为每条发布命令都需要有自己的上下文结构体，该任务无法像同步发布者任务那样重复使用一个上下文结构体， 
因为之前的命令可能还需要它。因此，它为每个 
上下文结构体分配内存，然后在所有要发布的消息排队后等待释放所有分配的内存。

```c
void prvAsyncPublishTask( void * pvParameters )  
{  
    ( void ) pvParameters;  
    Command_t xCommand;  
    MQTTPublishInfo_t pxPublishes[ mqttexamplePUBLISH_COUNT / 2 ];  
    uint32_t ulNotification = 0U;  
    uint32_t ulExpectedNotifications = 0U;  
    BaseType_t xCommandAdded = pdTRUE;  

    /* The following arrays are used to hold pointers to dynamically allocated memory. */  
    char * payloadBuffers[ mqttexamplePUBLISH_COUNT / 2 ];  
    char * topicBuffers[ mqttexamplePUBLISH_COUNT / 2 ];  
    CommandContext_t * pxContexts[ mqttexamplePUBLISH_COUNT / 2 ] = { 0 };  
  
    /* Add a delay. The main task will not be sending publishes for this interval  
     * anyway, as we want to give the broker ample time to process the  
     * subscription. */  
    vTaskDelay( mqttexampleSUBSCRIBE_TASK_DELAY_MS );  
  
    /* Asynchronous publishes. Although not necessary, we use dynamic  
     * memory here to avoid declaring many static buffers. */  
    for( int i = 0; i < mqttexamplePUBLISH_COUNT / 2; i++ )  
    {  
        pxContexts[ i ] = ( CommandContext_t * ) pvPortMalloc( sizeof( CommandContext_t ) );  
        memset( ( void * ) pxContexts[ i ], 0x00, sizeof( CommandContext_t ) );  
        pxContexts[ i ]->xTaskToNotify = xTaskGetCurrentTaskHandle();  
  
        /* Set the notification bit to be the publish number. This prevents this demo  
         * from having more than 32 publishes. If many publishes are desired, semaphores  
         * can be used instead of task notifications. */  
        pxContexts[ i ]->ulNotificationBit = 1U << i;  
        ulExpectedNotifications |= 1U << i;  
        payloadBuffers[ i ] = ( char * ) pvPortMalloc( mqttexampleDYNAMIC_BUFFER_SIZE );  
        topicBuffers[ i ] = ( char * ) pvPortMalloc( mqttexampleDYNAMIC_BUFFER_SIZE );  
        snprintf( payloadBuffers[ i ], mqttexampleDYNAMIC_BUFFER_SIZE, mqttexamplePUBLISH_PAYLOAD_FORMAT, "Async", i + 1 );  
        snprintf( topicBuffers[ i ], mqttexampleDYNAMIC_BUFFER_SIZE, mqttexamplePUBLISH_TOPIC_FORMAT_STRING, "async", i + 1 );  

        /* Set publish info. */  
        memset( &( pxPublishes[ i ] ), 0x00, sizeof( MQTTPublishInfo_t ) );  
        pxPublishes[ i ].pPayload = payloadBuffers[ i ];  
        pxPublishes[ i ].payloadLength = strlen( payloadBuffers[ i ] );  
        pxPublishes[ i ].pTopicName = topicBuffers[ i ];  
        pxPublishes[ i ].topicNameLength = ( uint16_t ) strlen( topicBuffers[ i ] );  
        pxPublishes[ i ].qos = MQTTQoS1;  
        pxContexts[ i ]->pxPublishInfo = &( pxPublishes[ i ] );  
        LogInfo( ( "Adding publish operation for message %s \non topic %.*s",  
                   payloadBuffers[ i ],  
                   pxPublishes[ i ].topicNameLength,  
                   pxPublishes[ i ].pTopicName ) );  
        prvCreateCommand( PUBLISH, pxContexts[ i ], prvCommandCallback, &xCommand );  
        xCommandAdded = prvAddCommandToQueue( &xCommand );  

        /* Ensure command was added to queue. */  
        configASSERT( xCommandAdded == pdTRUE );  

        /* Short delay so we do not bombard the broker with publishes. */  
        LogInfo( ( "Publish operation queued. Sleeping for %d ms.\n", mqttexamplePUBLISH_DELAY_ASYNC_MS ) );  
        vTaskDelay( pdMS_TO_TICKS( mqttexamplePUBLISH_DELAY_ASYNC_MS ) );  
    }  
  
    LogInfo( ( "Finished async publishes.\n" ) );  
  
    /* Receive all task notifications. We may receive notifications in a  
     * different order, so we have two loops. If all notifications have been  
     * received, we can break early. */  
    ( void ) prvNotificationWaitLoop( &ulNotification, ulExpectedNotifications, false );  
  
    for( int i = 0; i < mqttexamplePUBLISH_COUNT / 2; i++ )  
    {  
        configASSERT( ( ulNotification & ( 1U << i ) ) == ( 1U << i ) );  
  
        LogInfo( ( "Freeing publish context %d.", i + 1 ) );  
        vPortFree( pxContexts[ i ] );  
        vPortFree( topicBuffers[ i ] );  
        vPortFree( payloadBuffers[ i ] );  
        LogInfo( ( "Publish context %d freed.", i + 1 ) );  
        pxContexts[ i ] = NULL;  
    }  
  
    /* Clear this task's notifications. */  
    xTaskNotifyStateClear( NULL );  
    ulNotification = ulTaskNotifyValueClear( NULL, ~( 0U ) );  
  
    /* Notify main task this task has completed. */  
    xTaskNotify( xMainTask, mqttexamplePUBLISHER_ASYNC_COMPLETE_BIT, eSetBits );  
  
    /* Delete this task. */  
    LogInfo( ( "Deleting Async Publisher task." ) );  
    vTaskDelete( NULL );  
}  

```


## 订阅者任务

此任务订阅了一个主题过滤器， 
该过滤器与同步和异步任务发布的消息的所有主题相匹配。然后，它会在取消订阅之前等待接收所有这些已发布的消息。此任务也 
负责创建 '`TERMINATE`' 操作，该操作向主任务发出结束命令循环的信号。

```c
void prvSubscribeTask( void * pvParameters )  
{  
    ( void ) pvParameters;  
    MQTTSubscribeInfo_t xSubscribeInfo;  
    Command_t xCommand;  
    BaseType_t xCommandAdded = pdTRUE;  
    MQTTPublishInfo_t * pxReceivedPublish = NULL;  
    uint16_t usNumReceived = 0;  
    uint32_t ulNotification = 0;  
    CommandContext_t xContext;  
    PublishElement_t xReceivedPublish;  
    uint32_t ulWaitCounter = 0;  
  
    /* The QoS does not affect when subscribe operations are marked completed  
     * as it does for publishes. However, we still use QoS 1 here so that the  
     * broker will resend publishes if there is a network disconnect. */  
    xSubscribeInfo.qos = MQTTQoS1;  
    xSubscribeInfo.pTopicFilter = mqttexampleSUBSCRIBE_TOPIC_FILTER;  
    xSubscribeInfo.topicFilterLength = ( uint16_t ) strlen( xSubscribeInfo.pTopicFilter );  
    LogInfo( ( "Topic filter: %.*s", xSubscribeInfo.topicFilterLength, xSubscribeInfo.pTopicFilter ) );  
  
    /* Create the context and subscribe command. */  
    memset( &xContext, 0x00, sizeof( xContext ) );  
    xContext.pxResponseQueue = xSubscriberResponseQueue;  
    xContext.xTaskToNotify = xTaskGetCurrentTaskHandle();  
    xContext.ulNotificationBit = mqttexampleSUBSCRIBE_COMPLETE_BIT;  
    xContext.pxSubscribeInfo = &xSubscribeInfo;  
    xContext.ulSubscriptionCount = 1;  
    LogInfo( ( "Adding subscribe operation" ) );  
    prvCreateCommand( SUBSCRIBE, &xContext, prvCommandCallback, &xCommand );  
    xCommandAdded = prvAddCommandToQueue( &xCommand );  

    /* Ensure command was added to queue. */  
    configASSERT( xCommandAdded == pdTRUE );  

    /* This demo relies on the server processing our subscription before any publishes.  
     * Since this demo uses multiple tasks, we do not retry failed subscriptions, as the  
     * server has likely already processed our first publish, and so this demo will not  
     * complete successfully. */  
    LogInfo( ( "Waiting for subscribe operation to complete." ) );  
    ( void ) prvNotificationWaitLoop( &ulNotification, mqttexampleSUBSCRIBE_COMPLETE_BIT, true );  
  
    configASSERT( ( ulNotification & mqttexampleSUBSCRIBE_COMPLETE_BIT ) == mqttexampleSUBSCRIBE_COMPLETE_BIT );  
    configASSERT( xContext.xReturnStatus == MQTTSuccess );  

    LogInfo( ( "Operation wait complete.\n" ) );  

    for( ; ; )  
    {  
        /* It is possible that there is nothing to receive from the queue, and  
         * this is expected, as there are delays between each publish. For this  
         * reason, we keep track of the number of publishes received, and break  
         * from the outermost while loop when we have received all of them. If  
         * the queue is empty, we add a delay before checking it again. */  
        while( xQueueReceive( xSubscriberResponseQueue, &xReceivedPublish, mqttexampleDEMO_TICKS_TO_WAIT ) != pdFALSE )  
        {  
            pxReceivedPublish = &( xReceivedPublish.xPublishInfo );  
            pxReceivedPublish->pTopicName = ( const char * ) xReceivedPublish.pcTopicNameBuf;  
            pxReceivedPublish->pPayload = xReceivedPublish.pcPayloadBuf;  
            LogInfo( ( "Received publish on topic %.*s\nMessage payload: %.*s\n",  
                       pxReceivedPublish->topicNameLength,  
                       pxReceivedPublish->pTopicName,  
                       ( int ) pxReceivedPublish->payloadLength,  
                       ( const char * ) pxReceivedPublish->pPayload ) );  
            usNumReceived++;  

            /* Reset the wait counter every time a publish is received. */  
            ulWaitCounter = 0;  
        }  

        /* Since this is an infinite loop, we want to break if all publishes have  
         * been received. */  
        if( usNumReceived >= mqttexamplePUBLISH_COUNT )  
        {  
            break;  

        }  

        /* Break if we have been stuck in this loop for too long. The total wait  
         * here will be ( (loop delay + queue check delay) * `mqttexampleMAX_WAIT_ITERATIONS` ).  
         * For example, with a 1000 ms queue delay, a 400 ms loop delay, and a  
         * maximum iteration of 20, this will wait 28 seconds after receiving  
         * the last publish. */  
        if( ++ulWaitCounter > mqttexampleMAX_WAIT_ITERATIONS )  
        {  
            LogError( ( "Publish receive loop exceeded maximum wait time.\n" ) );  
            break;  
        }  

  
        /* Delay a bit to give more time for publish messages to be received. */  
        LogInfo( ( "No messages queued, received %u publish%s, sleeping for %d ms\n",  
                   usNumReceived,  
                   ( usNumReceived == 1 ) ? "" : "es",  
                   mqttexampleSUBSCRIBE_TASK_DELAY_MS ) );  
        vTaskDelay( pdMS_TO_TICKS( mqttexampleSUBSCRIBE_TASK_DELAY_MS ) );  
    }  
  
    LogInfo( ( "Finished receiving\n" ) );  
    prvCreateCommand( UNSUBSCRIBE, &xContext, prvCommandCallback, &xCommand );  
    memset( &xContext, 0x00, sizeof( xContext ) );  
    xContext.pxResponseQueue = xSubscriberResponseQueue;  
    xContext.xTaskToNotify = xTaskGetCurrentTaskHandle();  
    xContext.ulNotificationBit = mqttexampleUNSUBSCRIBE_COMPLETE_BIT;  
    xContext.pxSubscribeInfo = &xSubscribeInfo;  
    xContext.ulSubscriptionCount = 1;  
    LogInfo( ( "Adding unsubscribe operation\n" ) );  
    xCommandAdded = prvAddCommandToQueue( &xCommand );  

    /* Ensure command was added to queue. */  
    configASSERT( xCommandAdded == pdTRUE );  


    LogInfo( ( "Waiting for unsubscribe operation to complete." ) );  
    ( void ) prvNotificationWaitLoop( &ulNotification, mqttexampleUNSUBSCRIBE_COMPLETE_BIT, true );  

    configASSERT( ( ulNotification & mqttexampleUNSUBSCRIBE_COMPLETE_BIT ) == mqttexampleUNSUBSCRIBE_COMPLETE_BIT );  
    LogInfo( ( "Operation wait complete.\n" ) );  


    /* Create command to stop command loop. */  
    LogInfo( ( "Beginning command queue termination." ) );  
    prvCreateCommand( TERMINATE, NULL, NULL, &xCommand );  
    xCommandAdded = prvAddCommandToQueue( &xCommand );  

    /* Ensure command was added to queue. */  
    configASSERT( xCommandAdded == pdTRUE );  

    /* Notify main task this task has completed. */  
    xTaskNotify( xMainTask, mqttexampleSUBSCRIBE_TASK_COMPLETE_BIT, eSetBits );  

    /* Delete this task. */  
    LogInfo( ( "Deleting Subscriber task." ) );  
    vTaskDelete( NULL );  
}  

```

