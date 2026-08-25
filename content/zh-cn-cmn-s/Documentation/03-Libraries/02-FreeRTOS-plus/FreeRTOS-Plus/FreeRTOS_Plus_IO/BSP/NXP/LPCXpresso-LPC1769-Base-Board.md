---
title: "NXP LPC1769 LPCXpresso 基板"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

### 识别

|  |  |
| --- | --- |
| **硬件**  | <br/> BSP 基于<br/> LPCXpresso LPC1769<br/> CPU 板和 LPCXpresso 基板进行开发，并以此为目标。使用的是 Rev A 基板。<br/>  |
| **开发工具**  | [LPCXpresso IDE](https://www.nxp.com/design/design-center/development-boards-and-designs/lpcxpresso-boards:LPCXPRESSO-BOARDS) |
| **配置文件位置**  | <br/> FreeRTOS-Plus-IO/Device/LPC17xx/SupportedBoards/LPCXpresso17xx-base-board.h<br/>  |
| **端口层位置**  | <br/> FreeRTOS-Plus-IO/Device/LPC17xx<br/>  |

### 支持的外围设备和模式

|  |  |  |  |
| --- | --- | --- | --- |
| **外围设备**  | **连接至**  | **支持的传输模式**  | **[演示应用编号](/Documentation/03-Libraries/03-FreeRTOS-plus/04-FreeRTOS-plus-IO/04-Demos/01-NXP_LPC1769_Demo_Description)** |
| <br/> UART3<br/>  | <br/> 通过 RS232 - USB 转换器，连接至基板上的 USB 连接口。<br/>  | <br/> 轮询 Rx - 轮询 Tx - 中断驱动的零拷贝 Tx -<br/> 中断驱动的循环缓冲区 Rx - 中断驱动的字符队列 Tx -<br/> 中断驱动的字符队列 Rx<br/>  | <br/> #1<br/>  |
| <br/> I2C2<br/>  | <br/> OLED 和串行 EEPROM<br/>  | <br/> 轮询 Rx - 轮询 Tx - 中断驱动的零拷贝 Tx -<br/> 中断驱动的循环缓冲区 Rx<br/>  | <br/> #1<br/>  |
| <br/> SSP1（用于 SPI 模式）<br/>  | <br/> 7 段显示器和 SD 卡 MMC 驱动器<br/>  | <br/> 轮询 Rx - 轮询 Tx - 中断驱动的零拷贝 Tx -<br/> 中断驱动的循环缓冲区 Rx - 中断驱动的字符队列 Tx -<br/> 中断驱动的字符队列 Rx<br/>  | <br/> 1号（7 段显示器）<br/> <br/> 2号（SD 卡 MMC 驱动器）<br/>  |

 此外，演示应用程序还集成了 lwIP 和 FatFS。

### BSP 特定 [FreeRTOS_ioctl()](/Documentation/03-Libraries/03-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/05-FreeRTOS_ioctl) 请求代码

|  |  |  |
| --- | --- | --- |
| **请求代码** | **说明** | **参数** |
| <br/> ioctlSET_SSP_FRAME_FORMAT<br/>  | <br/> SSP 端口可以在多种不同模式下运行，<br/> 其中一个是 SPI 模式。<br/>  | <br/> boardSSP_FRAME_SPI 是唯一支持的值，且可配置<br/> SSP 端口，以使用 SPI 模式。<br/>  |

### 演示应用程序

[单击此处](/Documentation/03-Libraries/03-FreeRTOS-plus/04-FreeRTOS-plus-IO/04-Demos/01-NXP_LPC1769_Demo_Description)查看演示应用程序文档。

