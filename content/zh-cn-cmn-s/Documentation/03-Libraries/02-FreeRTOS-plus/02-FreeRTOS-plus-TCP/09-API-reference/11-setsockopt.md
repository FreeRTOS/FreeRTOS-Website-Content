---
title: FreeRTOS_setsockopt()
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
BaseType_t FreeRTOS_setsockopt( Socket_t xSocket, int32_t lLevel,
                                int32_t lOptionName, const void *pvOptionValue,
                                size_t xOptionLength );
```

设置套接字选项。


**参数：** 

+ *xSocket*

  目标套接字（正在修改的套接字）。套接字必须已通过成功 
  调用 [FreeRTOS_socket()](socket) 创建。  

+ *lLevel*

  FreeRTOS-Plus-TCP [目前]不使用 lLevel 参数。加入该参数是为了确保 
  与预期的标准伯克利套接字 API 保持一致， 
  并确保与 FreeRTOS-Plus-TCP 的未来版本兼容。  

+ *lOptionName*

  正在设置或修改的选项。请参阅[下文](#有效-loptionname-值)了解有效值。  

+ *pvOptionValue*

  pvOptionValue 的含义取决于 lOptionName 的值。请参阅 
  lOptionName 参数的说明。  

+ *xOptionLength*

  FreeRTOS-Plus-TCP [目前]不使用 xOptionLength 参数。加入该参数是为了确保 
  与预期的标准伯克利套接字 API 保持一致， 
  并确保与 FreeRTOS-Plus-TCP 的未来版本兼容。  


**返回：** 

+ 如果使用无效的 lOptionName 值，则返回 -pdFREERTOS_ERRNO_EINVAL，否则返回 0。
  （按照伯克利套接字标准，返回 0 表示成功，与 FreeRTOS 标准相反，返回 0 
  表示失败！）


**用法示例：** 

在此示例中，首先创建 UDP 套接字， 
根据函数的参数配置套接字的行为，然后返回创建和配置的套接字。

```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
Socket_t xCreateASocket( TickType_t xReceiveTimeout_ms,  
                         TickType_t xSendTimeout_ms,  
                         int32_t iUseChecksum )  
{  
/* Variable to hold the created socket. */  
Socket_t xSocket;  
  
    /* Create the socket. */  
    xSocket = FreeRTOS_socket( FREERTOS_AF_INET,  
                               FREERTOS_SOCK_DGRAM,  
                               FREERTOS_IPPROTO_UDP );  
  
    /* Check the socket was created successfully. */  
    if( xSocket != FREERTOS_INVALID_SOCKET )  
    {  
        /* Convert the receive timeout into ticks. */  
        xReceiveTimeout_ms /= portTICK_PERIOD_MS;  
  
        /* Set the receive timeout. */  
        FreeRTOS_setsockopt( xSocket,            /* The socket being modified. */  
                             0,                   /* Not used. */  
                             FREERTOS_SO_RCVTIMEO,/* Setting receive timeout. */  
                             &xReceiveTimeout_ms, /* The timeout value. */  
                             0 );                 /* Not used. */  
  
        /* Convert the send timeout into ticks. */  
        xSendTimeout_ms /= portTICK_PERIOD_MS;  
  
        /* Set the send timeout. */  
        FreeRTOS_setsockopt( xSocket,            /* The socket being modified. */  
                             0,                   /* Not used. */  
                             FREERTOS_SO_SNDTIMEO,/* Setting send timeout. */  
                             &xSendTimeout_ms,    /* The timeout value. */  
                             0 );                 /* Not used. */  
  
        if( iUseChecksum == pdFALSE )  
        {  
            /* Turn the UDP checksum creation off for outgoing UDP packets. */  
            FreeRTOS_setsockopt( xSocket,        /* The socket being modified. */  
                                 0,               /* Not used. */  
                                 FREERTOS_SO_UDPCKSUM_OUT, /* Setting checksum on/off. */  
                                 NULL,            /* NULL means off. */  
                                 0 );             /* Not used. */  
        }  
        else  
        {  
            /* The checksum is used by default, so there is nothing to do here.  
               If the checksum was off it could be turned on again using an option  
               value other than NULL, for example ( ( void * ) 1 ). */  
        }  
    }  
  
    return xSocket;  
}  
```
*FreeRTOS_setsockopt() API 函数用法示例*


### 有效 lOptionName 值

+ FREERTOS_SO_RCVTIMEO
  
  设置 [](../TCP_IP_Configuration#ipconfigsock_default_receive_block_time) 
  使用 UDP 套接字调用 [FreeRTOS_recvfrom()](recvfrom) 或调用 [FreeRTOS_recv()](recv) 时的接收超时
  （后者使用 TCP 套接字调用）。

  如果 lOptionName 是 FREERTOS_SO_RECTIMEO，那么 pvOptionValue 必须指向 TickType_t 类型的变量。

  超时值以滴答为单位。要将以毫秒为单位的时间转换为以滴答为单位的时间，
  请将以毫秒为单位的时间除以 portTICK_PERIOD_MS，或使用 pdMS_TO_TICKS() 宏。


+ FREERTOS_SO_SNDTIMEO

  设置 [](../TCP_IP_Configuration#ipconfigSOCK_DEFAULT_SEND_BLOCK_TIME) 
  当 [FreeRTOS_send()](send) 与 TCP 套接字一起使用，或 [FreeRTOS_sendto()](sendto)
  与 UDP 套接字一起使用时的发送超时。

  如果 lOptionName 是 FREERTOS_SO_SNDTIMEO，那么 pvOptionValue 必须指向 TickType_t 类型的变量。

  超时值以滴答为单位。要将以毫秒为单位的时间转换为以滴答为单位的时间， 
  请将以毫秒为单位的时间除以 portTICK_PERIOD_MS，或使用 pdMS_TO_TICKS() 宏。


+ FREERTOS_SO_UDPCKSUM_OUT

  仅对 UDP 套接字有效。

  打开或关闭为传出的 UDP 数据包生成校验和值。

  如果 lOptionName 为 FREERTOS_SO_UDPCKSUM_OUT，并且 lOptionValue 为 NULL (0)，则传出 UDP 数据包 
  的校验和将始终设置为 0。

  如果 lOptionName 为 FREERTOS_SO_UDPCKSUM_OUT，并且 lOptionValue 为除 NULL (0) 以外的任何值， 
  则传出 UDP 数据包将包含一个有效的校验和值。


+ FREERTOS_SO_SET_SEMAPHORE

  只有当 [ipconfigSOCKET_HAS_USER_SEMAPHORE](../TCP_IP_Configuration#ipconfigSOCKET_HAS_USER_SEMAPHORE)
  在 FreeRTOSIPConfig.h 中设置为 1 时才可用。

  该选项允许将一个信号量的引用传递给套接字。然后， TCP/IP RTOS 任务 
  将在以下任何事件发生时提供信号量：

  * 新数据到达
  * 传输数据后，新的传输缓冲区空间可用时
  * 传出 TCP 连接已成功
  * 新客户端已连接到 TCP 套接字
  * TCP 连接已关闭或重置

  用法示例：

  ```c
  /* Declare the semaphore. */
  SemaphoreHandle_t xSemaphore;

  /* Create the semaphore. */
  xSemaphore = xSemaphoreCreateBinary();
  if( xSemaphore != NULL )
  {
      /* Pass the semaphore to the socket. */
      FreeRTOS_setsockopt( xSocket,
                           0,
                           FREERTOS_SO_SET_SEMAPHORE,
                           ( void * )&xSemaphore,
                           sizeof( xSemaphore ) );
  
      /* The semaphore has been passed to the socket
         and will be used.
  
         **Note:** If a socket has a reference to a semaphore
         then the semaphore must not be deleted! To
         remove the semaphore call FreeRTOS_setsockopt()
         again, but this time with a NULL semaphore. */
      SemaphoreHandle_t xNoSem = NULL;
      FreeRTOS_setsockopt( xSocket,
                           0,
                           FREERTOS_SO_SET_SEMAPHORE,
                           ( void * ) &xNoSem,
                           sizeof( xNoSem ) );
  
      /* Now the semaphore can be deleted. */
      vSemaphoreDelete( xSemaphore );
  }
  ```
  *将信号量传递给套接字的示例*
  

+ FREERTOS_SO_RCVBUF

  仅对 TCP 套接字有效。

  设置[接收缓冲区](../TCP_IP_Configuration#ipconfigTCP_RX_BUFFER_LENGTH)的大小。
  理想情况下，应将其设置为[滑动窗口](../TCP_IP_Configuration#ipconfigUSE_TCP_WIN)大小的两倍。

  该参数只能在创建套接字和套接字接收数据之间设置， 
  因为接收缓冲区的大小在缓冲区创建后就已固定。

  如果 lOptionName 是 FREERTOS_SO_RCVBUF，那么 pvOptionValue 必须指向 int32_t 类型的变量。

  接收缓冲区大小以字节为单位。在内部，指定的大小将四舍五入为 
  最接近 [ipconfigTCP_MSS](../TCP_IP_Configuration#ipconfigTCP_MSS) 大小的倍数。例如， 
  如果 ipconfigTCP_MSS 为 500，那么设置缓冲区大小为 400 时， 
  会指定缓冲区大小为 500（1 * ipconfigTCP_MSS）；设置缓冲区大小为 500 时， 
  会指定缓冲区大小为 500（1 * ipconfigTCP_MSS）；设置缓冲区大小为 510 时， 
  会指定缓冲区大小为 1000 (2 * ipconfigTCP_MSS)。


+ FREERTOS_SO_SNDBUF
  
  仅对 TCP 套接字有效。

  设置[传输缓冲区](../TCP_IP_Configuration#ipconfigTCP_RX_BUFFER_LENGTH)的大小。
  这与数据包或滑动窗口的大小无关，它只设置缓冲区的大小。

  该参数只能在创建套接字和在套接字上发送数据之间设置， 
  因为发送缓冲区的大小在缓冲区创建后就已固定。

  如果 lOptionName 是 FREERTOS_SO_SNDBUF，那么 pvOptionValue 必须指向 int32_t 类型的变量。

  接收缓冲区大小以字节为单位。在内部，指定的大小将四舍五入为 
  最接近 [ipconfigTCP_MSS](../TCP_IP_Configuration#ipconfigTCP_MSS) 大小的倍数。例如， 
  如果 ipconfigTCP_MSS 为 500，那么设置缓冲区大小为 400 时， 
  缓冲区大小为 500（1 * ipconfigTCP_MSS）；设置缓冲区大小为 500 时， 
  会指定缓冲区大小为 500（1 * ipconfigTCP_MSS）；设置缓冲区大小为 510 时， 
  会指定缓冲区大小为 1000 (2 * ipconfigTCP_MSS)。


+ FREERTOS_SO_WIN_PROPERTIES

  仅限高级用户。

  仅对 TCP 套接字有效。

  一次调用即可设置[接收缓冲区](../TCP_IP_Configuration#ipconfigTCP_RX_BUFFER_LENGTH)、
  接收[滑动窗口](../TCP_IP_Configuration#ipconfigUSE_TCP_WIN)、
  [传输缓冲区](../TCP_IP_Configuration#ipconfigTCP_RX_BUFFER_LENGTH)以及传输滑动窗口 
  的大小。

  缓冲区和滑动窗口大小只能在创建套接字和向套接字发送数据 
  或从套接字接收数据之间设置。

  用法示例：

  ```c
  /* Declare an xWinProperties structure. */
  WinProperties_t  xWinProps;

  /* Fill in the required buffer and window sizes. */
  /* Unit: bytes */
  xWinProps.lTxBufSize = 4 * ipconfigTCP_MSS;
  /* Unit: MSS */
  xWinProps.lTxWinSize = 2;
  /* Unit: bytes */
  xWinProps.lRxBufSize = 4 * ipconfigTCP_MSS;
  /* Unit: MSS */
  xWinProps.lRxWinSize = 2;

  /* Use the structure with the
     FREERTOS_SO_WIN_PROPERTIES parameter in a call to
     FreeRTOS_setsockopt(). */
  FreeRTOS_setsockopt( xSocket,
                       0,
                       FREERTOS_SO_WIN_PROPERTIES,
                       ( void * ) &xWinProps,
                       sizeof( xWinProps ) );
  ```
  *设置缓冲区和滑动窗口大小的示例*


+ FREERTOS_SO_REUSE_LISTEN_SOCKET

  仅对 TCP 套接字有效。

  默认情况下，[监听](listen)套接字会创建一个新的套接字来处理任何接受的连接。
  FREERTOS_SO_REUSE_LISTEN_SOCKET 可以用来改变这种行为， 
  以便由监听套接字本身处理接受的连接。

  如果 lOptionName 为 FREERTOS_SO_REUSE_LISTEN_SOCKET，则 pvOptionValue 必须指向一个 
  BaseType_t 类型的变量，该变量设置为 1 表示监听套接字应被重新用于处理传入的连接， 
  设置为 0 表示监听套接字应创建一个新套接字来处理每个 
  传入的连接。

  对于可重复使用的套接字，可选择调用 FreeRTOS_accept()。还可以通过调用 FreeRTOS_connected() 
  来确定套接字是否已连接。建议调用 FreeRTOS_accept()，因为它标志着 
  从未连接更改为已连接。

  成功后，FreeRTOS_accept() 将返回已连接的父套接字的引用。 
  现在它被标记为已接受，并停止监听新连接。

  连接结束时，必须通过调用 FreeRTOS_closesocket() 关闭套接字。之后， 
  可创建一个新套接字并将其绑定到同一端口。

  用法示例：

  ```c
  BaseType_t xReuseSocket = pdTRUE;
  FreeRTOS_setsockopt( xSocket,
                       0,
                       FREERTOS_SO_REUSE_LISTEN_SOCKET,
                       ( void * ) &xReuseSocket,
                       sizeof( xReuseSocket ) );
  ```
  *将重复使用选项设置为 "true" 的示例*


+ FREERTOS_SO_CLOSE_AFTER_SEND

  仅限高级用户。

  仅对 TCP 套接字有效。

  FREERTOS_SO_CLOSE_AFTER_SEND TCP 允许在发送完最后一个数据后 
  立即关闭套接字。在发送文件的 FTP 中，此选项很有用。在最后一次调用 
  FreeRTOS_send() 之前设置该选项，以便堆栈知道最后一个数据包必须包含
  FIN 标志。堆栈将确保只有在最后一个字节传送完毕并得到对等方确认后， 
  连接才会关闭。

  如果 lOptionName 为 FREERTOS_SO_CLOSE_AFTER_SEND，那么 pvOptionValue 必须指向一个
  BaseType_t 类型的变量，该变量被设置为 1 表示套接字应在最后一个数据发送完毕后关闭， 
  设置为 0 表示套接字应使用其默认行为，即保持套接字打开状态， 
  直到任一对等方明确表示。

  用法示例：

  ```c
  BaseType_t xCloseAfterNextSend = pdTRUE;
  FreeRTOS_setsockopt( xSocket,
                       0,
                       FREERTOS_SO_CLOSE_AFTER_SEND,
                       ( void * ) &xCloseAfterNextSend,
                       sizeof( xCloseAfterNextSend ) );
  ```
  *使用 FREERTOS_SO_CLOSE_AFTER_SEND 参数的示例*


+ FREERTOS_SO_SET_FULL_SIZE

  仅限高级用户。

  仅对 TCP 套接字有效。

  FREERTOS_SO_SET_FULL_SIZE 选项告诉 TCP/IP 堆栈， 
  在至少有一个完整 [MSS](../TCP_IP_Configuration#ipconfigTCP_MSS) 大小的数据准备好发送之前， 
  不要从套接字发送任何数据。该选项可用于提高性能，但必须谨慎使用。该 
  选项不会过期，因此请确保在最后一次发送时关闭该选项， 
  这样最后一个字节（小于 MSS）也会被发送。

  如果 lOptionName 为 FREERTOS_SO_SET_FULL_SIZE，那么 pvOptionValue 必须指向一个
  BaseType_t 类型的变量，该变量设置为 1 表示套接字只有在至少有 MSS 字节等待发送时才发送， 
  设置为 0 表示套接字应使用默认行为。


+ FREERTOS_SO_STOP_RX
  
  仅限高级用户。

  仅对 TCP 套接字有效。

  TCP 套接字会不断向其对等方公布窗口大小， 
  以便对等方知道在等待确认之前可以发送多少字节。这一切都会自动根据 
  低水位和高水位发生。

  FREERTOS_SO_STOP_RX 会强制套接字公布一个零窗口， 
  使套接字暂时停止接收数据。

  如果 lOptionName 为 FREERTOS_SO_STOP_RX，那么 pvOptionValue 必须指向一个 BaseType_t 类型的变量， 
  该变量被设置为 1 表示套接字应将窗口大小设为 0，设置为 0 表示 
  套接字应使用默认行为。

  ```c
  BaseType_t xValue = pdTRUE;

  /* Temporarily advertise a window size of 0 to stop
  reception of data */
  FreeRTOS_setsockopt( xSocket,
                       0,
                       FREERTOS_SO_STOP_RX,
                       ( void * ) &xValue,
                       sizeof( xValue ) );
  {
      /* Do what ever you need to do. */
  }
  
  xValue = pdFALSE;
  
  /* Allow further reception */
  FreeRTOS_setsockopt( xSocket,
                       0,
                       FREERTOS_SO_STOP_RX,
                       ( void * ) &xValue,
                       sizeof( xValue ) );
  ```
  *使用 FREERTOS_SO_STOP_RX 参数的示例*


+ FREERTOS_SO_UDP_MAX_RX_PACKETS
  
  仅对 UDP 套接字有效，且 [ipconfigUDP_MAX_RX_PACKETS](../TCP_IP_Configuration#ipconfigUDP_MAX_RX_PACKETS) 必须
  在 FreeRTOSIPConfig.h 中设置为 1。

  使用参数 ipconfigUDP_MAX_RX_PACKETS 可以 
  限制一个 UDP 套接字中存储的最大数据包数量。该选项可以更改对单个套接字的限制。

  如果 lOptionName 为 FREERTOS_SO_UDP_MAX_RX_PACKETS，那么 pvOptionValue 必须指向一个
  BaseType_t 类型的变量，该变量用于保存 UDP 套接字上可排队等待的最大 RX 数据包数。

  ```c
  /* Allow a maximum of ten packets. */
  BaseType_t xValue = 10;
  
  FreeRTOS_setsockopt( xSocket,
                       0,
                      FREERTOS_SO_UDP_MAX_RX_PACKETS,
                      ( void * ) &xValue,
                      sizeof( xValue ) );
  ```
  *使用 FREERTOS_SO_UDP_MAX_RX_PACKETS 参数的示例、*


+ FREERTOS_SO_TCP_CONNECT_HANDLER

  仅限高级用户。

  仅对 TCP 套接字有效。

  存储 TCP 套接字上发生连接和断开事件时调用的函数的地址。


+ FREERTOS_SO_TCP_RECV_HANDLER

  仅限高级用户。

  仅对 TCP 套接字有效。

  存储 TCP 套接字收到数据时调用的函数的地址。


+ FREERTOS_SO_TCP_SENT_HANDLER

  仅限高级用户。

  仅对 TCP 套接字有效。

  存储当发送到 TCP 套接字的数据已送达并经对等方确认后调用的函数的地址 
  。


+ FREERTOS_SO_UDP_RECV_HANDLER

  仅限高级用户。

  仅对 UDP 套接字有效。

  存储 UDP 套接字接收到数据后立即调用的函数的地址。


+ FREERTOS_SO_UDP_SENT_HANDLER
  
  仅限高级用户。

  仅对 UDP 套接字有效。

  存储在数据发送到 UDP 套接字后立即调用的函数的地址。

