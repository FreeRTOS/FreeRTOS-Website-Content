---
title: 为什么要编写另一个 MQTT 库？
date: null
feature: blog
categories:
- 长期支持
authors:
- gooddan
relatedLinks:
- title: FreeRTOS 简介
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Dan Good](../author/gooddan) 发表于 2021 年 3 月 8 日

库记录了关于世界如何运作的一系列决策。如果幸运的话， 
您可以在库中找到符合自己需求和限制条件的模型。如果不够幸运， 
最终找到的模型可能毫无用处或需要修改，或者您必须搜索其他 
更合适的库。无论是哪种不幸的结果，您都需要为此付出代价，要么增加开发工作量，要么提高最终的材料成本， 
要么在产品发布后处理严重错误。如果我们这些库作者 
将决策权交给您，您可以根据自己的需求使用库， 
减少不必要的投入或浪费。

FreeRTOS 的 [LTS 版本](../../lts-libraries) 包含为满足物联网和嵌入式设备不断变化的需求 
而打造的库。其中最主要的是 [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)， 
该库为其他核心库设定了标准，并将决策权交给您。

举个具体的例子，直接依赖基于软件的 TLS 的 MQTT 库 
可能不适合具有固有 TCP 和 TLS 功能的蜂窝模块。随着 
设备连接到云端的方式越来越多，供应商提供的模块种类也越来越多， 
选择范围多种多样，从普通到特别，应有尽有，包括 802.11 Wi-Fi、802.15.4 6LoWPAN、LTE-M、NB-IoT 
和 LoRa。其中许多模块卸载了网络功能，并提供 AT 命令进行控制， 
这些命令可能由 socket 库封装 。将网络功能与 coreMQTT 解耦意味着 
无论底层传输方式如何，coreMQTT 都可能同样有用。

[coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) 实现了支持所有 [QoS 级别](../../mqtt/mqtt_terminology) 的 MQTT 3.1.1 客户端， 
受 MIT 开源许可证保护，并符合 ISO C90 和 MISRA C:2012。该库强调 
占用空间小、无依赖性和可组合性。该库不使用堆内存，因此适用于仅使用静态分配的应用程序， 
还可提供内存安全证明。


## 读写接口

coreMQTT 库可通过读取函数和写入函数与网络交互。 
您需要向该库提供这些函数，或使用/改编随演示提供的示例，该示例涵盖 
常见场景，诸如使用 mbedTLS 进行基于 TLS 的双向认证；或者 
如 [FreeRTOS 蜂窝演示](../../cellular-demo) 中那样，封装卸载模块提供的函数；抑或实现一种新颖的方法， 
例如与智能手机配对的低功耗蓝牙代理。您甚至可以 
在同一应用程序中使用多种连接。

为了实现这种灵活性，您需要为每个 MQTT 连接提供用于在结构体中读写的函数指针 
以及表示网络上下文的不透明指针。我们称之为传输 
接口。这与传统的平台抽象层方法不同，在传统方法中， 
库需要一组（通常很多）固定函数和数据类型，您必须实现 
且无差别地使用这些函数和数据类型。coreMQTT 所体现的前提是，小型接口比大型接口更有用， 
可以解决更多问题，并且可以更广泛地共享。我们 
与 [coreHTTP](../../http/index) 库共享[传输接口](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface)。下方 
文档字符串描述了构成传输接口的类型。

