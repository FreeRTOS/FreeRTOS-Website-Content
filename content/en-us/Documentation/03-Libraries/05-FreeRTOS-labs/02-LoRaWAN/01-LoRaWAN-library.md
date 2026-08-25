---
title: LoRaWAN
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


**NOTE**: The FreeRTOS LoRaWAN demo project is provided in the [FreeRTOS Labs](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction)
for community interest and to serve as a reference. It is fully functional, but may not comply with our
production code standards. It is available from
the [Lab-Project-FreeRTOS-LoRaWAN](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-LoRaWAN) repository
on GitHub.


## Introduction

[LoRa](https://en.wikipedia.org/wiki/LoRa) (short term for long range) is a spread spectrum modulation
technique derived from chirp spread spectrum (CSS) technology. LoRaWAN is the network system architecture
and communication protocol specification for LoRa, developed by the [LoRa Alliance](https://lora-alliance.org/).
LoRaWAN is a Media Access Control (MAC) layer protocol that enables LoRa in wider applications.

The LoRa Alliance defines the networking layer and the system architecture for the network. A LoRaWAN
connectivity flow is depicted in Figure 1, showing the different components that connect end nodes to the
cloud and to application servers.

[![](/media/2020/Figure-1-2.png)](/media/2020/Figure-1-2.png)
*Figure 1 - LoRaWAN Network Architecture. Click to enlarge.*

Unlike cellular technologies, LoRa end-nodes are not associated with a specific gateway. Instead, data
is transmitted by a node and received by multiple gateways. Each gateway then forwards the packet from
the end-node to a cloud based LoRa Network Server (LNS) via some backhaul (either cellular, ethernet,
satellite, WiFi). LNS has the complexity and intelligence to manage the network, filter redundant packets,
perform security checks, and enable adaptive data rates, etc. As a result, there is no handover from
one gateway to another for a mobile LoRaWAN end device.

Application server (AS) is responsible for securely handling, managing and interpreting sensor application
data. It also feeds the data to drive dashboard UI.

The Join Server (JS) manages over-the-air activation (OTAA) process for end devices to be added to the
network. The JS performs the Join procedure (mutual authentication) with end device and notifies the
LNS which AS should the end device connect to and performs the session keys derivation. Each JS is identified
by a 64-bit globally unique identifier, AppEUI/JoinEUI. The end device derives session keys locally, based
on the DevEUI, Join EUI, DevNonce, root keys (AppKey, NwkKey), such that security keys aren’t exchanged
over the air. JS communicates to LNS the Network Session Key and to AS the Application Session Key.
Individual root keys are securely stored on the end devices, and equivalent matching keys are securely
stored on the JS. As such, JS contains the following information for each end-device under its control:

* DevEUI (end-device serial unique identifier)
* Root Keys
  + AppKey (application encryption key)
  + NwkKey (network encryption key)
* Application Server identifier
* End-Device Service Profile

In Activation by Personalization (ABP) activation procedure, a simplified and less secure commissioning
process, the Join procedure is skipped and the IDs and keys are personalized at the time of fabrication.
End devices are tied to a specific network/service and the network identifier (NetID) is part of
the device network address such that end devices become immediately functional upon powering up.

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

LoRaWAN Stack in FreeRTOS, as shown in Figure 2, uses a LoRaWAN management task to abstract away the
timing constraints for a LoRaWAN network and thereby providing a simpler programming model for applications.
It separates the concern of processing radio interrupts and MAC layer events from the user application.
This allows the application task to be more modular with a sequential flow of execution. Also this allows
having well defined helper APIs that can be reused across different applications - for example blocking
APIs for joining a network, sending and receiving raw data. There are also helper functions for configuring
and retrieving the join credentials, if the device does not support secure provisioning. For the current
release, only Class A capabilities are supported. Class B & C will be supported in future releases along
with the ability for applications to switch between different classes of operation. Stack also exposes
the radio Hardware Abstraction Layer (HAL) which provides applications the ability to control LoRa radio
or modem directly. The HAL can be implemented for one or more LoRa radio transceivers or LoRa radio modems.

LoRaWAN stack in FreeRTOS uses the LoRaMac-Node, which is Semtech’s open source implementation of the LoRaWAN
end device protocol specification. The stack implements version 1.0.3 of LoRaWAN specification. For more
details on LoRaMac-Node visit the [Semtech’s documentation](http://stackforce.github.io/LoRaMac-doc/).
Source code for FreeRTOS support for LoRaWAN is available [here](https://github.com/Lora-net/LoRaMac-node).

[![](/media/2020/Figure-2.png)](/media/2020/Figure-2.png)
*Figure 2 - LoRaWAN Stack in FreeRTOS. Click to enlarge.*
