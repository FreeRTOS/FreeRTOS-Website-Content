---
title: 传输接口
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


## 简介

[coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) 和 [coreHTTP](http/index.md) 不依赖于任何特定的 TCP/IP 堆栈。 
因此，您需提供传输接口结构体才能使用 coreMQTT 或 coreHTTP 库 
。传输接口的实例包含 
在单个网络连接上发送和接收数据所需的函数指针和上下文数据。FreeRTOS 发行版 
包括传输接口的[示例实现](#示例实现)，您可在您的应用程序中使用此实现。


## 自定义实现

如果 
[示例实现](#示例实现)与底层网络或 TLS 协议栈不匹配，应用程序可以提供自己的传输接口实现。实现 
由两部分组成。第一部分是包装底层数据流 
（例如，套接字句柄或 TLS 上下文）的网络上下文数据结构体的定义。第二部分是 
一对可以在该网络上下文中发送和接收数据的函数——这两个函数只是将您已经在使用的网络发送和接收函数 
封装在具有传输接口结构体所期望的原型的函数中 
。下文展示了一个[有效示例](#有效示例)。

传输接口结构体定义如下：

```c
/*  
 * The NetworkContext is an incomplete type. An implementation of this  
 * interface must define struct NetworkContext for the system's requirements.  
 * For example, a plain-text implemention of the NetworkContext type might  
 * include a socket, and a TLS implementation might add a TLS context. This  
 * context is passed into the network interface send() and recv() functions.  
 */  
struct NetworkContext;  
typedef struct NetworkContext NetworkContext_t;  
  
/*  
 * @brief Transport interface for receiving data on the network.  
 *  
 * @note It is RECOMMENDED that the transport receive implementation  
 * does NOT block when requested to read a single byte. A single byte  
 * read request can be made by the caller to check whether there is a  
 * new frame available on the network for reading.  
 * However, the receive implementation MAY block for a timeout period when  
 * it is requested to read more than 1 byte. This is because once the caller  
 * is aware that a new frame is available to read on the network, then  
 * the likelihood of reading more than one byte over the network becomes high.  
 *  
 * @param[in, out] pNetworkContext Implementation-defined network context.  
 * @param[in, out] pBuffer Buffer to receive the data into.  
 * @param[in] bytesToRecv Number of bytes requested from the network.  
 *  
 * @return The number of bytes received or a negative value to indicate  
 * error.  
 *  
 * @note If no data is available on the network to read and no error  
 * has occurred, zero MUST be the return value. A zero return value  
 * SHOULD represent that the read operation can be retried by calling  
 * the API function. Zero MUST NOT be returned if a network disconnection  
 * has occurred.  
 */  
typedef int32_t ( * TransportRecv_t )( NetworkContext_t * pNetworkContext,  
                                       void * pBuffer,  
                                       size_t bytesToRecv );  
  
/*  
 * @brief Transport interface for sending data over the network.  
 *  
 * @note It is RECOMMENDED that a non-fatal failure in transmitting bytes over  
 * the network, like a full transmit buffer of the underlying TCP stack, is  
 * treated as a retriable error operation by returning a zero return value.  
 *  
 * @param[in, out] pNetworkContext Implementation-defined network context.  
 * @param[in] pBuffer Buffer containing the bytes to send over the network.  
 * @param[in] bytesToSend Number of bytes to send over the network.  
 *  
 * @return The number of bytes sent or a negative value to indicate error.  
 *  
 * @note If no data is transmitted over the network and no network error  
 * has occurred, this MUST return zero as the return value.  
 * A zero return value SHOULD represent that the send operation can be retried  
 * by calling the API function. Zero MUST NOT be returned if a network   
 * disconnection has occurred.  
 */  
typedef int32_t ( * TransportSend_t )( NetworkContext_t * pNetworkContext,  
                                       const void * pBuffer,  
                                       size_t bytesToSend );  
  
typedef struct TransportInterface  
{  
    TransportRecv_t recv;               /* Receive function (see above) */  
    TransportSend_t send;               /* Send function (see above) */   
    NetworkContext_t * pNetworkContext; /* Network context (see above) */  
} TransportInterface_t;  

```
*传输接口结构体*


## 有效示例

本示例介绍了如何创建适用于 FreeRTOS-Plus-TCP 堆栈的传输接口 
（此示例仅作为展示使用，因为 FreeRTOS 源代码下载文件已包含适用于 
FreeRTOS-Plus-TCP 的传输接口）。为简单起见，本示例中使用的 TCP 不含 TLS 或其他 
加密形式。**生产 IoT 设备应始终使用加密连接**，FreeRTOS 
下载[包括使用 FreeRTOS-Plus-TCP 和 TLS 堆栈的传输接口](#示例实现)。


### 起点

在创建网络传输接口前，请务必确保您的应用程序可以
成功发送和接收网络上的数据——
如此一来，传输接口仅包装已在运行的发送和接收函数
。


### 定义 NetworkContext 结构体

FreeRTOS-Plus-TCP [套接字](FreeRTOS-Plus/FreeRTOS_Plus_TCP/socket.md)
存储在 Socket_t  类型的变量中。因此，NetworkContext 结构体
可定义为：

```c
/* The network context just contains the FreeRTOS-Plus-TCP socket   
 * (Note: production systems should use TLS, not just the underlying   
 * socket, so could use the TLS context here instead of the socket) */  
struct NetworkContext  
{  
    Socket_t tcpSocket;  
};
```
*定义仅包含 FreeRTOS-Plus-TCP 套接字的 NetworkContext 结构体。*


### 实现发送和接收包装器

接下来，FreeRTOS-Plus-TCP [发送](FreeRTOS-Plus/FreeRTOS_Plus_TCP/API/send.md) 
和[接收](FreeRTOS-Plus/FreeRTOS_Plus_TCP/API/recv.md)函数需要
由具有传输接口发送和接收函数所需的原型的函数来包装
。下述示例还演示了如何
从 NetworkContext 参数中获取发送和接收函数使用的套接字：

```c
/* The prototypes of the following send and receive functions match that  
   expected by the transport interface's function pointers. These simple  
   implementations show how to use the network context structure defined  
   above. */  

int32_t transport_recv( NetworkContext_t * pNetworkContext,  
                        void * pBuffer,  
                        size_t bytesToRecv )  
{  
    int32_t socketStatus = 1;  
  
    /* The TCP socket may have a receive block time. If bytesToRecv is greater   
     * than 1, then a frame is likely already part way through reception and   
     * blocking to wait for the desired number of bytes to be available is the  
     * most efficient thing to do. If bytesToRecv is 1, then this may be a   
     * speculative call to read to find the start of a new frame, in which case   
     * blocking is not desirable as it could block an entire protocol agent   
     * task for the duration of the read block time and therefore negatively   
     * impact performance. So if bytesToRecv is 1, then don't call recv unless   
     * it is known that bytes are already available. */  
    if( bytesToRecv == 1 )  
    {  
        socketStatus = ( int32_t ) FreeRTOS_recvcount( pPlaintextTransportParams->tcpSocket );  
    }  
     
    if( socketStatus > 0 )  
    {  
        socketStatus = FreeRTOS_recv( pNetworkContext->tcpSocket, pBuffer, bytesToRecv, 0 );  
    }  
  
    return socketStatus;  
}  
  
int32_t transport_send( NetworkContext_t * pNetworkContext,  
                        const void * pBuffer,  
                        size_t bytesToSend )  
{  
    int32_t socketStatus;  
  
    socketStatus = FreeRTOS_send( pNetworkContext->tcpSocket, pBuffer, bytesToSend, 0 );  
  
    if( socketStatus == -pdFREERTOS_ERRNO_ENOSPC )  
    {  
       /* The TCP buffers could not accept any more bytes so zero bytes were sent.  
        * This is not necessarily an error that should cause a disconnect unless  
        * it persists so return 0 bytes received rather than an error. */  
        socketStatus = 0;  
    }  
  
    return socketStatus;  
}  

```
*实现适用于 FreeRTOS-Plus-TCP* 的传输发送和接收函数

  
### 填充 TransportInterface_t 结构体

最后，下述代码显示了如何
用 NetworkContext 结构体，以及上文定义的 transport_send () 和  transport_recv () 函数填充传输接口结构体的过程：

```c
/* Populating the TransportInterface_t structure with the definitions above. */  
void init_transport_from_socket( Socket_t tcpSocket,  
                                 NetworkContext_t * pNetworkContext,  
                                 TransportInterface_t * pTransport )  
{  
    pNetworkContext->tcpSocket = tcpSocket;  
    pTransport->recv = transport_recv;  
    pTransport->send = transport_send;  
    pTransport->pNetworkContext = pNetworkContext;  
}  

```
*定义 transport_interface.h 中声明的网络上下文*

  
## 示例实现

[包括明文通信和 TLS 通信的示例](https://github.com/FreeRTOS/FreeRTOS/tree/master/FreeRTOS-Plus/Source/Application-Protocols/network_transport)。 
我们强烈建议生产应用程序使用 TLS 进行通信。它所提供的传输 
接口经过身份验证，并被加密过，正如 
[MQTT TLS 演示](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication)所展示的那样。 

FreeRTOS 下载中包含的传输接口实现分为两个文件： 
一个是专门针对 TCP 堆栈的包装器 C 文件， 
另一个是专门针对使用 TLS 堆栈和所选 TCP 堆栈的补充 C 文件。例如，要将 FreeRTOS-Plus-TCP 与 mbedTLS 结合使用， 
请在源代码发布版的 [network_transport/freertos_plus_tcp 目录](https://github.com/FreeRTOS/FreeRTOS/tree/master/FreeRTOS-Plus/Source/Application-Protocols/network_transport/freertos_plus_tcp)中编译 sockets_wrapper.c， 
然后在 using_mbedtls 子目录中编译 using_mbedtls.c。

