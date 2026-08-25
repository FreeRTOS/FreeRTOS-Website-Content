---
title: Transport Interface
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


## Introduction

[coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) and [coreHTTP](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/01-coreHTTP) has no dependency on any particular TCP/IP stack.
Therefore, in order to use either the coreMQTT or coreHTTP library, you'll need to provide a Transport
Interface structure. An instance of the Transport Interface contains function pointers and context data
required to send and receive data on a single network connection. The FreeRTOS distribution
includes [example implementations](#example-implementations) of the Transport Interface which you can use in your applications.


## Custom Implementations

Applications can provide their own implementation of the Transport Interface if
the [example implementations](#example-implementations) don't match the underlying network or TLS stack. An implementation
has two parts. The first is the definition of a network context data structure that wraps an underlying
data stream, such as a socket handle or a TLS context. The second is a pair of functions that can send
and receive data on that network context - these two functions just wrap whichever network send and
receive functions you are already using within functions that have the prototype expected by the transport
interface structure. There is a [worked example](#worked-example) below.

The Transport Interface structure is defined as follows:

```c
/*
 * The NetworkContext is an incomplete type. An implementation of this
 * interface must define struct NetworkContext for the system's requirements.
 * For example, a plain-text implementation of the NetworkContext type might
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
*Transport Interface Structure*


## Worked Example

This example describes how to create a transport interface for the FreeRTOS-Plus-TCP stack (this is
for demonstration purposes only as the FreeRTOS source code download already contains a transport interface
for FreeRTOS-Plus-TCP). For simplicity the example is using TCP without TLS or other form of
encryption. **Production IoT devices should always use encrypted connections** and the FreeRTOS
download [includes transport interfaces that use FreeRTOS-Plus-TCP with TLS stacks](#example-implementations).


### Starting point

It is recommended to ensure your application is able to successfully send and
receive from the network before creating a network transport interface - that
way the transport interface is just wrapping send and receive functions that are
already working.


### Defining the NetworkContext structure

FreeRTOS-Plus-TCP [sockets](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket)
are stored in variables of type Socket\_t. So the NetworkContext structure
can be defined as:

```c
/* The network context just contains the FreeRTOS-Plus-TCP socket
 * (Note: production systems should use TLS, not just the underlying
 * socket, so could use the TLS context here instead of the socket) */
struct NetworkContext
{
    Socket_t tcpSocket;
};
```
*Defining a NetworkContext structure that just contains a FreeRTOS-Plus-TCP socket.*


### Implementing the send and receive wrappers

Next, the FreeRTOS-Plus-TCP [send](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/07-send)
and [receive](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/09-recv) functions need to
be wrapped by functions that have the prototype expected by the transport interface's
send and receive functions. The example below also demonstrates how to obtain the socket used
by the send and receive functions from the NetworkContext parameter:

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
*Implementing the transport send and receive functions for FreeRTOS-Plus-TCP*


### Populating the TransportInterface\_t structure

Finally, the code below shows how to populate the transport interface structure
with the NetworkContext structure, and transport\_send() and transport\_recv() functions defined above:

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
*Defines the NetworkContext declared in transport\_interface.h*


## Example Implementations

[Examples for both plain-text and TLS communication are included](https://github.com/FreeRTOS/FreeRTOS/tree/master/FreeRTOS-Plus/Source/Application-Protocols/network_transport).
We strongly recommend that production applications use TLS for communication. This provides a Transport
Interface which is both authenticated and encrypted, as demonstrated in
the [MQTT TLS demo](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication).

The transport interface implementations included in the FreeRTOS download are split into two files -
a wrapper C file specific to the TCP stack, and a supplemental C file specific to using a TLS stack with
the selected TCP stack. For example, to use FreeRTOS-Plus-TCP with mbedTLS, build sockets\_wrapper.c from
the [network\_transport/freertos\_plus\_tcp directory](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Source/Application-Protocols/network_transport)
in the source code distribution, then build using\_mbedtls.c from the using\_mbedtls subdirectory.
