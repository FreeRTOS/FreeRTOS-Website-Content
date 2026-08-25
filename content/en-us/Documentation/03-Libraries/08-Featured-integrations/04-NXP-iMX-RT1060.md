---
title: "Featured FreeRTOS IoT Reference Integration "
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

#### Targeting an NXP i.MX RT1060 MCU and EdgeLock® SE050 Secure Element

*This featured reference integration gives you great flexibility to adapt their functionality and utilize 
your hardware features. Or, to trade that flexibility for simplicity, also consider 
the [ExpressLink featured integration](06-STM32-Expresslink).*


## Introduction

These demos show how to integrate the [Long-Term Support (LTS)](/Community/Blogs/2021/freertos-aws-reference-integrations-now-include-freertos-202012-01-lts-libraries) FreeRTOS kernel
and libraries with hardware enforced security to help create more secure cloud connected applications.
The projects are preconfigured to run on
the [i.MX RT1060 Evaluation Kit](https://www.nxp.com/design/development-boards/i-mx-evaluation-and-development-boards/i-mx-rt1060-evaluation-kit:MIMXRT1060-EVK)
(i.MX RT1060-EVK) with
an [i.MX RT1060 Arm® Cortex®-M7 MCU](https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/i-mx-rt-crossover-mcus/i-mx-rt1060-crossover-mcu-with-arm-cortex-m7-core:i.MX-RT1060)
and the [EdgeLock® SE050 Development Kit](https://www.nxp.com/products/security-and-authentication/authentication/edgelock-se050-development-kit:OM-SE050X)
(OM-SE050) for hardware-based root of trust.


[![](/media/2022/imxrt1060-eval-kit.png)<br />i.MX RT1060 Evaluation Kit](https://www.nxp.com/design/development-boards/i-mx-evaluation-and-development-boards/i-mx-rt1060-evaluation-kit:MIMXRT1060-EVK)
[![](/media/2022/edgelockse050-dev-kit.png)<br />EdgeLock® SE050 Development Kit](https://www.nxp.com/products/security-and-authentication/authentication/edgelock-se050-development-kit:OM-SE050X) |


## Demonstrated security features and functions

### Preventing unauthorized software from running on the device

A secure boot process is designed to help ensure that firmware images running on the board were cryptographically signed by
the original equipment manufacturer (OEM). Code signing is done with [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) key
pairs. The private key of a pair, a secret key known only to the OEM, is used to sign images. The public key is programmed into
the device, and can be used to verify that an image was signed by the private key.

The boot process demonstrated has three stages, as described in
the [Featured FreeRTOS Integrations](01-Featured-integrations) page.

![](/media/2022/NXPimxrt1060GRI.png)
Figure 1: Security architecture

The first stage bootloader is built into the i.MX RT1060 in ROM and is cannot be modified. The second stage bootloader,
from the open source project [MCUboot](https://www.mcuboot.com/), is included as a buildable project in
the reference integration repository. The third stage is an application, built on FreeRTOS. The repository includes
multiple application projects, each demonstrating different ways to use AWS IoT services.

The first stage bootloader can verify the digital signature of the second stage bootloader, and establish that it can be
trusted using the public key from a secure store. The second stage bootloader verifies the signature on the application
image. In this way it establishes trust for the application before it runs it. The instructions in the
"Create Signing keys for the Bootloader" and "Create a Signed Application Image" sections of
the [Getting Started Guide](https://github.com/FreeRTOS/iot-reference-nxp-rt1060/tree/main)
include steps to generate the necessary keys, embed the public key in MCUboot, and sign the application executable.

The public key used to verify MCUboot must also be protected. The iMX RT1060 has one-time programmable (OTP)
fuses to enable this. An array of OTP fuses are used to implement a very small storage area that can only be programmed one
time. This storage area records the boot configuration including a hash of the public code signing keys used to validate code
signatures. Initially, the boot configuration is set to an "open" mode, allowing any code to be loaded and run on the device.
Once the boot configuration fuses are programmed for the "closed" mode, only a signed image of MCUboot can be run,
and it is impossible to return to the open mode. This one-way transition should be performed on all production devices.

This open configuration is convenient for development, so the reference integration's Getting Started Guide explains how
to sign firmware images, but leaves the boot configuration open.


### Keeping device identity and secrets secure

Devices that connect to AWS IoT are uniquely identified by a TLS Client Certificate using a private key to prevent devices
from impersonating one another. The device's unique private key must be kept secret to prevent unauthorized access and
communication. The EdgeLock SE050, a separate peripheral from the main processor, implements a secure storage
system for a client certificate and its associated private key. Each SE050 comes with a unique client certificate and
associated private key already programmed. See the "device certificate and private key" in figure 1 above. The SE050 does not
include an interface for reading out the private key, so only this single device can prove it owns the client certificate.

Unlike the private key, the client certificate is public information that can be extracted from the SE050. The Getting Started
Guide explains how to read the client certificate through a serial interface, which you will need to do to register the
evaluation kit's identity with your AWS account.

The secure [Transport Layer Security (TLS)](https://en.wikipedia.org/wiki/Transport_Layer_Security)
protocol requires clients to prove their ownership of a client certificate using its
associated private key. Since the private key is confined to the SE050, the reference integration code provides an
implementation of the [PKCS #11 API](https://en.wikipedia.org/wiki/PKCS_11),
which allows the required cryptographic operations to be performed on the SE050,
without direct access to the key.


### Secure TLS communication with mutual authentication

Communication between the device and the AWS IoT Core MQTT broker is encrypted
using [TLS version 1.2](https://en.wikipedia.org/wiki/Transport_Layer_Security#TLS_1.2).
See [Transport security in AWS IoT](https://docs.aws.amazon.com/iot/latest/developerguide/transport-security.html)
for details. The demos use the EdgeLock SE050 secure element which comes with a unique
client certificate and associated private key already programmed. The client certificate can be retrieved
without exposing the private key, and registered with AWS IoT to establish TLS connection with the AWS IoT Core
MQTT broker using the [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) library.


### Over the air (OTA) updates

The reference integration includes a demo of Over the Air (OTA) updates to enable remote patching of security
vulnerabilities and bug fixes. This demo uses
the [AWS IoT OTA service for FreeRTOS](https://docs.aws.amazon.com/freertos/latest/userguide/freertos-ota-dev.html)
to deploy new images through the cloud. The OTA client software, from the [AWS IoT OTA library](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates), runs
in a background task and waits to receive notifications from the cloud that new firmware images are available. Upon
receiving a notification, the device downloads the new image, and the device then reboots to run the new image.

The OTA demo uses two features of the reference integration to improve robustness and security: primary and secondary
firmware image slots, and signed OTA images.

The MCUboot secondary boot loader divides flash memory into three regions. One is for the bootloader itself, and the other
two are used as primary and secondary firmware image slots. Only one firmware slot is active at a time. When the OTA
library downloads a new firmware image, it stores the update in the inactive slot, leaving the active firmware untouched.
This allows MCUboot to fall back to the older firmware if something goes wrong with the new one, like a failed code
signing verification.

In addition to the code signature verification in the secure boot system, the OTA service and its client library add their own
code signing and verification steps to the image download process. As with the public keys used to validate images in
secure boot, the public key used to validate OTA signatures must be stored on each IoT device, and should be
protected from changes. The reference integration code shows how to store this key in the SE0050.


### Memory safety proofs

The "core" FreeRTOS libraries comply with documented code quality criteria, including memory safety proofs that run on
each code check-in.


## What the demo applications do

The reference integration includes demo applications that connect to the AWS IoT Core MQTT broker through the i.MX
RT1060's Ethernet connector. The applications carry out common IoT device functionality, including exchanging MQTT
messages with the cloud, and using the AWS IoT OTA service for FreeRTOS to download and install new firmware
images.


## Getting started with the demos

The README file in the root of this project's Git repo provides instructions on downloading the source code
and the GSG provides step by step instructions on how to build and run the demo. Visit
the [FreeRTOS/iot-reference-nxp-rt1060 Git repository](https://github.com/FreeRTOS/iot-reference-nxp-rt1060)
to get started.
