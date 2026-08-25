---
title: Secure OTA Updates for Cortex-M Devices with FreeRTOS
created: 2021-07-14
feature: blog
categories:
  - Long term support
authors:
  - arm-author
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Shebu Varghese Kuriakose](../author/arm-author) on 14 Jul 2021

IoT devices are getting rapid adoption in every market segment and becoming a major target for cyberattacks.
A significant proportion of attacks on IoT devices happens due to a lack of software updates once commissioned
in the field or updates done insecurely. Cyber attackers often target vulnerabilities in outdated software
components to take control of the device. Software updates are the means of responding to ongoing threats
by deploying timely fixes for newly discovered vulnerabilities.

Updating software manually is often not scalable for IoT devices in a fleet as they may require frequent
updates and users lack easy physical access to devices. Over-the-Air (OTA) updates are commonly used to
update IoT devices. OTA updates are done remotely by deploying updates wirelessly using cellular or internet
connections. This avoids the need for physical access to the devices and updates to millions of devices
in a fleet can be managed at scale centrally.

One of the major barriers for IoT devices to support secure OTA updates is the complexity of integrating
the OTA applications in the IoT ecosystem. This is due to the huge spectrum of hardware platforms with
different storage, update, and image authentication mechanisms. PSA Certified framework aims to make
security more accessible and easier for IoT developers. PSA Certified defines 10 security goals with
Secure update being one of them. PSA Firmware Update Specification that is part of PSA Certified
framework helps achieve this goal.

This blog discusses how FreeRTOS devices can seamlessly enable Secure OTA updates on Cortex-M devices
utilizing the PSA Firmware Update Specification. This blog introduces the PSA Firmware Update Specification
followed by how the reference implementation, Trusted Firmware-M, integrates with the existing FreeRTOS
OTA Agent on Cortex-M devices to perform secure OTA updates. An example implementation has been done
on an Arm v8-M reference platform, MuscaB1e.


## PSA Firmware Update – Standard Interface for Updates

