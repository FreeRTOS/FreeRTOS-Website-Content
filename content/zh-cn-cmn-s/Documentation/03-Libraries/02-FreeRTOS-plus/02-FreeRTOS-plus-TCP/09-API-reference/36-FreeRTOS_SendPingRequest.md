---
title: FreeRTOS_SendPingRequest()
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API 引用](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_sockets.h

```c
BaseType_t FreeRTOS_SendPingRequest( uint32_t ulIPAddress,
                                        size_t xNumberOfBytesToSend,
                                        TickType_t xBlockTimeTicks );
```

向远程计算机发送 ping[（ICMP 回显）](http://en.wikipedia.org/wiki/Ping_(networking_utility)请求。

要使用 FreeRTOS_SendPingRequest()，必须在 FreeRTOSIPConfig.h 中将 ipconfigSUPPORT_OUTGOING_PINGS 设置为 1。

在收到对传出 ping 请求的回复时，TCP/IP 堆栈会调用应用程序定义的 [vApplicationPingReplyHook()](vApplicationPingReplyHook)
钩子（或*回调*）函数。


**参数：** 

+ *ulIPAddress* 
  
  向其发送 ping 请求的 IP 地址。

  IP 地址是以网络字节顺序表示的 32 位数字。

+ *xNumberOfBytesToSend* 
  
  ping 请求中要发送的数据字节数。

+ *xBlockTimeTicks* 
  
  如果网络缓冲区无法立即可用，调用的 RTOS 任务愿意等待的最长时间 
  。

  如果网络缓冲区不可用，则调用的 RTOS 任务将处于阻塞状态（以便其他任务可以执行）， 
  直到缓冲区可用且 ping 请求得以传输， 
  或阻塞时间到期。

  阻塞时间以滴答为单位。将以毫秒表示的时间除以 portTICK_PERIOD_MS， 
  即可转换为以滴答为单位的时间。


**返回：** 

+ 如果 ping 请求发送成功，则返回 ping 消息中发送的序列号， 
  以确保应用程序编写者可以将传输的 ping 请求与收到的 ping 回复匹配起来。请参阅 
  下方示例。

+ 如果无法发送 ping 请求，则返回 pdFAIL。


**用法示例：** 

此示例定义了两个函数。vSendPing() 可将 8 个字节传输到远程 IP 地址。
vApplicationPingReplyHook() 是标准的 FreeRTOS-Plus-TCP ping 回复回调函数。
vApplicationPingReplyHook() 接收 ping 回复，然后将收到的序列号
发送到 vSendPing()。vSendPing() 函数可将接收到的序列号与 ping 请求中的序列号进行比较。

```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
/* This example code snippet assumes the queue has already been created! */  
QueueHandle_t xPingReplyQueue;  
  
/* If ipconfigSUPPORT_OUTGOING_PINGS is set to 1 in FreeRTOSIPConfig.h then  
   vApplicationPingReplyHook() is called by the TCP/IP stack when the stack receives a  
   ping reply. */
void vApplicationPingReplyHook( ePingReplyStatus_t eStatus, uint16_t usIdentifier )  
{  
    switch( eStatus )  
    {  
        case eSuccess    :  
            /* A valid ping reply has been received. Post the sequence number  
               on the queue that is read by the vSendPing() function below. Do  
               not wait more than 10ms trying to send the message if it cannot be  
               sent immediately because this function is called from the TCP/IP  
               RTOS task - blocking in this function will block the TCP/IP RTOS task. */  
            xQueueSend( xPingReplyQueue, &usIdentifier, 10 / portTICK_PERIOD_MS );  
            break;  
  
        case eInvalidChecksum :  
        case eInvalidData :  
            /* A reply was received but it was not valid. */  
            break;  
    }  
}  
  
  
BaseType_t vSendPing( const int8_t *pcIPAddress )  
{  
uint16_t usRequestSequenceNumber, usReplySequenceNumber;  
uint32_t ulIPAddress;  
  
    /* The pcIPAddress parameter holds the destination IP address as a string in  
       decimal dot notation (for example, "192.168.0.200"). Convert the string into  
       the required 32-bit format. */  
    ulIPAddress = FreeRTOS_inet_addr( pcIPAddress );  
  
    /* Send a ping containing 8 data bytes. Wait (in the Blocked state) a  
       maximum of 100ms for a network buffer into which the generated ping request  
       can be written and sent. */  
    usRequestSequenceNumber = FreeRTOS_SendPingRequest( ulIPAddress, 8, 100 / portTICK_PERIOD_MS );  
  
    if( usRequestSequenceNumber == pdFAIL )  
    {  
        /* The ping could not be sent because a network buffer could not be  
           obtained within 100ms of FreeRTOS_SendPingRequest() being called. */  
    }  
    else  
    {  
        /* The ping was sent. Wait 200ms for a reply. The sequence number from  
           each reply is sent from the vApplicationPingReplyHook() on the  
           xPingReplyQueue queue (this is not standard behaviour, but implemented in  
           the example function above). It is assumed the queue was created before  
           this function was called! */  
        if( xQueueReceive( xPingReplyQueue,  
                           &usReplySequenceNumber,  
                           200 / portTICK_PERIOD_MS ) == pdPASS )  
        {  
            /* A ping reply was received. Was it a reply to the ping just sent? */  
            if( usRequestSequenceNumber == usReplySequenceNumber )  
            {  
                /* This was a reply to the request just sent. */  
            }  
        }  
    }  
}  
```
*FreeRTOS_SendPingRequest() API 函数用法示例*

