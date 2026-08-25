---
title: "NXP LPC1769 LPCXpresso Base Board"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

### Identification

|  |  |
| --- | --- |
| **Hardware**  | <br/> The BSP was developed on and targets the<br/> LPCXpresso LPC1769<br/> CPU board and LPCXpresso Base Board. Rev A of the base board was used.<br/>  |
| **Development Tools**  | [LPCXpresso IDE](https://www.nxp.com/design/design-center/development-boards-and-designs/lpcxpresso-boards:LPCXPRESSO-BOARDS) |
| **Configuration Files Location**  | <br/> FreeRTOS-Plus-IO/Device/LPC17xx/SupportedBoards/LPCXpresso17xx-base-board.h<br/>  |
| **Port Layer Location**  | <br/> FreeRTOS-Plus-IO/Device/LPC17xx<br/>  |

### Supported peripherals and modes

|  |  |  |  |
| --- | --- | --- | --- |
| **Peripheral**  | **Connected To**  | **Transfer Modes Supported**  | **[Demo App #](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/04-Demos/01-NXP_LPC1769_Demo_Description)** |
| <br/> UART3<br/>  | <br/> USB connector on the base board via an RS232 to USB converter.<br/>  | <br/> Polled Rx - Polled Tx - Interrupt driven zero copy Tx -<br/> Interrupt driven circular buffer Rx - Interrupt driven character queue Tx -<br/> Interrupt driven character queue Rx<br/>  | <br/> #1<br/>  |
| <br/> I2C2<br/>  | <br/> OLED and serial EEPROM<br/>  | <br/> Polled Rx - Polled Tx - Interrupt driven zero copy Tx -<br/> Interrupt driven circular buffer Rx<br/>  | <br/> #1<br/>  |
| <br/> SSP1 (used in SPI mode)<br/>  | <br/> 7-segment display and SD card MMC driver<br/>  | <br/> Polled Rx - Polled Tx - Interrupt driven zero copy Tx -<br/> Interrupt driven circular buffer Rx - Interrupt driven character queue Tx -<br/> Interrupt driven character queue Rx<br/>  | <br/> #1 (7-segment display)<br/> <br/> #2 (SD card MMC driver)<br/>  |

 The demo application also integrates lwIP and FatFS.

### BSP specific [FreeRTOS\_ioctl()](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/05-FreeRTOS_ioctl) request codes

|  |  |  |
| --- | --- | --- |
| **Request Code** | **Description** | **Parameter** |
| <br/> ioctlSET\_SSP\_FRAME\_FORMAT<br/>  | <br/> The SSP port can operate in a number of different modes, one of<br/> which is SPI mode.<br/>  | <br/> boardSSP\_FRAME\_SPI is the only supported value, and configures the<br/> SSP port to use SPI mode.<br/>  |

### Demo Application

[Click here](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/04-Demos/01-NXP_LPC1769_Demo_Description) for the demo application documentation.
