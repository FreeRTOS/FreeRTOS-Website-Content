---
title: Design for Named Shadow support in Shadow Library
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## Introduction

The AWS Shadow service supports multiple Shadow documents for an IoT Thing using a feature called Named 
Shadows. More details about this addition can be found in 
the [AWS release announcement](https://aws.amazon.com/about-aws/whats-new/2020/07/aws-iot-core-now-supports-multiple-shadows-for-a-single-iot-device/) 
and in the [AWS Shadow Service documentation](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html#device-shadow-using). 
Support for Named Shadows is not present in the Device Shadow library up to 
the [v1.0.2](https://github.com/aws/Device-Shadow-for-AWS-IoT-embedded-sdk/releases/tag/v1.0.2) release. 
This document describes the design of the Named Shadow support in the Device Shadow library.


## Design

The design for the Named Shadow is an extension of the [design for the Classic Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow) for 
an IoT Thing. 
The [existing version of the Device Shadow library](https://github.com/aws/Device-Shadow-for-AWS-IoT-embedded-sdk/releases/tag/v1.0.2), 
helps in building and matching the Classic Shadow MQTT topics used for interacting with the AWS Shadow 
service. Refer to 
the [design and design diagram of the Shadow library in AWS docs](https://docs.aws.amazon.com/embedded-csdk/202012.00/lib-ref/libraries/aws/device-shadow-for-aws-iot-embedded-sdk/docs/doxygen/output/html/shadow_design.html). 
The design for Named Shadows is an extension of the same design. The topics used by Classic Shadows 
and Named Shadows differ only in the topic prefix. This table shows the topic prefix used by each shadow 
type.

|  | ShadowTopicPrefix | Shadow type |
| --- | --- | --- |
|  1  | `$aws/things/thingName/shadow` | Unnamed (classic) shadow |
|  2  | `$aws/things/thingName/shadow/name/shadowName` | Named shadow |

To provide support for Named Shadow MQTT topics, additional APIs and helper MACROs are introduced. 
Compared to the already existing APIs, these APIs and MACROs take additional parameters for the shadow 
name and length. The new APIs and MACROs are discussed in the sections below.


### APIs

Two new APIs are added for providing the support for Named Shadows.

1. An API to assemble MQTT topic strings for a Shadow - **Shadow\_AssembleTopicString()**. This API 
   will work for both Classic Shadow and Named Shadow. Apps that do not know the Thing Name and Shadow 
   names at compile time can use this function to assemble the topic string at run time.

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

2. An API to check if an MQTT topic is a Shadow topic- **Shadow\_MatchTopicString()**. This API will work 
   for both Classic Shadow and Named Shadow.

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


#### Backward compatibility

Backward compatibility will be provided to the already existing Device Shadow APIs, which will only 
support Classic Shadow. 

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


### MACROs

A new set of function-like MACROS provide the support for Named Shadows. There is a matching new 
function-like macro for each old function-like macro:

| Old | New |
| --- | --- |
| SHADOW\_TOPIC\_STRING | SHADOW\_TOPIC\_STR |
| SHADOW\_TOPIC\_LENGTH | SHADOW\_TOPIC\_LEN |
| SHADOW\_TOPIC\_LENGTH\_MAX | SHADOW\_TOPIC\_LEN\_MAX |
| SHADOW\_TOPIC\_STRING\_UPDATE | SHADOW\_TOPIC\_STR\_UPDATE |
| SHADOW\_TOPIC\_LENGTH\_UPDATE | SHADOW\_TOPIC\_LEN\_UPDATE |
| SHADOW\_TOPIC\_STRING\_UPDATE\_ACCEPTED | SHADOW\_TOPIC\_STR\_UPDATE\_ACC |
| SHADOW\_TOPIC\_LENGTH\_UPDATE\_ACCEPTED | SHADOW\_TOPIC\_LEN\_UPDATE\_ACC |
| SHADOW\_TOPIC\_STRING\_UPDATE\_REJECTED | SHADOW\_TOPIC\_STR\_UPDATE\_REJ |
| SHADOW\_TOPIC\_LENGTH\_UPDATE\_REJECTED | SHADOW\_TOPIC\_LEN\_UPDATE\_REJ |
| SHADOW\_TOPIC\_STRING\_UPDATE\_DOCUMENTS | SHADOW\_TOPIC\_STR\_UPDATE\_DOCS |
| SHADOW\_TOPIC\_LENGTH\_UPDATE\_DOCUMENTS | SHADOW\_TOPIC\_LEN\_UPDATE\_DOCS |
| SHADOW\_TOPIC\_STRING\_UPDATE\_DELTA | SHADOW\_TOPIC\_STR\_UPDATE\_DELTA |
| SHADOW\_TOPIC\_LENGTH\_UPDATE\_DELTA | SHADOW\_TOPIC\_LEN\_UPDATE\_DELTA |
| SHADOW\_TOPIC\_STRING\_GET | SHADOW\_TOPIC\_STR\_GET |
| SHADOW\_TOPIC\_LENGTH\_GET | SHADOW\_TOPIC\_LEN\_GET |
| SHADOW\_TOPIC\_STRING\_GET\_ACCEPTED | SHADOW\_TOPIC\_STR\_GET\_ACC |
| SHADOW\_TOPIC\_LENGTH\_GET\_ACCEPTED | SHADOW\_TOPIC\_LEN\_GET\_ACC |
| SHADOW\_TOPIC\_STRING\_GET\_REJECTED | SHADOW\_TOPIC\_STR\_GET\_REJ |
| SHADOW\_TOPIC\_LENGTH\_GET\_REJECTED | SHADOW\_TOPIC\_LEN\_GET\_REJ |
| SHADOW\_TOPIC\_STRING\_DELETE | SHADOW\_TOPIC\_STR\_DELETE |
| SHADOW\_TOPIC\_LENGTH\_DELETE | SHADOW\_TOPIC\_LEN\_DELETE |
| SHADOW\_TOPIC\_STRING\_DELETE\_ACCEPTED | SHADOW\_TOPIC\_STR\_DELETE\_ACC |
| SHADOW\_TOPIC\_LENGTH\_DELETE\_ACCEPTED | SHADOW\_TOPIC\_LEN\_DELETE\_ACC |
| SHADOW\_TOPIC\_STRING\_DELETE\_REJECTED | SHADOW\_TOPIC\_STR\_DELETE\_REJ |
| SHADOW\_TOPIC\_LENGTH\_DELETE\_REJECTED | SHADOW\_TOPIC\_LEN\_DELETE\_REJ |

The new macro names respect MISRA 5.1. We ensure that every macro is, conservatively, 31 characters 
or fewer.

The new macros accept a shadowName or shadowNameLength parameter. They can be used for both Named and 
Classic shadows.

Here is an example using a new macro:

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

All old macros are retained for backwards compatibility. Here is an example:

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
