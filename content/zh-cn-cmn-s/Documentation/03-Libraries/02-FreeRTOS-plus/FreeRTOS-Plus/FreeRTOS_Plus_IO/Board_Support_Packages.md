---
title: FreeRTOS-Plus-IO 板级支持包
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


### 引言

板级支持包 (BSP) 可在特定板上将 FreeRTOS-Plus-IO 代码
导向特定微控制器。其等同于
在 FreeRTOS 中的端口层。

FreeRTOS-Plus-IO 代码包括一个名为 FreeRTOS_IO_BSP.h 的头文件。
此头文件应直接包含 BSP 信息，或
其本身用于包含对于所使用目标而言正确的 BSP 头文件
。

建议最好将 FreeRTOS_IO_BSP.h 放在应用程序目录中，
与 FreeRTOSIOConfig.h 放在一起，因为头文件针对的是
应用程序所使用的硬件，而不是核心 FreeRTOS-Plus-IO 代码所使用的硬件。

BSP 包括：

* 一张定义所支持的外围设备，并定义
  在调用 [FreeRTOS_open()](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/02-FreeRTOS_open) 过程中如何识别每台外围设备的表格。

* 设备特定的外围驱动器。

* 一组常量，用于定义外围 pin 输出、LED 极性等。

* [FreeRTOSIOConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/06-FreeRTOS_Plus_IO_Configuration) 头文件示例。

* 描述任何目标特定 [FreeRTOS_ioctl() request codes](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/05-FreeRTOS_ioctl) 的文档。


### 外围设备支持定义

定义所支持的外围设备的表格，形式
为 Available_Peripherals_t 结构体数组：

```c
typedef struct xAVAILABLE_DEVICES
{
    /* Text name of the peripheral. For example, "/UART0/", or "/SPI2/". */
    const int8_t * const pcPath;

    /* The type of the peripheral, as defined by the Peripheral_Types_t enum. */
    const Peripheral_Types_t xPeripheralType;

    /* The base address of the peripheral in the microcontroller memory map. */
    const void *pvBaseAddress;
} Available_Peripherals_t;

The Available_Peripheral_t structure

```

数组被分配给宏 boardAVAILABLE_DEVICES_LIST，因此会出现
在 BSP 配置文件中，例如：

```c
#define boardAVAILABLE_DEVICES_LIST
{
    { "/UART3/", eUART_TYPE, MCU_UART3 },
    { "/SSP1/", eSSP_TYPE,   MCU_SPI1 },
    { "/I2C2/", eI2C_TYPE,   MCU_I2C2 }
}

```
*分配给 boardAVAILABLE_DEVICES_LIST 宏的 Available_Peripheral_t 结构体数组*


以上示例定义了三台外围设备。使用路径字符串
"/UART3/" 访问的外围设备属于 UART 类型，其基地址
为 MCU_UART3。同表还定义了在各自地址处的 SPI 外围设备和 I2C 外围设备
。

将数组分配给 boardAVAILABLE_DEVICES_LIST 宏允许与多份 BSP 配置文件使用相同的
核心 FreeRTOS-Plus-IO 代码，
只需更改 BSP 标头文件即可。
