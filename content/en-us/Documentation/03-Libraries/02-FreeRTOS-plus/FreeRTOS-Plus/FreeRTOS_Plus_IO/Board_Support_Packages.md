---
title: FreeRTOS-Plus-IO Board Support Packages
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


### Introduction

Board support packages, or BSPs, target the FreeRTOS-Plus-IO code to a specific
microcontroller, on a specific board. It is the equivalent to the port layer
found in FreeRTOS itself.

The FreeRTOS-Plus-IO code includes a header file called FreeRTOS\_IO\_BSP.h.
This header file should ether contain the BSP information directly, or
itself just be used to include the BSP header file that is correct for
the target being used.

It is best to locate FreeRTOS\_IO\_BSP.h in an application directory, along side
FreeRTOSIOConfig.h, because the header file is specific to the hardware
being used by the application rather than the core FreeRTOS-Plus-IO code.

A BSP includes:

* A table that defines the supported peripherals, and how each peripheral is identified in calls
  to [FreeRTOS\_open()](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/02-FreeRTOS_open).

* Device specific peripheral drivers.

* A set of constants that define peripheral pin outs, LED polarities, etc.

* An example [FreeRTOSIOConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/06-FreeRTOS_Plus_IO_Configuration) header file.

* Documentation that describes any target specific [FreeRTOS\_ioctl() request codes](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/05-FreeRTOS_ioctl).


### Peripheral support definition

The table that defines the supported peripherals takes the form of an
array of Available\_Peripherals\_t structures:

```c
typedef struct xAVAILABLE_DEVICES
{
    /* Text name of the peripheral. For example, "/UART0/", or "/SPI2/". */
    const int8_t * const pcPath;

    /* The type of the peripheral, as defined by the Peripheral\_Types\_t enum. */
    const Peripheral_Types_t xPeripheralType;

    /* The base address of the peripheral in the microcontroller memory map. */
    const void *pvBaseAddress;
} Available_Peripherals_t;

The Available_Peripheral_t structure
```

The array is assigned to the macro boardAVAILABLE\_DEVICES\_LIST, so appears
in a BSP configuration files as something like:

```c
#define boardAVAILABLE_DEVICES_LIST
{
    { "/UART3/", eUART_TYPE, MCU_UART3 },
    { "/SSP1/", eSSP_TYPE,   MCU_SPI1 },
    { "/I2C2/", eI2C_TYPE,   MCU_I2C2 }
}
```
*An array of Available_Peripheral_t structures assigned to the boardAVAILABLE_DEVICES_LIST macro*


The above example defines three peripherals. The peripheral accessed
using the path string "/UART3/" is of type UART, and has a base address
of MCU\_UART3. The same table also defines an SPI peripheral and an I2C
peripheral at their respective addresses.

Assigning the array to the boardAVAILABLE\_DEVICES\_LIST macro allows the same
core FreeRTOS-Plus-IO code to be used with multiple BSP configuration files,
simply by changing the BSP header file.
