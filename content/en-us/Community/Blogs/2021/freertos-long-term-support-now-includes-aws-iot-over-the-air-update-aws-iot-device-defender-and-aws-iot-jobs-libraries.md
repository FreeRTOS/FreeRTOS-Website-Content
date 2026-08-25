---
title: FreeRTOS Long Term Support now includes AWS IoT over-the-air update, AWS IoT Device Defender, and AWS IoT Jobs libraries
created: 2021-03-01
feature: blog
categories:
  - Long term support
authors: 
  - stanmoy
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Tanmoy Sen](../author/stanmoy) on 01 Mar 2021

FreeRTOS Long Term Support (LTS) release 202012.01 now includes 
the [over-the-air update (OTA)](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates), [AWS IoT Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender), 
and [AWS IoT Jobs](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/01-AWS-IoT-jobs) libraries in the first LTS release (FreeRTOS 202012.00 LTS). 
With this release, developers can use the FreeRTOS LTS libraries to update firmware, manage device fleets, 
and monitor fleet metrics for their microcontroller-based IoT devices. In addition, developers can rely 
on a FreeRTOS version that provides feature stability, and security patches and critical bug fixes for 
two years.

The [OTA library](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates) makes it easier to download and perform cryptographic verification 
of firmware updates. You can use the OTA library with your preferred MQTT library, HTTP library, and 
underlying operating system (e.g. FreeRTOS, Linux). The [Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) 
library enables customers to send device metrics to the AWS IoT Device Defender service. This library 
also supports custom metrics, a feature that helps you monitor operational health metrics that are unique 
to your fleet or use case. For example, you can define a new metric to monitor the memory usage or CPU 
usage on your devices. The [Jobs library](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/01-AWS-IoT-jobs) helps you notify connected IoT devices 
of a [pending Job](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/02-Jobs-terminology). Jobs can be used to manage fleets of devices, update 
firmware and security certificates, or perform administrative tasks such as restarting devices and performing 
diagnostic

Updating firmware remotely over-the-air and monitoring device metrics are critical to improving and 
maintaining security of IoT devices over their lifecycle. Given the importance of these functionalities 
for customers building IoT devices using FreeRTOS LTS libraries, we have included the OTA, Device Defender 
and Jobs libraries in the LTS release – [FreeRTOS 202012.01 LTS](https://github.com/FreeRTOS/FreeRTOS-LTS). 
These libraries are additive – there are no changes, fixes, or features added to pre-existing FreeRTOS 
LTS libraries. In addition, to give developers at least two years of maintenance on all LTS libraries, 
we have extended support for FreeRTOS 202012.01 LTS to March 31, 2023.

Like the rest of the FreeRTOS LTS libraries, the OTA, Device Defender and Jobs libraries have been refactored 
to improve design flexibility, security, and code quality. First, each LTS library comes in its own GitHub 
repository, which makes it easier for developers to integrate and update libraries in their FreeRTOS projects. 
Second, the Device Defender and Jobs libraries have been validated for memory safety with the C Bounded 
Model Checker ([CBMC](/Community/Blogs/2020/ensuring-the-memory-safety-of-freertos-part-1)) automated 
reasoning tool to mitigate code security issues such as buffer overflow. Lastly, all LTS libraries have 
undergone code quality checks including [MISRA-C](https://www.misra.org.uk/)  compliance 
and [Coverity](https://scan.coverity.com/) static analysis to enhance code safety, portability, and reliability 
in embedded systems (see [LTS Code Quality Checklist](/Community/Blogs/2021/freertos-aws-reference-integrations-now-include-freertos-202012-01-lts-libraries#checklist)).

You can find more information on the FreeRTOS LTS libraries on [FreeRTOS.org](/Community/Blogs/2021/freertos-aws-reference-integrations-now-include-freertos-202012-01-lts-libraries) and 
get started by downloading the FreeRTOS 202012.01 LTS source code from the [Downloads page](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) 
or [GitHub](https://github.com/FreeRTOS/FreeRTOS-LTS).


## About the author

![](https://secure.gravatar.com/avatar/4b004f93afe063d6b8444f0fafc89d00?s=200&d=mm&r=g)   
Tanmoy Sen is a Senior Product Manager at Amazon Web Services where he focuses on helping customers and 
embedded developers connect microcontroller-based devices to the cloud.   
[View articles by this author](../author/stanmoy) 

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
