---
title: coreHTTP Demo (without TLS)
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


* On this Page
	+ [Introduction](#introduction)
		- [Single Threaded vs. Multi Threaded](#single-threaded-vs-multi-threaded)
	+ [Source Code Organization](#source-code-organization)
	+ [Configuring the Demo Project](#configuring-the-demo-project)
	+ [Configuring the HTTP server Connection](#configuring-the-http-server-connection)
		- [Option 1: Using a publicly hosted HTTP server](#option-1-using-a-publicly-hosted-http-server)
		- [Option 2: Using a locally hosted HTTP server](#option-2-using-a-locally-hosted-http-server)
		- [Option 3: Any other unencrypted HTTP server of your choosing:](#option-3-any-other-unencrypted-http-server-of-your-choosing)
	+ [Building the Demo Project](#building-the-demo-project)
	+ [Functionality](#functionality)
		- [Connecting to the HTTP server](#connecting-to-the-http-server)
		- [Sending an HTTP request and receiving the response](#sending-an-http-request-and-receiving-the-response)


**Notice: We recommend that you use mutual authentication in any Internet of
Things (IoT) application. The demo on this page is only meant for educational purposes because it demonstrates
HTTP communication prior to introducing encryption and authentication. It is not intended to be suitable for
production use.**


## Introduction

This demo shows how to use the coreHTTP library to establish a connection with an HTTP server to demonstrate
a simple request/response workflow. After it creates a request, the request is sent, and the demo synchronously
waits for the response to be received.

This example project introduces the concepts described on the ["TLS Introduction"](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/02-TLS-introduction)
page one at a time. The first example (this page) demonstrates unencrypted HTTP communication.
The [second example](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/03-coreHTTP-demos/02-Mutual-authentication) builds on this to introduce strong mutual
authentication (where the HTTP server also authenticates the IoT client connecting to it).

This demo **does not** create a secure connection and therefore it is not suitable for production use -
do not send any confidential information on an unencrypted network connection. The demo demonstrates how to
connect using an exponential backoff time (including timing jitter) in case of a connection failure. Exponentially
increasing the time between connection attempts, and including some random timing jitter, are best practices for
large IoT device fleets because it prevents all the IoT devices attempting to reconnect at the same time if they
all became disconnected at the same time.


This basic HTTP demo project uses
the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW),
so it can be built and evaluated with
the [free Community version of Visual Studio](https://visualstudio.microsoft.com/vs/community/) on Windows,
without the need for any particular MCU hardware.

The coreHTTP library is an [MIT licensed](/Documentation/03-Libraries/01-Library-overview/04-Licensing), open source HTTP client C library for microcontroller
and small microprocessor based IoT devices.


### Single Threaded Vs Multi Threaded

There are two coreHTTP usage models, *single threaded* and *multithreaded* (multitasking). Although
the demo on this page runs the HTTP library in a thread, it actually demonstrates how to use coreHTTP in a
single threaded environment (that is, only one task uses the HTTP API in the demo). Although single threaded
applications must repeatedly call the HTTP library, multithreaded applications can instead send HTTP requests
in the background within an agent (or daemon) task.


## Source Code Organization

The demo project is called `http_plain_text_demo.sln` and can be found in
the `FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_Plaintext` directory of
the [main FreeRTOS download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) (and it can be found in Github, linked from the download
page).


## Configuring the Demo Project

The demo uses the [FreeRTOS-Plus-TCP TCP/IP stack](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP), so follow
the instructions provided for
the [TCP/IP starter project](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator) to ensure you:


1. Have the [pre-requisite components installed](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites) (such as WinPCap).

2. Optionally [set a static or dynamic IP address, gateway address and netmask](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic).

3. Optionally [set a MAC address](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr).

4. [Select an Ethernet network interface](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface) on your host machine.

5. …and **importantly** [test your network connection](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#connectivity-test) before you attempt to run the HTTP demo.

Each demo project has its own configuration settings. So when you follow these network configuration
instructions, make sure to apply the settings in the HTTP demo project only, and not in the TCP/IP starter
project. By default, the TCP/IP stack is configured to use a dynamic IP address.


## Configuring the HTTP server Connection

### Option 1: Using a publicly hosted HTTP server

The demo project can communicate with the publicly hosted HTTP server at "httpbin.org". This should
work if the demo connects to a network that has a DHCP service and Internet access. Note that the FreeRTOS
Windows port only works with a wired Ethernet network adapter, which can be a virtual Ethernet adapter.
You should use a separate HTTP client, such as your current web browser, to test the HTTP connection from
your host machine to the public HTTP server. To use the hosted HTTP server:

1. Open your local copy of `/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_Plaintext/demo_config.h`.

2. Add the following lines:

   ```c
   #define democonfigSERVER_HOSTNAME "httpbin.org"
   #define democonfigHTTP_PORT ( 80 )
   ```

**Note**: httpbin is an open source HTTP server that supports HTTP/1.1. It is part of Postmanlabs and
can be found [here](https://github.com/postmanlabs/httpbin). The httpbin.org server is not affiliated
with, or maintained by, FreeRTOS and may be unavailable at any time.


### Option 2: Using a locally hosted HTTP server

The httpbin server can also run locally, or on another machine on your local network. To do this:

1. Install [Docker](https://docs.docker.com/docker-for-windows/install/).

2. Run httpbin from port 80 using the following commands:

   ```c
   docker pull kennethreitz/httpbin
   docker run -p 80:80 kennethreitz/httpbin
   ```

3. Verify that the httpbin server is running locally and listening on port 8080 by following these steps:

   1. Open PowerShell.
   2. To check if there is an active connection listening on port 80, type in the command

      ```c
      netstat -a -p TCP | findstr 80
      ```
   3. Verify that you see output like this:

      ```c
      TCP    0.0.0.0:80           <HOST-NAME>:0       LISTENING
      ```

4. Open `FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_Plaintext/demo_config.h`.

5. Add the following lines:

   ```c
   #define democonfigSERVER_HOSTNAME "ipv4_address_of_your_machine"
   #define democonfigHTTP_PORT ( 80 )
   ```

   You should use a separate HTTP client, such as your web browser, to test the HTTP connection from your
   host machine to the installed HTTP client.

   **Note:** Port number 80 is the default port number for unencrypted HTTP. If you cannot use that
   port (for example, if it is blocked by your IT security policy or used by another system process in Windows), then
   change the port used by the docker container to a high port number (for example, something in the 50000 to 55000
   range), and set `democonfigHTTP_PORT` accordingly. To make this change, you can run

   ```c
   docker run -p *<HIGH\_PORT\_NUMBER>*:80 kennethreitz/httpbin
   ```


### Option 3: Any other unencrypted HTTP server of your choosing:

Any HTTP server that supports unencrypted TCP/IP communication can also be used with this demo. To do this:

1. Open your local copy of `/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_Plaintext/demo_config.h`.

2. Add the following lines with settings specific to your chosen server:

   ```c
   #define democonfigSERVER_HOSTNAME "your-desired-endpoint"
   #define democonfigHTTP_PORT ( 80 )
   ```


## Building the Demo Project

The demo project uses the [free community edition of Visual Studio](https://visualstudio.microsoft.com/vs/community/).
To build the demo:

1. Open the `/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_Plaintext/http_plain_text_demo.sln`
   Visual Studio solution file from within the Visual Studio IDE

2. Select '**build solution**' from the IDE's '**build**' menu.


## Functionality

The demo creates a single application task that demonstrates how to:

* connect to the AWS IoT HTTP server,
* create an HTTP request,
* send the HTTP request and
* receive the HTTP response, then finally,
* disconnect from the server.

The structure of the demo is:

```c
static void prvHTTPDemoTask( void * pvParameters )
{
    /* The transport layer interface used by the HTTP Client library. */
    TransportInterface_t xTransportInterface;
    /* The network context for the transport layer interface. */
    NetworkContext_t xNetworkContext = { 0 };
    PlaintextTransportParams_t xPlaintextTransportParams = { 0 };
    /* An array of HTTP paths to request. */
    const httpPathStrings_t xHttpMethodPaths[] =
    {
        { democonfigGET_PATH,  httpexampleGET_PATH_LENGTH  },
        { democonfigHEAD_PATH, httpexampleHEAD_PATH_LENGTH },
        { democonfigPUT_PATH,  httpexamplePUT_PATH_LENGTH  },
        { democonfigPOST_PATH, httpexamplePOST_PATH_LENGTH }
    };
    /* The respective method for the HTTP paths listed in #httpMethodPaths. */
    const httpMethodStrings_t xHttpMethods[] =
    {
        { HTTP_METHOD_GET,  httpexampleHTTP_METHOD_GET_LENGTH  },
        { HTTP_METHOD_HEAD, httpexampleHTTP_METHOD_HEAD_LENGTH },
        { HTTP_METHOD_PUT,  httpexampleHTTP_METHOD_PUT_LENGTH  },
        { HTTP_METHOD_POST, httpexampleHTTP_METHOD_POST_LENGTH }
    };
    BaseType_t xIsConnectionEstablished = pdFALSE;
    UBaseType_t uxHttpPathCount = 0U;

    /* The user of this demo must check the logs for any failure codes. */
    BaseType_t xDemoStatus = pdPASS;

    /* Remove compiler warnings about unused parameters. */
    ( void ) pvParameters;

    /* Set the pParams member of the network context with desired transport. */
    xNetworkContext.pParams = &xPlaintextTransportParams;


    /**************************** Connect. ******************************/


    /* Attempt to connect to the HTTP server. If connection fails, retry after a
     * timeout. The timeout value will be exponentially increased until either the
     * maximum number of attempts or the maximum timeout value is reached. The
     * function returns pdFAIL if the TCP connection cannot be established with
     * the server after the number of attempts. */
    xDemoStatus = connectToServerWithBackoffRetries( prvConnectToServer,
                                                     &xNetworkContext );

    if( xDemoStatus == pdPASS )
    {
        /* Set a flag indicating that a TCP connection has been established. */
        xIsConnectionEstablished = pdTRUE;

        /* Define the transport interface. */
        xTransportInterface.pNetworkContext = &xNetworkContext;
        xTransportInterface.send = Plaintext_FreeRTOS_send;
        xTransportInterface.recv = Plaintext_FreeRTOS_recv;
    }
    else
    {
        /* Log error to indicate connection failure after all
         * reconnect attempts are over. */
        LogError( ( "Failed to connect to HTTP server %.*s.",
                    ( int32_t ) httpexampleSERVER_HOSTNAME_LENGTH,
                    democonfigSERVER_HOSTNAME ) );
    }


    /*********************** Send HTTP request.************************/


    for( uxHttpPathCount = 0;
         uxHttpPathCount < httpexampleNUMBER_HTTP_PATHS;
         ++uxHttpPathCount )
    {
        if( xDemoStatus == pdPASS )
        {
            xDemoStatus = prvSendHttpRequest(
                              &xTransportInterface,
                              xHttpMethods[ uxHttpPathCount ].pcHttpMethod,
                              xHttpMethods[ uxHttpPathCount ].ulHttpMethodLength,
                              xHttpMethodPaths[ uxHttpPathCount ].pcHttpPath,
                              xHttpMethodPaths[ uxHttpPathCount ].ulHttpPathLength );
        }
        else
        {
            break;
        }
    }


    /**************************** Disconnect. ******************************/


    /* Close the network connection to clean up any system resources that the
     * demo may have consumed. */
    if( xIsConnectionEstablished == pdTRUE )
    {
        /* Close the network connection. */
        Plaintext_FreeRTOS_Disconnect( &xNetworkContext );
    }


    if( xDemoStatus == pdPASS )
    {
        LogInfo( ( "prvHTTPDemoTask() completed successfully. "
                   "Total free heap is %u.\r\n",
                   xPortGetFreeHeapSize() ) );
        LogInfo( ( "Demo completed successfully.\r\n" ) );
    }
}
```


### Connecting to the HTTP server

In the function above, `connectToServerWithBackoffRetries()` attempts to make a TCP connection to the
HTTP server. If the connection fails, it retries after a timeout. The timeout value will exponentially
increase and include some randomised jitter until the maximum number of attempts are reached or the
maximum timeout value is reached. This type of backoff is used in production devices to ensure that if
a fleet of IoT devices all get disconnected at the same time, they do not all try to re-connect at the
same time - and, in so doing, overwhelm the server. If the connection is successful, then the connected
TCP socket is returned in the `xNetworkContext` parameter.

The function `prvConnectToServer()` demonstrates how to establish an unencrypted connection to an HTTP
server. It uses the FreeRTOS-Plus-TCP [transport interface](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface), which is implemented
in the file `FreeRTOS-Plus/Source/Application-Protocols/network_transport/freertos_plus_tcp/using_plaintext/using_plaintext.c`.
The definition of `prvConnectToServer()` is shown here:

```c
static BaseType_t prvConnectToServer( NetworkContext_t * pxNetworkContext )
{
    BaseType_t xStatus = pdPASS;

    PlaintextTransportStatus_t xNetworkStatus;

    configASSERT( pxNetworkContext != NULL );

    /* Establish a TCP connection with the HTTP server. This example connects
     * to the HTTP server as specified in democonfigSERVER\_HOSTNAME and
     * democonfigHTTP\_PORT in demo\_config.h. */
    LogInfo( ( "Establishing a TCP connection to %.*s:%d.",
               ( int32_t ) httpexampleSERVER_HOSTNAME_LENGTH,
               democonfigSERVER_HOSTNAME,
               democonfigHTTP_PORT ) );
    xNetworkStatus = Plaintext_FreeRTOS_Connect(
                         pxNetworkContext,
                         democonfigSERVER_HOSTNAME,
                         democonfigHTTP_PORT,
                         democonfigTRANSPORT_SEND_RECV_TIMEOUT_MS,
                         democonfigTRANSPORT_SEND_RECV_TIMEOUT_MS );

    if( xNetworkStatus != PLAINTEXT_TRANSPORT_SUCCESS )
    {
        xStatus = pdFAIL;
    }

    return xStatus;
}
```


### Sending an HTTP request and receiving the response

The function `prvSendHttpRequest()` demonstrates how to create an HTTP request then send it to
the server. The response is received synchronously in the same API call to `HTTPClient_Send()`.

```c
static BaseType_t prvSendHttpRequest(
                      const TransportInterface_t * pxTransportInterface,
                      const char * pcMethod,
                      size_t xMethodLen,
                      const char * pcPath,
                      size_t xPathLen )
{
    /* Return value of this method. */
    BaseType_t xStatus = pdPASS;

    /* Configurations of the initial request headers that are passed to
     * #HTTPClient\_InitializeRequestHeaders. */
    HTTPRequestInfo_t xRequestInfo;
    /* Represents a response returned from an HTTP server. */
    HTTPResponse_t xResponse;
    /* Represents header data that will be sent in an HTTP request. */
    HTTPRequestHeaders_t xRequestHeaders;

    /* Return value of all methods from the HTTP Client library API. */
    HTTPStatus_t xHTTPStatus = HTTPSuccess;

    configASSERT( pcMethod != NULL );
    configASSERT( pcPath != NULL );

    /* Initialize all HTTP Client library API structs to 0. */
    ( void ) memset( &xRequestInfo, 0, sizeof( xRequestInfo ) );
    ( void ) memset( &xResponse, 0, sizeof( xResponse ) );
    ( void ) memset( &xRequestHeaders, 0, sizeof( xRequestHeaders ) );

    /* Initialize the request object. */
    xRequestInfo.pHost = democonfigSERVER_HOSTNAME;
    xRequestInfo.hostLen = httpexampleSERVER_HOSTNAME_LENGTH;
    xRequestInfo.pMethod = pcMethod;
    xRequestInfo.methodLen = xMethodLen;
    xRequestInfo.pPath = pcPath;
    xRequestInfo.pathLen = xPathLen;

    /* Set "Connection" HTTP header to "keep-alive" so that multiple requests
     * can be sent over the same established TCP connection. */
    xRequestInfo.reqFlags = HTTP_REQUEST_KEEP_ALIVE_FLAG;

    /* Set the buffer used for storing request headers. */
    xRequestHeaders.pBuffer = ucUserBuffer;
    xRequestHeaders.bufferLen = democonfigUSER_BUFFER_LENGTH;

    xHTTPStatus = HTTPClient_InitializeRequestHeaders( &xRequestHeaders,
                                                       &xRequestInfo );

    if( xHTTPStatus == HTTPSuccess )
    {
        /* Initialize the response object. The same buffer used for storing
         * request headers is reused here. */
        xResponse.pBuffer = ucUserBuffer;
        xResponse.bufferLen = democonfigUSER_BUFFER_LENGTH;

        LogInfo( ( "Sending HTTP %.*s request to %.*s%.*s...",
                   ( int32_t ) xRequestInfo.methodLen, xRequestInfo.pMethod,
                   ( int32_t ) httpexampleSERVER_HOSTNAME_LENGTH, democonfigSERVER_HOSTNAME,
                   ( int32_t ) xRequestInfo.pathLen, xRequestInfo.pPath ) );
        LogInfo( ( "Request Headers:\n%.*s\n"
                   "Request Body:\n%.*s\n",
                   ( int32_t ) xRequestHeaders.headersLen,
                   ( char * ) xRequestHeaders.pBuffer,
                   ( int32_t ) httpexampleREQUEST_BODY_LENGTH, democonfigREQUEST_BODY ) );

        /* Send the request and receive the response. */
        xHTTPStatus = HTTPClient_Send( pxTransportInterface,
                                       &xRequestHeaders,
                                       ( uint8_t * ) democonfigREQUEST_BODY,
                                       httpexampleREQUEST_BODY_LENGTH,
                                       &xResponse,
                                       0 );
    }
    else
    {
        LogError( ( "Failed to initialize HTTP request headers: Error=%s.",
                    HTTPClient_strerror( xHTTPStatus ) ) );
    }

    if( xHTTPStatus == HTTPSuccess )
    {
        LogInfo( ( "Received HTTP response from %.*s%.*s...\n",
                   ( int32_t ) httpexampleSERVER_HOSTNAME_LENGTH,
                   democonfigSERVER_HOSTNAME,
                   ( int32_t ) xRequestInfo.pathLen, xRequestInfo.pPath ) );
        LogDebug( ( "Response Headers:\n%.*s\n",
                    ( int32_t ) xResponse.headersLen, xResponse.pHeaders ) );
        LogDebug( ( "Status Code:\n%u\n",
                    xResponse.statusCode ) );
        LogDebug( ( "Response Body:\n%.*s\n",
                    ( int32_t ) xResponse.bodyLen, xResponse.pBody ) );
    }
    else
    {
        LogError( ( "Failed to send HTTP %.*s request to %.*s%.*s: Error=%s.",
                    ( int32_t ) xRequestInfo.methodLen,
                    xRequestInfo.pMethod,
                    ( int32_t ) httpexampleSERVER_HOSTNAME_LENGTH,
                    democonfigSERVER_HOSTNAME,
                    ( int32_t ) xRequestInfo.pathLen,
                    xRequestInfo.pPath,
                    HTTPClient_strerror( xHTTPStatus ) ) );
    }

    if( xHTTPStatus != HTTPSuccess )
    {
        xStatus = pdFAIL;
    }

    return xStatus;
}
```
