---
title: Previewing the new Arm Corstone FreeRTOS Featured Reference Integration
date: 1 Aug 2023
feature: blog
authors:
  - sam-tayloramazon-com
---
Most people know Arm for our hardware designs and our Cortex CPUs, but our ongoing commitment to the software ecosystem
 that enables this hardware is just as critical. It's really important to us that developers can easily take advantage of
 the latest features of our CPUs, ML accelerators and other system IP. Because FreeRTOS powers more and more Embedded and
 IoT devices, it’s a crucial piece of software for us and the whole Arm ecosystem. In this post I'd like to tell you a
 little about the ways we're working closely with the FreeRTOS team to make sure Arm hardware is fully supported with
 FreeRTOS and how developers can make a fast start with the latest Cortex-M CPUs.


Recently we've been working on a
 [FreeRTOS Featured Reference Integration](/Documentation/03-Libraries/08-Featured-integrations/01-Featured-integrations)
 (FRI) for our [Arm Corstone-300 and Corstone-310 platforms](/Documentation/03-Libraries/08-Featured-integrations/03-ARM-corstone3xx).
 This reference integration demonstrates how cloud connected applications can be updated securely
 by integrating the modular FreeRTOS kernel and libraries and utilizing hardware enforced security
 based on Arm TrustZone (Armv8-M). Today we're pleased to announce that the first preview software
 for Corstone-300 is available in FreeRTOS GitHub for anyone to try out:
 [https://github.com/FreeRTOS/iot-reference-arm-corstone3xx](https://github.com/FreeRTOS/iot-reference-arm-corstone3xx).


Over the next couple of months we'll be adding to this project to make it into a complete,
 portable and secure example of running FreeRTOS and the
 [AWS IoT Device SDK for Embedded C](https://docs.aws.amazon.com/iot/latest/developerguide/iot-sdks.html#iot-device-sdks) on Arm Cortex-M
 microcontrollers.


What is Arm Corstone? What is Arm Virtual Hardware?
---------------------------------------------------


For those of you not familiar with Corstone-300 and Corstone-310, I should probably take a
 moment to explain what they are. Arm develops a lot of different IP for microcontrollers:
 from our Cortex-M processor cores and our Ethos-U Machine Learning accelerators, through
 system IP, software and tools. Our Corstone platforms bring all these pieces together into
 configurable subsystems which SoC designers can use as a starting point for their designs.


Because Cortex-M55 and -M85 devices are still pretty new in the market, we also make our
 Corstone platforms available as
 [Arm Virtual Hardware](https://www.arm.com/products/development-tools/simulation/virtual-hardware) and as
 [Fixed Virtual Platforms](https://developer.arm.com/downloads/-/arm-ecosystem-fvps) (FVPs).
 These provide a model of the hardware which allows software to be tested ahead of
 available silicon. Virtual platforms are increasingly popular as an easy way for developers to
 try out all the latest cores and architectural features from Arm, for free, and without having
 to wait for hardware to become available.


Our two most recent Corstones are:


* [Corstone-300](https://developer.arm.com/Processors/Corstone-300): Featuring the Cortex-M55 with
 [TrustZone-M](https://www.arm.com/technologies/trustzone-for-cortex-m) and
 [Helium
 vector extensions](https://www.arm.com/technologies/helium), along with an optional Ethos-U55 ML accelerator.
* [Corstone-310](https://developer.arm.com/Processors/Corstone-310): Featuring the high performance Cortex-M85 with TrustZone-M and
 Helium vector extensions, along with an integrated Ethos-U55 ML accelerator.


[![Example integration of the Corstone-310 SSE-310 subsystem](/media/2023/example-integration-corstone3xx.png)](/media/2023/example-integration-corstone3xx.png)


Example integration of the Corstone-310 SSE-310 subsystem. Click to enlarge.

So, when thinking about building a FreeRTOS FRI, it made sense to start with our two latest
Corstone platforms.


Elements of the Arm Corstone FRI
--------------------------------


We've tried to keep the following in mind when building our FRI:


* Keep things as simple and as familiar as possible, and follow the approach used in
 other FreeRTOS FRIs.
* Include the essential software to access all the capabilities of the Corstone-300 and -310.
* Make it easy to build, modify and port to other Arm-based hardware.
* Show how the capabilities of the AWS IoT Device SDK for Embedded C can be backed
 up with secure services running in TrustZone for Cortex-M.


Portability is key for us, because we'd like developers and partners to be able to use this on
 other platforms. For that reason we started with a simple BSP based on
 [CMSIS](https://www.arm.com/technologies/cmsis)
 drivers. CMSIS is a generic standard for low-level microcontroller software which is supported by
 many different silicon vendors. It also includes optimised libraries for things like signal
 processing ([CMSIS-DSP](https://arm-software.github.io/CMSIS_5/DSP/html/index.html)) and machine learning
 ([CMSIS-NN](https://arm-software.github.io/CMSIS_5/NN/html/index.html)) which you can add to your application if appropriate.


In the future we'd like to include some other optional CMSIS portability APIs, like the
 generic IoT Socket interface, to make it easy for developers who are already using CMSIS in
 an existing product. It also gives Arm's silicon partners an excellent example of how to
 support FreeRTOS, and so accelerate their time to market.


Making it Secure & Updateable
-----------------------------


These days everyone knows how important it is to secure your IoT device. We also know
 that security isn't something you do just at development time; a device will only stay secure
 if you can update its firmware in the field. That's why it's been a major focus for Arm over
 the past couple of years. We've already shared some of our earlier work on this blog, and I
 was really interested to see developments by other industry players in the past few months.


Many of you know that Arm's IoT security efforts are standardised using
 [PSA Certified](https://www.psacertified.org/).
 As well as providing a standard for a hardware root of trust in IoT devices, PSA Certified also
 includes APIs for [Crypto](https://arm-software.github.io/psa-api/crypto/),
 [Secure Storage](https://arm-software.github.io/psa-api/storage/),
 [Attestation](https://arm-software.github.io/psa-api/attestation/) and, most recently,
 [Firmware
 Update](https://arm-software.github.io/psa-api/fwu/). The Arm Corstone FRI includes TrustedFirmware-M with Mbed TLS and MCUboot to
 provide a full set of security software meeting all the PSA Certified security requirements.


Now our ultimate goal is to ensure that TLS connections and firmware updates are able to
 use the security services provided by TF-M and backed by hardware isolation in TrustZone-M.
 We do that through two important integration points:


1. **PKCS11 support** - We have a simple wrapper which implements PCKS11 support on
 top of Mbed TLS and the PSA Crypto API. This allows the
 [PKCS#11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/02-PKCS11-functions) APIs to perform TLS
 client authentication and import TLS client certificate and private key into the device using
 underlying PSA Secure Storage and PSA Crypto support from TF-M.
2. **AWS OTA PAL support** – We've also integrated a shim which maps the AWS OTA PAL
 to the PSA Firmware Update API implemented by TF-M. This allows Corstone-300 to
 receive new images from AWS IoT Core and authenticate using TF-M before deploying
 the image as the active image. The secure (TF-M) and the non-secure (FreeRTOS
 kernel and the application) images can be updated separately. Every time the device
 boots, MCUBoot (bootloader) verifies that the image signature is valid before
 booting the image. Since the secure (TF-M) and the non-secure (FreeRTOS kernel
 and the application) images are signed separately, MCUBoot verifies that both image
 signatures are valid before booting. If either of the verification fails, then MCUBoot
 stops the booting process.


Both those shims previously existed in separate repos, but we've included them directly in
 the Corstone FRI. You can read more about the security features of our FRI on the project
 Landing page.


Stay tuned – Plenty more to come
--------------------------------


As I mentioned already, the code we've published today is just the first preview of the Arm
 Corstone FRI. In the coming months we have a long list of things we want to add. For
 example, this first preview uses the virtual socket interface built into our FVP for basic
 connectivity, but in the future we want to have full support for FreeRTOS TCP/IP as well as
 lwIP. We also plan to add in support for HTTP,
 [AWS IoT Device Shadow](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html) and
 [AWS IoT Device Defender](https://docs.aws.amazon.com/iot/latest/developerguide/device-defender.html).
 After that there are a whole host of things we'd like to do, including enablement
 for Ethos-U and ML examples. Anyone interested in updating the ML assets on a device
 without doing a full firmware update? No promises, but that's the sort of thing we have in
 mind for the future.


As for today, we're just happy to be sharing this first preview. We'd love it if you try it out
 and please share your feedback on the
 [FreeRTOS forums](https://forums.freertos.org/),
 and your ideas for what you'd like to see us work on next.
