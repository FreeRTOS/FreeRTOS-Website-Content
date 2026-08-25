---
title: "coreMQTT Demo (with TLS Server Authentication)"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

coreMQTT is an MIT licensed open source MQTT client C library for microcontroller and small microprocessor based IoT devices.

**Notice: We recommend using mutual authentication (both the IoT MQTT client and server authenticate
each other) when building any Internet of Things (IoT) application. The demo on this page is only meant
for educational purposes as it demonstrates encrypted communication without client authentication. It
is not intended for production use.**


## Single Threaded Vs Multi Threaded

There are two coreMQTT usage models, *single threaded* and *multithreaded* (multitasking). Using the
MQTT library solely from one thread within an otherwise multi-threaded application, as the demo documented
on this page does, is equivalent to the single threaded use case. Single threaded use cases require
the application writer to make repeated explicit calls into the MQTT library. Multithreaded use cases
can instead execute the MQTT protocol in the background within [an agent (or daemon) task](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo).
Executing the MQTT protocol in an agent task removes the need for the application writer to explicitly
manage any MQTT state or call the `MQTT_ProcessLoop()` API function. Using an agent task also enables
multiple application tasks to share a single MQTT connection without the need for synchronization primitives
such as mutexes.


## Demo Introduction

This example project is one of three that introduce the concepts described on
the ["TLS Introduction"](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/02-TLS-introduction) page one at a time.
The [first example](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/01-coreMQTT-demo) demonstrates unencrypted MQTT communication. The second
example (on this page) builds on the first to introduce server authentication (where the IoT client
authenticates the MQTT server it connects to). The [third example](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication) 
builds on the second to introduce strong mutual authentication (where the MQTT server also authenticates
the client connecting to it).

This demo does not use mutual authentication so is intended to be used as a learning exercise **only**. 

This MQTT demo uses an mbedTLS-based [network transport interface](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface) implementation
to first establish a server-authenticated TLS connection with the MQTT broker, and then demonstrate the
subscribe-publish workflow of MQTT at the [QoS 2](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/01-MQTT-terminology) level. The demo has the broker echo
messages back by subscribing to a single topic filter and then publishing to that same topic. After each
publish, it waits to receive the message back from the server at the [QoS 2](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/01-MQTT-terminology) level.
This cycle of publishing to the broker and receiving the same message back from the broker is repeated
indefinitely. Messages in this demo are sent at QoS 2 which guarantees *exactly* once message delivery.

