---
title: "Featured FreeRTOS IoT Integrations"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## Internet Connected Devices
The internet of things (IoT) refers to networked devices that exchange data with other devices, and the cloud, over the internet.  IoT devices are used in a wide range of industries from basic consumer goods, for example smart plugs, to heavy industries, for example oil well sensors.  Many of these devices run FreeRTOS.

IoT applications require more than just basic connectivity. They need robust security, privacy, and authentication mechanisms. This, in turn, requires a way to give each connecting device a unique cryptographic identity and associated secret keys - a process known as "device provisioning."

Building a secure, internet-connected device is a non-trivial task. To help with this, this page provides example integrations containing everything necessary.

Best practices demonstrated by these examples include making sure the device:

* only runs software approved by the original equipment manufacturer (OEM).
* uses a verifiable, per-device identity when authenticating to cloud services.
* helps keep network data secure using cryptography and the Transport Layer Security (TLS) protocol.
* stays up to date with the latest, publicly available security fixes through the lifetime of the device.


This page describes the functionality common across all examples.  There are two categories:

1. A very simple method using AWS IoT ExpressLink. This offloads all the required security and provisioning functionality to a radio module that is accessible to any microcontroller or microprocessor with a UART interface.

	* [ExpressLink featured integration](06-STM32-Expresslink)

1. More flexible and performant software-only [IoT library](/Documentation/03-Libraries/01-Library-overview/01-All-libraries) integrations running on microcontrollers. These include hardware-backed security capable of keeping cryptographic identities and keys private.

	* [NXP i.MX RT1060 Arm Cortex-M7 MCU with EdgeLock SE050 Secure Element](04-NXP-iMX-RT1060)
	* [STMicroelectronics STM32U5 Arm Cortex-M33 MCU with TrustZone and TF-M](05-STMicroelectronics-STM32U5)
	* [Espressif ESP32-C3 RISC-V MCU with Digital Signature Peripheral (DSP)](02-Espressif-ESP32c3)
	* [ARM Corstone 3xxx](03-ARM-corstone3xx)


## What the demo application does

Each FreeRTOS IoT integration implements a basic IoT demo application that connects to the AWS IoT
Core MQTT broker to exchange messages with the cloud. The application can also download updates to
its own image from the cloud. The source code demonstrates security best practices in software, and
shows how to integrate hardware security features to achieve even stronger security assurance.


## How the FreeRTOS IoT integrations implement security

Each of these integrations includes code that demonstrates how to use hardware features that
support secure operation. Each board has two key capabilities implemented in its hardware:
keeping critical code unchanged, and keeping cryptographic keys hidden. This core functionality is designed to create
a hardware-based root of trust, a foundation that supports software security features. The FreeRTOS IoT
integration software builds a more secure boot process, a verifiable device identity, and a firmware update
system on top of it.


### Secure boot

Secure boot means that when a device starts, its application software is checked for authenticity before
it starts running. Each FreeRTOS IoT integration board embeds an unchangeable boot loader directly in
hardware. This boot loader is the first code that runs when the device starts, and it can be trusted
because it can't be modified due to a security vulnerability or operational mistake. The boot loader's
only job is to validate the authenticity of the OEM supplied firmware image, and then run it if the image
is authentic.

The validation step uses a pair of cryptographic keys to implement a code-signing system. The
details of the code-signing process vary across boards, but each implementation accomplishes the same
thing-- the OEM can ensure that only their own firmware will run on the board. An OEM
cryptographically signs their firmware images using a private code-signing key, and the bootloader uses
the corresponding public key to verify the signature. The private code-signing key is secret, and known
only to the OEM. Therefore, only the OEM can sign new firmware images with this key. The public key is
not secret, and can be stored on each device. The reference boards each provide a way to program the
public code-signing key and then permanently freeze its value.

In the board-specific documentation provided by the manufacturer, you'll see a description of a
simplified boot process with only one boot loader. The integrations add a second stage boot loader into the process,
between the first stage boot loader in hardware, and the OEM firmware. The fundamentals of the two-stage process are the same.
The first stage boot loader verifies a signature on the second stage boot
loader, and the second stage loader verifies the OEM firmware signature. This two-stage boot allows the
first boot loader to be extremely small, reducing cost and reducing the chances of building an unfixable
bug into hardware. Since the second stage is a software image, it can be larger and can implement more
features. For example, the second stage boot loaders can support two OEM firmware slots, one for the
current firmware, and one for an update image.


### Secure, per-device identity and TLS

All devices that connect with AWS IoT are uniquely identified by a TLS Client Certificate. The client certificate tells the
cloud which device it is talking to. Each device stores a unique TLS private key.
Using a feature of the TLS protocol called Mutual Authentication, the device uses its private key to prove
that it is the owner of its client certificate. (The authentication is mutual because TLS always verifies the
identity of the server with another certificate.) For this system to be secure, each device must have its
own unique certificate, and the private key must not leak outside the device. Each of the reference
boards provides a secure store that holds the private key and never allows it to be read, even by
software running on the same board! The FreeRTOS IoT integration software shows how to make TLS work
without direct access to the private key.


### Over the Air (OTA) updates

Secure boot and secure networking help build in strong security from the start. OTA helps IoT devices to stay
more secure. Security researchers discover and publish new security vulnerabilities all the time. Most IoT
devices will be exposed to multiple vulnerabilities during their lifetime. When a new vulnerability is
discovered, an OTA update can fix the issue.

The demo applications use the [AWS IoT OTA library](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates) to receive updates from
the [AWS IoT OTA service for FreeRTOS](https://docs.aws.amazon.com/freertos/latest/userguide/freertos-ota-dev.html).
The OTA client software runs in a background task, waiting for update messages from the
cloud. When an update notification arrives, the OTA client downloads the new image from the cloud,
and validates the code-signing signature on the image. If the signature is valid, the new firmware image
is marked as the active image, and the board is rebooted.


## Conclusion

Secure boot, secure networking, and over the air updates built on top of a hardware root of trust are the
security best practices that keep IoT devices safe. Check out these FreeRTOS IoT integration pages to see
how each board implements the hardware root of trust-- follow the links to the software repositories,
and find the Getting Started Guides that show how to get them up and running.

* [NXP i.MX RT1060 Arm Cortex-M7 MCU with EdgeLock SE050 Secure Element](04-NXP-iMX-RT1060)
* [STMicroelectronics STM32U5 Arm Cortex-M33 MCU with TrustZone and TF-M](05-STMicroelectronics-STM32U5)
* [ARM Corstone 3xxx](03-ARM-corstone3xx)
* [Espressif ESP32-C3 RISC-V MCU with Digital Signature Peripheral (DSP)](02-Espressif-ESP32c3)
* [STM32 with an AWS IoT Expresslink module](06-STM32-Expresslink)
