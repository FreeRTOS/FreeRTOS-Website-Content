---
title: "Featured FreeRTOS IoT Integration Using AWS IoT ExpressLink"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


## Introduction

Other [featured FreeRTOS reference integrations](/Documentation/03-Libraries/08-Featured-integrations/01-Featured-integrations) 
demonstrate the [long-term support (LTS) versions of the FreeRTOS libraries](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries), 
along with hardware backed security, and are used to help create secure and authenticated cloud connections. 
This page shows how to use AWS IoT ExpressLink modules (from here on "ExpressLink") to more easily achieve 
the same goal.


ExpressLink modules are [hardware Wi-Fi and cellular modules](https://devices.amazonaws.com/search?page=1&sv=iotxplnk) 
with built-in cloud connectivity, over-the-air (OTA) updates, and hardware backed secure storage for 
encryption and authentication keys. Host processors that execute IoT applications communicate with 
ExpressLink through a serial port using a simple AT command set. All ExpressLink modules use the same 
command set, irrespective of the underlying radio types (e.g. Wi-Fi, cellular). By using ExpressLink 
modules, IoT application writers no longer have to handle the complexity of radio, security, and IoT 
libraries. Instead, these developers can focus on their differentiating functionality.

ExpressLink modules can be used from any device with a serial port, from tiny 8-bit microcontrollers (MCUs) 
to rack mounted servers. This page highlights ExpressLink demos created 
by [ST's I-Cube-ExpressLink](https://github.com/stm32-hotspot/I-CUBE-ExpressLink) that target a range of 
STM32 MCUs.


[![](/media/2023/design-of-connected-apps-iotel.png)](/media/2023/design-of-connected-apps-iotel.png)   
**Figure 1: Design of connected applications with AWS IoT ExpressLink**


## Demonstrated security features and functions

All AWS IoT ExpressLink modules implement the security best practices described in the following subsections.


### Secure TLS communication with mutual authentication

ExpressLink modules establish a secure and encrypted connection with AWS IoT Core 
using [Transport Layer Security (TLS)](https://en.wikipedia.org/wiki/Transport_Layer_Security). This 
connection is mutually authenticated, ensuring the identity of both the device and the cloud. Each 
module is pre-configured with a unique identifier, private key, and certificate necessary to establish
this secure connection. The certificate is signed by a Certificate Authority (CA) that is already registered 
with AWS by the module vendor. This solves the scalability, potential for error, and security problems 
associated with IoT device provisioning, while reducing complexity and costs.


### Keeping device identity and secrets secure

ExpressLink modules use hardware backed secure storage to keep device identity and private keys safe.


### No disclosure of confidential information within the supply chain

*Onboarding* is the process of binding the module's credentials to a "thing" inside 
the [AWS IoT registry](https://docs.aws.amazon.com/iot/latest/developerguide/iot-thing-management.html) 
of the OEM's account. ExpressLink uses a 
novel [onboarding-by-claim](https://docs.aws.amazon.com/iot-expresslink/latest/oemonboardingguide/oemog.html) 
mechanism to do this automatically the first time the device powers up. This late binding removes the 
need to provide any secret information, such as private keys, to suppliers with the IoT device's supply 
chain.


### Preventing unauthorized software from running on the device

ExpressLink modules include a hardware root of trust backed secure bootloader that cryptographically 
verifies its firmware integrity at each boot stage, helping to prevent unauthorized ExpressLink firmware 
modification.


The STM32 examples also use Tiny Secure Boot, ensuring ECDSA signature verification of the host (the 
MCU that communicates with ExpressLink) software. Tiny SecureBoot has a compact footprint of less than 
15K of Flash. They also leverage the ExpressLink module’s capability to verify the integrity (hash) and 
authenticity (signature) of the new host images received over the air – offloading these cryptography 
tasks from the host application.


### Secure over the air (OTA) updates

OTA updates enhance security by patching security vulnerabilities and bugs in already deployed devices. 
ExpressLink's OTA feature enables secure firmware updates for both the ExpressLink module and host MCU.

Module updates occur without disrupting the host MCU. Each module comes pre-provisioned with an OTA 
"birth certificate" used to verify its firmware updates were authorized by the module manufacturer. The 
module signals the host MCU to accept or reject the update after successful verification, ensuring the 
compatibility.

Host MCU updates can receive any file type, not just new firmware versions. They use the same mechanism 
as module updates, except that host MCU OTA certificates can't be pre-provisioned. Instead, the certificate 
must first be generated, uploaded, and securely stored within the ExpressLink module. The ST examples 
provide a script for this purpose.

Authenticating firmware updates in the ExpressLink module offloads this heavy cryptographic task from the host application.


## Getting started with I-CUBE-ExpressLink

[I-Cube-ExpressLink](https://github.com/stm32-hotspot/I-CUBE-ExpressLink) is a CMSIS pack containing 
an extensive collection of FreeRTOS projects that use ExpressLink and 
target [STM32 Arm Cortex MCUs](https://www.st.com/en/microcontrollers-microprocessors/stm32-32-bit-arm-cortex-mcus.html).
It includes an ExpressLink driver which is a single wrapper that manages ExpressLink commands and responses 
over a serial interface. These commands and responses are common to, and used extensively in application 
examples that run on, >10 STM32 development boards. The pack also includes a rich set of tools that 
simplify the Host OTA process and help you to deploy at scale, reducing the number of steps and eliminating 
the need for familiarity with the AWS console. The FreeRTOS projects demonstrate typical IoT scenarios:

* Transmitting sensor data to the cloud.
* Sending and receiving messages to and from cloud.
* Using [AWS IoT Shadows](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html) 
  to control LEDs and other actuators from the cloud. (ExpressLink includes Shadow functionality.)
* Updating host firmware over-the-air.
* Managing ExpressLink module events.

These examples function seamlessly with both ExpressLink cellular and Wi-Fi modules, and don't require any
code modification.

To get started, watch the STM32 ExpressLink tutorial videos:

* Video 1: [Get started with I-Cube-ExpressLink](https://www.youtube.com/watch?v=CAu-zse7nbM).
* Video 2: [Build FreeRTOS, issue a host OTA update, and enable ExpressLink\_Event](https://youtu.be/CJrZzpHr38g).
* Video 3: [Use Tiny Secure Boot and perform a host OTA](https://youtu.be/r7H9otJWWCI).

then visit the [I-Cube-ExpressLink](https://github.com/stm32-hotspot/I-CUBE-ExpressLink) github repository 
to begin development. The repository provides a comprehensive list of features, including the ExpressLink 
driver, example source code, as well as instructions for installing the packs, generating, building, and 
running the FreeRTOS ExpressLink demos.

