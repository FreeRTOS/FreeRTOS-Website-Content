---
title: "FreeRTOS LPC2148 演示（由 JC Wren 提供） 包括 FatFS 和 LPCUSB"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

J.C. Wren 汇总了一个非常完整且实用的示例 FreeRTOS 应用程序，其中包括但不限于以下内容：
* 来自 ChaN 的 FatFS [免费 FAT 文件系统](http://elm-chan.org/fsw/ff/00index_e.html)。
* Bertrik Sikken 为 LPC214x 提供的 LPCUSB [免费 USB 堆栈](http://sourceforge.net/projects/lpcusb)。
* 一个 newlib 实现。
* 一个控制台命令解释器。
* 一个 GPS NMEA 接口。
* 各种外设驱动程序，包括 I2C、SPI、UART、ADC、外部中断、实时时钟、GPIO，当然，还有 USB。

源代码 zip 文件包括所有 FreeRTOS、FatFS 和 LPCUSB 源代码，可以直接从 [JC Wren](http://jcwren.com/arm) 网站下载，
适用于 Windows 和 Linux 用户。

**有关完整信息，包括构建和下载说明，请参阅随源代码一起提供的
[应用程序注意事项](http://jcwren.com/arm/xREADME_latest)。**

在此，特向 J.C. Wren 表示感谢，感谢他的出色工作，并将成果分享给 FreeRTOS 社区。
