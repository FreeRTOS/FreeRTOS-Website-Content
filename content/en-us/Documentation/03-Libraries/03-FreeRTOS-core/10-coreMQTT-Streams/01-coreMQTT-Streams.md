---
title: "AWS IoT Core MQTT File Streams Embedded C"
created: 2018-09-20
categories:
  - kernel
description: An introduction to the AWS IoT Core MQTT File Streams Embedded C client library
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: Beginner's guide to FreeRTOS
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: Download FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FAQs
    link: /Why-FreeRTOS/FAQs
---

### Introduction

In AWS IoT, a stream is a publicly addressable resource that is an abstraction for a list of files that can be transferred to an IoT device. The MQTT file streams library uses the MQTT protocol to accomplish this transfer. It supports both JSON and CBOR format to send requests and receive data. More information about streams and MQTT-based file delivery can be found [here](https://docs.aws.amazon.com/iot/latest/developerguide/mqtt-based-file-delivery.html).

This library has gone through code quality checks including verification that no function has a [GNU Complexity](https://www.gnu.org/software/complexity/manual/complexity.html) score over 8, and checks against deviations from mandatory rules in the [MISRA coding standard](https://www.misra.org.uk/). Deviations from the MISRA C:2012 guidelines are documented under [MISRA Deviations](https://github.com/aws/aws-iot-core-mqtt-file-streams-embedded-c/blob/main/MISRA.md). This library has also undergone static code analysis using [Coverity static analysis](https://scan.coverity.com/), and validation of memory safety through the [CBMC automated reasoning tool](https://www.cprover.org/cbmc/).

This library can be freely used and is distributed under the MIT Open Source License.

**Code Size of AWS IoT Core MQTT File Streams Embedded C library (example generated with GCC for ARM Cortex-M)**

| File | With -O1 Optimization | With -Os Optimization |
| ---- | --------------------- | --------------------- | 
| MQTTFileDownloader.c | 1.1K | 1.0K |
| MQTTFileDownloader\_cbor.c | 0.8K | 0.6K |
| MQTTFileDownloader\_base64.c | 0.6K | 0.6K |
| core\_json.c | 2.9K | 2.4K |
| cborparser.c | 2.8K | 2.2K |
| cborencoder.c | 2.0K | 0.7K |
| cborencoder\_close\_container\_checked.c | 0.1K | 0.1K |
| Total estimates | 10.3K | 7.6K |

 
### MQTT File Streams Config File

The MQTT file streams library exposes build configuration macros that are required for building the library. A list of all the configurations and their default values are defined in [MQTTFileDownloader_defaults.h](https://github.com/aws/aws-iot-core-mqtt-file-streams-embedded-c/blob/main/source/include/MQTTFileDownloader_defaults.h). To provide custom values for the configuration macros, a custom config file named MQTTFileDownloader_config.h can be provided by the application to the library.

By default, a `MQTTFileDownloader_config.h` custom config is required to build the library. To disable this requirement and build the library with default configuration values, provide `MQTT_STREAMS_DO_NOT_USE_CUSTOM_CONFIG` as a compile-time preprocessor macro.

Thus, the MQTT library can be built by either:
  - Defining a `MQTTFileDownloader_config.h` file in the application, and adding it to the include directories list of the library OR
  - Defining the `MQTT_STREAMS_DO_NOT_USE_CUSTOM_CONFIG` preprocessor macro for the library build.

**MQTT File Streams Library workflow**

[![MQTT File Streams Library workflow](/media/2024/mqtt-file-streams-lib.png)](/media/2024/mqtt-file-streams-lib.png)

_Click to enlarge_
 
### How to use MQTT-streams library for an OTA update

Follow these steps:
  1. The user will need to use the [jobs library](https://github.com/aws/Jobs-for-AWS-IoT-embedded-sdk) and 
     [MQTT streams library](https://github.com/aws/aws-iot-core-mqtt-file-streams-embedded-c) to be able to use AWS IoT Jobs for an OTA update.
  1. Once a Job Document is received, the job ID is extracted from AWS IoT Jobs Library .
  1. The MQTT streams downloaded can be initialized using `mqttDownloader_init` . Here the parameters extracted from 
     the AWS IoT OTA jobs document using OTA jobs parser are passed. This initializes the MQTT file downloader. It also creates the topic names for the DATA and Get Stream Data topics.
  1. When an OTA event is received for requesting file block:
      1. `mqttDownloader_createGetDataBlockRequest` is used to create the Get data block request. MQTT streams library only 
         creates the get block request. To publish the request, MQTT libraries like coreMQTT need to be employed.
      1. MQTT library will call the `mqttDownloader_isDataBlockReceived` API to determine if an OTA block has been received. 
         The API performs this operation by comparing the incoming MQTT message topic with MQTT streams topics.
      1. If an OTA block was received, the MQTT streams library will extract and decode the received OTA data block from the 
         incoming MQTT message. The API `mqttDownloader_processReceivedDataBlock` is to be used for decoding the block for the application to handle.
  1. It is left to the user's discretion to design the platform abstraction layer APIs for the OTA update. These PAL APIs might allow 
     the user to perform the following functions:
  1. Abort an OTA transfer (if the IOT Jobs OTA require this)
  1. Various file operations like creation, deletion, and activation of the new received image.
  1. Storing data from a received block - This will be required once a received data block has been processed by the streams library.

_Note : The creation, deletion, and activation operations do not necessitate an abstraction layer. The application integrator could directly use their port specific APIs for file operations, signature verification, and boot-loading._

### Documentation

  - [API Reference](https://aws.github.io/aws-iot-core-mqtt-file-streams-embedded-c/latest/)

### Demos:

These demos make use of the MQTT file streams library to demonstrate an OTA update.

  1. [OTA (Using Simple OTA Orchestrator)](https://www.freertos.org/freertos-core/over-the-air-updates/mqtt-simple-orchestrator.html)
  1. [OTA (Using OTA Agent Orchestrator)](https://www.freertos.org/freertos-core/over-the-air-updates/mqtt-ota-agent-orchestrator.html)
