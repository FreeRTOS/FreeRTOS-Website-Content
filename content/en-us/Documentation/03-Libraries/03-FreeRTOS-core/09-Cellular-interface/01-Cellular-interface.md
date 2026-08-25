---
title: "Cellular interface"
created: 2018-09-20
categories:
  - kernel
description: An introduction to the Cellular interface library
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
externalLinks:
  - title: Cellular interface API reference
    link: https://freertos.github.io/FreeRTOS-Cellular-Interface/v1.3.0/
---

## Introduction

The Cellular Interface library implements a simple
unified [API](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/01-Cellular-interface) that hides the complexity
of cellular modem-specific AT commands and exposes a socket-like interface to C programmers.

Most cellular modems implement more or less of the AT commands defined by
the [3GPP TS v27.007](https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=1515)
standard. This project provides an [implementation](https://github.com/FreeRTOS/FreeRTOS-Cellular-Interface/tree/main/source)
of such standard AT commands in a [reusable common component](https://freertos.github.io/FreeRTOS-Cellular-Interface/main/cellular_porting_module_guide.html).
The three Cellular Interface libraries in this project all take advantage of that common code. The library
for each modem only implements the vendor-specific AT commands, then exposes the complete Cellular Interface API.

The common component that implements the 3GPP TS v27.007 standard has been written in compliance with the
following code quality criteria:

* GNU Complexity scores are not over 8
* MISRA C:2012 coding standard. Any deviations from the standard are documented in source code comments marked by "coverity".


## Getting Started

###  Download the source code

The source code can be downloaded from the FreeRTOS libraries or by itself.

To clone from Github using HTTPS:

```c
git clone https://github.com/FreeRTOS/FreeRTOS-Cellular-Interface.git
```

Using SSH:

```c
git clone git@github.com:FreeRTOS/FreeRTOS-Cellular-Interface.git
```


### Folder structure

At the root of this repository are these folders:

* source: reusable common code that implements the standard AT commands defined by 3GPP TS v27.007
* docs : documentation
* test: unit test and cbmc
* tools: tools for Coverity static analysis and CMock


### Configure and build the Library

The Cellular Interface library should be built as part of an application. In order to do so, certain
configurations must be provided.
The [FreeRTOS Cellular Demo](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator)
project provides an [example](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator/MQTT_Mutual_Auth_Demo_with_BG96/cellular_config.h)
of how to configure the build. More information can be found in
the [Cellular Interface API Reference](https://freertos.github.io/FreeRTOS-Cellular-Interface/main/cellular_config.html).


Please refer to the [Cellular Interface Demo (Mutual Authentication)](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/03-Cellular-interface-demo) for more information.


## Integrate the Cellular Interface Library with MCU platforms

The Cellular Interface library runs on MCUs that use an abstracted interface,
the [Comm Interface](https://github.com/FreeRTOS/FreeRTOS-Cellular-Interface/blob/main/source/interface/cellular_comm_interface.h),
to communicate with cellular modems. A Comm Interface must be implemented on the MCU platform as well.
The most common implementations of the Comm Interface work over UART hardware, but they can be implemented
over other physical interfaces, such as SPI, as well. The documentation for the Comm Interface can be
found in the [Cellular API Reference](https://freertos.github.io/FreeRTOS-Cellular-Interface/main/cellular_porting.html#cellular_porting_comm_if).
These are example implementations of the Comm Interface:

* [FreeRTOS windows simulator comm interface](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator/Common/comm_if_windows.c)
* [FreeRTOS Common IO UART comm interface](https://github.com/aws/amazon-freertos/blob/main/libraries/abstractions/common_io/include/iot_uart.h)
* [STM32 L475 discovery board comm interface](https://github.com/aws/amazon-freertos/blob/feature/cellular/vendors/st/boards/stm32l475_discovery/ports/comm_if/comm_if_uart.c)
* [Sierra Sensor Hub board comm interface](https://github.com/aws/amazon-freertos/blob/feature/cellular/vendors/sierra/boards/sensorhub/ports/comm_if/comm_if_sierra.c)
