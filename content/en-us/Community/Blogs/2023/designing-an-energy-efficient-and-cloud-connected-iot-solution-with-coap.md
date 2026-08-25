---
title: Designing an energy efficient and cloud-connected IoT solution with CoAP
date: 12 Dec 2023
feature: blog
authors:
  - mohameda
---
Two of the main factors considered during the development of Internet of Things (IoT) devices are 
efficiency and cloud compatibility. Efficiency, both in energy consumption and data usage, is important 
to reduce operational and maintenance costs - especially for cellular, battery-operated devices. Energy 
saving is a puzzle with many pieces, and choosing the appropriate communication protocol is an important 
piece. In general, IoT devices must communicate with cloud platforms that can process and analyze the 
data to generate useful insights, in addition to device management.


This blog provides an overview of the Constrained Application Protocol (CoAP), a communication protocol 
with built-in efficiencies, and it details the steps for maintaining cloud compatibility. Later in the 
blog, there is a sample implementation sequence using 
[1NCE 
FreeRTOS Blueprint](https://github.com/1NCE-GmbH/blueprint-freertos).


### Protocol selection in constrained IoT devices


CoAP is a client/server, request/response, UDP-based protocol. It includes the main web concepts, such 
as [Uniform Resource Identifier](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier) (URI) and internet media types, and it also provides RESTful (REST) services, 
making it a subset of HTTP optimized for constrained IoT devices. For secure communication, CoAP can be 
combined with Datagram Transport Layer Security (DTLS). 


Figures 1 & 2 show the communication stages required to send a test packet for MQTT and CoAP.


To use MQTT, you need to consider:


1. The 3-way TCP handshake (186 bytes).
2. MQTT Connect & [Connect Acknowledgment](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html) (ACK) (253 bytes).
3. The actual publish packet containing the payload (126 bytes).


...requiring a total of 565 bytes.

The first 2 stages must be repeated if the connection is not kept active with periodic PINGREQ packets, 
which can be challenging to realize for constrained IoT devices that have a long reporting interval, during 
which the device usually needs to go into power saving mode. Unstable cellular network coverage can cause 
the client to disconnect and also require initiating a new connection.


[![Sample MQTT communication](/media/2023/sample-mqtt-comm.png)](/media/2023/sample-mqtt-comm.png)
  

**Figure 1: Sample MQTT communication** 

With CoAP and the connectionless UDP protocol, the IoT device can directly send data without the need 
to establish a connection. In this example, we can see that the test packet needed 59 bytes, and if more 
reliable communication is required, the optional confirmation feature can be enabled. That adds a 46 byte 
ACK message from the server, requiring a total of 105 bytes.


[![Sample CoAP communication](/media/2023/sample-coap-comm.png)](/media/2023/sample-coap-comm.png)
  

**Figure 2: Sample CoAP communication** 

Using a connectionless protocol and sending less data can reduce the energy consumption of IoT devices. 
The following figure from an experiment conducted at 1NCE shows a possible reduction of up to 47.6% when 
using CoAP. Further energy saving is also possible with the 
[Energy 
Saver tool](https://help.1nce.com/dev-hub/docs/1nce-os-energy-saver) on the 1NCE software platform, which can be used to minimize the payload size.


[![Energy consumption comparison (MQTT/CoAP)](/media/2023/energy-consumption.png)](/media/2023/energy-consumption.png)
  

**Figure 3: Energy consumption comparison (MQTT/CoAP)** 

### Using more efficient IoT protocols while maintaining cloud compatibility


CoAP can be a suitable choice for constrained IoT devices. However, its adoption in cloud IoT platforms 
is still limited, which makes it challenging to design an IoT solution that is efficient and also accessible 
from different cloud platforms.


To solve this, 1NCE introduced the [IoT Integrator](https://help.1nce.com/dev-hub/docs/1nce-os-device-integrator) (Figure 4). Using this tool, IoT devices can 
send messages to 1NCE endpoints through protocols like CoAP, UDP or Lightweight Machine to Machine (LwM2M). 
Those messages can then be forwarded to [AWS IoT Core](https://aws.amazon.com/iot-core), as well as webhooks and other integrations.


[![1NCE OS – IoT Integrator](/media/2023/1nce-os-iot.png)](/media/2023/1nce-os-iot.png)
  

**Figure 4: 1NCE OS – IoT Integrator** 

### 1NCE FreeRTOS Blueprint


The 1NCE FreeRTOS Blueprint contains multiple demos that demonstrate how IoT devices can establish 
secure and efficient communication with 1NCE’s software platform using cellular connectivity.


#### Prerequisites


* [1NCE SIM Card](https://1nce.com/en-us/1nce-connect).
* [B-L475E-IOT01A2 
 STM32 Discovery kit IoT node](https://www.st.com/en/evaluation-tools/b-l475e-iot01a.html) connected to [BG96 (LTE Cat M1/Cat NB1/EGPRS modem) through X-NUCLEO-STMODA1 expansion board](https://www.st.com/en/evaluation-tools/steval-stmodlte.html).
* [STM32CubeIDE](https://www.st.com/en/development-tools/stm32cubeide.html)
* [STM32 ST-LINK 
 utility](https://www.st.com/en/development-tools/stsw-link004.html)


### CoAP demo components


For secure communication, the blueprint uses 1NCE SDK integration (as shown in Figure 5) to get DTLS 
credentials from the 1NCE OS device authentication endpoint. The credentials can be retrieved after identifying 
the device by the SIM ICCID. The blueprint also contains a sample MbedTLS configuration for DTLS with PSK 
authentication.


To get the DTLS credentials, the application calls the `os_auth()` function. This function uses 
the network interface defined in the SDK to communicate with the 1NCE Device Authentication endpoint. Received 
credentials can then be added to the Mbedtls configuration.


[![1NCE SDK integration](/media/2023/1nce-sdk-integration.png)](/media/2023/1nce-sdk-integration.png)
  

**Figure 5: 1NCE SDK integration
 (Click to Enlarge)**

It is also required to integrate a 3rd party library that can create and process CoAP packets. The 
blueprint uses the open source Lobaro CoAP library, which is integrated as shown in Figure 6. A network 
interface is added between the CoAP library and the FreeRTOS Secure Socket API by defining the functions 
`CoAP_Send` & `CoAP_Recv`. Those functions use a socket handle that has been 
configured for DTLS communication and connected to 1NCE’s CoAP server.


[![CoAP library integration](/media/2023/coap-lib-integration.png)](/media/2023/coap-lib-integration.png)
  

**Figure 6: CoAP library integration
 (Click to Enlarge)**

#### Configuration


* **Device**   

 To enable the CoAP demo, the definition "`CONFIG_COAP_DEMO_ENABLED`" should be added 
 to `config_files/aws_demo_config.h`.  

 In `/aws_demos/config_files/nce_demo_config.h`, the demo can be configured as follows:
	+ `PUBLISH_PAYLOAD_FORMAT`   The test payload
	+ `COAP_PORT`    Should be set to 5684 for DTLS communication
	+ `CLIENT_ICCID`    The SIM ICCID
	+ `COAP_URI_QUERY`   The CoAP URI-query option, used to configure the 
	 topic for MQTT Publish packets in AWS IoT core.
* **Cloud**   

 The user needs to set up the required cloud integration from the 1NCE portal. For example: 
 [AWS integration setup](https://help.1nce.com/dev-hub/docs/cloud-integrator-aws-configuration).


#### Running the demo


After you configure the demo and flash it to the board, the device will register with 1NCE OS and 
the following event will be displayed in the portal.


[![1NCE OS device registration](/media/2023/1nce-os-dev-reg.png)](/media/2023/1nce-os-dev-reg.png)
  

**Figure 7: 1NCE OS device registration** 

After that, the CoAP messages sent from the device will show on the portal as follows:


[![](/media/2023/coap-msg-sent.png)](/media/2023/coap-msg-sent.png)
  

**Figure 8: CoAP message sent to 1NCE OS** 

It will also be forwarded to the configured cloud integration (AWS IoT Core).


[![Forwarded MQTT message](/media/2023/fwd-mqtt-msg.png)](/media/2023/fwd-mqtt-msg.png)
  

**Figure 9: Forwarded MQTT message** 

With the Energy Saver tool, the application can only send the value updates instead of sending the 
whole JSON object, as shown in the following example.


[![Payload size reduction](/media/2023/payload-size-reduc.png)](/media/2023/payload-size-reduc.png)
  

**Figure 10: Payload size reduction** 

This can help reduce the energy consumption of the device and data usage as well. This feature can be 
enabled by defining "`CONFIG_NCE_ENERGY_SAVER`" in `/aws_demos/config_files/nce_demo_config.h`.
The function `os_energy_save()` can then be used to create the payload.


### Additional demos (UDP & LwM2M)


The blueprint also includes a [UDP demo](https://github.com/1NCE-GmbH/blueprint-freertos/tree/main#udp-demo) for basic communication. In addition, a 
[LwM2M demo](https://github.com/1NCE-GmbH/blueprint-freertos/tree/main#lwm2m-demo) can be used for applications requiring more advanced IoT device 
management.


### Summary


Using CoAP can provide a considerable reduction in the energy and data usage of IoT devices. With the 
IoT Integrator tool from 1NCE OS, this reduction can be achieved without affecting cloud compatibility. 
The CoAP demo in the 1NCE FreeRTOS Blueprint provides a starting point for developers interested in testing 
and evaluating CoAP, and shows how CoAP can be integrated with FreeRTOS. It also includes the communication 
with 1NCE’s software platform for device authentication and for sending CoAP messages that can be forwarded 
to the configured cloud platforms.
