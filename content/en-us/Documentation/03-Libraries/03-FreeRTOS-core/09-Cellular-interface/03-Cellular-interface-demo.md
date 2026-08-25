---
title: Cellular Interface Demo (Mutual Authentication)
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## Introduction

FreeRTOS offers a suite of networking stacks designed for IoT applications. Applications can access
communication protocols at different levels - MQTT, HTTP, Secure Sockets, etc. Common connectivity
technologies such as Ethernet, Wi-Fi and BLE have been integrated with the networking stacks of
FreeRTOS, with a wide selection of [microcontrollers and modules](https://devices.amazonaws.com/search?page=1&sv=freertos)
pre-integrated.

The demos in this project demonstrate how to establish mutually authenticated MQTT connections to MQTT
brokers, such as AWS IoT Core, by using cellular connectivity. The demos use
the [Cellular Interface library](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/01-Cellular-interface) sub-moduled from an external
project. The Cellular Interface library exposes the capability of a few popular cellular modems through
a uniform API.

- [Quectel BG96](https://www.quectel.com/product/lpwa-bg96-cat-m1-nb1-egprs)
- [Sierra Wireless HL7802](https://www.sierrawireless.com/iot-modules/lpwa-modules/hl7802/)
- [U-Blox Sara-R4](https://www.u-blox.com/en/product/sara-r4-series)

The MQTT and HTTP libraries of FreeRTOS use an
abstract [Transport Interface](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface) to send/receive data in a generic way. The demos
in this project offer
an [implementation](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Source/Application-Protocols/network_transport/transport_mbedtls.c)
of the Transport Interface on top of the uniform API exposed by the Cellular Interface library.

## Hardware Setup

The demos in this project can be run in
the [FreeRTOS Windows Simulator](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW).
You will need a Windows PC and one of the supported cellular modems to run the demos. A version of Visual
Studio, such as the free Community version of [Visual Studio](https://visualstudio.microsoft.com/vs/community/),
will be needed to build the demos.

The FreeRTOS Windows simulator makes use of a COM port to communicate with the cellular module.
Set up your cellular module communication with the following steps.

1. Connect the cellular module to your PC. Most cellular dev kits have a USB connector, so you
   can just connect it to your PC's USB port and look for the COM port in Window's Device Manager.
   For example, as shown below, you will see a new COM69 show up when you connect the modem. If
   your cellular dev kit does not have USB, use a USB
   adapter [like one of these](https://www.amazon.com/Serial-Usb-Adapter/s?k=Serial+To+Usb+Adapter).

   ![Screenshot 1: Cellular module COM port in windows device manager](/media/2020/Screenshot-1.png)

2. Use [Putty](https://www.putty.org/) or any other terminal tool to verify the connection with the cellular
   module. Refer to your cellular module's manual for settings like baud rate, parity, and flow control. In
   the terminal tool, enter "ATE1". The modem should return "OK". Depending on your modem setting, you may
   also see an echo of "ATE1" as well. Enter "AT". The modem should return "OK".

   ![Screenshot 2. Testing the COM port with AT commands in putty](/media/2020/Screenshot-2.png)

## Components and Interfaces

This project makes use of five (5) sub-modules from other GitHub projects, shown as yellow boxes in the
diagram below.

![Figure 1: Components and Interfaces](/media/2020/12/Figure-1.png)

- The [Cellular Demo Application](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator/Common)
  is largely the same functionality as
  the [coreMQTT demo](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth),
  with added logic to set up cellular as the transport. (The original coreMQTT demo was designed for Wi-Fi
  on the FreeRTOS Windows Simulator.)

- The [Transport Interface](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Source/Application-Protocols/network_transport/transport_mbedtls.c)
  is needed by the MQTT library (sub-moduled from the [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)
  project) to send and receive packets.

- The [TLS porting interface](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/VisualStudio_StaticProjects/MbedTLS/mbedtls_freertos_port.c)
  is needed by the mbedTLS library to run on FreeRTOS.

- The [Comm Interface](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator/Common/comm_if_windows.c)
  is used by the Cellular Interface library to communicate with cellular modems over a UART connection.

## Developer References and API Documents

Please refer to the [hosted doxygen](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/01-Cellular-interface).

## Source Code Organization

The demo project files for Visual Studio are named _\<xyz>_\_mqtt*mutual_auth_demo.sln, where \_xyz*
is the name of the cellular modem. They can be found in
the [FreeRTOS_Cellular_Interface_Windows_Simulator](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator)
repository on GitHub in the following directories:

1. [MQTT_Mutual_Auth_Demo_with_BG96](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator/MQTT_Mutual_Auth_Demo_with_BG96)

2. [MQTT_Mutual_Auth_Demo_with_HL7802](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator/MQTT_Mutual_Auth_Demo_with_HL7802)

3. [MQTT_Mutual_Auth_Demo_with_SARA_R4](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator/MQTT_Mutual_Auth_Demo_with_SARA_R4)

```c
./FreeRTOS-Plus
├── Demo
│   ├── FreeRTOS_Cellular_Interface_Windows_Simulator
│   │   ├── Common
│   │   │   ├── FreeRTOSConfig.h
│   │   │   ├── FreeRTOSIPConfig.h
│   │   │   ├── MutualAuthMQTTExample.c
│   │   │   ├── cellular_platform.c
│   │   │   ├── cellular_platform.h
│   │   │   ├── cellular_setup.c
│   │   │   ├── comm_if_windows.c
│   │   │   ├── core_mqtt_config.h
│   │   │   ├── main.c
│   │   │   └── mbedtls_config.h
│   │   ├── MQTT_Mutual_Auth_Demo_with_BG96 ( demo project for Quectel BG96 )
│   │   │   ├── WIN32.vcxproj
│   │   │   ├── WIN32.vcxproj.filters
│   │   │   ├── WIN32.vcxproj.user
│   │   │   ├── cellular_config.h
│   │   │   ├── demo_config.h
│   │   │   └── mqtt_mutual_auth_demo_with_bg96.sln
│   │   ├── MQTT_Mutual_Auth_Demo_with_HL7802 ( demo project for Sierra Wireless HL7802 )
│   │   └── MQTT_Mutual_Auth_Demo_with_SARA_R4 ( demo project for U-Blox Sara-R4 )
│   │
├── Source
│   ├── Application-Protocols
│   │   ├── coreMQTT ( submodule : coreMQTT )
│   ├── FreeRTOS-Cellular-Interface ( submodule : FreeRTOS-Cellular-Interface )
│   ├── FreeRTOS-Cellular-Modules
│   │   ├── bg96 ( submodule : Lab-FreeRTOS-Cellular-Interface-Reference-Quectel-BG96 )
│   │   ├── hl7802 ( submodule : Lab-FreeRTOS-Cellular-Interface-Reference-Sierra-Wireless-HL7802 )
│   │   └── sara-r4 ( submodule : Lab-FreeRTOS-Cellular-Interface-Reference-ublox-SARA-R4 )
│   ├── Utilities
│   │   ├── backoff_algorithm ( submodule : backoffAlgorithm )
│   │   ├── logging
│   │   ├── mbedtls_freertos
│   │   │   ├── mbedtls_bio_freertos_cellular.c
│   │   │      └── ( code for adapting mbedtls with cellular socket )
│   │   │   ├── mbedtls_bio_freertos_plus_tcp.c
│   │   │   ├── mbedtls_freertos_port.c
│   │   │   └── threading_alt.h
├── ThirdParty
│   ├── mbedtls ( submodule : mbedtls )
```

## Configure the Application Settings

### Configure the cellular network

The following parameters in the cellular
configuration, [cellular_config.h](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator), (located
in "MQTT_Mutual_Auth_Demo_with\__\<cellular_module>_/cellular_config.h") must be modified for your
network environment.

| Configuration                | Description                                                                                                                                          | Value                                                 |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| CELLULAR_COMM_INTERFACE_PORT | The cellular communication interface makes use of a COM port on your computer to<br/> communicate with the cellular module on the Windows simulator. | Your COM port connected to the cellular module.       |
| CELLULAR_APN                 | The default [APN](https://en.wikipedia.org/wiki/Access_Point_Name) for network registration.                                                         | Specify the value according to your network operator. |
| CELLULAR_PDN_CONTEXT_ID      | PDN context id for the cellular network.                                                                                                             | The default value is CELLULAR_PDN_CONTEXT_ID_MIN.     |
| CELLULAR_PDN_CONNECT_TIMEOUT | PDN connect timeout for network registration.                                                                                                        | The default value is 100000 milliseconds.             |

### Configure the MQTT broker

The configuration to connect to an MQTT broker can be found in the demo
configuration, [demo_config.h](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator), (located
in "MQTT_Mutual_Auth_Demo_with\__\<cellular_module>_/demo_config.h"). Refer to the documentation
for the [MQTT Mutual Authentication Demo](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication#configuring-the-mqtt-broker-connection))
for more information.

### Configure the COM port settings

Refer to your cellular module's documentation for COM port settings. Update the settings
in [comm_if_windows.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator/Common/comm_if_windows.c)
if necessary.

### Configure the other sub-modules

"FreeRTOSConfig.h", "mbedtls_config.h" and "core_mqtt_config.h" (located
in "MQTT_Mutual_Auth_Demo_with\__\<cellular_module>_) contain configurations for their corresponding
sub-modules.

## Demo Execution Step flow

The demo app performs three types of operations. By searching for the names of the functions in the
diagram below, you can find the exact places these operations are performed in the source code.

1. Register to a cellular
   network. (See [cellular_setup.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator/Common/cellular_setup.c).)

2. Establish a secure connection to AWS IoT with the MQTT
   broker. (See [using_mbedtls.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Source/Application-Protocols/network_transport/transport_mbedtls.c).)

3. Perform MQTT
   operations. (See [MutualAuthMQTTExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator/Common/MutualAuthMQTTExample.c).)

The following diagram illustrates the interactions between the demo app and other components.

[![Demo Flow](/media/2020/cellular_demo_sequence-1.png) **Demo Flow Click image to enlarge**](/media/2020/cellular_demo_sequence-1.png)

## Build and run the MQTT mutual authentication demo

1. In Visual Studio, open one of the mqtt_mutual_auth_demo.sln projects that matches your cellular
   modem.

2. Set up an Amazon Web Services account and register a device as an AWS IoT thing on AWS IoT Core.
   See [Using the AWS IoT message broker](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication#configuring-the-mqtt-broker-connection) in
   the coreMQTT Mutual Authentication Demo for more details.

3. Configure the thing Name, AWS IoT thing Endpoint and setup the credentials
   in [demo_config.h](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator), (located
   in "MQTT_Mutual_Auth_Demo_with\__\<cellular_module>_/demo_config.h").

4. Compile and run.

The following is the console output of a successful execution of the bg96_mqtt_mutual_auth_demo.sln project.

```c
[INFO] [CELLULAR] [commTaskThread:287] Cellular commTaskThread started
>>>  Cellular SIM okay  <<<
>>>  Cellular GetServiceStatus failed 0, ps registration status 0  <<<
>>>  Cellular module registered  <<<
>>>  Cellular module registered, IP address 10.160.13.238  <<<
[INFO] [MQTTDemo] [prvConnectToServerWithBackoffRetries:583] Creating a TLS connection to xxxxx-ats.iot.us-west-2.amazonaws.com:8883.

[INFO] [MQTTDemo] [MQTTDemoTask:465] Creating an MQTT connection to xxxxx-ats.iot.us-west-2.amazonaws.com.

[INFO] [MQTTDemo] [prvCreateMQTTConnectionWithBroker:683] An MQTT connection is established with XXXXXXXXXX-ats.iot.us-west-2.amazonaws.com.
[INFO] [MQTTDemo] [prvMQTTSubscribeWithBackoffRetries:741] Attempt to subscribe to the MQTT topic testClient13:24:47/example/topic.

[INFO] [MQTTDemo] [prvMQTTSubscribeWithBackoffRetries:748] SUBSCRIBE sent for topic testClient13:24:47/example/topic to broker.


[INFO] [MQTTDemo] [prvMQTTProcessResponse:872] Subscribed to the topic testClient13:24:47/example/topic with maximum QoS 1.

[INFO] [MQTTDemo] [MQTTDemoTask:479] Publish to the MQTT topic testClient13:24:47/example/topic.

[INFO] [MQTTDemo] [MQTTDemoTask:485] Attempt to receive publish message from broker.

[INFO] [MQTTDemo] [prvMQTTProcessResponse:853] PUBACK received for packet Id 2.

[INFO] [MQTTDemo] [MQTTDemoTask:490] Keeping Connection Idle...


[INFO] [MQTTDemo] [MQTTDemoTask:479] Publish to the MQTT topic testClient13:24:47/example/topic.

[INFO] [MQTTDemo] [MQTTDemoTask:485] Attempt to receive publish message from broker.

[INFO] [MQTTDemo] [prvMQTTProcessIncomingPublish:908] Incoming QoS : 1

[INFO] [MQTTDemo] [prvMQTTProcessIncomingPublish:919]
Incoming Publish Topic Name: testClient13:24:47/example/topic matches subscribed topic.
Incoming Publish Message : Hello World!
```
