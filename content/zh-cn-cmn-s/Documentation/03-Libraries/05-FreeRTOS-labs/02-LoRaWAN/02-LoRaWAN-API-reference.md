---
title: LoRaWAN API 引用
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


**注意**：FreeRTOS LoRaWAN 演示项目位于 FreeRTOS-Labs 中。该演示功能齐全，但正在进行 
优化或重构，以提高内存使用率、增强模块性、完善说明文档、提升演示可用性或测试覆盖率 
。它位于 GitHub 的 [Lab-Project-FreeRTOS-LoRaWAN](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-LoRaWAN) 
存储库，与 Labs 项目主下载文件分隔开。 


以下部分提供了 FreeRTOS 中 LoRaWAN API 的详细描述和使用示例。


## 设置

LoRaWAN_Init() 可用于初始化区域的 LoRaWAN 堆栈。它将区域参数作为输入， 
并使用该区域的默认参数初始化 LoRaMAC 堆栈。此 API 还 
会创建后台 LoRaMAC 任务。该任务会循环处理来自无线电和 MAC 层的事件。此 
API 不是可重入或线程安全的。

```c
LoRaMacStatus_t status;  

status = LoRaWAN_Init( LORAMAC_REGION_US915 );  

if( status == LORAMAC_STATUS_OK )   
{  
      /* Continue with LoRaWAN Activation. */  
}  
else  
{  
      /* Exit the program with the appropriate error code. */  
}  

```


## 配置 LoRaWAN 的网络参数

可以使用以下 API 配置 LoRAWAN 的网络参数。 

`LoRaWAN_SetAdaptiveDataRate()` 可以打开或关闭终端设备的自适应数据速率。 
LoRaWAN 初始化后，可以随时调用此 API。开启自适应数据速率后， 
网络服务器会基于终端设备的位置和其他因素来为终端设备计算优化的数据速率 
。

`LoRaWAN_GetNetworkParams()` 和 `LoRaWAN_SetNetworkParams()` 等 API 可修改 
设备的第二接收窗口和 TX 功率的其他网络参数，诸如信道频率和数据速率 
。如果正在使用 Over the Air 激活 (OTAA) ，则应启动加入以使新参数生效 
。 


## 激活

有两种类型的激活受支持：Over The Air 激活 (OTAA) 或个性化激活 (ABP)。

`LoRaWAN_Join()` API 用于 OTAA。示例：

```c
LoRaMacStatus_t status;  

status = LoRaWAN_Join();  

if( status == LORAMAC_STATUS_OK )   
{  
      /* Send or receive data with LoRaWAN. */  
}  
else  
{  
      /*All JOIN attempts are exhausted. Report this to end user. */  
}  

```

此 API 是一个阻塞调用，直到加入握手完成或用尽所有重试次数。 
Over the Air 激活所需的凭据应使用下面的 getter 函数提供，或使用安全元素预设 
。

```c
void getDeviceEUI( uint8_t * param )  
{  
    /* Copy the 8 byte device EUI into param here. */   
}  
  
void getJoinEUI( uint8_t * param )  
{  
   /* Copy the 8 byte join EUI into param here. */  
}  
  
void getAppKey( uint8_t * param )  
{  
  /* Copy the 16 byte app key into param here. */  
}  

```

此 API 在配置的次数内尝试加入。如 LoRaWAN 规范所推荐， 
以随机间隔和不同频带重试。重试次数 
和间隔可以通过 `demos/classA/Nordic_NRF52/config/LoRaWANConfig.h` 中的以下配置来调整：

```c
#define lorawanConfigMAX_JOIN_ATTEMPTS      ( 1000 )  
#define lorawanConfigJOIN_RETRY_INTERVAL_MS ( 2000 )  
#define lorawanConfigMAX_JITTER_MS          ( 500 )  

```

(2) 通过 ABP 方法，可使用 `LoRaWAN_ActivateByPersonalization()` API 激活设备。


```c
LoRaMacStatus_t status;  

status = LoRaWAN_ActivateByPersonalization();  
  
if( status == LORAMAC_STATUS_OK )   
{  
      /* Send or receive data with LoRaWAN. */  
}  
else  
{  
      /* ABP activation failed. Report this to end user. */  
}  

```

在 ABP 方法中，终端设备使用其预设的凭据，而不与网络服务器握手 
。可以使用以下 getter 函数提供 ABP 的凭据：