```c
/**  
 * NetworkContext_t is the incomplete type struct NetworkContext.  
 * The implemented struct NetworkContext must contain all of the information  
 * that is needed to receive and send data with the TransportRecv_t  
 * and the TransportSend_t implementations.  
 * In the case of TLS over TCP, struct NetworkContext is typically implemented  
 * with the TCP socket context and a TLS context.  
 *  
 * Example code:  
 *  
 * struct NetworkContext  
 * {  
 * struct MyTCPSocketContext tcpSocketContext;  
 * struct MyTLSContext tlsContext;  
 * };  
 */  

/**  
 * @brief Transport interface for receiving data on the network.  
 *  
 * This function is expected to populate a buffer, with bytes received from the  
 * transport, and return the number of bytes placed in the buffer.  
 * In the case of TLS over TCP, TransportRecv_t is typically implemented by  
 * calling the TLS layer function to receive data. In case of plaintext TCP  
 * without TLS, it is typically implemented by calling the TCP layer receive  
 * function. TransportRecv_t may be invoked multiple times by the protocol  
 * library, if fewer bytes than were requested to receive are returned.  
 *  
 * @param[in] pNetworkContext Implementation-defined network context.  
 * @param[out] pBuffer Buffer to receive the data into.  
 * @param[in] bytesToRecv Number of bytes requested from the network.  
 *  
 * @return The number of bytes received or a negative value to indicate  
 * error.  
 */  

typedef int32_t ( * TransportRecv_t )( NetworkContext_t * pNetworkContext,  
                                       void * pBuffer,  
                                       size_t bytesToRecv );  

/**  
 * @brief Transport interface for sending data over the network.  
 *  
 * This function is expected to send the bytes in the given buffer over the  
 * transport, and return the number of bytes sent.  
 * In the case of TLS over TCP, TransportSend_t is typically implemented by  
 * calling the TLS layer function to send data. In case of plaintext TCP  
 * without TLS, it is typically implemented by calling the TCP layer send  
 * function. TransportSend_t may be invoked multiple times by the protocol  
 * library, if fewer bytes than were requested to send are returned.  
 *  
 * @param[in] pNetworkContext Implementation-defined network context.  
 * @param[in] pBuffer Buffer containing the bytes to send over the network stack.  
 * @param[in] bytesToSend Number of bytes to send over the network.  
 *  
 * @return The number of bytes sent or a negative value to indicate error.  
 */  

typedef int32_t ( * TransportSend_t )( NetworkContext_t * pNetworkContext,  
                                       const void * pBuffer,  
                                       size_t bytesToSend );  

typedef struct TransportInterface  
{  
    TransportRecv_t recv;               /**&lt; Transport receive interface. */  
    TransportSend_t send;               /**&lt; Transport send interface. */  
    NetworkContext_t * pNetworkContext; /**&lt; Implementation-defined network context. */  
} TransportInterface_t;  
```

## 使用退避算法进行连接

