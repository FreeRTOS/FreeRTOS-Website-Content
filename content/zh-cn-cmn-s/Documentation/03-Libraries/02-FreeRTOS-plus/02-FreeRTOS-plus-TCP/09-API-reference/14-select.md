---
title: FreeRTOS_select()
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
BaseType_t FreeRTOS_select( SocketSet_t xSocketSet, TickType_t xBlockTimeTicks );
```

阻塞“套接字集”，直到集内的套接字上发生相关事件。 
ipconfigSUPPORT_SELECT_FUNCTION 必须在 
[FreeRTOSIPConfig.h](../TCP_IP_Configuration#ipconfigSUPPORT_SELECT_FUNCTION) 中设置为 1，
FreeRTOS_select()（及其相关函数）才可用。

*套接字集*允许应用程序 RTOS 任务在多个套接字上同时进入阻塞状态。

要使用套接字集，请执行下列操作：

1. 调用 [FreeRTOS_CreateSocketSet()](createsocketset) 创建套接字集。套接字集 
   相当于 Berkeley 套接字 fd_set 类型。

2. 调用 FreeRTOS_FD_SET() 向套接字集添加一个或多个套接字。FreeRTOS_FD_SET() 
   相当于 Berkeley 套接字 FD_SET() 宏。

3. 调用 FreeRTOS_Select() 以测试套接字集中的套接字，查看是否有任何套接字有事件处于挂起状态。

4. 如果 FreeRTOS_select() 返回非零值，则调用 
   [FreeRTOS_FD_ISSET()](FD_ISSET) 检查套接字集中的所有套接字，以确定哪些事件处于挂起状态。

在任何时候，套接字都只能属于一个套接字集。

[FreeRTOS_FD_CLR()](FD_CLR) API 函数从套接字集中移除套接字。


**参数：** 


+ *xSocketSet*

  当前正在测试的套接字集。  


+ *xBlockTimeTicks*

  调用 RTOS 任务处于阻塞状态 
  （有其他任务在执行）以等待套接字集成员获取事件的最长时间（单位：滴答）。  


**返回：** 

如果 xBlockTimeTicks 在套接字集中的套接字发生事件之前过期，则返回零。否则， 
返回非零值。必须通过 
调用 [FreeRTOS_FD_ISSET()](FD_ISSET) 检查所有属于套接字集的套接字。

如果套接字集中的某个套接字[接收到信号](FreeRTOS_SignalSocket)， 
导致该套接字上被阻塞的任务中止读取操作，那么调用 FreeRTOS_select() 将返回 eSELECT_INTR。


**用法示例：** 

```c
/* FreeRTOS includes. */  
#include "FreeRTOS.h"  
#include "task.h"  
#include "queue.h"  
  
/* FreeRTOS-Plus-TCP includes. */  
#include "FreeRTOS_IP.h"  
#include "FreeRTOS_Sockets.h"  
  
static void prvMultipleSocketRxTask( void *pvParameters )  
{  
SocketSet_t xFD_Set;  
BaseType_t xResult;  
Socket_t xSockets[2];  
struct freertos_sockaddr xAddress;  
uint32_t xClientLength = sizeof( struct freertos_sockaddr ), x;  
uint32_t ulReceivedValue = 0;  
int32_t lBytes;  
const TickType_t xRxBlockTime = 0;  
  
    /* Create the set of sockets that will be passed into FreeRTOS_select(). */  
    xFD_Set = FreeRTOS_CreateSocketSet();  
  
    /* Create two sockets to add to the set. */  
    for( x = 0; x < 2; x++ )  
    {  
        /* Create the socket. */  
        xSockets[x] = FreeRTOS_socket( FREERTOS_AF_INET,  
                                       FREERTOS_SOCK_DGRAM,  
                                       FREERTOS_IPPROTO_UDP );  
  
        /* Bind the socket to a port number 1000, 1001... */  
        xAddress.sin_port = FreeRTOS_htons( 1000 + x );  
        FreeRTOS_bind( xSockets[x], &xAddress, sizeof( struct freertos_sockaddr ) );  
  
        /* Once it has been tested that a socket has a eSELECT_READ  
           event, blocking on a read call is not necessary any more. Set the  
           Rx block time to 0. */  
        FreeRTOS_setsockopt( xSockets[x], 0, FREERTOS_SO_RCVTIMEO,  
                             &xRxBlockTime, sizeof( xRxBlockTime ) );  
  
        /* Add the created socket to the set for the READ event only. */  
        FreeRTOS_FD_SET( xSockets[x], xFD_Set, eSELECT_READ );  
    }  
  
    for( ;; )  
    {  
        /* Wait for any event within the socket set. */  
        xResult = FreeRTOS_select( xFD_Set, portMAX_DELAY );  
        if( xResult != 0 )  
        {  
            /* The return value should never be zero because FreeRTOS_select() was called  
               with an indefinite delay (assuming INCLUDE_vTaskSuspend is set to 1).  
               Now check each socket which belongs to the set if it had an event */  
  
            for( x = 0; x < 2; x++ )  
            {  
                if( FreeRTOS_FD_ISSET ( xSockets[x], xFD_Set ) )  
                {  
                    /* Read from the socket. */  
                    lBytes = FreeRTOS_recvfrom( xSockets[x], &( ulReceivedValue ), 
                                                sizeof( uint32_t ), 0, &xAddress,  
                                                &xClientLength );  
                    /* Process the received data here. */  
                }  
            }  
        }  
    }  
}  
```
*FreeRTOS_select() API 函数用法示例*

