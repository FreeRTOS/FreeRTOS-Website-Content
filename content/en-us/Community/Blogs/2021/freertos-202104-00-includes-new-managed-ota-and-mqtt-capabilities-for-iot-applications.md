---
title: FreeRTOS 202104.00 includes new managed OTA and MQTT capabilities for IoT applications
created: 2021-04-29
feature: blog
categories:
  - Long term support
authors:
  - stanmoy
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---


by [Tanmoy Sen](../author/stanmoy) on 29 Apr 2021

FreeRTOS version 202104.00 includes managed [AWS IoT Over-the-Air](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates) update (OTA)
and [coreMQTT Agent](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/01-coreMQTT-agent) libraries, and
the [AWS IoT Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) custom metrics feature. Developers can
use these libraries to remotely update IoT device firmware, manage IoT device fleets, and monitor IoT
device fleet metrics.

These libraries have been optimized for modularity and memory usage for constrained microcontrollers,
and have undergone code quality checks such
as [MISRA-C compliance](https://www.misra.org.uk/), [Coverity static analysis](https://scan.coverity.com/),
and memory safety validation with the C Bounded Model
Checker ([CBMC](/Community/Blogs/2020/ensuring-the-memory-safety-of-freertos-part-1)) automated
reasoning tool.

The [OTA library](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates) makes it easier to download and cryptographically verify firmware
updates. You can use the OTA library with your
preferred [MQTT library](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT), [HTTP library](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/01-coreHTTP), and underlying operating
system (e.g. FreeRTOS, Linux). The [coreMQTT Agent](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/01-coreMQTT-agent) library manages MQTT connections
by serializing access to the [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) library and reducing implementation overhead.
For example, the MQTT agent removes the need for the application to periodically
call [MQTT\_ProcessLoop()](https://freertos.github.io/coreMQTT/main/mqtt_processloop_function.html).
This not only simplifies application design, it allows tasks (threads) in your multi-threaded applications
to safely and efficiently share the same MQTT connection. See
the [coreMQTT-Agent demo](https://github.com/FreeRTOS/coreMQTT-Agent-Demos) for an example that
uses [OTA](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates), [Device Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow),
and [Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) in multiple threads but sharing the same MQTT
connection. The [Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) library enables you to send device
metrics to the AWS IoT Device Defender service. This library also supports custom metrics, a feature
that helps you monitor operational health metrics that are unique to your fleet or use case. For example,
you can define a new metric to monitor the memory usage or CPU load on your devices.

You can find more information on FreeRTOS libraries on the [Libraries page](/Documentation/03-Libraries/01-Library-overview/Library-categories)
and get started by downloading the FreeRTOS source code from
the [Downloads page](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) or [GitHub](https://github.com/FreeRTOS/FreeRTOS).


## About the author

![](https://secure.gravatar.com/avatar/4b004f93afe063d6b8444f0fafc89d00?s=200&d=mm&r=g)
Tanmoy Sen is a Senior Product Manager at Amazon Web Services where he focuses on helping customers and
embedded developers connect microcontroller-based devices to the cloud.
[View articles by this author](../author/stanmoy)

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the
globe. [View Forums](https://forums.freertos.org/)
