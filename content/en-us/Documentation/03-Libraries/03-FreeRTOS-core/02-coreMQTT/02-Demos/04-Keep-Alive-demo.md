---
title: coreMQTT Keep-Alive Demo
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

**Note: We recommend to always use mutual authentication in building any Internet of Things (IoT) application.
The demo on this page is only meant for educational purposes and demonstrates MQTT communication prior to
introducing encryption and authentication. It is not intended to be suitable for production use.**


## Introduction

The Keep-Alive MQTT demo project uses
the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW),
so you can build and evaluate it with
the [free Community version of Visual Studios](https://visualstudio.microsoft.com/vs/community/) on
Windows, without the need for any particular MCU hardware. This project provides an alternative to sending
the keep-alive packet to maintain a connection with the MQTT broker in case no control packets are sent
within the given keep-alive interval.

The Keep-Alive MQTT demo shows how to establish a plaintext TCP connection to an MQTT broker, with exponential
backoff logic if the connection fails. After the TCP connection is established, the client also sends an MQTT
connect packet, that includes information about the keep-alive interval for the broker. If the broker does not
receive a control packet within 1.5 times this given interval, the broker will close the connection. To avoid
this, an auto-reload software timer is used to send a ping request to the broker before the interval expires.
Whenever the timer is executed to send the ping request, another timer is started to expect the ping response
from the broker. Next, the client subscribes to a single topic filter then waits long enough to execute the timer.
After which, the client publishes to that topic at the [QoS 1](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/01-MQTT-terminology) level and repeatedly
invokes '`MQTT_ReceiveLoop`' to receive the publish acknowledgement from the broker. '`MQTT_ReceiveLoop`' is
passed a timeout of 0 to only run a single iteration with the task delaying between each iteration. Note that
if a publish acknowledgement hasn't been received within two iterations, the ping-request timer will be executed.
The whole cycle is repeated indefinitely. Keep in mind that the same effect is achieved when '`MQTT_ProcessLoop`'
is used in place of '`MQTT_ReceiveLoop`'. However, '`MQTT_ProcessLoop`' requires a timer-query function to return
the current time in milliseconds.

The instructions provided below will demonstrate how to connect to
either [Mosquitto’s test broker](https://test.mosquitto.org/) hosted on the internet or on a server
running locally on the host.

This demo is intended to be used as a learning exercise **only**. This demo **does not** create a
secure connection but can easily be modified to use a TLS connection. However, all MQTT messages are
sent in plaintext and are not encrypted. Do **NOT** send any confidential information from your IoT
device to the MQTT broker. The MQTT broker is publicly hosted by a 3rd party that is not affiliated
with FreeRTOS. This MQTT broker may be unavailable at any time, and it is not maintained by FreeRTOS.
Production IoT devices should use a network connection that is both mutually authenticated and encrypted,
as demonstrated in the [MQTT TLS demo](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication).

**Note**: Mosquitto is an open source MQTT message broker. More details are available [here](https://iot.eclipse.org/).


## Source Code Organization

The Visual Studio solution for the Keep-Alive MQTT demo is
called [`mqtt_keep_alive_demo.sln`](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Keep_Alive/mqtt_keep_alive_demo.sln)
and is located in
the [FreeRTOS-Plus/Demo/coreMQTT\_Windows\_Simulator/MQTT\_Keep\_Alive](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Keep_Alive)
directory of the [main FreeRTOS](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) download.

![](/media/2020/coreMQTT-keep-alive-2-217x300.png)


## Building the Demo Project

The demo project uses the [free community edition of Visual Studio](https://visualstudio.microsoft.com/vs/community/).
To build the demo:

1. Open the '`mqtt_keep_alive_demo.sln`' Visual Studio solution file from within the Visual Studio IDE.
2. Select '**Build Solution**' from the IDE's '**Build**' menu.

**Note**: If you are using Microsoft Visual Studio 2017 or earlier, then you must select a 'Platform Toolset'
compatible with your version: '`Project -> RTOSDemos Properties -> Platform Toolset`'.


## Configuring the Demo Project

The demo uses the [FreeRTOS-Plus-TCP TCP/IP stack](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP), so follow the
instructions provided for the [TCP/IP starter project](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)
to ensure you:

1. Have the [pre-requisite components installed](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites) (such as WinPCap).

2. Optionally [set a static or dynamic IP address, gateway address and netmask](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic).

3. Optionally [set a MAC address](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr).

4. [Select an Ethernet network interface](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface)
   on your host machine.

5. ...and **importantly** [test your network connection](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#connectivity-test)
   before attempting to run the MQTT demo.

All of these settings should be changed in the MQTT LTS rc1 demo project, not the TCP/IP starter project
referred to in the pages linked to above! As delivered, the TCP/IP stack is configured to use a dynamic IP
address.


## Configuring the MQTT Broker Connection

### Option 1: Using the publicly hosted Mosquitto MQTT broker (web hosted):

The demo project is pre-configured to communicate with Mosquitto's publicly hosted message broker
at "test.mosquitto.org". This should work if the demo connects to a network that has a DHCP service and
Internet access. Note that the FreeRTOS Windows port only works with a wired Ethernet network adapter,
which can be a virtual Ethernet adapter.

You should use a separate MQTT client, such as [MQTT.fx](https://mqttfx.jensd.de/), to test the MQTT
connection from your host machine to the public MQTT broker.


### Option 2: Using a locally hosted Mosquitto MQTT message broker (host machine):

The Mosquitto broker can also run locally, either on your host machine (the machine used to build the
demo application), or another machine on your local network. To do this:

1. [Download Mosquitto](https://mosquitto.org/download/)

2. Install Mosquitto as a Windows service by running the installer.

3. Start the Mosquitto service. More details about running Mosquitto as a Windows service can be found
   in their [Readme-windows](https://github.com/eclipse-mosquitto/mosquitto/blob/master/README-windows.txt)
   and [Readme](https://github.com/eclipse-mosquitto/mosquitto/blob/master/README.md)

   * **NOTE:** Starting from Mosquitto Version 2.0.0, when the Mosquitto broker is run without configuring any [`listener`](https://mosquitto.org/man/mosquitto-conf-5.html) it will now bind to the loopback interfaces `127.0.0.1` and/or `::1`, limiting the inbound connections to only from the local host. Also, all listeners now default to [`allow_anonymous`](https://mosquitto.org/man/mosquitto-conf-5.html) false, preventing the clients from connecting without providing a username. As a result, both `listener` and `allow_anonymous` need to be specified explicitly in the `mosquitto.conf` configuration file:
        ``` sh
        listener 1883
        allow_anonymous true
        ```
    * To start Mosquitto with a custom configuration file use: `mosquitto -v -c <path/to/config/file>`


4. Verify that the Mosquitto server is running locally and listening on port 1883 by following these steps:

    1. Open PowerShell.

    2. Type in the command

       ```c
       netstat -a -p TCP | findstr 1883
       ```

       to check if there is an active connection listening on port 1883.

    3. Verify that the command outputs something like the following:

       ```c
       TCP    0.0.0.0:1883           :0       LISTENING
       ```

    4. If there is no output as in the previous step, go through the Mosquitto documentation
    listed above to check if your setup was correct.

5. Make sure the Mosquitto broker is allowed to communicate through the Windows Firewall. Follow
   the [instructions](https://support.microsoft.com/help/4558235/windows-10-allow-an-app-through-microsoft-defender-firewall)
   from Microsoft to allow an application to communicate through the Windows 10 Defender Firewall. After
   you run this MQTT example, it is a good practice to disable the Mosquitto broker communication through
   the Windows Firewall to avoid unwanted network traffic to your machine.

6. After you verify that the Mosquitto broker is running successfully, update the config `democonfigMQTT_BROKER_ENDPOINT`
   to the local IP address of your Windows host machine. Please note that "localhost" or address "127.0.0.1"
   will not work because this example is running on a Windows Simulator and not on a Windows host natively.
   Also note that, if the Windows host uses a Virtual Private Network (VPN), the connection to the Mosquitto
   broker may not work.

Use a separate MQTT client, such as [MQTT.fx](https://mqttfx.jensd.de/), to test the MQTT connection from
your host machine to the local MQTT broker.

**Note:** Port number 1883 is the default port number for unencrypted MQTT. If you cannot use that
port (for example if it is blocked by your IT security policy), then change the port used by Mosquitto
to a high port number (for example something in the 50000 to 55000 range), and set `democonfigMQTT_BROKER_PORT`
accordingly. The port number used by Mosquitto is set by the '`port`' parameter in '`mosquitto.conf`', which
is located in the Mosquitto install directory.


### Option 3: Any other unencrypted MQTT broker of your choosing:

Any MQTT broker that supports unencrypted TCP/IP communication can also be used with this demo. To do
this:

1. Open your local copy of [/FreeRTOS-Plus/Demo/coreMQTT\_Windows\_Simulator/MQTT\_Keep\_Alive/demo\_config.h](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Keep_Alive/demo_config.h).

2. Add the following lines with settings specific to your chosen broker:

   ```c
   #define democonfigMQTT_BROKER_ENDPOINT "your-desired-endpoint"
   ```

   ```c
   #define democonfigMQTT_BROKER_PORT ( 1883 )
   ```


## Functionality

The demo creates a single application task that loops through a set of examples that demonstrate how
to connect to the broker, handle keep-alive with an auto-reload timer, subscribe to a topic on the
broker, publish to a topic on the broker, then finally, disconnect from the broker. The demo application
both subscribes to and publishes to the same topic. Each time the demo publishes a message to the MQTT
broker, the broker sends the same message back to the demo application. The structure of the demo is
shown below:

```c
static void prvMQTTDemoTask( void * pvParameters )
{
uint32_t ulTopicCount = 0U;
NetworkContext_t xNetworkContext = { 0 };
MQTTContext_t xMQTTContext;
MQTTStatus_t xMQTTStatus;
PlaintextTransportStatus_t xNetworkStatus;
BaseType_t xTimerStatus;

    /* Remove compiler warnings about unused parameters. */
    ( void ) pvParameters;

    /* Serialize a PINGREQ packet to send upon invoking the keep-alive timer
     * callback. */
    xMQTTStatus = MQTT_SerializePingreq( &xPingReqBuffer );
    configASSERT( xMQTTStatus == MQTTSuccess );

    for( ; ; )
    {
        /****************************** Connect. ******************************/

        /* Attempt to connect to the MQTT broker. If connection fails, retry
         * after a timeout. The timeout value will be exponentially increased
         * until the maximum number of attempts are reached or the maximum
         * timeout value is reached. The function below returns a failure status
         * if the TCP connection cannot be established to the broker after
         * the configured number of attempts. */
        xNetworkStatus = prvConnectToServerWithBackoffRetries( &xNetworkContext );
        configASSERT( xNetworkStatus == PLAINTEXT_TRANSPORT_SUCCESS );

        /* Sends an MQTT Connect packet over the already connected TCP socket,
         * and waits for connection acknowledgment (CONNACK) packet. */
        LogInfo( ( "Creating an MQTT connection to %s.", democonfigMQTT_BROKER_ENDPOINT ) );
        prvCreateMQTTConnectionWithBroker( &xMQTTContext, &xNetworkContext );

        /* Create timers to handle keep-alive. */
        xPingReqTimer = xTimerCreateStatic( "PingReqTimer",
                                            mqttexamplePING_REQUEST_DELAY,
                                            pdTRUE,
                                            ( void * ) &xMQTTContext.transportInterface,
                                            prvPingReqTimerCallback,
                                            &xPingReqTimerBuffer );
        configASSERT( xPingReqTimer );
        xPingRespTimer = xTimerCreateStatic( "PingRespTimer",
                                             mqttexamplePING_RESPONSE_DELAY,
                                             pdFALSE,
                                             NULL,
                                             prvPingRespTimerCallback,
                                             &xPingRespTimerBuffer );
        configASSERT( xPingRespTimer );

        /* Start the timer to send a PINGREQ. */
        xTimerStatus = xTimerStart( xPingReqTimer, 0 );
        configASSERT( xTimerStatus == pdPASS );

        /**************************** Subscribe. ******************************/

        /* If the server rejected the subscription request, attempt to resubscribe
         * to the topic. Attempts are made according to the exponential backoff retry
         * strategy declared in retry\_utils.h. */
        prvMQTTSubscribeWithBackoffRetries( &xMQTTContext );

        /************************ Send PINGREQ packet. ************************/

        /* Deliberately delay in order for the auto-reload timer to send a PINGREQ to the broker. */
        vTaskDelay( mqttexamplePING_REQUEST_DELAY );

        /********************* Publish and Receive Loop. **********************/
        /* Publish messages with QOS1, send and process keep-alive messages. */
        LogInfo( ( "Publish to the MQTT topic %s.", mqttexampleTOPIC ) );
        prvMQTTPublishToTopic( &xMQTTContext );

        /* Process the incoming publish echo. Since the application subscribed to
         * the same topic, the broker will send the same publish message back
         * to the application. */
        LogInfo( ( "Attempt to receive publish message from broker." ) );
        while( xReceivedPubAck == pdFALSE )
        {
            ulReceiveLoopIterations += 1U;
            configASSERT( ulReceiveLoopIterations <= mqttexampleMAX_RECEIVE_LOOP_ITERATIONS );

            vTaskDelay( mqttexampleRECEIVE_LOOP_ITERATION_DELAY );

            xMQTTStatus = MQTT_ReceiveLoop( &xMQTTContext, 0U );
            configASSERT( xMQTTStatus == MQTTSuccess );
        }

        /* Reset after loop. */
        ulReceiveLoopIterations = 0U;
        xReceivedPubAck = pdFALSE;

        /******************** Unsubscribe from the topic. *********************/
        LogInfo( ( "Unsubscribe from the MQTT topic %s.", mqttexampleTOPIC ) );
        prvMQTTUnsubscribeFromTopic( &xMQTTContext );

        /* Process an incoming packet from the broker. */
        while( xReceivedUnsubAck == pdFALSE )
        {
            ulReceiveLoopIterations += 1U;
            configASSERT( ulReceiveLoopIterations <= mqttexampleMAX_RECEIVE_LOOP_ITERATIONS );

            vTaskDelay( mqttexampleRECEIVE_LOOP_ITERATION_DELAY );

        }

        /* Reset after loop. */
        ulReceiveLoopIterations = 0U;
        xReceivedUnsubAck = pdFALSE;

        /**************************** Disconnect. *****************************/

        /* Send an MQTT disconnect packet over the connected TCP socket.
         * There is no corresponding response for the disconnect packet. After
         * sending the disconnect, the client must close the network connection. */
        LogInfo( ( "Disconnecting the MQTT connection with %s.",
        democonfigMQTT_BROKER_ENDPOINT ) );
        xMQTTStatus = MQTT_Disconnect( &xMQTTContext );
        configASSERT( xMQTTStatus == MQTTSuccess );

        /* Stop the keep-alive timers for the next iteration. */
        xTimerStatus = xTimerStop( xPingReqTimer, 0 );
        configASSERT( xTimerStatus == pdPASS );
        xTimerStatus = xTimerStop( xPingRespTimer, 0 );
        configASSERT( xTimerStatus == pdPASS );

        /* Close the network connection. */
        xNetworkStatus = Plaintext_FreeRTOS_Disconnect( &xNetworkContext );
        configASSERT( xNetworkStatus == PLAINTEXT_TRANSPORT_SUCCESS );

        /* Reset the SUBACK status for each topic filter after completion of the
         * subscription request cycle. */
        for( ulTopicCount = 0; ulTopicCount < mqttexampleTOPIC_COUNT; ulTopicCount++ )
        {
            xTopicFilterContext[ ulTopicCount ].xSubAckStatus = MQTTSubAckFailure;
        }

        /* Wait for some time between two iterations to ensure that we do not
         * bombard the broker. */
        LogInfo( ( "prvMQTTDemoTask() completed an iteration successfully. "
                   "Total free heap is %u.",
                   xPortGetFreeHeapSize() ) );
        LogInfo( ( "Demo completed successfully." ) );
        LogInfo( ( "Short delay before starting the next iteration.... \r\n" ) );
        vTaskDelay( mqttexampleDELAY_BETWEEN_DEMO_ITERATIONS );
    }
}
```

![](/media/2020/coreMQTT-keep-alive-1.png)


## Connecting to the MQTT Broker

The function `prvConnectToServerWithBackoffRetries()` attempts to make a TCP connection to the MQTT
broker. If the connection fails, it retries after a timeout. The timeout value will exponentially increase
until the maximum number of attempts are reached or the maximum timeout value is
reached. `prvConnectToServerWithBackoffRetries()` returns a failure status if the TCP connection cannot
be established to the broker after the configured number of attempts.

```c
static PlaintextTransportStatus_t prvConnectToServerWithBackoffRetries( NetworkContext_t * pxNetworkContext )
{
PlaintextTransportStatus_t xNetworkStatus;
RetryUtilsStatus_t xRetryUtilsStatus = RetryUtilsSuccess;
RetryUtilsParams_t xReconnectParams;

    /* Initialize reconnect attempts and interval. */
    RetryUtils_ParamsReset( &xReconnectParams );
    xReconnectParams.maxRetryAttempts = MAX_RETRY_ATTEMPTS;

    /* Attempt to connect to MQTT broker. If connection fails, retry after
     * a timeout. Timeout value will exponentially increase till maximum
     * attempts are reached.
     */
    do
    {
        /* Establish a TCP connection with the MQTT broker. This example connects to
         * the MQTT broker as specified in democonfigMQTT\_BROKER\_ENDPOINT and
         * democonfigMQTT\_BROKER\_PORT at the top of this file. */
        LogInfo( ( "Create a TCP connection to %s:%d.",
        democonfigMQTT_BROKER_ENDPOINT,
        democonfigMQTT_BROKER_PORT ) );
        xNetworkStatus = Plaintext_FreeRTOS_Connect( pxNetworkContext,
        democonfigMQTT_BROKER_ENDPOINT,
        democonfigMQTT_BROKER_PORT,
        mqttexampleTRANSPORT_SEND_RECV_TIMEOUT_MS,
        mqttexampleTRANSPORT_SEND_RECV_TIMEOUT_MS );

        if( xNetworkStatus != PLAINTEXT_TRANSPORT_SUCCESS )
        {
            LogWarn( ( "Connection to the broker failed. Retrying connection with backoff and jitter." ) );
            xRetryUtilsStatus = RetryUtils_BackoffAndSleep( &xReconnectParams );
        }

        if( xRetryUtilsStatus == RetryUtilsRetriesExhausted )
        {
            LogError( ( "Connection to the broker failed, all attempts exhausted." ) );
            xNetworkStatus = PLAINTEXT_TRANSPORT_CONNECT_FAILURE;
        }
    } while( ( xNetworkStatus != PLAINTEXT_TRANSPORT_SUCCESS ) && ( xRetryUtilsStatus == RetryUtilsSuccess ) );

    return xNetworkStatus;
}
```

The function '`prvCreateMQTTConnectionWithBroker()`' demonstrates how to establish an unencrypted connection
to an MQTT broker with a clean session. It uses the FreeRTOS-Plus-TCP transport interface that is implemented
in the file `FreeRTOS-Plus/Source/Application-Protocols/platform/freertos/transport/src/plaintext_freertos.c'`.
The definition of '`prvCreateMQTTConnectionWithBroker()`' is shown below. Keep in mind that we are setting the
keep-alive seconds for the broker in '`xConnectInfo.`'

The function below shows how the FreeRTOS-Plus-TCP transport interface is set in an MQTT context using `MQTT_Init()`.
It also shows how the event callback function pointer (`prvEventCallback`) is set. This callback is used to report
incoming messages.

```c
static void prvCreateMQTTConnectionWithBroker( MQTTContext_t * pxMQTTContext,
NetworkContext_t * pxNetworkContext )
{
MQTTStatus_t xResult;
MQTTConnectInfo_t xConnectInfo;
bool xSessionPresent;
TransportInterface_t xTransport;

    /***
     * For readability, error handling in this function is restricted to the use of
     * asserts().
     ***/

    /* Fill in Transport Interface send and receive function pointers. */
    xTransport.pNetworkContext = pxNetworkContext;
    xTransport.send = Plaintext_FreeRTOS_send;
    xTransport.recv = Plaintext_FreeRTOS_recv;

    /* Initialize MQTT library. */
    xResult = MQTT_Init( pxMQTTContext, &xTransport, prvGetTimeMs, prvEventCallback, &xBuffer );
    configASSERT( xResult == MQTTSuccess );

    /* Many fields not used in this demo so start with everything at 0. */
    ( void ) memset( ( void * ) &xConnectInfo, 0x00, sizeof( xConnectInfo ) );

    /* Start with a clean session i.e. direct the MQTT broker to discard any
     * previous session data. Also, establishing a connection with a clean session
     * will ensure that the broker does not store any data when this client
     * gets disconnected. */
    xConnectInfo.cleanSession = true;

    /* The client identifier is used to uniquely identify this MQTT client to
     * the MQTT broker. In a production device, the identifier can be something
     * unique, such as a device serial number. */
    xConnectInfo.pClientIdentifier = democonfigCLIENT_IDENTIFIER;
    xConnectInfo.clientIdentifierLength = ( uint16_t ) strlen( democonfigCLIENT_IDENTIFIER );

    /* Set MQTT keep-alive period. It is the responsibility of the application
     * to ensure that the interval between control packets being sent does not
     * exceed the keep-alive value. In the absence of sending any other control
     * packets, the client MUST send a PINGREQ Packet. */
    xConnectInfo.keepAliveSeconds = mqttexampleKEEP_ALIVE_TIMEOUT_SECONDS;

    /* Send MQTT CONNECT packet to broker. LWT is not used in this demo, so it
     * is passed as NULL. */
    xResult = MQTT_Connect( pxMQTTContext,
                            &xConnectInfo,
                            NULL,
                            mqttexampleCONNACK_RECV_TIMEOUT_MS,
                            &xSessionPresent );
                            configASSERT( xResult == MQTTSuccess );
}
```

`prvCreateMQTTConnectionWithBroker()` demonstrates how to establish an unencrypted connection to an
MQTT broker with a clean session.


## Handling Keep-Alive with an Auto-Reload Timer

After the application connects to the broker, it creates an auto-reload timer with the responsibility
of invoking a callback whenever '`mqttexampleKEEP_ALIVE_DELAY`' ticks have passed. This callback serializes
a ping-request packet using the coreMQTT serializer API then sends it to the MQTT broker. The definition
of the callback function is shown here:

```c
static void prvPingReqTimerCallback( TimerHandle_t pxTimer )
{
    TransportInterface_t * pxTransport;
    int32_t xTransportStatus;
    BaseType_t xTimerStatus;

    pxTransport = ( TransportInterface_t * ) pvTimerGetTimerID( pxTimer );

    /* Do not resend if waiting on a PINGRESP. */
    if( xWaitingForPingResp == false )
    {
        /* Send PINGREQ to broker */
        LogInfo( ( "Ping the MQTT broker." ) );
        xTransportStatus = pxTransport->send( pxTransport->pNetworkContext,
                                              ( void * ) xPingReqBuffer.pBuffer,
                                              xPingReqBuffer.size );
        configASSERT( ( size_t ) xTransportStatus == xPingReqBuffer.size );

        xWaitingForPingResp = true;

        /* Start the timer to expect a PINGRESP. */
        xTimerStatus = xTimerStart( xPingRespTimer, 0 );
        configASSERT( xTimerStatus == pdPASS );
    }
}
```

`prvKeepAliveTimerCallback()` demonstrates how to send a ping-request packet to the MQTT broker. After
it is sent, another timer is started to expect the ping response with another callback defined below:

```c
static void prvPingRespTimerCallback( TimerHandle_t pxTimer )
{
    ( void ) pxTimer;

    /* Assert that a pending PINGRESP has been received. */
    configASSERT( xWaitingForPingResp == false );
}
```

`prvKeepAliveTimerCallback()` simply asserts that a ping response has already been received.


## Subscribing to an MQTT Topic

The function '`prvMQTTSubscribeWithBackoffRetries()`' demonstrates how to subscribe to a topic filter
on the MQTT broker. The example demonstrates how to subscribe to one topic filter, but it is possible to
pass a list of topic filters in the same API call to subscribe to more than one topic filter. Also, if
the MQTT broker rejects the subscription request, then the subscription will be retried for '`MAX_RETRY_ATTEMPTS`'.
The definition of the function is shown here:

```c
static void prvMQTTSubscribeWithBackoffRetries( MQTTContext_t * pxMQTTContext )
{
MQTTStatus_t xResult = MQTTSuccess;
RetryUtilsStatus_t xRetryUtilsStatus = RetryUtilsSuccess;
RetryUtilsParams_t xRetryParams;
MQTTSubscribeInfo_t xMQTTSubscription[ mqttexampleTOPIC_COUNT ];
bool xFailedSubscribeToTopic = false;
uint32_t ulTopicCount = 0U;

    /* Some fields are not used by this demo so start with everything at 0. */
    ( void ) memset( ( void * ) &xMQTTSubscription, 0x00, sizeof( xMQTTSubscription ) );

    /* Get a unique packet id. */
    usSubscribePacketIdentifier = MQTT_GetPacketId( pxMQTTContext );

    /* Subscribe to the mqttexampleTOPIC topic filter. This example subscribes to
     * only one topic and uses QoS0. */
    xMQTTSubscription[ 0 ].qos = MQTTQoS0;
    xMQTTSubscription[ 0 ].pTopicFilter = mqttexampleTOPIC;
    xMQTTSubscription[ 0 ].topicFilterLength = ( uint16_t ) strlen( mqttexampleTOPIC );

    /* Initialize retry attempts and interval. */
    RetryUtils_ParamsReset( &xRetryParams );
    xRetryParams.maxRetryAttempts = MAX_RETRY_ATTEMPTS;

    do
    {
        /* The client is now connected to the broker. Subscribe to the topic
         * as specified in mqttexampleTOPIC at the top of this file by sending a
         * subscribe packet then waiting for a subscribe acknowledgment (SUBACK).
         * This client will then publish to the same topic it subscribed to, so it
         * will expect all the messages it sends to the broker to be sent back to it
         * from the broker. This demo uses QOS0 in Subscribe. Therefore, the publish
         * messages received from the broker will have QOS0. */
        LogInfo( ( "Attempt to subscribe to the MQTT topic %s.", mqttexampleTOPIC ) );
        xResult = MQTT_Subscribe( pxMQTTContext,
        xMQTTSubscription,
        sizeof( xMQTTSubscription ) / sizeof( MQTTSubscribeInfo_t ),
        usSubscribePacketIdentifier );
        configASSERT( xResult == MQTTSuccess );

        LogInfo( ( "SUBSCRIBE sent for topic %s to broker.\n\n", mqttexampleTOPIC ) );

        /* Process incoming packet from the broker. After sending the subscribe, the
         * client may receive a publish before it receives a subscribe ack. Therefore,
         * call the generic incoming packet processing function. Since this demo is
         * subscribing to the topic to which no one is publishing, probability of
         * receiving a publish message before a subscribe ack is zero; but the application
         * must be ready to receive any packet. This demo uses the generic packet
         * processing function everywhere to highlight this fact. */
        while( xReceivedSubAck == pdFALSE )
        {
            ulReceiveLoopIterations += 1U;
            configASSERT( ulReceiveLoopIterations <= mqttexampleMAX_RECEIVE_LOOP_ITERATIONS );

            vTaskDelay( mqttexampleRECEIVE_LOOP_ITERATION_DELAY );

            xResult = MQTT_ReceiveLoop( pxMQTTContext, 0U );
            configASSERT( xResult == MQTTSuccess );
        }

        /* Reset in case another attempt to subscribe is needed. */
        ulReceiveLoopIterations = 0U;
        xReceivedSubAck = pdFALSE;

        /* Reset flag before checking suback responses. */
        xFailedSubscribeToTopic = false;

        /* Check if the recent subscription request has been rejected. #xTopicFilterContext
         * is updated in the event callback to reflect the status of the SUBACK
         * sent by the broker. It represents either the QoS level granted by the
         * server upon subscription or acknowledgement of server rejection of the
         * subscription request. */
        for( ulTopicCount = 0; ulTopicCount < mqttexampleTOPIC_COUNT; ulTopicCount++ )
        {
            if( xTopicFilterContext[ ulTopicCount ].xSubAckStatus == MQTTSubAckFailure )
            {
                LogWarn( ( "Server rejected subscription request. Attempting to re-subscribe to topic %s.",
                xTopicFilterContext[ ulTopicCount ].pcTopicFilter ) );
                xFailedSubscribeToTopic = true;
                xRetryUtilsStatus = RetryUtils_BackoffAndSleep( &xRetryParams );
                break;
            }
        }

        configASSERT( xRetryUtilsStatus != RetryUtilsRetriesExhausted );

    } while( ( xFailedSubscribeToTopic == true ) && ( xRetryUtilsStatus == RetryUtilsSuccess ) );
}
```


## Receiving incoming messages

The application registers an event callback function before it connects to the broker as described earlier.
The function `'prvMQTTDemoTask()`' calls '`MQTT_ReceiveLoop()`' to receive incoming messages. When an incoming
MQTT message is received, it calls the event callback function registered by the application. The
function '`prvEventCallback()`' is an example of such an event callback function; it examines the incoming
packet type and calls the appropriate handler. In the example here, the function either
calls '`prvMQTTProcessIncomingPublish()`' to handle incoming publish messages or '`prvMQTTProcessResponse()`'
to handle Acks.

```c
static void prvEventCallback( MQTTContext_t * pxMQTTContext,
                              MQTTPacketInfo_t * pxPacketInfo,
                              MQTTDeserializedInfo_t * pxDeserializedInfo )
{
    /* The MQTT context is not used for this demo. */
    ( void ) pxMQTTContext;

    if( ( pxPacketInfo->type & 0xF0U ) == MQTT_PACKET_TYPE_PUBLISH )
    {
        prvMQTTProcessIncomingPublish( pxDeserializedInfo->pPublishInfo );
    }
    else
    {
        prvMQTTProcessResponse( pxPacketInfo, pxDeserializedInfo->packetIdentifier );
    }
}
```


## Publishing to a Topic

The function '`prvMQTTPublishToTopic()`' demonstrates how to publish to a topic filter on the MQTT broker.
The definition of the function is shown here:

```c
static void prvMQTTPublishToTopic( MQTTContext_t * pxMQTTContext )
{
MQTTStatus_t xResult;
MQTTPublishInfo_t xMQTTPublishInfo;
BaseType_t xTimerStatus;

    /***
     * For readability, error handling in this function is restricted to the use of
     * asserts().
     ***/

    /* Some fields are not used by this demo so start with everything at 0. */
    ( void ) memset( ( void * ) &xMQTTPublishInfo, 0x00, sizeof( xMQTTPublishInfo ) );

    /* This demo uses QoS0. */
    xMQTTPublishInfo.qos = MQTTQoS0;
    xMQTTPublishInfo.retain = false;
    xMQTTPublishInfo.pTopicName = mqttexampleTOPIC;
    xMQTTPublishInfo.topicNameLength = ( uint16_t ) strlen( mqttexampleTOPIC );
    xMQTTPublishInfo.pPayload = mqttexampleMESSAGE;
    xMQTTPublishInfo.payloadLength = strlen( mqttexampleMESSAGE );

    /* Send a PUBLISH packet. Packet ID is not used for a QoS0 publish. */
    xResult = MQTT_Publish( pxMQTTContext, &xMQTTPublishInfo, 0U );
    configASSERT( xResult == MQTTSuccess );

    /* When a PUBLISH packet has been sent, the keep-alive timer can be reset. */
    xTimerStatus = prvCheckTimeoutThenResetTimer( xKeepAliveTimer );
    configASSERT( xTimerStatus == pdPASS );
}
```


## Processing Incoming MQTT Publish Packets

The function '`prvMQTTProcessIncomingPublish()`' demonstrates how to process a `PUBLISH` packet from
the MQTT broker. The definition of the function is shown here:

```c
static void prvMQTTProcessIncomingPublish( MQTTPublishInfo_t * pxPublishInfo )
{
    configASSERT( pxPublishInfo != NULL );

    /* Process incoming Publish. */
    LogInfo( ( "Incoming QoS : %d\n", pxPublishInfo->qos ) );

    /* Verify the received publish is for the we have subscribed to. */
    if( ( pxPublishInfo->topicNameLength == strlen( mqttexampleTOPIC ) ) &&
        ( 0 == strncmp( mqttexampleTOPIC, pxPublishInfo->pTopicName, pxPublishInfo->topicNameLength ) ) )
    {
        LogInfo( ( "Incoming Publish Topic Name: %.*s matches subscribed topic.\r\n"
                   "Incoming Publish Message : %.*s",
                   pxPublishInfo->topicNameLength,
                   pxPublishInfo->pTopicName,
                   pxPublishInfo->payloadLength,
                   pxPublishInfo->pPayload ) );
    }
    else
    {
        LogInfo( ( "Incoming Publish Topic Name: %.*s does not match subscribed topic.",
        pxPublishInfo->topicNameLength,
        pxPublishInfo->pTopicName ) );
    }
}
```


## Unsubscribing from a Topic

The last step in the workflow unsubscribes from the topic so that the broker will no longer send any
messages published on the '`mqttexampleTOPIC`'. The definition of the function is shown here:

```c
static void prvMQTTUnsubscribeFromTopic( MQTTContext_t * pxMQTTContext )
{
MQTTStatus_t xResult;
MQTTSubscribeInfo_t xMQTTSubscription[ mqttexampleTOPIC_COUNT ];

    /* Some fields are not used by this demo, so start with everything at 0. */
    ( void ) memset( ( void * ) &xMQTTSubscription, 0x00, sizeof( xMQTTSubscription ) );

    /* Get a unique packet id. */
    usSubscribePacketIdentifier = MQTT_GetPacketId( pxMQTTContext );

    /* Subscribe to the mqttexampleTOPIC topic filter. This example subscribes to
     * only one topic and uses QoS0. */
    xMQTTSubscription[ 0 ].qos = MQTTQoS0;
    xMQTTSubscription[ 0 ].pTopicFilter = mqttexampleTOPIC;
    xMQTTSubscription[ 0 ].topicFilterLength = ( uint16_t ) strlen( mqttexampleTOPIC );

    /* Get the next unique packet identifier. */
    usUnsubscribePacketIdentifier = MQTT_GetPacketId( pxMQTTContext );

    /* Send the UNSUBSCRIBE packet. */
    xResult = MQTT_Unsubscribe( pxMQTTContext,
    xMQTTSubscription,
    sizeof( xMQTTSubscription ) / sizeof( MQTTSubscribeInfo_t ),
    usUnsubscribePacketIdentifier );

    configASSERT( xResult == MQTTSuccess );
}
```
