---
title: 阴影库中命名阴影支持的设计
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## 引言

AWS 阴影服务使用名为“命名阴影”的功能，支持 IoT Thing 的多个阴影文档 
。此新特性的详细信息，请参阅 
[AWS 版本公告](https://aws.amazon.com/about-aws/whats-new/2020/07/aws-iot-core-now-supports-multiple-shadows-for-a-single-iot-device/) 
和[AWS 阴影服务文档](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html#device-shadow-using)。 
在 
[v1.0.2](https://github.com/aws/Device-Shadow-for-AWS-IoT-embedded-sdk/releases/tag/v1.0.2) 版本及其之前版本中，设备阴影库中不支持命名阴影。 
本文档描述了设备阴影库中命名阴影支持的设计。


## 设计

命名阴影的设计是[经典阴影设计](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow)的扩展， 
后者适用于 IoT Thing。 
[设备阴影库的现有版本](https://github.com/aws/Device-Shadow-for-AWS-IoT-embedded-sdk/releases/tag/v1.0.2)， 
有助于构建和匹配用于与 AWS 阴影服务交互的经典阴影 MQTT 主题 
。请参阅 
[AWS 文档中的阴影库设计与设计图](https://docs.aws.amazon.com/embedded-csdk/202012.00/lib-ref/libraries/aws/device-shadow-for-aws-iot-embedded-sdk/docs/doxygen/output/html/shadow_design.html)。 
命名阴影的设计是对这一设计的扩展。经典阴影和 
命名阴影使用的主题区别在于主题前缀。下表列明了每个阴影类型使用的主题前缀 
。

|  | ShadowTopicPrefix | 阴影类型 |
| --- | --- | --- |
|  1  | `$aws/things/thingName/shadow` | 未命名（经典）阴影 |
|  2  | `$aws/things/thingName/shadow/name/shadowName` | 命名阴影 |

为了支持命名阴影 MQTT 主题，引入了其他 API 和辅助宏。 
与已经存在的 API 相比，上述 API 和宏会为阴影名称和长度采用额外参数 
。下文将讨论新 API 和宏。


### API

添加了两个新 API，用于为命名阴影提供支持。

1. 用于为阴影 **Shadow_AssembleTopicString()** 汇编 MQTT 主题字符串的 API。此 API 
   同时适用于经典阴影和命名阴影。在编译时不知道 Thing 名称和阴影名称的应用程序 
   可以使用此函数在运行时汇编主题字符串。

   ```c
   /**  
    * @brief Assemble shadow topic string when Thing Name or Shadow Name is only known at run time.  
    *        If both the Thing Name and Shadow Name are known at compile time, use  
    *        @link #SHADOW_TOPIC_STR SHADOW_TOPIC_STR_* @endlink macros instead.  
    *  
    * @param[in] topicType Indicates what topic will be written into the buffer pointed to by pTopicBuffer.  
    *            can be one of:  
    *                - ShadowTopicStringTypeGet  
    *                - ShadowTopicStringTypeGetAccepted  
    *                - ShadowTopicStringTypeGetRejected  
    *                - ShadowTopicStringTypeDelete  
    *                - ShadowTopicStringTypeDeleteAccepted  
    *                - ShadowTopicStringTypeDeleteRejected  
    *                - ShadowTopicStringTypeUpdate  
    *                - ShadowTopicStringTypeUpdateAccepted  
    *                - ShadowTopicStringTypeUpdateRejected  
    *                - ShadowTopicStringTypeUpdateDocuments  
    *                - ShadowTopicStringTypeUpdateDelta  
    * @param[in]  pThingName Thing Name string. No need to be null terminated. Must not be NULL.  
    * @param[in]  thingNameLength Length of Thing Name string pointed to by pThingName. Must not be zero.  
    * @param[in]  pShadowName Shadow Name string. No need to be null terminated. Must not be NULL. Empty string for classic shadow.  
    * @param[in]  shadowNameLength Length of Shadow Name string pointed to by pShadowName. Zero for classic shadow.  
    * @param[out] pTopicBuffer Pointer to buffer for returning the topic string.  
    *             Caller is responsible for supplying memory pointed to by pTopicBuffer.  
    *             This function does not fill in the terminating null character. The app  
    *             can supply a buffer that does not have space for holding the null character.  
    * @param[in]  bufferSize Length of pTopicBuffer. This function will return error if  
    *             bufferSize is less than the length of the assembled topic string.  
    * @param[out] pOutLength Pointer to caller-supplied memory for returning the length of the topic string.  
    * @return     One of the following:  
    *             - SHADOW_SUCCESS if successful.  
    *             - An error code if failed to assemble.  
    */  
    ShadowStatus_t Shadow_AssembleTopicString( ShadowTopicStringType_t topicType,  
                                              const char * pThingName,  
                                              uint8_t thingNameLength,  
                                              const char * pShadowName,  
                                              uint8_t shadowNameLength,  
                                              char * pTopicBuffer,  
                                              uint16_t bufferSize,  
                                              uint16_t * pOutLength );   
   ```

2. 用于检查 MQTT 主题是否为阴影主题 **Shadow_MatchTopicString()** 的 API。此 API 
   同时适用于经典阴影和命名阴影。

   ```c
   /**  
    * @brief Given the topic string of an incoming message, determine whether it is  
    *        related to a device shadow; if it is, return information about the type of  
    *        device shadow message, and pointers to the Thing Name and Shadow Name inside of  
    *        the topic string. See #ShadowMessageType_t for the list of message types.  
    *        Those types correspond to Device Shadow Topics.  
    *  
    * @note When this function returns, the pointer pThingName points at the first character  
    *       of the <thingName> segment inside of the topic string. Likewise, the pointer pShadowName  
    *       points at the first character of the <shadowName> segment inside of the topic string  
    *       (if the topic is for a named shadow, not the "Classic" shadow.)  
    *       Caller is responsible for keeping the memory holding the topic string around while  
    *       accessing the Thing Name through pThingName and the Shadow Name through pShadowName.  
    *  
    * @param[in]  pTopic Pointer to the MQTT topic string. Does not have to be null-terminated.  
    * @param[in]  topicLength Length of the MQTT topic string.  
    * @param[out] pMessageType Pointer to caller-supplied memory for returning the type of the shadow message.  
    * @param[out] pThingName Points to the 1st character of Thing Name inside of the topic string, and can be  
    *             null if caller does not need to know the Thing Name contained in the topic string.  
    * @param[out] pThingNameLength Pointer to caller-supplied memory for returning the length of the Thing Name,  
    *             and can be null if caller does not need to know the Thing Name contained in the topic string.  
    * @param[out] pShadowName Points to the 1st character of Shadow Name inside of the topic string, and can be  
    *             null if caller does not need to know the Shadow Name contained in the topic string. Null is  
    *             returned if the shadow is Classic.  
    * @param[out] pShadowNameLength Pointer to caller-supplied memory for returning the length of the Shadow Name,  
    *             and can be null if caller does not need to know the Shadow Name contained in the topic string.  
    *             A value of 0 is returned if the shadow is Classic.  
    * @return     One of the following:  
    *             - #SHADOW_SUCCESS if the message is related to a device shadow;  
    *             - An error code defined in #ShadowStatus_t if the message is not related to a device shadow,  
    *               if any input parameter is invalid, or if the function fails to  
    *               parse the topic string.  
    */  
    ShadowStatus_t Shadow_MatchTopicString( const char * pTopic,  
                                            uint16_t topicLength,  
                                            ShadowMessageType_t * pMessageType,  
                                            const char ** pThingName,  
                                            uint8_t * pThingNameLength,  
                                            const char ** pShadowName,  
                                            uint8_t * pShadowNameLength );  
   ```


#### 向后兼容性

现有的设备阴影 API 将具有向后兼容性，它们将仅支持经典阴影 
。 

```c
/**  
 * @brief Assemble unnamed ("Classic") shadow topic string when Thing Name is only known at run time.  
 *        If the Thing Name is known at compile time, use  
 *        @link #SHADOW_TOPIC_STRING SHADOW_TOPIC_STRING @endlink macro instead.  
 *  
 * @deprecated Please use @ref Shadow_AssembleTopicString in new designs.  
 *  
 * See @ref Shadow_AssembleTopicString for documentation of common behavior.  
 */  
#define Shadow_GetTopicString( topicType, pThingName, thingNameLength, pTopicBuffer, bufferSize, pOutLength ) \  
    Shadow_AssembleTopicString( topicType, pThingName, thingNameLength, SHADOW_NAME_CLASSIC, 0,               \  
                                pTopicBuffer, bufferSize, pOutLength )  
                                  
/**  
 * @brief Given the topic string of an incoming message, determine whether it is related to  
 *        an unnamed ("Classic") device shadow; if it is, return information about the type  
 *        of device shadow message, and a pointers to the Thing Name inside of  
 *        the topic string. See #ShadowMessageType_t for the list of message types.  
 *        Those types correspond to Device Shadow Topics.  
 *  
 * @deprecated Please use @ref Shadow_MatchTopicString in new designs.  
 *  
 * See @ref Shadow_MatchTopicString for documentation of common behavior.  
 */                                 
ShadowStatus_t Shadow_MatchTopic( const char * pTopic,  
                                  uint16_t topicLength,  
                                  ShadowMessageType_t * pMessageType,  
                                  const char ** pThingName,  
                                  uint16_t * pThingNameLength )  
{  
    uint8_t thingNameLength = 0U;  
    ShadowStatus_t shadowStatus = Shadow_MatchTopicString( pTopic,  
                                                           topicLength,  
                                                           pMessageType,  
                                                           pThingName,  
                                                           &thingNameLength,  
                                                           NULL,  
                                                           NULL );  
    if( pThingNameLength != NULL )  
    {  
        *pThingNameLength = thingNameLength;  
    }  

    return shadowStatus;  
}   
```


### 宏

一组新的仿函数 MACROS 会为命名阴影提供支持。每个旧的仿函数宏都 
有一个对应的新仿函数宏：

| 旧 | 新 |
| --- | --- |
| SHADOW_TOPIC_STRING | SHADOW_TOPIC_STR |
| SHADOW_TOPIC_LENGTH | SHADOW_TOPIC_LEN |
| SHADOW_TOPIC_LENGTH_MAX | SHADOW_TOPIC_LEN_MAX |
| SHADOW_TOPIC_STRING_UPDATE | SHADOW_TOPIC_STR_UPDATE |
| SHADOW_TOPIC_LENGTH_UPDATE | SHADOW_TOPIC_LEN_UPDATE |
| SHADOW_TOPIC_STRING_UPDATE_ACCEPTED | SHADOW_TOPIC_STR_UPDATE_ACC |
| SHADOW_TOPIC_LENGTH_UPDATE_ACCEPTED | SHADOW_TOPIC_LEN_UPDATE_ACC |
| SHADOW_TOPIC_STRING_UPDATE_REJECTED | SHADOW_TOPIC_STR_UPDATE_REJ |
| SHADOW_TOPIC_LENGTH_UPDATE_REJECTED | SHADOW_TOPIC_LEN_UPDATE_REJ |
| SHADOW_TOPIC_STRING_UPDATE_DOCUMENTS | SHADOW_TOPIC_STR_UPDATE_DOCS |
| SHADOW_TOPIC_LENGTH_UPDATE_DOCUMENTS | SHADOW_TOPIC_LEN_UPDATE_DOCS |
| SHADOW_TOPIC_STRING_UPDATE_DELTA | SHADOW_TOPIC_STR_UPDATE_DELTA |
| SHADOW_TOPIC_LENGTH_UPDATE_DELTA | SHADOW_TOPIC_LEN_UPDATE_DELTA |
| SHADOW_TOPIC_STRING_GET | SHADOW_TOPIC_STR_GET |
| SHADOW_TOPIC_LENGTH_GET | SHADOW_TOPIC_LEN_GET |
| SHADOW_TOPIC_STRING_GET_ACCEPTED | SHADOW_TOPIC_STR_GET_ACC |
| SHADOW_TOPIC_LENGTH_GET_ACCEPTED | SHADOW_TOPIC_LEN_GET_ACC |
| SHADOW_TOPIC_STRING_GET_REJECTED | SHADOW_TOPIC_STR_GET_REJ |
| SHADOW_TOPIC_LENGTH_GET_REJECTED | SHADOW_TOPIC_LEN_GET_REJ |
| SHADOW_TOPIC_STRING_DELETE | SHADOW_TOPIC_STR_DELETE |
| SHADOW_TOPIC_LENGTH_DELETE | SHADOW_TOPIC_LEN_DELETE |
| SHADOW_TOPIC_STRING_DELETE_ACCEPTED | SHADOW_TOPIC_STR_DELETE_ACC |
| SHADOW_TOPIC_LENGTH_DELETE_ACCEPTED | SHADOW_TOPIC_LEN_DELETE_ACC |
| SHADOW_TOPIC_STRING_DELETE_REJECTED | SHADOW_TOPIC_STR_DELETE_REJ |
| SHADOW_TOPIC_LENGTH_DELETE_REJECTED | SHADOW_TOPIC_LEN_DELETE_REJ |

新宏名称遵守 MISRA 5.1。我们确保每个宏适当拥有 31 个或更少字符 
。

新宏接受 shadowName 或 shadowNameLength 参数。它们可用于命名阴影和 
经典阴影。

下面是使用新宏的示例：

```c
/**  
 * @ingroup shadow_constants  
 * @brief Assemble shadow topic string "$aws/things/<thingName>/shadow/update/accepted" or  
 *        "$aws/things/<thingName>/shadow/name/<shadowName>/update/accepted".  
 *  
 * @param[in] thingName     Thing Name.  
 * @param[in] shadowName    Shadow Name. Empty string for an unnamed ("Classic") shadow.  
 *  
 * @return Topic string.  
 */  
#define SHADOW_TOPIC_STR_UPDATE_ACC( thingName, shadowName ) \  
    SHADOW_TOPIC_STR( thingName, shadowName, SHADOW_OP_UPDATE, SHADOW_SUFFIX_ACCEPTED )   
```

为了向后兼容性，保留所有旧的宏。示例如下：

```c
/**  
 * @ingroup shadow_constants  
 * @brief Assemble constant shadow topic strings when Thing Name and Shadow Name are known at compile time.  
 *  
 * When thingName and shadowName are known to be "myThing" and "myShadow" at compile time, invoke the macro like this:  
 *  
 *     SHADOW_ASSEMBLE_TOPIC_STRING ( SHADOW_OP_UPDATE_DELTA, "myThing", "myShadow" )  
 *  
 * When thingName and/or shadowName is only known at run time, do not use this macro. Use the  
 * Shadow_AssembleTopicString() function instead.  
 *  
 * @param[in] operation     Can be one of:  
 *                              - #SHADOW_OP_UPDATE  
 *                              - #SHADOW_OP_UPDATE_ACCEPTED  
 *                              - #SHADOW_OP_UPDATE_REJECTED  
 *                              - #SHADOW_OP_UPDATE_DOCUMENTS  
 *                              - #SHADOW_OP_UPDATE_DELTA  
 *                              - #SHADOW_OP_GET  
 *                              - #SHADOW_OP_GET_ACCEPTED  
 *                              - #SHADOW_OP_GET_REJECTED  
 *                              - #SHADOW_OP_DELETE  
 *                              - #SHADOW_OP_DELETE_ACCEPTED  
 *                              - #SHADOW_OP_DELETE_REJECTED  
 *  
 * @param[in] thingName     Thing Name.  
 * @param[in] shadowName    Shadow Name. Empty string for an unnamed ("Classic") shadow.  
 *  
 * @return Topic string.  
 */  

#define SHADOW_ASSEMBLE_TOPIC_STRING ( operation, thingName, shadowName )  \  
    ( ( sizeof( shadowName ) > 1 ) ?                                       \  
      ( SHADOW_PREFIX thingName SHADOW_NAMED_ROOT shadowName operation ) : \  
      ( SHADOW_PREFIX thingName SHADOW_CLASSIC_ROOT operation ) )  
```


```c
/**  
 * @brief Assemble unnamed "Classic" shadow topic string "$aws/things/<thingName>/shadow/update/accepted".  
 * @deprecated Please use @ref #SHADOW_TOPIC_STR_UPDATE_ACC in new designs.  
 *  
 * See @ref #SHADOW_TOPIC_STR_UPDATE_ACC for documentation of common behavior.  
 */  
#define SHADOW_TOPIC_STRING_UPDATE_ACCEPTED( thingName ) \  
    SHADOW_TOPIC_STR_UPDATE_ACC( thingName, SHADOW_NAME_CLASSIC )   
```
