---
title: FreeRTOS LTS libraries are now included in our partner toolchains
created: 2021-10-19
feature: blog
categories:
  - Long term support
authors: 
  - stanmoy
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Tanmoy Sen](../author/stanmoy) on 19 Oct 2021

In December 2020 we introduced the first FreeRTOS Long Term Support (LTS) version. With the LTS version, 
developers can rely on a FreeRTOS version that provides feature stability, and security patches and 
critical bug fixes for two years from the release date. Response from our partners was strong, and they 
are integrating the LTS version into their toolchains. In keeping with our philosophy of enabling users 
to consume our software in the environment of their choice, these integrations will allow developers 
building IoT applications to access all FreeRTOS libraries needed for IoT and AWS connectivity from a 
single location and in an environment they are familiar with - a vendor's Integrated Development Environment (IDE) 
or Software Development Kits (SDKs). We're happy to announce that the following partners have completed 
and validated the integration of the LTS version into their toolchains:


**Arm**:

Some developers use IDEs with plugins that allow drivers, board support packages (BSPs), and other libraries to 
be easily included and maintained. These plugins provide this functionality via the Common Microcontroller 
Software Interface Standard (CMSIS)-Pack format. Based on the Arm Cortex 
processors, [CMSIS-Pack](https://developer.arm.com/tools-and-software/embedded/cmsis/cmsis-packs) defines 
a standardized way to deliver software components, device parameters, board support information, and 
code. The FreeRTOS kernel was already available as a CMSIS-Pack; we now provide other FreeRTOS LTS libraries 
in the CMSIS Pack format to make them easily accessible to developers in their chosen workflow. These 
CMSIS-Packs have also been integrated with the recently-introduced [Keil Studio Cloud](https://www.keil.arm.com/), 
which is a browser-based IDE for IoT, ML and embedded development. If you want more details and a hands-on 
experience of using FreeRTOS libraries via Keil Studio Cloud, you will find 
this [workshop](https://devsummit.arm.com/en/sessions/73) and [session](https://devsummit.arm.com/en/sessions/145) 
at [Arm DevSummit](https://devsummit.arm.com/en) interesting.


**Espressif**:

Espressif launched support for the FreeRTOS LTS libraries from their SDK (beta) for Espressif 
boards: [ESP-AWS-IoT](https://github.com/espressif/esp-aws-iot/tree/release/beta). To simplify the use 
of the LTS libraries for AWS IoT connectivity, Espressif created several examples, including OTA over 
MQTT, Device Shadow, and coreMQTT with TLS Mutual Authentication. Refer 
to [The ESP Journal blog](https://blog.espressif.com/support-for-lts-release-of-aws-iot-device-sdk-for-embedded-c-on-esp32-8eeeea28b79b) 
for more details. 


**Infineon**:

Infineon has integrated the FreeRTOS LTS libraries with AnyCloud, Infineon's cloud connectivity solution 
to help developers rapidly build applications using connectivity devices with the PSoC 6 MCU. Offered 
from within [ModusToolbox](https://www.cypress.com/products/modustoolbox), AnyCloud provides core functionality 
including connectivity, security, firmware upgrade support, and application layer protocols like MQTT. 
More information on AnyCloud and support for libraries from FreeRTOS LTS can be found 
at [ModusToolBoxAnyCloudSDK](https://community.cypress.com/gfawx74859/attachments/gfawx74859/ModusToolboxAnyCloudSDK/46/2/AnyCloud_1.3_User_Guide_0C.pdf).


**NXP**:

NXP's MCUXpresso software and tools offer comprehensive development solutions designed to optimize, ease 
and help accelerate embedded system development of applications based on general purpose, crossover and 
Bluetooth™-enabled MCUs from NXP. MCUXpresso software and tools bring together the best of NXP's software 
enablement. The MCUXpresso software development kit (SDK) can be 
found [on NXP’s website](https://www.nxp.com/design/software/development-software/mcuxpresso-software-and-tools-/mcuxpresso-software-development-kit-sdk:MCUXpresso-SDK), 
which also has [self-paced training](https://www.nxp.com/pages/part-i-an-introduction-to-aws-iot-and-freertos-the-concepts-and-benefits-of-using-it-together-with-lpc-mcus:TIP-AMAZON-AND-LPC-PART-I) 
on getting connected to AWS IoT.


**Realtek**:

Realtek has integrated the FreeRTOS LTS libraries in their [AmebaPro SDK](https://github.com/ambiot/ambpro1_sdk). 
This SDK contains examples that demonstrate the use of FreeRTOS LTS libraries for AWS IoT connectivity 
and [Amazon Kinesis Video Streams](https://aws.amazon.com/kinesis/video-streams) on the AmebaPro board. Refer 
to the [Getting Started Guide](https://github.com/ambiot/ambpro1_sdk/blob/main/doc/AmebaPro_Amazon_FreeRTOS-LTS_Getting_Started_Guide_v1.2_r.pdf) 
to get started.


**Renesas**:

Renesas provides support for FreeRTOS LTS libraries via the Renesas Flexible Software Package (FSP), 
which includes software for embedded system designs that use the Renesas RA family of microcontrollers. 
Visit the Renesas Flexible Software Package [homepage](https://www.renesas.com/us/en/software-tool/flexible-software-package-fsp) 
for the latest [FSP release](https://info.renesas.com/en-fsp-download), [GitHub repository](https://github.com/renesas/fsp/releases), 
and [documentation](https://www.renesas.com/us/en/software-tool/flexible-software-package-fsp#document).

Our other partners are actively working on their integration efforts, and we expect to be able to share 
their results soon. We are eager to see how the FreeRTOS LTS release improves development and maintenance 
of the next generation of embedded applications. We look forward to your feedback. Reach out to us on 
the [FreeRTOS forums](https://forums.freertos.org/) if you have comments or requests! 


## About the author

![](https://secure.gravatar.com/avatar/4b004f93afe063d6b8444f0fafc89d00?s=200&d=mm&r=g)   
Tanmoy Sen is a Senior Product Manager at Amazon Web Services where he focuses on helping customers and 
embedded developers connect microcontroller-based devices to the cloud.   
[View articles by this author](../author/stanmoy) 

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
