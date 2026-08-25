---
title: AWS IoT Device Defender Demo
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

**NOTE**: The AWS IoT Device Defender library is now available with preconfigured examples in the
main [FreeRTOS download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) and in the [FreeRTOS](https://github.com/FreeRTOS/FreeRTOS) repository
on GitHub.

## Introduction

The AWS IoT Device Defender Demo shows you how to interact with
the [AWS IoT Device Defender service](https://docs.aws.amazon.com/iot/latest/developerguide/device-defender.html)
through an MQTT connection, submit a device defender report
including [custom metrics](https://docs.aws.amazon.com/iot/latest/developerguide/dd-detect-custom-metrics.html),
and verify that the report was accepted. The AWS IoT Device Defender Demo project uses
the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW),
so it can be built and evaluated with
the [free Community version of Visual Studio](https://visualstudio.microsoft.com/vs/community/) on
Windows. No microcontroller hardware is required to run this demo. This demo establishes a mutually
authenticated secure connection to the AWS IoT MQTT broker using [TLS](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/03-TLS-terminology).


## Source Code Organization

The demo project is called `defender_demo.sln` and can be found in
the [Device\_Defender\_Demo](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/AWS/Device_Defender_Windows_Simulator/Device_Defender_Demo)
repository on GitHub in the following directory:

```c
FreeRTOS-Plus/Demo/AWS/Device_Defender_Windows_Simulator/Device_Defender_Demo
```


## Configure the Demo Project

The demo uses the [FreeRTOS-Plus-TCP TCP/IP stack](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP),
so follow the instructions provided for
the [TCP/IP starter project](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator) to:

1. [Install the pre-requisite components](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites)
   (such as WinPCap).

2. Optionally [set a static or dynamic IP address, gateway address and netmask](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic).

3. Optionally [set a MAC address](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr).

4. [Select an Ethernet network interface](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface)
   on your host machine.

The above settings should be changed in the
[`FreeRTOSConfig.h`](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/VisualStudio_StaticProjects/FreeRTOS-Kernel/FreeRTOSConfig.h)
file.


### Configure the AWS IoT MQTT Broker Connection

In this demo you use an MQTT connection to the AWS IoT MQTT broker. This connection is configured in the
same way as the [MQTT mutual authentication demo](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication).


## Build the Demo Project

The demo project uses
the [free community edition of Visual Studio](https://visualstudio.microsoft.com/vs/community/). To
build the demo:

1. Open the Visual Studio solution
   file `FreeRTOS-Plus/Demo/AWS/Device_Defender_Windows_Simulator/Device_Defender_Demo/defender_demo.sln`
   from within the Visual Studio IDE.

2. Select **build solution** from the IDE's **build** menu.


## Functionality

This demo shows you how to construct a device defender report and publish it from a device to the AWS
IoT Device Defender Service. The demo connects to the AWS IoT broker, collects networking
and [custom](https://docs.aws.amazon.com/iot/latest/developerguide/dd-detect-custom-metrics.html)
metrics from the device, constructs a JSON report using the collected metrics, and publishes the report.
The structure of the demo is shown in the following sections.

The source code for the `prvDefenderDemoTask()` function can be found in
the [DefenderDemoExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Defender_Windows_Simulator/Device_Defender_Demo/DemoTasks/DefenderDemoExample.c#L721-L966)
file on Github.

This screenshot shows the expected output when the demo executes correctly:

[![](/media/2020/Defender-Terminal-Output.png)](/media/2020/Defender-Terminal-Output.png)
*Click to enlarge*


### Subscribing to Defender Topics

The function `prvSubscribeToDefenderTopics()` subscribes to MQTT topics to receive a response when:

* A device defender report it has published is accepted.

  The macro `DEFENDER_API_JSON_ACCEPTED` is used to construct the topic string.

* A device defender report it has published is rejected.

  The macro `DEFENDER_API_JSON_REJECTED` is used to construct the topic string.


The source code for the `prvSubscribeToDefenderTopics()` function can be found in
the [DefenderDemoExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Defender_Windows_Simulator/Device_Defender_Demo/DemoTasks/DefenderDemoExample.c#L636-L668)
file on GitHub.


### Collecting Device Metrics

The function `prvCollectDeviceMetrics()` gathers networking metrics, using the functions defined
in `metrics_collector.h`, as well as custom metrics. The networking metrics collected are:

* the number of bytes and packets sent and received
* the open TCP ports
* the open UDP ports
* the established TCP connections

The custom metrics collected are:

* the stack high water mark (with type number)
* the device’s task ids (with type number list)

The source code for the `prvCollectDeviceMetrics()` function can be found in
the [DefenderDemoExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Defender_Windows_Simulator/Device_Defender_Demo/DemoTasks/DefenderDemoExample.c#L467-L601rel=)
file on GitHub.


### Generating the Device Defender Report

The function `prvGenerateDeviceMetricsReport()` generates a device defender report. It is defined in
`report_builder.h`. The function takes the networking metrics and a buffer as input, creates a JSON
document in the format expected by the AWS IoT Device Defender Service, and writes it to the specified
buffer.  The format of the JSON document that the AWS IoT Device Defender Service expects is
specified [here](https://docs.aws.amazon.com/iot-device-defender/latest/devguide/detect-device-side-metrics.html).

The source code for the `prvGenerateDeviceMetricsReport()` function can be found in
the [DefenderDemoExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Defender_Windows_Simulator/Device_Defender_Demo/DemoTasks/DefenderDemoExample.c#L604-L633)
file on GitHub.


### Publishing the Device Defender Report

The function `prvPublishDeviceMetricsReport()` publishes the device defender report on the
appropriate MQTT topic. The report is constructed, in JSON, using the macro `DEFENDER_API_JSON_PUBLISH`.

The source code for the `prvPublishDeviceMetricsReport()` function can be found in
the [DefenderDemoExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Defender_Windows_Simulator/Device_Defender_Demo/DemoTasks/DefenderDemoExample.c#L692-L699)
file on GitHub.


### Callback for Handling Responses

The function `prvPublishCallback()` handles incoming MQTT messages. It uses the
`Defender_MatchTopic` API from the Device Defender library to check if the incoming MQTT message is
from the AWS IoT Device Defender service. If the message is from the service, it parses the received JSON
response and extracts the report ID. Then it verifies that the report ID is the same as the one sent
in the device defender report.

The source code for the `prvPublishCallback()` function can be found in
the [DefenderDemoExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Defender_Windows_Simulator/Device_Defender_Demo/DemoTasks/DefenderDemoExample.c#L380-L464)
file on GitHub.