This basic MQTT demo project uses
the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW),
enabling it to be built and evaluated with
the [free Community version of Visual Studio](https://visualstudio.microsoft.com/vs/community/) on Windows,
so without the need for any particular MCU hardware.


## Source Code Organization

The demo project is called mqtt\_basic\_tls\_demo.sln and can be found in the
FreeRTOS-Plus/Demo/coreMQTT\_Windows\_Simulator/MQTT\_Basic\_TLS directory of
the [main FreeRTOS download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) (and in Github, linked from the download page).


## Configuring the Demo Project

The demo uses the [FreeRTOS-Plus-TCP TCP/IP stack](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP).
Follow the instructions provided for
the [TCP/IP starter project](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)
to ensure you:

1. Have the [pre-requisite components installed](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites) (such as WinPCap).

2. Optionally, [set a static or dynamic IP address, gateway address and netmask](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic).

3. Optionally, [set a MAC address](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr).

4. [Select an Ethernet network interface](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface)
   on your host machine.

5. …and **most important**, [test your network connection](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#connectivity-test)
   before attempting to run the MQTT demo.

All these setting should be performed in the MQTT demo project, not the TCP/IP starter project referenced
from the same page! As delivered the TCP/IP stack is configured to use a dynamic IP address.


## Configuring the MQTT Broker Connection

### Option 1: Using the publicly hosted Mosquitto MQTT broker (web hosted):

To communicate with Mosquitto’s publicly hosted MQTT broker, follow these steps:

1. Open your local copy of `FreeRTOS/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Basic_TLS/demo_config.h`
2. Set the following two constants as shown here:
	* `#define democonfigMQTT_BROKER_ENDPOINT "test.mosquitto.org"`
	* `#define democonfigMQTT_BROKER_PORT (8883)`
3. Set the constant `#democonfigROOT_CA_PEM` (the server’s root CA certificate) to the PEM certificate
   linked to from the main [https://test.mosquitto.org](https://test.mosquitto.org/) page. The certificate
   needs to be pasted as a string, so it will look like this:

   ```c
   #define democonfigROOT_CA_PEM  \
      "-----BEGIN CERTIFICATE-----\n"\
      "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n"\
      "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n"\
      "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc\n"\
      "... etc. .......................................................\n"\
      "-----END CERTIFICATE-----"
   ```


This setup should work if the demo connects to a network that has a DHCP service and Internet access.
Note that the FreeRTOS Windows port only works with a wired Ethernet network adapter, which can be a
virtual Ethernet adapter.

You should use a separate MQTT client, such as [MQTT.fx](https://mqttfx.jensd.de/), to test the MQTT
connection from your host machine to the public MQTT broker.

**Note:** Mosquitto is an open source MQTT message broker that supports MQTT versions 5.0, 3.1.1, and 3.1.
It is part of the Eclipse foundation and is an Eclipse IoT project. The `test.mosquitto.org` MQTT broker
is not affiliated with or maintained by FreeRTOS and may be unavailable at any time. Further the server
authentication used by this broker is based on 1024-bit [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)),
a cipher that is not recommended for production purposes.  Do **NOT** send any confidential information
from your device to this MQTT broker. 


### Option 2: Using a locally hosted Mosquitto MQTT message broker (host machine)

The Mosquitto broker can also run locally, either on your host machine (the machine used to build the
demo application), or another machine on your local network. To do this:

1. Follow the instructions on https://mosquitto.org/download/ to download and install Mosquitto locally.
2. Open “mosquitto.conf”, which is located in the Mosquitto install directory, and set the following configurations:
   * **per\_listener\_settings:** true
   * **port:** 8883
   * **allow\_anonymous:** false
   * **cafile:** ./mosquitto/config/ca.crt
   * **certfile:** ./mosquitto/config/server.crt
   * **keyfile:** ./mosquitto/config/server.key
   * **tls\_version:** tlsv1.2

Note: The configurations “cafile”, “certfile”, and “keyfile” above refer to the locally-generated CA
certificate, server certificate, and server key, respectively. These can be generated using OpenSSL.
More information can be found on [mosquitto.org](https://mosquitto.org/man/mosquitto-tls-7.html).

- Open your local copy of `FreeRTOS/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Basic_TLS/demo_config.h`
- Add the following lines to set democonfigMQTT\_BROKER\_ENDPOINT and democonfigMQTT\_BROKER\_PORT:
  * `#define democonfigMQTT_BROKER_ENDPOINT "w.x.y.z"`
  * `#define democonfigMQTT_BROKER_PORT ( 8883 )`

**Note:** Port number 8883 is the default port number for encrypted MQTT.  If you cannot use that
port (for example if it is blocked by your IT security policy) then change the port used by Mosquitto
to a high port number (for example, something in the 50000 to 55000 range), and set `mqttexampleMQTT_BROKER_PORT`
accordingly. The port number used by Mosquitto is set by the “port” parameter in “mosquitto.conf”, which
is located in the Mosquitto install directory.


### Option 3: An MQTT broker of your choosing:

Any MQTT broker that supports encrypted TCP/IP communication can be used with this demo. To do this:

1. Open your local copy of `/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Basic_TLS/demo_config.h`
2. Add the following lines with settings specific to your chosen broker:
   * #define democonfigMQTT\_BROKER\_ENDPOINT "your-desired-endpoint"
   * #define democonfigMQTT\_BROKER\_PORT ( 8883 )
3. Optionally, set the server’s root CA certificate ( `#democonfigROOT_CA_PEM` ) in `demo_config.h`


### Building the Demo Project

The demo project is built in the same way as the [basic MQTT demo (without TLS).](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/01-coreMQTT-demo#source_code)

* Open the `FreeRTOS/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Basic_TLS/mqtt_basic_tls_demo.sln`
  Visual Studio solution file from within the Visual Studio IDE.
* Select Build Solution from the IDE’s Build menu.

**NOTE:** If you are using Microsoft Visual Studio 2017 or earlier, then you must select a Platform
Toolset compatible with your version: Project -> RTOSDemos Properties -> Platform Toolset


## Functionality

The demo provides the same functionality and structure as
the [basic MQTT demo](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/01-coreMQTT-demo#functionality) (without TLS), but uses
a [transport interface](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface) that includes TLS in place of the plaintext transport
interface.


### Connecting to the MQTT Broker (with TLS)

The function `prvConnectToServerWithBackoffRetries()` attempts to make a TLS connection to the MQTT
broker. If the connection fails, it retries after a timeout. The timeout value will exponentially increase
and include jitter until the maximum number of attempts are reached or the maximum timeout value is
reached. The function `RetryUtils_BackoffAndSleep()` provides exponentially increasing timeout value
and returns `RetryUtilsRetriesExhausted` when the maximum number of attempts have been reached. The
variance in the time between retries is used to ensure a fleet of IoT devices that happen to all get
disconnected at the same time don't all try to reconnect at exactly the same time.

```c
static TlsTransportStatus_t prvConnectToServerWithBackoffRetries(
                                NetworkCredentials_t * pxNetworkCredentials,
                                NetworkContext_t * pxNetworkContext )
{
    TlsTransportStatus_t xNetworkStatus;
    RetryUtilsStatus_t xRetryUtilsStatus = RetryUtilsSuccess;
    RetryUtilsParams_t xReconnectParams;

    /* Set the credentials for establishing a TLS connection. */
    pxNetworkCredentials->pRootCa = ( const unsigned char * ) democonfigROOT_CA_PEM;
    pxNetworkCredentials->rootCaSize = sizeof( democonfigROOT_CA_PEM );
    pxNetworkCredentials->disableSni = democonfigDISABLE_SNI;

    /* Initialize reconnect attempts and interval. */
    RetryUtils_ParamsReset( &xReconnectParams );
    xReconnectParams.maxRetryAttempts = MAX_RETRY_ATTEMPTS;

    /* Attempt to connect to the MQTT broker. If connection fails, retry after
     * a timeout. Timeout value will exponentially increase until maximum
     * attempts are reached. */
    do
    {
        /* Establish a TLS session with the MQTT broker. This example connects
         * to the MQTT broker as specified in democonfigMQTT\_BROKER\_ENDPOINT
         * and democonfigMQTT\_BROKER\_PORT at the top of this file. */
        xNetworkStatus = TLS_FreeRTOS_Connect( pxNetworkContext,
                                democonfigMQTT_BROKER_ENDPOINT,
                                democonfigMQTT_BROKER_PORT,
                                pxNetworkCredentials,
                                mqttexampleTRANSPORT_SEND_RECV_TIMEOUT_MS,
                                mqttexampleTRANSPORT_SEND_RECV_TIMEOUT_MS );

        if( xNetworkStatus != TLS_TRANSPORT_SUCCESS )
        {
            /* Connection failed. */
            xRetryUtilsStatus = RetryUtils_BackoffAndSleep( &xReconnectParams );
        }

        if( xRetryUtilsStatus == RetryUtilsRetriesExhausted )
        {
            /* Maximum number of connection attempts reached. */
            xNetworkStatus = TLS_TRANSPORT_CONNECT_FAILURE;
        }
    } while( ( xNetworkStatus != TLS_TRANSPORT_SUCCESS ) &&
             ( xRetryUtilsStatus == RetryUtilsSuccess ) );

    return xNetworkStatus;
}
```
