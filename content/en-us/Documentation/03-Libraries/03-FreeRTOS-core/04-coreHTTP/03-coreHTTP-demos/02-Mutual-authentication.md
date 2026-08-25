---
title: coreHTTP Demo (Mutual Authentication)
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---
**Note: We recommend to always use mutual authentication in building any Internet of Things (IoT) application.**

## Single Threaded Vs Multi Threaded

There are two coreHTTP usage models, _single threaded_ and _multithreaded_ (multitasking). Although
the demo on this page runs the HTTP library in a thread, it is actually demonstrating how to use coreHTTP
in a single threaded environment (only one task uses the HTTP API in the demo). Whereas single threaded
applications must repeatedly call the HTTP library, multithreaded applications instead can execute sending
HTTP requests in the background within an agent (or daemon) task.

## Demo Introduction

The coreHTTP (Mutual Authentication) demo uses a [network transport interface](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface)
that uses mbedTLS to establish a mutually authenticated connection between an IoT device client running
coreHTTP and a remote HTTP server. This demo can connect to any HTTP server capable of mutually authenticated
connections. Once connected the demo creates an HTTP request, then sends the request and receives the response.
The instructions below describe how to connect to
the [Amazon Web Services (AWS) IoT HTTP server](https://aws.amazon.com/iot-core/).

This example project is one of two that introduce the concepts described on
the ["TLS Introduction"](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/02-TLS-introduction) page one at a time.
The [first example](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/03-coreHTTP-demos/01-coreHTTP-demo) demonstrates unencrypted HTTP communication. The second
example (on this page) builds on the first to introduce strong mutual authentication (where the HTTP
server also authenticates the client connecting to it).

The coreHTTP (Mutual Authentication) demo project uses
the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW),
enabling it to be built and evaluated with
the [free Community version of Visual Studios](https://visualstudio.microsoft.com/vs/community/) on
Windows, so without the need for any particular MCU hardware.


## Source Code Organization

The demo project is called http_mutual_auth_demo.sln and is located in
the `FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_Mutual_Auth` directory of
the [main FreeRTOS download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) (links to Github are also on the download page).

The source code is organized as per the [basic HTTP demo (without TLS).](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/03-coreHTTP-demos/01-coreHTTP-demo)

## Configuring the HTTP Server Connection

The Mutual Authentication HTTP demo requires client authentication and server authentication.  As most
public HTTP servers do not authenticate the client, this demo will showcase a connection
to [AWS (Amazon Web Services) IoT](https://aws.amazon.com/iot-core/).  Additional steps are required
to acquire and set up credentials using existing tools provided by AWS. For enhanced security, AWS IoT
does not support plaintext and server side only authentication.
See [Security in AWS](https://docs.aws.amazon.com/freertos/latest/userguide/security.html), for more
details.

Follow the steps below for configuring your connection to AWS.

1. Set up an Amazon Web Services (AWS) account:

   - If you have not already, [create and activate an AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) (which
     includes a [free tier](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=categories%23iot)).

2. Accounts and permissions are set using [AWS Identity and Access Management (IAM)](https://aws.amazon.com/iam/).
   IAM allows you to manage the permissions for each user. By default, no users have permissions until granted
   by the root owner.

   - To add an IAM user to your AWS account, see the [IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/).
   - Set permissions for your AWS account to access FreeRTOS and AWS IoT by adding the policies below:

     - `AmazonFreeRTOSFullAccess`
     - `AWSIoTFullAccess`

   * To attach the AmazonFreeRTOSFullAccess policy to your IAM user:

     1. Browse to the [IAM console](https://console.aws.amazon.com/iam/home), and from the navigation pane, choose **Users**.
     2. Enter your user name in the search text box, and then choose it from the list.
     3. Choose **Add permissions**.
     4. Choose **Attach existing policies directly**.
     5. In the search box, enter **`AmazonFreeRTOSFullAccess`**, choose it from the list, and then choose **Next: Review**.
     6. Choose **Add permissions**.

   * To attach the AWSIoTFullAccess policy to your IAM user:

     1. Browse to the [IAM console](https://console.aws.amazon.com/iam/home) and, from the navigation pane, choose **Users**.
     2. Enter your user name in the search text box, and then choose it from the list.
     3. Choose **Add permissions**.
     4. Choose **Attach existing policies directly**.
     5. In the search box, enter **`AWSIoTFullAccess`**, choose it from the list, and then choose **Next: Review**.
     6. Choose **Add permissions**.

3. Create AWS IoT client certificates using the AWS IoT Core console.

   1. Add a device to AWS IoT Console

      Follow these [steps](https://docs.aws.amazon.com/iot/latest/developerguide/device-certs-create.html#device-certs-create-console)
      to create a private key and certificate in AWS IoT. Immediately download the certificate and private
      key created. You will also need your AWS IoT endpoint found in the following steps:

      1. Browse to the [AWS IoT console](https://console.aws.amazon.com/iotv2/).

      2. In the navigation pane, under **Connect**, choose **Domain Configurations**.

      Your AWS IoT endpoint is displayed as the **Domain Name**. It should look
      like **\<unique-identifier-for-your-AWS-IoT-account>`-ats.iot.`\<region>`.amazonaws.com`**.

   2. Once you have completed the setup on the service side, you need to configure credentials for AWS
      IoT credentials on the client side. Paste the endpoint and credentials
      into `FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_Mutual_Auth/demo_config.h`:

      1. Copy the **AWS IoT Domain Name** into `#define democonfigAWS_IOT_ENDPOINT `"\<Domain-Name>"

      2. Copy the root CA certificate that you downloaded from the AWS IoT console
         into `#define democonfigROOT_CA_PEM `"\<Root-CA>"

      3. Copy the client certificate that you downloaded from the AWS IoT console
         into `#define democonfigCLIENT_CERTIFICATE_PEM `"\<Client-Certificate>"

      4. Copy the client private key that you downloaded from the AWS IoT console
         into `#define democonfigCLIENT_PRIVATE_KEY_PEM `"\<Client-Private-Key>"

### Build the Demo Project

You build this demo project in the same way as the [basic HTTP demo (without TLS)](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/03-coreHTTP-demos/01-coreHTTP-demo#source_code).
The demo project uses the free community edition of [Visual Studio](https://visualstudio.microsoft.com/vs/community/).
To build this demo:

- Open the `FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_Mutual_Auth/http_mutual_auth_demo.sln` 
  Visual Studio solution file from within the Visual Studio IDE

- Select Build Solution from the IDE’s Build menu

**NOTE:** If you are using Microsoft Visual Studio 2017 or earlier, then you must select a Platform Toolset
compatible with your version: Project -> RTOSDemos Properties -> Platform Toolset

### Functionality

The demo provides the same functionality as the basic HTTP demo with the addition of a secure connection
to your AWS IoT endpoint.  For details on the additional functionality (creating an HTTP request, sending
the request, and receiving the response) please view the [basic HTTP demo (without TLS).](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/03-coreHTTP-demos/01-coreHTTP-demo#functionality)

The demo creates a single application task that demonstrate how to connect to the AWS IoT HTTP server,
create an HTTP request, send the HTTP request and receive the HTTP response, then finally, disconnect from
the server. The structure of the demo is shown below.

```c
static void prvHTTPDemoTask( void * pvParameters )
{
    /* The transport layer interface used by the HTTP Client library. */
    TransportInterface_t xTransportInterface;
    /* The network context for the transport layer interface. */
    NetworkContext_t xNetworkContext = { 0 };
    TlsTransportParams_t xTlsTransportParams = { 0 };
    BaseType_t xIsConnectionEstablished = pdFALSE;

    /* The user of this demo must check the logs for any failure codes. */
    BaseType_t xDemoStatus = pdPASS;

    /* Remove compiler warnings about unused parameters. */
    ( void ) pvParameters;

    /* Set the pParams member of the network context with desired transport. */
    xNetworkContext.pParams = &xTlsTransportParams;

    /**************************** Connect. ******************************/

    /* Attempt to connect to the HTTP server. If connection fails, retry after a
     * timeout. The timeout value will be exponentially increased until either the
     * maximum number of attempts or the maximum timeout value is reached. The
     * function returns pdFAIL if the TCP connection cannot be established with
     * the server after configured number of attempts. */
    xDemoStatus = connectToServerWithBackoffRetries( prvConnectToServer,
                                                     &xNetworkContext );

    if( xDemoStatus == pdPASS )
    {
        /* Set a flag indicating that a TLS connection exists. */
        xIsConnectionEstablished = pdTRUE;

        /* Define the transport interface. */
        xTransportInterface.pNetworkContext = &xNetworkContext;
        xTransportInterface.send = TLS_FreeRTOS_send;
        xTransportInterface.recv = TLS_FreeRTOS_recv;
    }
    else
    {
        /* Log error to indicate connection failure after all
         * reconnect attempts are over. */
        LogError( ( "Failed to connect to HTTP server %.*s.",
                    ( int32_t ) AWS_IOT_ENDPOINT_LENGTH,
                    democonfigAWS_IOT_ENDPOINT ) );
    }

    /*********************** Send HTTP request.************************/

    if( xDemoStatus == pdPASS )
    {
        xDemoStatus = prvSendHttpRequest( &xTransportInterface,
                                          HTTP_METHOD_POST,
                                          ( sizeof( HTTP_METHOD_POST ) - 1 ),
                                          democonfigPOST_PATH,
                                          ( sizeof( democonfigPOST_PATH ) - 1 ) );
    }

    /**************************** Disconnect. ******************************/

    /* Close the network connection to clean up any system resources that the
     * demo may have consumed. */
    if( xIsConnectionEstablished == pdTRUE )
    {
        /* Close the network connection. */
        TLS_FreeRTOS_Disconnect( &xNetworkContext );
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

### Connect to the HTTP server (with mutual authentication)

The function `connectToServerWithBackoffRetries()` attempts to make a mutually authenticated TLS connection
to the HTTP server. If the connection fails, it retries after a timeout. The timeout value will exponentially
increase until the maximum number of attempts are reached or the maximum timeout value is reached. The
function `BackoffAlgorithm_GetNextBackoff()` provides exponentially increasing timeout value and
returns `BackoffAlgorithmRetriesExhausted` when the maximum number of attempts have been
reached. `connectToServerWithBackoffRetries()` returns a failure status if the TLS connection cannot be
established to the server after the configured number of attempts.

```c
BaseType_t connectToServerWithBackoffRetries( TransportConnect_t connectFunction,
                                              NetworkContext_t * pxNetworkContext )
{
    BaseType_t xReturn = pdFAIL;
    /* Status returned by the retry utilities. */
    BackoffAlgorithmStatus_t xBackoffAlgStatus = BackoffAlgorithmSuccess;
    /* Struct containing the next backoff time. */
    BackoffAlgorithmContext_t xReconnectParams;
    uint16_t usNextBackoff = 0U;

    assert( connectFunction != NULL );

    /* Initialize reconnect attempts and interval */
    BackoffAlgorithm_InitializeParams( &xReconnectParams,
                                       RETRY_BACKOFF_BASE_MS,
                                       RETRY_MAX_BACKOFF_DELAY_MS,
                                       RETRY_MAX_ATTEMPTS );

    /* Attempt to connect to the HTTP server. If connection fails, retry after a
     * timeout. The timeout value will exponentially increase until either the
     * maximum timeout value is reached or the set number of attempts are
     * exhausted.*/
    do
    {
        xReturn = connectFunction( pxNetworkContext );

        if( xReturn != pdPASS )
        {
            LogWarn( ( "Connection to the HTTP server failed. "
                       "Retrying connection with backoff and jitter." ) );
            LogInfo( ( "Retry attempt %lu out of maximum retry attempts %lu.",
                       ( xReconnectParams.attemptsDone + 1 ),
                         RETRY_MAX_ATTEMPTS ) );

            /* Generate a random number and calculate backoff value (in milliseconds) for
             * the next connection retry.
             * Note: It is recommended to seed the random number generator with a device-specific
             * entropy source so that possibility of multiple devices retrying failed network operations
             * at similar intervals can be avoided. */
            xBackoffAlgStatus = BackoffAlgorithm_GetNextBackoff( &xReconnectParams, uxRand(), &usNextBackoff );
        }
    } while( ( xReturn == pdFAIL ) && ( xBackoffAlgStatus == BackoffAlgorithmSuccess ) );

    if( xReturn == pdFAIL )
    {
        LogError( ( "Connection to the server failed, all attempts exhausted." ) );
    }

    return xReturn;
}
```

The function `prvConnectToServer()` demonstrates how to establish an HTTP connection to a server. It
uses the TLS transport interface which is implemented in the
file `FreeRTOS-Plus/Source/Application-Protocols/network_transport/freertos_plus_tcp/using_mbedtls/using_mbedtls.c`.
The definition of `prvConnectToServer()` is shown below.

```c
static BaseType_t prvConnectToServer( NetworkContext_t * pxNetworkContext )
{
    BaseType_t xStatus = pdPASS;

    TlsTransportStatus_t xNetworkStatus;
    NetworkCredentials_t xNetworkCredentials = { 0 };

    configASSERT( pxNetworkContext != NULL );

    if( democonfigAWS_HTTP_PORT == 443 )
    {
        /* ALPN protocols must be a NULL-terminated list of strings. Therefore,
         * the first entry will contain the actual ALPN protocol string while the
         * second entry must remain NULL. */
        static const char * pcAlpnProtocols[] = { IOT_CORE_ALPN_PROTOCOL_NAME, NULL };
        xNetworkCredentials.pAlpnProtos = pcAlpnProtocols;
    }

    xNetworkCredentials.disableSni = democonfigDISABLE_SNI;
    /* Set the credentials for establishing a TLS connection. */
    xNetworkCredentials.pRootCa = ( const unsigned char * ) democonfigROOT_CA_PEM;
    xNetworkCredentials.rootCaSize = sizeof( democonfigROOT_CA_PEM );
    xNetworkCredentials.pClientCert = ( const unsigned char * ) democonfigCLIENT_CERTIFICATE_PEM;
    xNetworkCredentials.clientCertSize = sizeof( democonfigCLIENT_CERTIFICATE_PEM );
    xNetworkCredentials.pPrivateKey = ( const unsigned char * ) democonfigCLIENT_PRIVATE_KEY_PEM;
    xNetworkCredentials.privateKeySize = sizeof( democonfigCLIENT_PRIVATE_KEY_PEM );

    /* Establish a TLS session with the HTTP server. This example connects to
     * the HTTP server as specified in democonfigAWS\_IOT\_ENDPOINT and
     * democonfigAWS\_HTTP\_PORT in demo\_config.h. */
    LogInfo( ( "Establishing a TLS session to %.*s:%d.",
               ( int32_t ) AWS_IOT_ENDPOINT_LENGTH,
               democonfigAWS_IOT_ENDPOINT,
               democonfigAWS_HTTP_PORT ) );

    /* Attempt to create a mutually authenticated TLS connection. */
    xNetworkStatus = TLS_FreeRTOS_Connect( pxNetworkContext,
                                           democonfigAWS_IOT_ENDPOINT,
                                           democonfigAWS_HTTP_PORT,
                                           &xNetworkCredentials,
                                           democonfigTRANSPORT_SEND_RECV_TIMEOUT_MS,
                                           democonfigTRANSPORT_SEND_RECV_TIMEOUT_MS );

    if( xNetworkStatus != TLS_TRANSPORT_SUCCESS )
    {
        xStatus = pdFAIL;
    }

    return xStatus;
}
```
