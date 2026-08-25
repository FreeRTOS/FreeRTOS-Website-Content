---
title:
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

FreeRTOS-Plus-IO Configuration


### Introduction

Just like the FreeRTOS kernel itself, FreeRTOS-Plus-IO is configured using a header file.
Whereas the FreeRTOS configuration header file is called FreeRTOSConfig.h,
the FreeRTOS-Plus-IO configuration header file is called FreeRTOS**IO**Config.h.

The settings in the kernel's configuration file (FreeRTOSConfig.h) do not
greatly impact the size of the executable binary created when the code is
compiled. This is because, for the most part,
the settings it contains are used to include or exclude entire functions.
The default* behaviour of most linkers is to remove any unreferenced
functions from the executable binary anyway.
The settings in the FreeRTOS-Plus-IO configuration file (FreeRTOS**IO**Config.h), on the
other hand, **do** greatly impact code size. This is because they are used to optionally
include or exclude code within functions, rather than optionally include or exclude the entire function itself.
It is important to ensure FreeRTOSIOConfig.h is configured optimally if flash/ROM
space is at a premium.

* GCC is the exception to this, where specific compile time options are required to request that
  unreferenced code is removed.


### An example FreeRTOSIOConfig.h header file

The details of the parameters contained in a FreeRTOSIOConfig.h header
file are dependent on the [board support package](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_IO/Board_Support_Packages) being used.
Below is an example, and below that an explanation.

```c
/* Globally include or exclude transfer modes. -------------------------------*/
#define ioconfigUSE_ZERO_COPY_TX                     1
#define ioconfigUSE_TX_CHAR_QUEUE                    1
#define ioconfigUSE_CIRCULAR_BUFFER_RX               1
#define ioconfigUSE_RX_CHAR_QUEUE                    1


/* Peripheral options --------------------------------------------------------*/

/* There is one group of definitions for each peripheral defined by the
board support package. More details are provided below this example. */

/* Globally include or exclude the UART driver. */
#define ioconfigINCLUDE_UART                         1
    /* Include or exclude transfer modes for this particular peripheral. These
 are dependent on the global transfer mode settings at the top, and the
 global setting for the UART peripheral directly above. */
    #define ioconfigUSE_UART_POLLED_TX               0
    #define ioconfgiUSE_UART_POLLED_RX               0
    #define ioconfigUSE_UART_ZERO_COPY_TX            0
    #define ioconfigUSE_UART_TX_CHAR_QUEUE           1
    #define ioconfigUSE_UART_CIRCULAR_BUFFER_RX      0
    #define ioconfigUSE_UART_RX_CHAR_QUEUE           1

/* As above, but for the SPI peripheral. */
#define ioconfigINCLUDE_SPI                          1
    #define ioconfigUSE_SPI_POLLED_TX                0
    #define ioconfigUSE_SPI_POLLED_RX                0
    #define ioconfigUSE_SPI_ZERO_COPY_TX             1
    #define ioconfigUSE_SPI_CIRCULAR_BUFFER_RX       1
    #define ioconfigUSE_SPI_RX_CHAR_QUEUE            0
    #define ioconfigUSE_SPI_TX_CHAR_QUEUE            0

/* Etc. for any other peripherals defined by the board support package. */
```

### Global transfer mode options

In the example above, the top group of options are used to include or exclude
specific [transfer modes](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes) from FreeRTOS-Plus-IO. The polling mode is always available,
so there is no option specific to that.

| **FreeRTOSIOConfig.h parameter** | **Usage** |
| --- | --- |
|  ioconfigUSE\_ZERO\_COPY\_TX  |  Must be set to 1 if you are going to use the  [interrupt driven zero copy transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/08-Zero_Copy_Transfer_Mode). Otherwise, set to zero to ensure the best run time and code size efficiency.   |
|  ioconfigUSE\_CIRCULAR\_BUFFER\_RX  |  Must be set to 1 if you are going to use the  [interrupt driven circular buffer transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/09-Circular_Buffer_Transfer_Mode). Otherwise, set to zero to ensure the best run time and code size efficiency.   |
|  ioconfigUSE\_TX\_CHAR\_QUEUE  |  Must be set to 1 if you are going to use the  [interrupt driven character queue transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/10-Character_Queue_Transfer_Mode) to write data. Otherwise, set to zero to ensure the best run time and code size efficiency.   |
|  ioconfigUSE\_RX\_CHAR\_QUEUE  |  Must be set to 1 if you are going to use the  [interrupt driven character queue transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/10-Character_Queue_Transfer_Mode) to read data. Otherwise, set to zero to ensure the best run time and code size efficiency.   |


### Peripheral specific options

The board support package defines which peripherals are available.
For each peripheral there is a global include or exclude option. For
example, to include the SPI peripheral, set configINCLUDE\_SPI to 1. To
exclude the SPI peripheral, set configINCLUDE\_SPI to 0.

Each peripheral then has a sub-option for each transfer mode supported
by the peripheral. For example, if you want to use the SPI port in
interrupt driven zero copy mode set ioconfigUSE\_SPI\_ZERO\_COPY\_TX to 1,
otherwise set ioconfigUSE\_SPI\_ZERO\_COPY\_TX to 0.

Therefore, to continue the example, to use the SPI port in interrupt
driven zero copy mode three settings are required:

1. ioconfigUSE\_ZERO\_COPY\_TX must be set to 1 to enable the transfer mode in FreeRTOS-Plus-IO.
2. ioconfigINCLUDE\_SPI must be set to 1 to enable SPI support.
3. ioconfigUSE\_SPI\_ZERO\_COPY\_TX must be set to 1 to specifically enable the use of the zero copy
   transfer mode on the SPI port.