```c
void getDeviceEUI( uint8_t * param )  
{  
    /* Copy the 8 byte device EUI into param here. */   
}  
  
void getJoinEUI( uint8_t * param )  
{  
   /* Copy the 8 byte join EUI into param here. */  
}  
  
uint32_t getDeviceAddress( void )  
{  
   /* Return the 24 bit network id of the address. */  
}  
  
void getGetAppSessionKey( uint8_t * param )  
{  
    /* Copy the 16 byte app session key into param here. */  
}  
  
void getGetNwkSessionKey( uint8_t * param )  
{  
     /* Copy the 16 byte network session key into param here. */  

}
```


## 发送上行链路数据

`LoRaWAN_Send()` API 可发送上行链路数据到 LoRa 网络服务器。上行链路数据可以 
是已确认或未确认。对于确认的消息，API 将阻塞，直到收到网络服务器的确认 
。此 API 还会以不同的数据速率，按配置的次数执行重试，直到收到确认 
。对于未经确认的消息，此 API 在无线电发送消息后立即返回 
。

```c
LoRaWANMessage_t uplink;  

uplink.port = LORAWAN_APP_PORT;  
memcpy( uplink.data, &data, bytesToSend );  
uplink.length = bytesToSend;  
uplink.dataRate = dataRateToSend; /* Set to zero if using adaptive data rate. */  
  
status = LoRaWAN_Send( &uplink, IS_CONFIRMED );  
  
if( status == LORAMAC_STATUS_OK )  
{  
   /*   
    * Successfully sent uplink data.  
    * Wait for receive windows to receive any downlink data.  
    */   
}  
else  
{  
    /* Failed to send data uplink, Check end-device and gateway connectivity. */
}  

```


## 接收下行链路数据

`LoRaWAN_Receive()` API 可以在指定时间内阻塞，直到接收到数据。通过 
设置以毫秒为单位的超时参数，应用程序可以选择在任何一段时间内等待下行链路数据。 
例如，对于 A 类用例，应用程序在发送上行链路消息之后，在接收窗口的持续时间内等待 
。下行链路队列大小可以根据应用程序需求， 
通过 `demos/classA/Nordic_NRF52/config/LoRaWANConfig.h` 中的配置 `lorawanConfigDOWNLINK_QUEUE_SIZE` 调整 

```c
LoRaWANMessage_t downlink;  

status = LoRaWAN_Receive( &downlink, CLASSA_RECEIVE_WINDOW_DURATION_MS );  

if( status == pdTRUE )  
{  
    /* Successfully received downlink data. */  
    decodeData( &downlink.data, downlink.length; downlink.port );  
}  
else  
{  
     /* No data downlink. Do Nothing. */  
}  

```


## LoRaWAN 事件轮询

`LoRaWAN_PollEvent()` API 可轮询从 LoRaWAN 网络接收的任何事件。 
网络支持在应用程序层接收以下事件。 

```c
typedef enum LoRaWANEventType  
{  
    LORAWAN_EVENT_UNKNOWN = 0,                  
/**< @brief Type to denote an unexpected event type. */   
    LORAWAN_EVENT_DOWNLINK_PENDING,            
/**< @brief Indicates that server has to send more downlink data or waiting for a mac command uplink. */   
    LORAWAN_EVENT_TOO_MANY_FRAME_LOSS,         
/**< @brief Indicates too many frames are missed between end device and LoRa network server. */   
    LORAWAN_EVENT_DEVICE_TIME_UPDATED,         
/**< @brief Indicates the device time has been synchronized with LoRa network server. */   
    LORAWAN_EVENT_LINK_CHECK_REPLY             
/**< @brief Reply for a link check request from end device. */   
}
  
```

应用程序可以通过阻塞事件对它们进行轮询，然后采取适当措施。 
下面的示例显示了应用程序针对两个此类事件的行为。

```c
BaseType_t status;  
LoRaWANEventInfo_t event;  

for (;;)  
{  
    status = LoRaWAN_PollEvent( &event, 0 );  
  
   if( status == pdTRUE )  
   {  
        switch( event.type)  
        {  
            case LORAWAN_EVENT_DOWNLINK_PENDING:  
                /*   
                 * MAC layer indicated a pending downlink event or an uplink command to be flushed.  
                 * Send an empty uplink to fetch the downlink packet.  
                 */   
                prvFetchDownlinkPacket();  
                break;  

           case LORAWAN_EVENT_TOO_MANY_FRAME_LOSS:  
                /* Too many frame loss between end-device and Network server. Trigger a re-join. */  
                LoRaWAN_Join();   
                break;  

           ....  

           ....  

           default:  
               break;  

       }  
   }  
   else  
   {  
        break;  
   }  
}    

```

## 清理

`LoRaWAN_Cleanup()` API 可停止和反初始化 LoRaMac 堆栈，并删除 LoRaMac 任务和相关资源 
。 
