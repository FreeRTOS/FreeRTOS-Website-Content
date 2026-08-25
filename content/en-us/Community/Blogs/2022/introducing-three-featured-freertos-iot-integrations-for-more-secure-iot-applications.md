---
title: Introducing Three Featured FreeRTOS IoT Integrations for More Secure IoT Applications
date: 9 May 2022
feature: blog
categories:
  - Long term support
authors:
  - luciodj
---
We are excited to announce three [Featured FreeRTOS IoT Integrations](/Documentation/03-Libraries/08-Featured-integrations/01-Featured-integrations)
developed in collaboration with our partners Espressif, NXP and STMicroelectronics. Each project
demonstrates the use of the latest FreeRTOS and AWS Embedded C SDK
[Long Term Support (LTS)](https://freertos.org/lts-libraries.html) libraries, and the latest
microcontroller architecture capabilities to *raise the bar for the security and modularity of IoT
applications*. All three projects are designed to offer the developer not just an example
of a more secure cloud connected device, but one that can be easily customized into a complete,
production-worthy, IoT product.

These reference integration projects demonstrate the use of different microcontroller architectures
and different approaches to securely storing secrets. They all establish a more secure cloud connection
via mutual TLS authentication with the AWS IoT Core service and support Over the Air (OTA) updates to help
keep the application safe over the life of the product. OTA updates are performed seamlessly side by
side with the application (MQTT) telemetry and command/control tasks, thanks to the implementation of
the new [MQTT-Agent library](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/01-coreMQTT-agent).

In detail, you will find that:

* The **[Espressif ESP32-C3](/Documentation/03-Libraries/08-Featured-integrations/02-Espressif-ESP32c3)**
  integration is designed to leverage its latest generation RISC-V (32-bit) core and takes advantage
  of the on-board Digital Signature Peripheral (an on-chip secure enclave) to manage secrets more securely
  and accelerate all crypto-graphical operations. Thanks to the Bluetooth (BLE5) capabilities of the ESP32-C3
  system in a chip,
  the [ESP32-C3 DevKitM-1](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/hw-reference/esp32c3/user-guide-devkitm-1.html)
  evaluation kit provides an inexpensive yet complete IoT device development platform.

* The **[NXP i.MX RT1060](/Documentation/03-Libraries/08-Featured-integrations/04-NXP-iMX-RT1060)** integration is based on
  the [i.MX RT1060 Evaluation Kit](https://www.nxp.com/design/development-boards/i-mx-evaluation-and-development-boards/i-mx-rt1060-evaluation-kit:MIMXRT1060-EVK)
  (MIMXRT1060-EVK) combined with the EdgeLock® SE050 Development Kit (OM-SE050) for hardware-based security.
  Building on the work done previously to achieve the
  first [FreeRTOS SESIP security certification](https://freertos.org/2021/03/why-sesip-certification-for-freertos-matters.html),
  this new project provides a useful example of combining the AWS IoT Embedded C SDK libraries with a
  pre-provisioned (Plug & Trust) secure element to establish the IoT device identity and enable more
  secure communication with AWS IoT Core.

* The **[STMicro STM32U5](/Documentation/03-Libraries/08-Featured-integrations/05-STMicroelectronics-STM32U5)** integration is based on
  the [STM32U5 series](https://www.st.com/en/microcontrollers-microprocessors/stm32u5-series.html) Arm
  32-bit Cortex-M33 core (featuring ARM v8-M architecture) which
  incorporates [Arm TrustZone technology](https://developer.arm.com/ip-products/security-ip/trustzone)
  with on-chip hardware Root of Trust (RoT) to support secure boot, and secure data storage. In this
  project the OTA client makes use of Arm's PSA API. Private keys and other secrets required for
  local executable image and remote IoT cloud authentication are stored entirely within the TF-M
  and are not accessible from the non-secure side.

Make sure to read each of these new [Featured FreeRTOS IoT integrations](/Documentation/03-Libraries/08-Featured-integrations/01-Featured-integrations)
pages to dive deeper and learn how FreeRTOS and its
[Core libraries](/Documentation/03-Libraries/03-FreeRTOS-core/01-Introduction) allow you to quickly
and easily develop more secure and robust IoT applications.

FreeRTOS is an MIT licensed, open source, real-time operating system for microcontrollers and small microprocessors 
that makes small, low-power edge devices easy to program, deploy, secure, connect, and manage. Follow these links 
to get started with [FreeRTOS](https://freertos.org/RTOS.html), and its 
many [libraries and demo projects](/Documentation/03-Libraries/01-Library-overview/Library-categories). 
Download the source code 
from [FreeRTOS.org](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/) 
or [GitHub](https://github.com/freertos/freertos).


### About the author

![](https://secure.gravatar.com/avatar/9938f7b242eb47e5e8c3f41e0e927283?s=200&d=mm&r=g)
Lucio is a Product Manager at Amazon Web Services. He has held various technical and marketing roles
in the semiconductor industry for the past 20 years. As an opinionated and prolific author he has published
numerous articles and technical books on programming for embedded control applications. Following his
passion for flying, he has achieved both FAA and EASA private pilot licenses.
[View articles by this author](../author/luciodj)

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the
globe. [View Forums](https://forums.freertos.org/)
