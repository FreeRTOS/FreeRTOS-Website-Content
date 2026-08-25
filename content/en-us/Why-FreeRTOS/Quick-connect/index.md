---
title: AWS Quick Connect Demos
---
**This is intended as a short-term demonstration application and does not provide data privacy guarantees. Setting up an AWS account will allow you to take advantage of many new features and functionality, including data privacy. Learn more about [setting up an AWS account](https://docs.aws.amazon.com/accounts/latest/reference/accounts-welcome.html).**

Quick Connect demos make it simple to setup and connect a partner provided, FreeRTOS qualified board 
to [AWS IoT](https://aws.amazon.com/iot/), all in the space of a few minutes; no toolchain to install 
and configure, no dependencies to install, no source code to download and build, and no AWS account 
and AWS IoT setup and configuration required. Once your device is connected, messages can be sent from 
the device to AWS IoT, allowing you to simulate an IoT application. Furthermore, one can choose to modify 
the demo source code, then build and flash the demo using the chosen board’s build system and tools, 
and immediately see the affect of one’s code change on the demo application. 

These simulations can be used for non-production applications to explore the IoT space for up to 7 days. 
By connecting your device using Quick Connect, you agree to the terms and conditions provided in 
the [AWS Customer Agreement](https://aws.amazon.com/agreement/) and 
the [Privacy Notice](https://aws.amazon.com/privacy/). 

The supported boards are listed here. New boards will be added as they become available. 

LTS - boards using the FreeRTOS LTS libraries. [Learn more about LTS.](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries)


### Supported Boards

| Board Name | Manufacturer | LTS Libraries | Quick Connect |
| ---------- | ------------ | ------------- | ------------- |
| [STM32L4+ Discovery Kit IoT Node](/Why-FreeRTOS/Quick-connect/stm32l4-demo) |  STMicroelectronics  | [coreMQTT](https://github.com/FreeRTOS/coreMQTT/tree/v1.1.0), [backoffAlgorithm](https://github.com/FreeRTOS/backoffAlgorithm/tree/v1.0.0) | [Connect board](/Why-FreeRTOS/Quick-connect/stm32l4-demo) |
| [ESP32-C3-DevKitC-02](/Why-FreeRTOS/Quick-connect/esp32c3-demo) |  Espressif  | [coreMQTT](https://github.com/FreeRTOS/coreMQTT/tree/v1.1.0) | [Connect board](/Why-FreeRTOS/Quick-connect/esp32c3-demo) |
| [QEMU MPS2-AN385](/Why-FreeRTOS/Quick-connect/qemu-mps2-an385-demo) | FreeRTOS | [coreMQTT](https://github.com/FreeRTOS/coreMQTT/tree/v1.1.0), [backoffAlgorithm](https://github.com/FreeRTOS/backoffAlgorithm/tree/v1.0.0) | [Start Emulator](/Why-FreeRTOS/Quick-connect/qemu-mps2-an385-demo) |