The PSA Firmware Update [specification](https://developer.arm.com/documentation/ihi0093/0000) defines
a standard set of firmware update interfaces that can be used by update applications and cloud connector
clients. The interfaces provide enough flexibility for an efficient implementation on hugely varied IoT
SoC architectures and different trust models. The interfaces are also independent of the protocol used
to communicate with the device and the medium through which updates are delivered to the device.

Below are the set of interfaces defined.

| PSA FWU API | What Does it Do |
| --- | --- |
| psa\_fwu\_query () | Query image information such as state of installed, rejected and candidate images |
| psa\_fwu\_write () | Write candidate image to its staging area |
| psa\_fwu\_install () | Starts installation of an image |
| psa\_fwu\_request\_reboot () | Trigger platform reboot to apply authenticated new image |
| psa\_fwu\_request\_rollback () | Rollback recently applied updates |
| psa\_fwu\_accept () | Indicate whether recently applied updates are working correctly. |

The update applications can invoke these interfaces to query the state of the current image, store, verify
and finally install new images.

Trusted Firmware-M (TF-M), the PSA certified reference implementation for Cortex-M devices, implements
these interfaces. This allows update applications to make use of these interfaces on TF-M enabled
Cortex-M devices.


## Trusted Firmware-M and Secure Boot

Trusted Firmware-M (TF-M) implements a Secure Processing Environment (SPE) for processors based on the
Armv8-M architecture (e.g., Cortex-M55, Cortex-M33 and Cortex-M23 processors) and dual-core Cortex-M
devices. Enabling faster development of [PSA Certified](http://psacertified.org/) devices, TF-M offers
a reference implementation in line with PSA Certified guidelines. It is enabled on several
Cortex-M [platforms](https://tf-m-user-guide.trustedfirmware.org/platform/index.html)
such as NXP LPC55S69, ST STM32L5, Infineon PSoC64, Nordic nrf5340, nrf9160 and Nuvoton M2351, M2354.
FreeRTOS integration with TF-M run-time services to make Cortex-M devices secure as
described [here](https://freertos.org/2020/07/security-for-arm-cortex-m-devices-with-freertos.html).
FreeRTOS has achieved PSA Certified Level 1. This assures fundamental security principles have been
built into system software which can be leveraged by OEM application developers.

![](/media/2021/trusted-firmware-m-300x110.png)
*Figure 1: Diagram showing Trusted Firmware-M in Secure Processing Environment within a Cortex-M device.
PSA Functional APIs can be availed by Non-secure Processing Environment (RTOS and Applications)*

An important capability provided by TF-M is secure boot. Secure boot ensures that only authorized software
is running on the device. This is critical as devices are connected and software can be updated once
deployed in the field. The open source community project [MCUboot](https://github.com/mcu-tools/mcuboot)
is used as the secure bootloader of TF-M. The bootloader authenticates run-time images by hash and digital
signatures using an image key in the MCUboot image or provisioned in the SoC.

In addition to PSA Crypto, Storage and Attestation secure runtime services, TF-M has implemented PSA
Firmware Update (PSA FWU) interfaces in the Secure Processing Environment as a Secure service (Figure 1).
These interfaces are exposed to the Non-Secure Processing Environment (NSPE) allowing update applications
to make use of the interfaces. The PSA FWU service, in turn, relies on TF-M secure boot (MCUboot) to
authenticate new images and, once successfully authenticated, to deploy them as an active image.

Building on the FreeRTOS and TF-M integration
done [previously](/Community/Blogs/2020/security-for-arm-cortex-m-devices-with-freertos), the PSA FWU
Secure Service has been integrated with FreeRTOS as described in the following section.


## TF-M Integration with FreeRTOS OTA

FreeRTOS provides an [OTA Agent library](https://docs.aws.amazon.com/freertos/latest/userguide/ota-agent-library.html)
for FreeRTOS devices to receive and deploy firmware updates from AWS IoT. This makes it possible for IoT
devices running FreeRTOS to apply OTA /updates. The library also defines a set OTA Platform Abstraction
Layer (PAL) APIs for vendors integrating the library to implement. Every Cortex-M silicon platform need
to provide an implementation of the OTA PAL APIs to enable the OTA Agent on the platform.

An implementation of the OTA PAL APIs that uses TF-M for secure firmware updates on Cortex-M devices is
available. The API implementation uses PSA Functional APIs including the PSA FWU APIs discussed above and
PSA cryptographic APIs.

The table below shows the [PSA Functional APIs](https://www.psacertified.org/getting-certified/functional-api-certification/)
used in OTA PAL APIs.

| OTA PAL API | PSA Functional API  |
| --- | --- |
| prvPAL\_Abort | psa\_fwu\_abort<br/>  |
| prvPAL\_CreateFileForRx | None |
| prvPAL\_CloseFile | psa\_fwu\_query  psa\_asymmetric\_verify |
| prvPAL\_WriteBlock | psa\_fwu\_write |
| prvPAL\_ActivateNewImage | psa\_fwu\_install  psa\_fwu\_request\_reboot |
| prvPAL\_ResetDevice | psa\_fwu\_request\_reboot |
| prvPAL\_SetPlatformImageState | psa\_fwu\_accept |

The OTA PAL API implementation above that makes use of the PSA Functional APIs can be used as a generic
implementation on all TF-M enabled Cortex-M platforms. This avoids the need for every Cortex-M platform
to invest in developing and maintaining an implementation of the OTA PAL APIs. The secure processing
environment, including secure boot provided by TF-M, ensures the OTA updates are done securely on the
platform.

An example implementation of the OTA agent with TF-M OTA PAL has been built on the Arm Musca-B1e platform.
The TF-M OTA PAL uses TF-M's Firmware Update service via the PSA Functional APIs. The implementation can
connect to AWS IoT, receive a new firmware image, authenticate, and deploy the image. Figure 2 below shows
the implementation. Find more about TF-M OTA PAL and implementation with FreeRTOS in the ota\_pal\_psa
GitHub folder [here](https://github.com/Linaro/freertos-ota-pal-psa/tree/0b6db7d7cc0260fbb1e54a26ad6ff25cdcde3697).

![](/media/2021/enabling-secure-ota-300x155.png)
*Figure 2: Diagram showing OTA Agent, OTA PAL Implementation and TF-M Integration enabling Secure OTA Updates from AWS IoT Service*


## Streamlining OTA updates on Cortex-M with TF-M and FreeRTOS

OTA is an essential building block to keep IoT devices secure once
deployed. [NIST 8259A](https://www.nist.gov/news-events/news/2020/06/security-iot-device-manufacturers-nist-publishes-nistirs-8259-and-8259a)
and [EN 303 645](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/02.01.01_60/en_303645v020101p.pdf)
outline cybersecurity best practices and a common baseline to raise the security bar on IoT devices. Like
PSA Certified, these guidelines require devices to support the mechanism for software and firmware updates.
IoT device manufacturers have found it challenging to enable OTA at scale due to the variations and complexities
in the underlying hardware platform. Adopting the TF-M OTA PAL and TF-M abstracts away these complexities
allowing FreeRTOS Cortex-M devices to be seamlessly and securely updated during their lifetime, leveraging
the security in the silicon and system software. Visit the FreeRTOS Reference Integrations
on [Github](https://github.com/aws/amazon-freertos/tree/main/libraries/abstractions/)
and [Trusted Firmware](https://www.trustedfirmware.org/projects/tf-m/) to learn more about the TF-M
OTA PAL and TF-M implementation.


## About the author

![](https://secure.gravatar.com/avatar/db732371ff8ea1e00013619782acc940?s=200&d=mm&r=g)
Shebu Varghese Kuriakose is Director, Software Technology Management with Arm’s Open Source Software Group
and Chairman of the Trusted Firmware Project Board. Shebu drives the Trusted Firmware-M development roadmap
and collaboration with Silicon vendors, RTOS and Tools ecosystem.
[View articles by this author](../author/arm-author)

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the
globe. [View Forums](https://forums.freertos.org/)
