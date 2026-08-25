---
title: What's New in November 2021 FreeRTOS Releases
created: 2021-11-12
feature: blog
categories:
  - Long term support
authors: 
  - stanmoy
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Tanmoy Sen](../author/stanmoy) on 12 Nov 2021

We're excited to share these latest updates: 

* The FreeRTOS download now contains an example of code that demonstrates a method of minimizing the 
  time that an application spends in privileged mode in FreeRTOS ports on microcontrollers (MCUs) with 
  Memory Protection Unit (MPU) support. These  [FreeRTOS ports with MPU support](/Security/04-FreeRTOS-MPU-memory-protection-unit) 
  enable MCU applications to be more robust and secure by running application tasks in unprivileged mode, 
  where they have access only to their own stacks and pre-configured memory regions. The only application 
  code sections that run in privileged mode on these MPU enabled MCUs are Interrupt Service Routines (ISRs). 
  The example code demonstrates an approach to keeping ISRs short and deferring most of the application 
  work to unprivileged FreeRTOS tasks. This helps improve the security of the application by minimizing 
  the time it spends in privileged mode. To learn more and get started, visit 
  the [demo page](/safe-interrupt-demo-nxp-lpcxpresso55s69) and download the example code from 
  the [Downloads page](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) or [GitHub](https://github.com/FreeRTOS/FreeRTOS).
 
* Last year we [introduced](/Community/Blogs/2020/introducing-the-freertos-cellular-library) a preview 
  of a new FreeRTOS library designed to simplify the development of IoT applications that connect to 
  the cloud using [cellular LTE-M technology](https://en.wikipedia.org/wiki/LTE-M). We're excited to 
  announce that the FreeRTOS cellular LTE-M interface library is now part of the main FreeRTOS download. 
  With this launch, developers will find it easier to build IoT devices that use the cellular LTE-M protocol 
  to connect to cloud services. To learn more about the FreeRTOS cellular interface library, visit 
  the [libraries page](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/01-Cellular-interface), and download 
  the [FreeRTOS cellular interface library](https://github.com/FreeRTOS/FreeRTOS-Cellular-Interface) 
  and [demos.](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator) 
  The main FreeRTOS download includes AWS IoT reference integrations with cellular modules from vendors 
  such as Sierra Wireless, u-blox, and Quectel.

We're looking forward to your feedback. Reach out to us on the [FreeRTOS forums](https://forums.freertos.org/) 
if you have comments or requests! 


## About the author

![](https://secure.gravatar.com/avatar/4b004f93afe063d6b8444f0fafc89d00?s=200&d=mm&r=g)   
Tanmoy Sen is a Senior Product Manager at Amazon Web Services where he focuses on helping customers 
and embedded developers connect microcontroller-based devices to the cloud.   
[View articles by this author](../author/stanmoy) 

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