创建连接的方式由您和您的应用程序自行决定。 
这有助于保持库的简洁和接口的小巧。请注意连接重试时的 
潜在陷阱。过于简单的重试，如果来自大量设备，可能实际上会构成拒绝服务攻击， 
也可能由于服务限制而导致意外故障模式。为了降低这种风险，FreeRTOS 
提供了 [backoffAlgorithm 库](../../backoff-algorithm)，  根据带有抖动的上限指数值来计算 
重试之间的延迟。此演示代码展示了如何利用 
OpenSSL 和 backoffAlgorithm 库建立连接。请注意， 
[BackoffAlgorithm_GetNextBackoff()](https://github.com/FreeRTOS/backoffAlgorithm/blob/a70291444c556bc3392bf9b7b60626b93b120319/source/backoff_algorithm.c#L38) 
本身并不调用任何休眠函数。您可以直接使用返回的值调用休眠函数。

```c
/* Initialize reconnect attempts and interval. */  
BackoffAlgorithm_InitializeParams( &reconnectParams,  
                                   CONNECTION_RETRY_BACKOFF_BASE_MS,  
                                   CONNECTION_RETRY_MAX_BACKOFF_DELAY_MS,  
                                   CONNECTION_RETRY_MAX_ATTEMPTS );  

/* Attempt to connect to MQTT broker. If connection fails, retry after  
 * a timeout until maximum attempts are reached.  
 */  
do  
{  
    LogInfo( ( "Establishing a TLS session to %.*s:%d.",  
               BROKER_ENDPOINT_LENGTH,  
               BROKER_ENDPOINT,  
               BROKER_PORT ) );  

    opensslStatus = Openssl_Connect( pNetworkContext,  
                                     &serverInfo,  
                                     &opensslCredentials,  
                                     TRANSPORT_SEND_RECV_TIMEOUT_MS,  
                                     TRANSPORT_SEND_RECV_TIMEOUT_MS );  

    if( opensslStatus != OPENSSL_SUCCESS )  
    {  
        /* Generate a random number and get back-off value (in milliseconds) for the next connection retry. */  
        backoffAlgStatus = BackoffAlgorithm_GetNextBackoff( &reconnectParams, generateRandomNumber(), &nextRetryBackOff );  

        if( backoffAlgStatus == BackoffAlgorithmRetriesExhausted )  
        {  
            LogError( ( "Connection to the broker failed, all attempts exhausted." ) );  
            returnStatus = EXIT_FAILURE;  
        }  
        else if( backoffAlgStatus == BackoffAlgorithmSuccess )  
        {  
            LogWarn( ( "Connection to the broker failed. Retrying connection "  
                       "after %hu ms backoff.",  
                       ( unsigned short ) nextRetryBackOff ) );  
            Clock_SleepMs( nextRetryBackOff );  
        }  
    }  
} while( ( opensslStatus != OPENSSL_SUCCESS ) && ( backoffAlgStatus == BackoffAlgorithmSuccess ) );  
```


## 可组合性

可组合性是 coreMQTT 设计的核心原则。这一设计原则意味着功能以小件的形式存在， 
这些小件可组成更丰富的功能。coreMQTT 库既具有丰富的功能， 
也提供用于实现这些功能的部件。您可以按原样使用某功能，也可以重新组合这些部件以实现自定义行为 ， 
还可以添加自己的部件以实现更多可能性。

例如，由 MQTT_Publish() 函数执行的序列化分别在 
MQTT_GetPublishPacketSize() 和 MQTT_SerializePublishHeader() 函数中可用。有关这些 
小型序列化和反序列化函数的替代组合， 
请查看[超轻量级 MQTT 客户端演示](https://github.com/aws/aws-iot-device-sdk-embedded-C/tree/main/demos/mqtt/mqtt_demo_serializer)。 
虽然功能齐全的 MQTT_Publish() 函数可与状态引擎交互，支持 QoS 1 和 QoS 2， 
但超轻量级演示仅支持 QoS 0 ，无需会话或状态引擎。 
超轻量级演示中的 publish 函数显示了序列化函数的实际应用。 
MQTT_GetPublishPacketSize() 返回序列化消息标头所需的字节数。 
如果该数字小于所提供缓冲区的大小，则 MQTT_SerializePublishHeader() 
会将标头写入缓冲区。两次调用使用传输接口先发送标头，再发送 
有效负载。

```c
static void mqttPublishToTopic( NetworkContext_t * pNetworkContext,  
                                MQTTFixedBuffer_t * pFixedBuffer )  
{  
    MQTTStatus_t result;  
    MQTTPublishInfo_t mqttPublishInfo;  
    size_t remainingLength;  
    size_t packetSize = 0;  
    size_t headerSize = 0;  
    int status;  
  
    /* Suppress unused variable warnings when asserts are disabled in build. */  
    ( void ) status;  
    ( void ) result;  

    /***  
     * For readability, error handling in this function is restricted to the use of  
     * asserts().  
     ***/  

    /* Some fields not used by this demo so start with everything as 0. */  
    memset( ( void * ) &mqttPublishInfo, 0x00, sizeof( mqttPublishInfo ) );  

    /* This demo uses QOS0 */  
    mqttPublishInfo.qos = MQTTQoS0;  
    mqttPublishInfo.retain = false;  
    mqttPublishInfo.pTopicName = MQTT_EXAMPLE_TOPIC;  
    mqttPublishInfo.topicNameLength = ( uint16_t ) strlen( MQTT_EXAMPLE_TOPIC );  
    mqttPublishInfo.pPayload = MQTT_EXAMPLE_MESSAGE;  
    mqttPublishInfo.payloadLength = strlen( MQTT_EXAMPLE_MESSAGE );  

    /* Find out length of Publish packet size. */  
    result = MQTT_GetPublishPacketSize( &mqttPublishInfo, &remainingLength, &packetSize );  
    assert( result == MQTTSuccess );  

    /* Make sure the packet size is less than static buffer size. */  
    assert( packetSize < pFixedBuffer->size );  

    /* Serialize MQTT Publish packet header. The publish message payload will  
     * be sent directly in order to avoid copying it into the buffer.  
     * QOS0 does not make use of packet identifier, therefore value of 0 is used */  
    result = MQTT_SerializePublishHeader( &mqttPublishInfo,  
                                          0,  
                                          remainingLength,  
                                          pFixedBuffer,  
                                          &headerSize );  

    LogDebug( ( "Serialized PUBLISH header size is %lu.",  
                ( unsigned long ) headerSize ) );  
    assert( result == MQTTSuccess );  

    /* Send Publish header to the broker. */  
    status = Plaintext_Send( pNetworkContext, ( void * ) pFixedBuffer->pBuffer, headerSize );  
    assert( status == ( int ) headerSize );  

    /* Send Publish payload to the broker */  
    status = Plaintext_Send( pNetworkContext, ( void * ) mqttPublishInfo.pPayload, mqttPublishInfo.payloadLength );  
    assert( status == ( int ) mqttPublishInfo.payloadLength );  
}  
```


## 处理收到的消息

应用程序需要做出许多重大决策，其中一项是如何处理新收到的消息。 
您可能会采用简单的工作流程，只需要处理一种类型的消息；您还有可能采用更复杂的方法， 
需要在整个应用程序中对多种消息进行多路复用。coreMQTT 从简单情况入手， 
MQTT_Init() 接受单个回调函数，用于在每次接收到 PUBLISH 或 ACK 消息时调用。 
MQTTEventCallback_t 类型和 MQTT_Init() 函数的文档字符串描述了传递给回调的值， 
并举例说明如何调用 MQTT_Init()。

```c
/**  
 * @ingroup mqtt_callback_types  
 * @brief Application callback for receiving incoming publishes and incoming  
 * acks.  
 *  
 * @note This callback will be called only if packets are deserialized with a  
 * result of #MQTTSuccess or #MQTTServerRefused. The latter can be obtained  
 * when deserializing a SUBACK, indicating a broker's rejection of a subscribe.  
 *  
 * @param[in] pContext Initialized MQTT context.  
 * @param[in] pPacketInfo Information on the type of incoming MQTT packet.  
 * @param[in] pDeserializedInfo Deserialized information from incoming packet.  
 */  

typedef void (* MQTTEventCallback_t )( struct MQTTContext * pContext,  
                                       struct MQTTPacketInfo * pPacketInfo,  
                                       struct MQTTDeserializedInfo * pDeserializedInfo );  

/**  
 * @brief Initialize an MQTT context.  
 *  
 * This function must be called on a #MQTTContext_t before any other function.  
 *  
 * @note The #MQTTGetCurrentTimeFunc_t function for querying time must be defined. If  
 * there is no time implementation, it is the responsibility of the application  
 * to provide a dummy function to always return 0, provide 0 timeouts for  
 * all calls to #MQTT_Connect, #MQTT_ProcessLoop, and #MQTT_ReceiveLoop and configure  
 * the #MQTT_RECV_POLLING_TIMEOUT_MS and #MQTT_SEND_RETRY_TIMEOUT_MS configurations  
 * to be 0. This will result in loop functions running for a single iteration, and  
 * #MQTT_Connect relying on #MQTT_MAX_CONNACK_RECEIVE_RETRY_COUNT to receive the CONNACK packet.  
 *  
 * @param[in] pContext The context to initialize.  
 * @param[in] pTransportInterface The transport interface to use with the context.  
 * @param[in] getTimeFunction The time utility function to use with the context.  
 * @param[in] userCallback The user callback to use with the context to  
 * notify about incoming packet events.  
 * @param[in] pNetworkBuffer Network buffer provided for the context.  
 *  
 * @return #MQTTBadParameter if invalid parameters are passed;  
 * #MQTTSuccess otherwise.  
 *  
 * Example  
 *  
 * // Function for obtaining a timestamp.  
 * uint32_t getTimeStampMs();  
 * // Callback function for receiving packets.  
 * void eventCallback(  
 * MQTTContext_t * pContext,  
 * MQTTPacketInfo_t * pPacketInfo,  
 * MQTTDeserializedInfo_t * pDeserializedInfo  
 * );  
 * // Network send.  
 * int32_t networkSend( NetworkContext_t * pContext, const void * pBuffer, size_t bytes );  
 * // Network receive.  
 * int32_t networkRecv( NetworkContext_t * pContext, void * pBuffer, size_t bytes );  
 *  
 * MQTTContext_t mqttContext;  
 * TransportInterface_t transport;  
 * MQTTFixedBuffer_t fixedBuffer;  
 * uint8_t buffer[ 1024 ];  
 *  
 * // Clear context.  
 * memset( ( void * ) &mqttContext, 0x00, sizeof( MQTTContext_t ) );  
 *  
 * // Set transport interface members.  
 * transport.pNetworkContext = &someTransportContext;  
 * transport.send = networkSend;  
 * transport.recv = networkRecv;  
 *  
 * // Set buffer members.  
 * fixedBuffer.pBuffer = buffer;  
 * fixedBuffer.size = 1024;  
 *  
 * status = MQTT_Init( &mqttContext, &transport, getTimeStampMs, eventCallback, &fixedBuffer );  
 *  
 * if( status == MQTTSuccess )  
 * {  
 * // Do something with mqttContext. The transport and fixedBuffer structs were  
 * // copied into the context, so the original structs do not need to stay in scope.  
 * }  
 */  

MQTTStatus_t MQTT_Init( MQTTContext_t * pContext,  
                        const TransportInterface_t * pTransportInterface,  
                        MQTTGetCurrentTimeFunc_t getTimeFunction,  
                        MQTTEventCallback_t userCallback,  
                        const MQTTFixedBuffer_t * pNetworkBuffer );  
```

非常简单的回调可能会忽略所有 ACK 消息并解析所有 PUBLISH 消息，以获得所需值。如果 
需要根据主题由不同的函数处理消息，请使用 
MQTT_MatchTopic() 函数来组成回调。下方 MQTT_MatchTopic() 文档字符串包括一个简单的示例。

```c
/**  
 * @brief A utility function that determines whether the passed topic filter and  
 * topic name match according to the MQTT 3.1.1 protocol specification.  
 *  
 * @param[in] pTopicName The topic name to check.  
 * @param[in] topicNameLength Length of the topic name.  
 * @param[in] pTopicFilter The topic filter to check.  
 * @param[in] topicFilterLength Length of topic filter.  
 * @param[out] pIsMatch This is filled with the whether there  
 * exists a match or not.  
 *  
 * @note The API assumes that the passed topic name is valid to meet the  
 * requirements of the MQTT 3.1.1 specification. Invalid topic names (for example,  
 * containing wildcard characters) should not be passed to the function.  
 * Also, the API checks validity of topic filter for wildcard characters ONLY if  
 * the passed topic name and topic filter do not have an exact string match.  
 *  
 * @return Returns one of the following:  
 * - #MQTTBadParameter, if any of the input parameters is invalid.  
 * - #MQTTSuccess, if the matching operation was performed.  
 *  
 * Example  
 *  
 * // Variables used in this example.  
 * const char * pTopic = "topic/match/1";  
 * const char * pFilter = "topic/#";  
 * MQTTStatus_t status = MQTTSuccess;  
 * bool match = false;  
 *  
 * status = MQTT_MatchTopic( pTopic, strlen( pTopic ), pFilter, strlen( pFilter ), &match );  
 * // Our parameters were valid, so this will return success.  
 * assert( status == MQTTSuccess );  
 *  
 * // For this specific example, we already know this value is true. This  
 * // check is placed here as an example for use with variable topic names.  
 * if( match )  
 * {  
 * // Application can decide what to do with the matching topic name.  
 * }  
 */  
MQTTStatus_t MQTT_MatchTopic( const char * pTopicName,  
                              const uint16_t topicNameLength,  
                              const char * pTopicFilter,  
                              const uint16_t topicFilterLength,  
                              bool * pIsMatch );  
```

MQTT_MatchTopic() 可组合，创建功能齐全的订阅管理器， 
如[订阅管理器演示](https://github.com/aws/aws-iot-device-sdk-embedded-C/tree/main/demos/mqtt/mqtt_demo_subscription_manager) 所示。 
下方显示的两个函数、typedef 及其文档字符串描述了如何将回调函数绑定到 
匹配的主题字符串。


```c
/**  
 * @brief Callback type to be registered for a topic filter with the subscription manager.  
 *  
 * For incoming PUBLISH messages received on topics that match the registered topic filter,  
 * the callback would be invoked by the subscription manager.  
 *  
 * @param[in] pContext The context associated with the MQTT connection.  
 * @param[in] pPublishInfo The incoming PUBLISH message information.  
 */  

typedef void (* SubscriptionManagerCallback_t )( MQTTContext_t * pContext,  
                                                 MQTTPublishInfo_t * pPublishInfo );  

/**  
 * @brief Dispatches the incoming PUBLISH message to the callbacks that have their  
 * registered topic filters matching the incoming PUBLISH topic name. The dispatch  
 * handler will invoke all these callbacks with matching topic filters.  
*  
* @param[in] pContext The context associated with the MQTT connection.  
* @param[in] pPublishInfo The incoming PUBLISH message information.  
*/  
void SubscriptionManager_DispatchHandler( MQTTContext_t * pContext,  
                                          MQTTPublishInfo_t * pPublishInfo );  

/**  
 * @brief Utility to register a callback for a topic filter in the subscription manager.  
 *  
 * The callback will be invoked when an incoming PUBLISH message is received on  
 * a topic that matches the topic filter, @a pTopicFilter. The subscription manager  
 * accepts wildcard topic filters.  
 *  
 * @param[in] pTopicFilter The topic filter to register the callback for.  
 * @param[in] topicFilterLength The length of the topic filter string.  
 * @param[in] callback The callback to be registered for the topic filter.  
 *  
 * @note The subscription manager does not allow more than one callback to be registered  
 * for the same topic filter.  
 * @note The passed topic filter, @a pTopicFilter, is saved in the registry.  
 * The application must not free or alter the content of the topic filter memory  
 * until the callback for the topic filter is removed from the subscription manager.  
 *  
 * @return Returns one of the following:  
 * - #SUBSCRIPTION_MANAGER_SUCCESS if registration of the callback is successful.  
 * - #SUBSCRIPTION_MANAGER_REGISTRY_FULL if the registration failed due to registry  
 * being already full.  
 * - #SUBSCRIPTION_MANAGER_RECORD_EXISTS, if a registered callback already exists for  
 * the requested topic filter in the subscription manager.  
 */  
SubscriptionManagerStatus_t SubscriptionManager_RegisterCallback( const char * pTopicFilter,  
                                                                  uint16_t topicFilterLength,  
                                                                  SubscriptionManagerCallback_t pCallback );  
```

演示代码展示了如何结合使用 subscribeToTopic() 函数进行订阅以及 
使用 SubscriptionManager_RegisterCallback() 注册回调。演示中，首先注册回调， 
如果订阅失败则将其删除。此方法涵盖了这样一种情况： 
subscribeToTopic() 调用的 MQTT_ProcessLoop() 函数等待 SUBACK 消息时，消息可能已发布到主题， 
这种情况极有可能发生。

```c
static int subscribeToAndRegisterTopicFilter( MQTTContext_t * pContext,  
                                              const char * pTopicFilter,  
                                              uint16_t topicFilterLength,  
                                              SubscriptionManagerCallback_t callback )  
{  
    int returnStatus = EXIT_SUCCESS;  
    SubscriptionManagerStatus_t managerStatus = 0u;  

    /* Register the topic filter and its callback with subscription manager.  
     * On an incoming PUBLISH message whose topic name that matches the topic filter  
     * being registered, its callback will be invoked. */  
    managerStatus = SubscriptionManager_RegisterCallback( pTopicFilter,  
                                                          topicFilterLength,  
                                                          callback );  

    if( managerStatus != SUBSCRIPTION_MANAGER_SUCCESS )  
    {  
        returnStatus = EXIT_FAILURE;  
    }  
    else  
    {  
        LogInfo( ( "Subscribing to the MQTT topic %.*s.",  
                   topicFilterLength,  
                   pTopicFilter ) );  

        returnStatus = subscribeToTopic( pContext,  
                                         pTopicFilter,  
                                         topicFilterLength );  
    }  

    if( returnStatus != EXIT_SUCCESS )  
    {  
        /* Remove the registered callback for the temperature topic filter as  
         * the subscription operation for the topic filter did not succeed. */  
        ( void ) SubscriptionManager_RemoveCallback( pTopicFilter,  
                                                     topicFilterLength );  
    }  

    return returnStatus;  
}  
```


## 并发性

您应该将应用程序组织为简单的超级循环，还是由 RTOS 或调度器管理的一组任务？ 
任一选择对于 coreMQTT 均可行。如果您选择并发执行，则必须确保 
代码安全。在为 FreeRTOS 编写代码时，一种有用方法是专门指定一项任务来处理 MQTT， 
并通过安全 FreeRTOS 队列向该任务传递命令。FreeRTOS MQTT Agent 使用 
此方法。[该 Agent](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo) 为 FreeRTOS 提供独立的守护进程任务 
来处理所有 MQTT 交互。请参阅相关后续文章。


## 总结

Alan Kay 曾经说过：“简单的事情应该简单，复杂的事情应该是可能的。” 
coreMQTT 可实现这一目标，或提供适用于最简单超级循环的库函数，或可组合成复杂的 
多任务实时应用程序。您可以参考随附示例，了解如何操作。关键决策权 
在您手中。


## 作者简介

![](https://secure.gravatar.com/avatar/d2018791072245fa4f97f31e914090e2?s=200&d=mm&r=g)   
Dan Good 在 Amazon Web Services 担任高级软件开发工程师。在网络领域工作多年后， 
蓬勃发展的创客文化激励他投身于 IoT 领域。Dan 为 FreeRTOS 
Core* 库和适用于嵌入式 C 语言的 AWS IoT SDK 贡献了自己的力量，帮助客户进行创新。  
[查看此作者的文章](../author/gooddan) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

