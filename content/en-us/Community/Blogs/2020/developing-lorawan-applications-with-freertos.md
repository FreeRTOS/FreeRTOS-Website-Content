---
title: Developing LoRaWAN Applications with FreeRTOS
date: 
feature: blog
categories:
  - Long term support
authors: 
  - gvg
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---


by [Gaurav Gupta](../author/gvg) on 14 Dec 2020

We are excited to introduce the [LoRaWAN - FreeRTOS Labs Project](/Documentation/03-Libraries/05-FreeRTOS-labs/02-LoRaWAN/01-LoRaWAN-library), a reference 
implementation of LoRaWAN connectivity with FreeRTOS. This project is meant to demonstrate how FreeRTOS 
can simplify the development of IoT applications using LoRa technology. LoRa is a long range and low-power 
wireless technology operating in the unlicensed spectrum. It is designed for sensors that need to send 
infrequent, small amounts of data over long distances in a variety of environments. LoRa is the physical 
layer spread spectrum modulation technique derived from chirp spread spectrum (CSS) wireless communication 
technology. LoRaWAN is the network system architecture and communication protocol specification for LoRa, 
developed by the [LoRa Alliance](https://lora-alliance.org/). 


## LoRaWAN Network Architecture

The LoRa Alliance defines the networking layer and the system architecture for the network. A LoRaWAN 
connectivity flow is depicted in Figure 1, showing the different components that connect end nodes to 
the cloud and to application servers.

![Figure 1 - LoRaWAN Network Architecture](/media/2020/Figure-1-2.png)  
*Figure 1 - LoRaWAN Network Architecture*


Unlike cellular technologies, LoRa end-nodes are not associated with a specific gateway. Instead, data 
is transmitted by a node and received by multiple gateways. Each gateway then forwards the packet from 
the end-node to a cloud based LoRa Network Server (LNS) via some backhaul (either cellular, ethernet, 
satellite, WiFi). LNS has the complexity and intelligence to manage the network, filter redundant packets, 
perform security checks, and enable adaptive data rates, etc. As a result, there is no handover from one 
gateway to another for a mobile LoRaWAN end device. 

Application server (AS) is responsible for securely handling, managing and interpreting sensor application 
data. It also feeds the data to drive dashboard UI. 

The Join Server (JS) manages over-the-air activation (OTAA) process for end devices to be added to the 
network. The JS performs the Join procedure (mutual authentication) with end device and notifies the 
LNS which AS should the end device connect to and performs the session keys derivation. Each JS is identified 
by a 64-bit globally unique identifier, AppEUI/JoinEUI. The end device derives session keys locally, 
based on the DevEUI, Join EUI, DevNonce, root keys (AppKey, NwkKey), such that security keys aren’t 
exchanged over the air. JS communicates to LNS the Network Session Key and to AS the Application Session 
Key. Individual root keys are securely stored on the end devices, and equivalent matching keys are securely 
stored on the JS. As such, JS contains the following information for each end-device under its control:

* DevEUI (end-device serial unique identifier)
* Root Keys
  + AppKey (application encryption key)
  + NwkKey (network encryption key)
* Application Server identifier
* End-Device Service Profile

In Activation by Personalization (ABP) activation procedure, a simplified and less secure commissioning 
process, the Join procedure is skipped and the IDs and keys are personalized at the time of fabrication. 
End devices are tied to a specific network/service and the network identifier (NetID) is part of the 
device network address such that end devices become immediately functional upon powering up. 

LoRaWAN specification defines three types of end devices: Class A, Class B and Class C. Class A device 
spends most of the time in Idle state (i.e. power save mode). When there are changes to sensor environment 
the end device is monitoring, the device wakes up and initiates an uplink, transmitting (Tx) the sensor 
reading to the LNS. The end device then listens for the response from LNS, it opens up to two receive (Rx) 
windows at specified times (1s and 2s) after the last uplink transmission (Tx). The LNS can send the downlink 
in either of the Rx windows. Class B extends the Class A Rx functionality by adding scheduled Rx windows 
for downlink messages from LNS. This is done by using time-synchronized beacons transmitted by the gateway, 
indicating the end device to periodically open Rx windows. Class C further extends Class A by keeping the 
receive (Rx) window, always on. Class C devices do not depend on battery power and are always listening 
for downlink messages, except when they are transmitting (Tx) uplink. As a result, Class C offers lowest 
latency for communication between the LNS and end-device. For detailed description of LoRaWAN 1.0.3, 
see [here](https://resources.lora-alliance.org/document/lorawan-specification-v1-0-3). 


## LoRaWAN stack in FreeRTOS

FreeRTOS offers several benefits for embedded software developers. [Read more](/Why-FreeRTOS/FAQs/What-is-this-all-about#why-use-an-rtos). 

LoRaWAN Stack in FreeRTOS, as shown in Figure 2, uses a LoRaWAN management task to abstract away the timing 
constraints for a LoRaWAN network and thereby providing a simpler programming model for applications. It 
separates the concern of processing radio interrupts and MAC layer events from the user application. This 
allows the application task to be more modular with a sequential flow of execution. Also this allows having 
well defined helper APIs that can be reused across different applications - for example blocking APIs for 
joining a network, sending and receiving raw data. There are also helper functions for configuring and 
retrieving the join credentials, if the device does not support secure provisioning. For the current release, 
only Class A capabilities are supported. Class B & C will be supported in future releases along with the 
ability for applications to switch between different classes of operation. Stack also exposes the radio 
Hardware Abstraction Layer (HAL) which provides applications the ability to control LoRa radio or modem 
directly. The HAL can be implemented for one or more LoRa radio transceivers or LoRa radio modems.

LoRaWAN stack in FreeRTOS uses the LoRaMac-Node, which is Semtech’s open source implementation of the 
LoRaWAN end device protocol specification. The stack implements version 1.0.3 of LoRaWAN specification. 
For more details on LoRaMac-Node visit the [Semtech’s documentation](http://stackforce.github.io/LoRaMac-doc/). 
Source code for FreeRTOS support for LoRaWAN is available [here](https://github.com/Lora-net/LoRaMac-node). 

![](/media/2020/Figure-2.png)   
**Figure 2 - LoRaWAN Stack in FreeRTOS**  


## Developing LoRaWAN IoT Applications

In LoRaWAN communication, both uplink and downlink messages can be either confirmed (an ACK is required 
from the other party) or unconfirmed (no-ACK required). The following diagrams Figure 3a and 3b shows the 
sequence of confirmed uplink and downlink. For detailed explanation, refer to Section 18 
of [LoRaWAN 1.0.3](https://lora-alliance.org/wp-content/uploads/2020/11/lorawan1.0.3.pdf) specification. 

![Figure 3a - Uplink timing diagram for confirmed data messages (Source: LoRa Alliance)](/media/2020/Figure-3a.png)  
*Figure 3a - Uplink timing diagram for confirmed data messages (Source: LoRa Alliance)*
  
  
![Figure 3b - Downlink timing diagram for confirmed data messages (Source: LoRa Alliance)](/media/2020/Figure-3b.png)  
*Figure 3b - Downlink timing diagram for confirmed data messages (Source: LoRa Alliance)*
  
The FreeRTOS stack spawns a Class A application task which sends an uplink message periodically following 
the link fair access policy defined by 
the [LoRaWAN regional parameters](https://resources.lora-alliance.org/technical-specifications/rp002-1-0-4-regional-parameters). 
Uplink messages can be send either in confirmed or unconfirmed mode. After a successful uplink, the task 
waits for any downlink messages or other events from the MAC layer. It writes the frame payload and port 
received downlink to the console. If MAC layer indicates that there are further downlink messages pending 
or an uplink needs to be sent for control purposes, then it sends an empty uplink immediately. If a frame 
loss is detected by MAC layer, then it triggers a re-join procedure to reset the frame counters. Once all 
downlink data and events are processed, the task goes back to sleep until the next transfer cycle.

All events from MAC layer to application are sent using light weight task notifications. LoRaWAN allows 
multiple requests for the server to be piggy-backed to an uplink message. The responses to these requests 
are received by application in order using a queue. A downlink queue exists in case application wants to 
read multiple payloads received at once, before sending an uplink payload. 


## Low Power Mode

An important feature of Class A based communication is that application sleeps for most part of its 
lifecycle thereby consuming less power. Low power mode can be enabled for the demo using FreeRTOS tickless 
idle feature as described [here](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support). Tickless idle mode can be enabled by 
providing a board specific implementation for `portSUPPRESS_TICKS_AND_SLEEP(`) macro and 
setting `configUSE_TICKLESS_IDLE` to the appropriate value in `FreeRTOSConfig.h`. Enabling tickless mode 
allows MCU to sleep when the tasks are idle, but be waken up by an interrupt from the radio or other 
timer events.


## Supported Platforms

| Vendor | MCU | LoRa Radio Shield | IDE |
| ------ | --- | ----------------- | --- |
| Nordic | [NRF52840-DK](https://www.nordicsemi.com/Software-and-Tools/Development-Kits/nRF52840-DK) | [sx1262mb2cas](https://www.semtech.com/products/wireless-rf/lora-transceivers/sx1262mb2cas) | [Segger Embedded Studio (SES)](https://www.segger.com/downloads/embedded-studio) |
| STMicroeletronics | [STM32-L4](https://www.st.com/en/microcontrollers-microprocessors/stm32l4-series.html) | [sx1276MB1LAS](https://www.semtech.com/products/wireless-rf/lora-transceivers/sx1276mb1las) | [System workbench for STM32](https://www.st.com/en/development-tools/sw4stm32.html) |

Gateway hardware needed to build and test FreeRTOS LoRaWAN applications:
 
* [LoRa Raspberry Pi Gateway](https://www.sparkfun.com/products/15336) (see [Getting Started](https://cdn.sparkfun.com/assets/3/0/d/e/2/Get_Start_with_RAK2245_Pi_HAT_V2.4R.pdf) to connect to The Things Network)


## Summary

The [LoRaWAN FreeRTOS Lab project](/Documentation/03-Libraries/05-FreeRTOS-labs/02-LoRaWAN/01-LoRaWAN-library) provides a reference implementation of a LoRaWAN 
node using FreeRTOS to simplify development of low power and long range IoT applications using LoRa 
technology. You will find the full application source code and a detailed API reference for the LoRaWAN 
manager in the [FreeRTOS LoRaWAN repository](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-LoRaWAN). 
We encourage your contributions to expand the catalog of supported platforms and application examples of 
this exciting technology. 

FreeRTOS is an MIT licensed open source, real-time operating system for microcontrollers and small microprocessors
that makes small, low-power edge devices easy to program, deploy, secure, connect, and manage. You can get started 
by [downloading source code](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) from FreeRTOS.org or GitHub (https://github.com/freertos/freertos) 
and can find more information about the FreeRTOS, its libraries and demos on 
the [FreeRTOS User Guide](/Documentation/03-Libraries/02-FreeRTOS-plus/01-Introduction).


## Authors:

* Gaurav Gupta (Sr. Partner Solutions Architect - AWS IoT)
* Paul Butler (Sr. Partner Solutions Architect - AWS IoT)
* Ravishankar Bhagavandas (Software Development Engineer - AWS IoT)


## About the author
![](https://secure.gravatar.com/avatar/9f2c9ea3a14d003577468a67df66cb35?s=200&d=mm&r=g) 

Gaurav Gupta is a Global Partner Solutions Architect at AWS IoT where he focuses on helping customers & 
partners, specifically IoT connectivity enablers in LoRaWAN and Telco, build and integrate their products 
with AWS services. Prior to AWS, he has 15+ years of experience in wireless standards, network architecture 
and deployment in tier-1 operator. He has 11 granted patents in wireless/IoT/cloud and several patents 
pending.   
[View articles by this author](../author/gvg) 


FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
