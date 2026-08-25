---
title: Porting the Cellular Interface Library to another Modem
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

FreeRTOS now supports the AT commands of a TCP offloaded Cellular abstraction Layer. In order to add
support for a new cellular modem, a developer can use
the [common component](https://github.com/FreeRTOS/FreeRTOS-Cellular-Interface/tree/main/source) that
has already implemented the 3GPP standard AT commands.

In order to port the [common component](https://freertos.github.io/FreeRTOS-Cellular-Interface/v1.4.0/cellular_porting_module_guide.html):

1. Implement the cellular modem porting interface defined
   in [cellular\_common\_portable.h](https://github.com/FreeRTOS/FreeRTOS-Cellular-Interface/blob/main/source/include/common/cellular_common_portable.h) ([Documentation](https://freertos.github.io/FreeRTOS-Cellular-Interface/main/cellular__common__portable_8h.html)).

2. Implement the subset of the Cellular Interface library API's that use vendor-specific (non-3GPP) AT
   commands. The APIs to be implemented are the ones **not marked** with an "o"
   in [this table](https://freertos.github.io/FreeRTOS-Cellular-Interface/main/cellular_common__a_p_is.html).

3. Implement the Cellular Interface library callback functions that handle vendor-specific (non-3GPP)
   Unsolicited Result Codes (URC). The URC handlers to be implemented are the ones **not marked** with an "o"
   in [this table](https://freertos.github.io/FreeRTOS-Cellular-Interface/main/cellular_common__u_r_c_handlers.html).

The [Cellular common APIs document](https://freertos.github.io/FreeRTOS-Cellular-Interface/v1.4.0/cellular_porting_module_guide.html) provides
detailed information required for each step. We recommend that you start by cloning the implementation of one
of the existing modems, then make modifications where your modem's vendor-specific (non-3GPP) AT commands are
different.

Current Example Implementations:

* [Quectel BG96](https://github.com/FreeRTOS/FreeRTOS-Cellular-Interface-Reference-Quectel-BG96)
* [Sierra Wireless HL7802](https://github.com/FreeRTOS/FreeRTOS-Cellular-Interface-Reference-Sierra-Wireless-HL7802)
* [u-blox Sara-R4](https://github.com/FreeRTOS/FreeRTOS-Cellular-Interface-Reference-ublox-SARA-R4)
