---
title: "coreMQTT Demo (without TLS)"
created: 2018-09-20
categories:
  - kernel
description: A demo and information regarding coreMQTT (without TLS)
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: Beginner's guide to FreeRTOS
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: Download FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FAQs
    link: /Why-FreeRTOS/FAQs
---

coreMQTT is an MIT licensed open source MQTT C library for microcontroller and small microprocessor based IoT devices.
* On this Page
	+ [Source Code Organization](#source-code-organization)
	+ [Configuring the Demo Project](#configuring-the-demo-project)
	+ [Build Instructions](#building-the-demo-project)
	+ [Functionality](#functionality)
		- [Connecting to the MQTT Broker](#connecting-to-the-mqtt-broker)
		- [Subscribing to a MQTT Topic](#subscribing-to-a-mqtt-topic)
		- [Publishing to a Topic](#publishing-to-a-topic)
		- [Receiving incoming messages](#receiving-incoming-messages)
		- [Processing Incoming MQTT Publish Packets](#processing-incoming-mqtt-publish-packets)
		- [Unsubscribing from a Topic](#unsubscribing-from-a-topic)


**Notice:  We recommend using mutual authentication in any Internet of Things (IoT) application. The
demo on this page is only meant for educational purposes as it demonstrates MQTT communication prior to
introducing encryption and authentication. It is not intended to be suitable for production use.**


## Single Threaded Vs Multi Threaded

There are two coreMQTT usage models, *single threaded* and *multithreaded* (multitasking). Using the MQTT library
solely from one thread within an otherwise multi-threaded application, as the demo documented on this page does,
is equivalent to the single threaded use case. Single threaded use cases require the application writer to make
repeated explicit calls into the MQTT library. Multithreaded use cases can instead execute the MQTT protocol in the
background within [an agent (or daemon) task](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo). Executing the MQTT protocol in an agent task
removes the need for the application writer to explicitly manage any MQTT state or call the `MQTT_ProcessLoop()`
API function. Using an agent task also enables multiple application tasks to share a single MQTT connection without
the need for synchronization primitives such as mutexes.


## Demo Introduction

This example project is one of three that introduce the concepts described on the ["TLS Introduction"](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/02-TLS-introduction)
page one at a time. The first example (this page) demonstrates unencrypted MQTT communication.
The [second example](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/02-coreMQTT-demo-LTS) builds on the first to introduce server authentication (where
the IoT client authenticates the MQTT server it connects to).
The [third example](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication) builds on the second to introduce strong mutual authentication (where
the MQTT server also authenticates the IoT client connecting to it).

This first project in the series only demonstrated the basic MQTT use cases of how to connect to a MQTT broker and the
subscribe-publish workflow of MQTT at the [QoS 0](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/01-MQTT-terminology) level. After it subscribes to a single topic filter,
it publishes to that topic, then waits to receive that same message back from the server. This cycle of publishing to the
broker and receiving the same message back from the broker is repeated indefinitely. As it uses QoS 0 it does not implement
any retransmission mechanism for publish messages.

This demo **does not** create a secure connection and is therefore not suitable for production use - do not send any
confidential information on an unencrypted network connection. The demo does demonstrate how to connect with an exponential
backoff time (including timing jitter) in the event of a connection failure. Exponentially increasing the time between
connection attempts and including some random timing jitter is best practice for large IoT device fleets as it prevents
all the IoT devices attempting to reconnect at the same time should they all become disconnected at the same time.

This basic MQTT demo project uses
the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW), enabling it
to be built and evaluated with the [free Community version of Visual Studio](https://visualstudio.microsoft.com/vs/community/)
on Windows, so without the need for any particular MCU hardware.


## Source Code Organization

The demo project is called mqtt\_plain\_text\_demo.sln and can be found in the
FreeRTOS-Plus/Demo/coreMQTT\_Windows\_Simulator/MQTT\_Plain\_Text  directory of the [main FreeRTOS download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) (and
in Github, linked from the download page).


## Configuring the Demo Project

The demo uses the [FreeRTOS-Plus-TCP TCP/IP stack](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP), so follow the
instructions provided for the [TCP/IP starter project](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)
to ensure you:

1. Have the [pre-requisite components installed](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites) (such
   as WinPCap).
2. Optionally [set a static or dynamic IP address, gateway address and netmask](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic).
3. Optionally [set a MAC address](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr).
4. [Select an Ethernet network interface](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface) on
   your host machine.
5. …and **importantly** [test your network connection](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#connectivity-test)
   before attempting to run the MQTT demo.

Each demo project has its own configuration settings. When you are following the network
configuration instructions, make sure to apply the settings in the MQTT demo project, rather than
the TCP/IP starter project. By default the TCP/IP stack is configured to use a dynamic IP address.


## Configuring the MQTT Broker Connection

### Option 1: Using the publicly hosted Mosquitto MQTT broker (web hosted)

The demo project can communicate with Mosquitto's publicly hosted message broker at “test.mosquitto.org”. This should
work if the demo connects to a network that has a DHCP service and Internet access. Note that the FreeRTOS Windows
port only works with a wired Ethernet network adapter, which can be a virtual Ethernet adapter. You should use a
separate MQTT client, such as [MQTT.fx](https://mqttfx.jensd.de/), to test the MQTT connection from your host machine
to the public MQTT broker. To use the hosted Mosquitto server:

1. Open your local copy of `/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Plain_Text/demo_config.h`
2. Add the following lines:
   * #define democonfigMQTT\_BROKER\_ENDPOINT "test.mosquitto.org"
   * #define democonfigMQTT\_BROKER\_PORT ( 1883 )

**Note**: Mosquitto is an open source MQTT message broker that supports MQTT versions 5.0, 3.1.1, and 3.1. 
It is part of the Eclipse foundation and is an [Eclipse IoT](https://iot.eclipse.org/) project. The
test.mosquitto.org MQTT broker is not affiliated with or maintained by FreeRTOS and may be unavailable
at any time.


### Option 2: Using a locally hosted Mosquitto MQTT message broker (host machine)

The Mosquitto broker can also run locally, either on your host machine (the machine used to build the demo application), or
another machine on your local network. To do this:

1. Follow the instructions on https://mosquitto.org/download/ to download and install Mosquitto locally.
2. Open “mosquitto.conf”, which is located in the Mosquitto install directory, and set the “bind\_address” to the network
   on which Mosquitto will listen for connection on your system.
   * **NOTE:** Starting from Mosquitto Version 2.0.0, when the Mosquitto broker is run without configuring any [`listener`](https://mosquitto.org/man/mosquitto-conf-5.html) it will now bind to the loopback interfaces `127.0.0.1` and/or `::1`, limiting the inbound connections to only from the local host. Also, all listeners now default to [`allow_anonymous`](https://mosquitto.org/man/mosquitto-conf-5.html) false, preventing the clients from connecting without providing a username. As a result, both `listener` and `allow_anonymous` need to be specified explicitly in the `mosquitto.conf` configuration file:
        ``` sh
        listener 1883
        allow_anonymous true
        ```
    * To start Mosquitto with a custom configuration file use: `mosquitto -v -c <path/to/config/file>`
3. Find the IP address of your host machine (run the `ipconfig` command on Windows, or `ifconfig` on Linux or MAC OS). Note
   that the FreeRTOS Windows port only works with a wired Ethernet network adapter, which can be a virtual Ethernet adapter.
4. Open `FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Plain_Text/demo_config.h`.
5. Add the following lines to set democonfigMQTT\_BROKER\_ENDPOINT to the IP address of the machine on which Mosquitto is
   running, which must be a machine on the same subnet as the network to which the demo is connected:
   * `#define democonfigMQTT_BROKER_ENDPOINT "w.x.y.z"`
   * `#define democonfigMQTT_BROKER_PORT ( 1883 )`

You should use a separate MQTT client, such as [MQTT.fx](https://mqttfx.jensd.de/), to test the MQTT connection from your
host machine to the installed MQTT broker.

**Note:** Port number 1883 is the default port number for unencrypted MQTT.  If you cannot use that port (for example if
it is blocked by your IT security policy) then change the port used by Mosquitto to a high port number (for example
something in the 50000 to 55000 range), and set `mqttexampleMQTT_BROKER_PORT` accordingly.


### Option 3: Any other unencrypted MQTT broker of your choosing:

Any MQTT broker that supports unencrypted TCP/IP communication can also be used with this demo. To do this:

1. Open your local copy of `/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Plain_Text/demo_config.h`
2. Add the following lines with settings specific to your chosen broker:
   * #define democonfigMQTT\_BROKER\_ENDPOINT "your-desired-endpoint"
   * #define democonfigMQTT\_BROKER\_PORT ( 1883 )


## Building the Demo Project

The demo project uses the  [free community edition of Visual Studio](https://visualstudio.microsoft.com/vs/community/).

To build the demo:
1. Open the `/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Plain_Text/mqt_plain_text_demo.sln` Visual Studio
   solution file from within the Visual Studio IDE
2. Select ‘build solution’ from the IDE’s ‘build’ menu


## Functionality

The demo creates a single application task that loops through a set of examples that demonstrate how to connect to the broker,
subscribe to a topic on the broker, publish to a topic on the broker, and disconnect from the broker again. The demo application
both subscribes to and publishes to the same topic, as a result of which each time the demo publishes a message to the MQTT
broker the broker sends the same message back to the demo application. The structure of the demo is shown below:

```c
static void prvMQTTDemoTask( void * pvParameters )
{

    uint32_t ulPublishCount = 0U, ulTopicCount = 0U;
    const uint32_t ulMaxPublishCount = 5UL;
    NetworkContext_t xNetworkContext = { 0 };
    MQTTContext_t xMQTTContext;
    MQTTStatus_t xMQTTStatus;
    PlaintextTransportStatus_t xNetworkStatus;

    /***
    * For readability, error handling in this function is restricted to
    * the use of asserts().
    ***/

    for( ; ; )
    {
        /*************************** Connect. *********************************/

        /* Attempt to connect to the MQTT broker. The socket is returned in
         * the network context structure. */
        xNetworkStatus = prvConnectToServerWithBackoffRetries( &xNetworkContext );
        configASSERT( xNetworkStatus == PLAINTEXT_TRANSPORT_SUCCESS );

        /* Connect to the MQTT broker using the already connected TCP socket. */
        prvCreateMQTTConnectionWithBroker( &xMQTTContext, &xNetworkContext );

        /**************************** Subscribe. ******************************/

        /* Subscribe to the test topic. */
        prvMQTTSubscribeWithBackoffRetries( &xMQTTContext );

        /******************* Publish and Keep Alive Loop. *********************/

        /* Publish messages with QoS0, then send and process Keep Alive
         * messages. */
        for( ulPublishCount = 0; ulPublishCount < ulMaxPublishCount; ulPublishCount++ )
        {
            prvMQTTPublishToTopic( &xMQTTContext );

            /* Process the incoming publish echo. Since the application subscribed
             * to the same topic, the broker will send the same publish message
             * back to the application. Note there is a separate demo that
             * shows how to use coreMQTT in a thread safe way - in which case the
             * MQTT protocol runs in the background and this call is not
             * required. */
            xMQTTStatus = MQTT_ProcessLoop( &xMQTTContext, mqttexamplePROCESS_LOOP_TIMEOUT_MS );
            configASSERT( xMQTTStatus == MQTTSuccess );

            /* Leave the connection idle for some time. */
            vTaskDelay( mqttexampleDELAY_BETWEEN_PUBLISHES );
        }

        /******************** Unsubscribe from the topic. *********************/

        prvMQTTUnsubscribeFromTopic( &xMQTTContext );

        /* Process the incoming packet from the broker. Note there is a separate
         * demo that shows how to use coreMQTT in a thread safe way - in which case
         * the MQTT protocol runs in the background and this call is not required. */
        xMQTTStatus = MQTT_ProcessLoop( &xMQTTContext, mqttexamplePROCESS_LOOP_TIMEOUT_MS );
        configASSERT( xMQTTStatus == MQTTSuccess );

        /**************************** Disconnect. *****************************/

        xMQTTStatus = MQTT_Disconnect( &xMQTTContext );

        /* Close the network connection. */
        xNetworkStatus = Plaintext_FreeRTOS_Disconnect( &xNetworkContext );
        configASSERT( xNetworkStatus == PLAINTEXT_TRANSPORT_SUCCESS );

        /* Wait for some time between two iterations to ensure that we do not
         * bombard the MQTT broker. */
        vTaskDelay( mqttexampleDELAY_BETWEEN_DEMO_ITERATIONS );
    }
}
```

### Connecting to the MQTT Broker

In the function above, `prvConnectToServerWithBackoffRetries()` attempts to make a TCP connection to the MQTT broker.
If the connection fails, it retries after a timeout. The timeout value will exponentially increase and include some
randomised jitter until the maximum number of attempts are reached or the maximum timeout value is reached. This type
of backoff is used in production devices to ensure a fleet of IoT devices that all get disconnected at the same time
do not all try and re-connect at the same time - and in so doing - overwhelm the server. If the connection is successful
then the connected TCP socket is returned in the xNetworkContext

The function `prvCreateMQTTConnectionWithBroker()` demonstrates how to establish an unencrypted connection to a MQTT broker
with [clean session](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/01-MQTT-terminology). It uses the FreeRTOS-Plus-TCP [transport interface](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface) which
is implemented in the file `FreeRTOS-Plus/Source/Application-Protocols/platform/freertos/transport/src/plaintext_freertos.c`.
The definition of `prvCreateMQTTConnectionWithBroker()` is shown below. The keep-alive seconds for the broker is set
in `xConnectInfo`.

The function below shows how FreeRTOS-Plus-TCP transport interface and time function are set in MQTT Context using MQTT\_Init().
It also shows how event callback function pointer ( `prvEventCallback` ) is set. This callback is used for reporting incoming
messages.

```c
static void prvCreateMQTTConnectionWithBroker( MQTTContext_t * pxMQTTContext, NetworkContext_t * pxNetworkContext )
{
    MQTTStatus_t xResult;
    MQTTConnectInfo_t xConnectInfo;
    bool xSessionPresent;
    TransportInterface_t xTransport;

    /***
     * For readability, error handling in this function is restricted to
     * the use of asserts().
     ***/

    /* Fill in [Transport Interface](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface) send and receive function pointers. */
    xTransport.pNetworkContext = pxNetworkContext;
    xTransport.send = Plaintext_FreeRTOS_send;
    xTransport.recv = Plaintext_FreeRTOS_recv;

    /* Initialize MQTT library. */
    xResult = MQTT_Init(
        pxMQTTContext,
        &xTransport,
        prvGetTimeMs,
        prvEventCallback,
        &xBuffer );
    configASSERT( xResult == MQTTSuccess );

    /* Many fields not used in this demo so start with everything at 0. */
    ( void ) memset( ( void * ) &xConnectInfo, 0x00, sizeof( xConnectInfo ) );

    /* Start with a clean session i.e. direct the MQTT broker to discard any
    * previous session data. Also, establishing a connection with clean
    * session will ensure that the broker does not store any data when this
    * client gets disconnected. */
    xConnectInfo.cleanSession = true;

    /* The client identifier is used to uniquely identify this MQTT client to
    * the MQTT broker. In a production device the identifier can be something
    * unique, such as a device serial number. */
    xConnectInfo.pClientIdentifier = democonfigCLIENT_IDENTIFIER;
    xConnectInfo.clientIdentifierLength = ( uint16_t ) strlen( democonfigCLIENT_IDENTIFIER );

    /* Set MQTT keep-alive period. It is the responsibility of the application
    * to ensure that the interval between Control Packets being sent does not
    * exceed the Keep Alive value. In the absence of sending any other
    * Control Packets, the Client MUST send a PINGREQ Packet. */
    xConnectInfo.keepAliveSeconds = mqttexampleKEEP_ALIVE_TIMEOUT_SECONDS;

    /* Send MQTT CONNECT packet to broker. LWT is not used in this demo, so it
    * is passed as NULL. */
    xResult = MQTT_Connect(
        pxMQTTContext,
        &xConnectInfo,
        NULL,
        mqttexampleCONNACK_RECV_TIMEOUT_MS,
        &xSessionPresent );
    configASSERT( xResult == MQTTSuccess );
}
```

### Subscribing to a MQTT Topic

The function `prvMQTTSubscribeWithBackoffRetries()` demonstrates how to subscribe to a topic filter on the MQTT broker.
The example demonstrates how to subscribe to one topic filter, but it is possible to pass a list of topic filters in the
same subscribe API call to subscribe to more than one topic filter. Also, in case the MQTT broker rejects the subscription
request, then the subscription will be retried for MAX\_RETRY\_ATTEMPTS. The definition of the function is shown below:

```c
static const char *const pcExampleTopic = "/example/topic";

static void prvMQTTSubscribeWithBackoffRetries( MQTTContext_t * pxMQTTContext )
{
    MQTTStatus_t xResult = MQTTSuccess;
    RetryUtilsStatus_t xRetryUtilsStatus = RetryUtilsSuccess;
    RetryUtilsParams_t xRetryParams;
    MQTTSubscribeInfo_t xMQTTSubscription[ mqttexampleTOPIC_COUNT ];
    bool xFailedSubscribeToTopic = false;

    /***
     * For readability, error handling in this function is restricted to
     * the use of asserts().
     ***/

    /* Some fields not used by this demo so start with everything at 0. */
    ( void ) memset( ( void * ) &xMQTTSubscription, 0x00, sizeof( xMQTTSubscription ) );

    /* Each packet requires a unique ID. */
    usSubscribePacketIdentifier = MQTT\_GetPacketId( pxMQTTContext );

    /* Subscribe to the pcExampleTopic topic filter. This example subscribes
     * to only one topic and uses QoS0. */
    xMQTTSubscription[ 0 ].qos = MQTTQoS0;
    xMQTTSubscription[ 0 ].pTopicFilter = pcExampleTopic;
    xMQTTSubscription[ 0 ].topicFilterLength = strlen( pcExampleTopic );

    /* Initialize retry attempts and interval. */
    RetryUtils_ParamsReset( &xRetryParams );
    xRetryParams.maxRetryAttempts = MAX_RETRY_ATTEMPTS;

    do
    {

        /* The client is already connected to the broker. Subscribe to the topic
         * as specified in pcExampleTopic by sending a subscribe packet then
         * waiting for a subscribe acknowledgment (SUBACK). */
        xResult = MQTT_Subscribe(
            pxMQTTContext,
            xMQTTSubscription,
            1, /* Only subscribing to one topic. */
            usSubscribePacketIdentifier );
        configASSERT( xResult == MQTTSuccess );

        /* Process incoming packet from the broker. After sending the
         * subscribe, the client may receive a publish before it receives a
         * subscribe ack. Therefore, call generic incoming packet processing
         * function. Since this demo is subscribing to the topic to which no
         * one is publishing, probability of receiving Publish message before
         * subscribe ack is zero; but application must be ready to receive any
         * packet. This demo uses the generic packet processing function
         * everywhere to highlight this fact. Note there is a separate demo that
         * shows how to use coreMQTT in a thread safe way – in which case the
         * MQTT protocol runs in the background and this call is not required. */
        xResult = MQTT_ProcessLoop( pxMQTTContext, mqttexamplePROCESS_LOOP_TIMEOUT_MS );
        configASSERT( xResult == MQTTSuccess );

        /* Reset flag before checking suback responses. */
        xFailedSubscribeToTopic = false;

        /* Check if recent subscription request has been rejected.
         * #xTopicFilterContext is updated in the event callback (shown in a
         * code block below) to reflect the status of the SUBACK sent by the
         * broker. It represents either the QoS level granted by the server upon
         * subscription, or acknowledgment of server rejection of the
         * subscription request. */
        if( xTopicFilterContext.xSubAckStatus == MQTTSubAckFailure )
        {
            xFailedSubscribeToTopic = true;
            xRetryUtilsStatus = RetryUtils_BackoffAndSleep( &xRetryParams );
            break;
        }
        configASSERT( xRetryUtilsStatus != RetryUtilsRetriesExhausted );
    }
    while( ( xFailedSubscribeToTopic == true ) &&  ( xRetryUtilsStatus == RetryUtilsSuccess ) );
}
```

### Publishing to a Topic

The function `prvMQTTPublishToTopic()` demonstrates how to publish to a topic filter on the MQTT broker. The definition
of the function is shown below:

```c
static const char *const pcExampleTopic = "/example/topic";

static void prvMQTTPublishToTopic( MQTTContext_t * pxMQTTContext )
{
    MQTTStatus_t xResult;
    MQTTPublishInfo_t xMQTTPublishInfo;

    /***
     * For readability, error handling in this function is restricted to the
     * use of asserts().
     ***/

    /* Some fields are not used by this demo so start with everything at 0. */
    ( void ) memset( ( void * ) &xMQTTPublishInfo, 0x00, sizeof( xMQTTPublishInfo ) );

    /* This demo uses QoS0. */
    xMQTTPublishInfo.qos = MQTTQoS0;
    xMQTTPublishInfo.retain = false;
    xMQTTPublishInfo.pTopicName = pcExampleTopic;
    xMQTTPublishInfo.topicNameLength = ( uint16_t ) strlen( pcExampleTopic );
    xMQTTPublishInfo.pPayload = mqttexampleMESSAGE;
    xMQTTPublishInfo.payloadLength = strlen( mqttexampleMESSAGE );

    /* Send PUBLISH packet. Packet ID is not used for a QoS0 publish. */
    xResult = MQTT_Publish(
        pxMQTTContext,
        &xMQTTPublishInfo,
        0U );
    configASSERT( xResult == MQTTSuccess );

}
```

### Receiving incoming messages

The application registers an event callback function before connecting to the broker as described earlier. The
function `prvMQTTDemoTask()` calls `MQTT_ProcessLoop()` to receive incoming messages. When an incoming MQTT message
is received, it calls the event callback function registered by the application. The function `prvEventCallback()`
is an example of such event callback function; it examines the incoming packet type and calls appropriate handler. In
the example below, the function either calls `prvMQTTProcessIncomingPublish()` for handling incoming publish messages
or `prvMQTTProcessResponse()` to handle Acks. Note there is a separate demo that shows how to use coreMQTT in a thread
safe way – in which case the MQTT protocol runs in the background and it is not required to call MQTT\_ProcessLoop().

```c
static void prvEventCallback( MQTTContext_t * pxMQTTContext, MQTTPacketInfo_t * pxPacketInfo, MQTTDeserializedInfo_t * pxDeserializedInfo )
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

### Processing Incoming MQTT Publish Packets

The function `prvMQTTProcessIncomingPublish()` demonstrates how to process an incoming PUBLISH packet from the
MQTT broker. `prvMQTTProcessResonse()` demonstrates how to process acknowledgement packets. The definition of
the functions are shown below:


```c
static const char *const pcExampleTopic = "/example/topic";

static void prvMQTTProcessIncomingPublish( MQTTPublishInfo_t * pxPublishInfo )
{
    /* Verify the received publish is for the we have subscribed to. */
    if( ( pxPublishInfo->topicNameLength == strlen( pcExampleTopic ) ) &&
        ( 0 == strcmp( pcExampleTopic, pxPublishInfo->pTopicName ) ) )
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

static void prvMQTTProcessResponse( MQTTPacketInfo_t * pxIncomingPacket, uint16_t usPacketId )
{
    MQTTStatus_t xResult = MQTTSuccess;
    uint8_t * pucPayload = NULL;
    size_t ulSize = 0;

    switch( pxIncomingPacket->type )
    {
        case MQTT_PACKET_TYPE_SUBACK:
            /* A SUBACK from the broker, containing the server response to our
             * subscription request, has been received. It contains the status
             * code indicating server approval/rejection for the subscription to
             * the single topic requested. The SUBACK will be parsed to obtain
             * the status code, and this status code will be stored in
             * #xTopicFilterContext. */
            xResult = MQTT_GetSubAckStatusCodes( pxIncomingPacket, &pucPayload, &ulSize );

            /* MQTT\_GetSubAckStatusCodes always returns success if called with
             * packet info from the event callback and non-NULL parameters. */
            configASSERT( xResult == MQTTSuccess );

            /* This should be the QOS level, 0 in this case. */
            xTopicFilterContext.xSubAckStatus = *pucPayload;

            /* Make sure ACK packet identifier matches with Request packet
             * identifier. */
            configASSERT( usSubscribePacketIdentifier == usPacketId );
            break;

        case MQTT_PACKET_TYPE_UNSUBACK:
            LogInfo( ( "Unsubscribed from the topic %s.", mqttexampleTOPIC ) );

            /* Make sure ACK packet identifier matches with Request packet
             * identifier. */
            configASSERT( usUnsubscribePacketIdentifier == usPacketId );
            break;

        case MQTT_PACKET_TYPE_PINGRESP:

            /* Nothing to be done from application as library handles
             * PINGRESP with the use of MQTT\_ProcessLoop API function. */
            LogWarn( ( "PINGRESP should not be handled by the application "
                "callback when using MQTT_ProcessLoop.\n" ) );
            break;

        /* Any other packet type is invalid. */
        default:
            LogWarn( ( "prvMQTTProcessResponse() called with unknown packet type:(%02X).", pxIncomingPacket->type ) );
    }
}
```

### Unsubscribing from a Topic

The last step in the workflow is to unsubscribe from the topic so that the broker will no longer send any publishes
from `pcExampleTopic`. The definition of the function is shown below:

```c
static const char *const pcExampleTopic = "/example/topic";

static void prvMQTTUnsubscribeFromTopic( MQTTContext_t * pxMQTTContext )
{
    MQTTStatus_t xResult;
    MQTTSubscribeInfo_t xMQTTSubscription[ mqttexampleTOPIC_COUNT ];

    /* Some fields not used by this demo so start with everything at 0. */
    ( void ) memset( ( void * ) &xMQTTSubscription, 0x00, sizeof( xMQTTSubscription ) );

    /* Subscribe to the pcExampleTopic topic filter. This example subscribes
    * to only one topic and uses QoS0. */
    xMQTTSubscription[ 0 ].qos = MQTTQoS0;
    xMQTTSubscription[ 0 ].pTopicFilter = pcExampleTopic;
    xMQTTSubscription[ 0 ].topicFilterLength = ( uint16_t ) strlen( pcExampleTopic);

    /* Each packet requires a unique ID. */
    usUnsubscribePacketIdentifier = MQTT_GetPacketId( pxMQTTContext );

    /* Send UNSUBSCRIBE packet. */
    xResult = MQTT_Unsubscribe(
        pxMQTTContext,
        xMQTTSubscription,
        sizeof( xMQTTSubscription ) / sizeof( MQTTSubscribeInfo_t ),
        usUnsubscribePacketIdentifier );
    configASSERT( xResult == MQTTSuccess );
}
```
