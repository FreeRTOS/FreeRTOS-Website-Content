---
title: FreeRTOS AWS reference integrations now include FreeRTOS 202012.01 LTS libraries
created: 2021-07-14
feature: blog
categories:
  - Long term support
authors: 
  - stanmoy
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Tanmoy Sen](../author/stanmoy) on 14 Jul 2021

FreeRTOS AWS reference integrations are pre-integrated FreeRTOS projects ported to microcontroller-based 
evaluation boards that demonstrate end-to-end connectivity to AWS IoT Core. This helps developers save 
months of development effort and accelerate time to market. FreeRTOS AWS reference integrations now 
include the new managed [AWS IoT Over-the-Air](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates) (OTA) update 
library, [AWS IoT Jobs](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/01-AWS-IoT-jobs) library, 
the [AWS IoT Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) custom metrics feature from the FreeRTOS 
202012.01 LTS release, and the [coreMQTT Agent](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/01-coreMQTT-agent) library from 
the [FreeRTOS 202104.00](https://github.com/FreeRTOS/FreeRTOS/releases/tag/202104.00) release.

Developers can use the reference integrations to get started on a wide variety of evaluation boards 
and use the integrated libraries to remotely update IoT device firmware, manage IoT device fleets, monitor 
IoT device fleet metrics, and to simplify the management of MQTT connections in multi-threaded applications. 
See more details on the functionality of these libraries in the FreeRTOS 202012.01 LTS 
announcement [blog](/Community/Blogs/2021/freertos-long-term-support-now-includes-aws-iot-over-the-air-update-aws-iot-device-defender-and-aws-iot-jobs-libraries) 
and the FreeRTOS 202104.00 release [blog](/Community/Blogs/2021/freertos-202104-00-includes-new-managed-ota-and-mqtt-capabilities-for-iot-applications).

You can find a list of evaluation boards that use the LTS libraries on AWS reference 
integrations [page](/Documentation/03-Libraries/04-AWS-libraries/09-AWS-reference-integrations) (marked “LTS”) and get started by downloading 
202107.00 FreeRTOS AWS reference integrations source code from [GitHub](https://github.com/aws/amazon-freertos) 
or the [FreeRTOS console](https://console.aws.amazon.com/freertos).


## About the author
 
![](https://secure.gravatar.com/avatar/4b004f93afe063d6b8444f0fafc89d00?s=200&d=mm&r=g)   
Tanmoy Sen is a Senior Product Manager at Amazon Web Services where he focuses on helping customers and 
embedded developers connect microcontroller-based devices to the cloud.   
[View articles by this author](../author/stanmoy) 

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
