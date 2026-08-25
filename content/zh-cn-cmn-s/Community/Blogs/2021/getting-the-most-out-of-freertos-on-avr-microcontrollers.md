---
title: 在 AVR® 微控制器上充分利用 FreeRTOS
created: 2021-02-11 00:00:00.0 UTC
feature: blog
categories:
- 长期支持
authors:
- jacoblassen
relatedLinks:
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Jacob Lunn Lassen](../author/jacoblassen) 于 2021 年 2 月 11 日发布

令人兴奋的是，FreeRTOS™ 10.3.1 版本中新增了两个 [AVR](../../a00090#ATMEL)® 微控制器 (MCU) 移植， 
或更确切地说是六个新移植。这些移植不仅涵盖 megaAVR® 0 系列 MCU 和 
全新的 AVR Dx 设备，还涵盖 AVR MCU 的三个主要编译器，分别为 MPLAB XC8 编译器、 
AVR-GCC 和 IAR Embedded Workbench® for AVR。为什么这是个好消息？原因在于 
FreeRTOS 早期版本支持的 ATmega323 和 ATmega128 MCU 属于陈旧设备。虽然 
这些设备产品仍然可用，但 AVR MCU 早已历经演进，性能显著提升： 
谁不想体验最新一代产品呢？

通过对新设备和新编译器的支持功能，我很想了解 
标准 FreeRTOS 演示示例在某个新 MCU 上消耗多少内存、编译器的选择 
对代码大小的实际影响。我将仅关注 AVR Dx MCU 系列移植， 
确保本文言简意赅。


## AVR Dx 大揭秘：是 tinyAVR ® 、megaAVR 还是 AVR XMEGA ® MCU？

广为人知的 AVR MCU 可能是 ATmega328，该 MCU 主要用于 
[Arduino® UNO](https://store.arduino.cc/arduino-uno-rev3) 套件。AVR Dx 是最新一代 
AVR MCU ，类似于最新的 tinyAVR 1 系列，如 ATtiny817 ， 
也与 AVR XMEGA 设备相类似。因此，相较于旧版 MegaAVR MCU，AVR Dx 的复杂度更高。这种差异 
在外围设备中最为明显，也体现在如何在内存映射中更好地组织它们。

目前有两个AVR Dx MCU 系列。 
[AVR DA 系列](https://www.microchip.com/design-centers/8-bit/avr-mcus/device-selection/avr-da?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG) 
采用用于接口电容式传感器的最新版本外围触摸控制器 (PTC) 模块， 
可用于可触摸用户界面。 
[AVR DB 系列](https://www.microchip.com/design-centers/8-bit/avr-mcus/device-selection/avr-db?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG) 
具有内置运算放大器和多电压 I/O，即表示可以从单独电压域运行所选引脚 
。这样就无需使用昂贵的电平转换器。

与过去AVR MCU 相比，AVR Dx MCU 性能有显著改善。内部稳压电源运行核心逻辑， 
表示核心的最大速度不受外部电源电压的限制 
。无论电源电压如何，皆可以在 24 MHz 条件下运行。换言之， 
即使在低电压应用中，也可以获得更多马力且有源模式功耗更低。


### IDE 和编译器

支持 AVR MCU 的最新编译器是 
**[MPLAB XC8](https://www.microchip.com/development-tools-tools-and-software/mplab-xc-compilers?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG)** 
编译器，它是 GCC 编译器的一个变体。它已集成到 
[MPLAB X IDE](https://www.microchip.com/mplab/mplab-x-ide?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG)中， 
并被添加到 Microchip  Studio 7.0.2542 版本中 。MPLAB XC8 编译器提供免费版本， 
囊括优化选项子集。MPLAB XC8 PRO 属于商业版本， 
提供用户期待的专业级编译器的所有优化。虽然 IAR EWAVR 和 
Microchip  Studio 仅适用于 Windows ®操作系统，但 MPLAB X 和 MPLAB XC8 编译器 
可用于 Linux®和 macOS® 系统以及 Windows 系统。顺便一提，MPLAB X IDE 亦兼容 AVR-GCC 
编译器。

多年来用户群一直维护 GNU GCC 编译器的 AVR-GCC 变体版本， 
虽然并未积极维护 WIN-AVR 原有版本，但这一版本仍然存在。后来 Atmel 决定将 
AVR-GCC 并入 Atmel Studio 集成开发环境，然后将 AVR-GCC 作为 Atmel Studio 
插件提供给 AVR MCU 用户 。AVR-GCC 编译器和 Arduino 板为 AVR MCU 在 Maker 社区的普及 
发挥重大作用。2020 年 11 月，Microchip  将 Atmel Studio 7 
更名为 [Microchip AVR 和 SAM 设备专属 Studio](https://www.microchip.com/mplab/microchip-studio?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG)； 
我将其称为 Microchip  Studio。虽然功能未作更改，但值得一提的是有一项绝佳附加功能： 
Microchip  Studio 兼容 MPLAB XC8 编译器。这说明熟悉 
Atmel Studio 和 AVR-GCC 的用户可以仍然使用这一知名的集成开发环境， 
同时能够发挥 MPLAB XC8 编译器的优势。

AVR 专用 **[IAR 嵌入式工作台](https://www.iar.com/iar-embedded-workbench/#!?architecture=AVR)**（IAR 
简称 EWAVR ）是首个可使用 AVR MCU 的 C 编译器。如果定义指令集， 
则 AVR Core 发明者与 IAR 密切合作，产生优化 C 代码的较好指令集 
。IAR EWAVR 集 IDE、编译器和模拟器于一身。Microchip’ 的调试和编程工具 
也可在 IAR EWAVR 中使用。

所用编译器版本：

* AR EWAVR (v7.30)
* AVR-GCC (build v3.6.2.1778)
* MPLAB XC8 编译器 (v2.30)


### 查找合适的移植和设备

查看 [FreeRTOS](/Documentation/02-Kernel/03-Supported-devices/00-Supported-devices) 网站的支持设备时，我意识到 
有必要向你们介绍一下半导体公司的历史。虽然 AVR MCU 属于 Microchip  产品， 
但最初是由 Atmel（后于 2016 年被 Microchip  收购）发布。这就是为什么 AVR 设备被列在 Atmel 
而不是 Microchip  下的原因（请参阅 FreeRTOS 网站）。此处还提供了 Microchip’ 的 
Arm® 基于核心的 MCU 完整列表。

![图 1：带有 FreeRTOS 移植的 Microchip 产品线。](/media/2021/figure1-300x51.png)   
*图 1：带有 FreeRTOS 移植的 Microchip  产品线。*

深入浏览 FreeRTOS 网站结构后，我找到了[AVR Dx 移植页面](../../microchip-avr-dx-demo)， 
该页面同时支持 AVR DA 和 AVR DB 设备。移植附带演示使用 
[AVR128DA48](https://www.microchip.com/wwwproducts/en/AVR128DA48?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG) 
设备和相应的 [AVR128DA48 Curiosity Nano 评估板](https://www.microchip.com/DevelopmentTools/ProductDetails/PartNO/DM164151?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG)。 
此主板适用于所有移植，用于确认代码是否正在运行。

![图 2：AVR128DA48 Curiosity Nano 评估套件。](/media/2021/figure2-300x200.png)   
*图 2：AVR128DA48 Curiosity Nano 评估套件。*


### 下载（或使用 Git 克隆）

我从 [FreeRTOS 下载页面](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)下载了标准发行版。标准发行版 
是包含所有移植和演示、以及内核和 FreeRTOS 库的压缩文件。如果用户希望 
拥有代码的本地 Git 分支，也可以从 FreeRTOS GitHub 项目中将其克隆出来。

下载 zip 压缩文件，将其解压并存放到 Demo 文件夹。如果您喜欢使用 MCU， 
那么这里就如同糖果店一样，琳琅满目，选择多样！

![图 3：FreeRTOS 文件夹结构中的 AVR MCU 移植。](/media/2021/figure3-300x211.png)   
*图 3：FreeRTOS 文件夹结构中的 AVR MCU 移植。*

在详细介绍编译器之前，值得一提的是 Demo 示例。


### Demo 示例

AVR Dx 移植带有三个演示。将三个演示集成到各编译器移植的单个代码项目中 
。这三个演示是：

* Blinky
* Minimal
* Full

可以使用 `mainSELECTED_APPLICATION` define 在编译时选择演示。在 main.c 文件中， 
可将 `mainSELECTED_APPLICATION` 定义为 0、1 或 2，进而在点击 build 按键之前 
选择所需的演示。

![图 4：在 main.c 中选择活跃演示](/media/2021/figure4-300x154.png)   
*图 4：在 main.c 中选择活跃演示*


## MPLAB X IDE (v5.40) 和 MPLAB XC8 编译器 (v2.31)

在菜单中，**“打开项目”**并导航到 AVR_DX_MPLAB 项目文件。MPLAB X IDE 中的项目文件 
是一个扩展名为“.X”的文件夹，在这种情况下为“ **AVR_Dx_MPLAB.X**”。

![图 5：MPLAB X 项目 "file" 是 .X 文件夹。](/media/2021/figure5-300x156.png)   
*图 5：MPLAB X 项目 "file" 是 .X 文件夹。*

**“项目属性”**描述了编译器的配置方式。**“配置”**确认 
项目被配置为使用 MPLAB XC8 v2.31 编译器，并且所选的**“设备”**是 
AVR128DA48。移植页面指出，MPLAB XC8 v2.20 编译器 
用于移植的开发和测试， 
但使用 v2.31（本文撰写时最新版本）也很流畅。

![图 6：项目属性对话框。选择设备和编译器工具链。](/media/2021/figure6-300x193.png)   
*图 6：项目属性对话框。选择设备和编译器工具链。点击放大。*

那么，启用了哪些优化级别？优化选项位于 
**选项类别**下拉菜单中的 **XC8 全局选项** -> **XC8 编译器**。

![图 7：项目属性对话框-编译器优化。](/media/2021/figure7-300x84.png)   
*图 7：项目属性对话框-编译器优化。单击以放大*

选中所有优化复选框，但“调试”选项除外， 
这样旨在检查是否使用系统内调试器进行调试，例如 
[MPLAB PICkit™ 4](https://www.microchip.com/developmenttools/ProductDetails/PG164140?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG)、[MPLAB ICD 4](https://www.microchip.com/developmenttools/ProductDetails/dv164045?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG) 
或 [Atmel-ICE 编程器/调试器](https://www.microchip.com/DevelopmentTools/ProductDetails/ATATMEL-ICE?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG)， 
但这完全是两回事。**“优化级别”**设置为 “s” ， 
这是尺寸优化的最高级别。此优化级别可供 
[MPLAB XC8 PRO 编译器](https://www.microchip.com/developmenttools/ProductDetails/sw006021-sub?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG)的 PRO 版本访问。 
MPLAB XC8 编译器免费版支持优化级别 -O1 和 -O2。使用 -Os 编译 
会发出警告，即由于 -Os 某些优化设置需要 MPLAB XC8 PRO 编译器， 
因而这些优化会被忽略掉，但编译时不会出错。

此外，在**“附加选项”**文本框中指定 -flto 开关。我参考了 
MPLAB XC8 编译器用户指南查看开关控件。-flto 开关打开 
“标准链接时间优化器” ，这是在 MPLAB XC8 编译器 PRO 版本中发现的一个功能。附带说明： 
AVR-GCC 编译器未记录 -flto 选项， 
因此这是 MPLAB XC8 编译器和 AVR-GCC 的区别所在。

![图 8：项目属性对话框。选择优化级别并使用附加选项启用链接时间优化。](/media/2021/figure8-300x193.png)   
*图 8：项目属性对话框。选择优化级别并使用附加选项启用链接时间优化
。点击放大。*

由于 Microchip  拥有 MPLAB XC 编译器所有既往版本的在线存档和相应用户指南， 
因此搜索引擎可能无法提供最新版本的用户指南； 
建议直接从 
[MPLAB XC 编译器产品页面](https://www.microchip.com/development-tools-tools-and-software/mplab-xc-compilers?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG)获取所需版本。


### 代码大小结果

由于并非每个人皆持有 MPLAB XC8 PRO 编译器许可证， 
现已提供免费编译器和 PRO 编译器的代码大小结果。编译器不会在“输出”窗口中生成任何代码大小信息， 
但“控制面板”窗口则显示了规整图形和纯文本表现形式 
。

![图 9： MPLAB X 仪表板显示代码项目的内存大小。](/media/2021/figure9-300x211.png)   
*图 9： MPLAB X 仪表板显示代码项目的内存大小。*

根据三个示例的代码大小结果，获得 demo 应用程序的大小：

**MPLAB XC8 PRO 版编译器 (-Os)**
| 演示 | 闪存大小 | SRAM 大小 |
| ---- | ---------- | --------- |
| Blinky | 6836 | 4271 |
| Minimal | 10230 | 4308 |
| Full | 13255 | 4332 |

**MPLAB XC8 免费版编译器 (-Os)**
| Demo | 闪存大小 | SRAM 大小 |
| ---- | ---------- | --------- |
| Blinky | 9078 | 4287 |
| Minimal | 13840 (-O1) | 4319 |
| Full | 16691 | 4338 |

如您所见，在生成小于免费版本的程序代码方面，MPLAB XC8 PRO 编译器显然性能更佳， 
而这两项设置的数据内存使用率几乎无差异。


## Microchip Studio (v7.0.2542) 和 AVR-GCC (v3.6.2.1778)

现在可以打开 Microchip  Studio 项目了。在 Microchip  Studio选择**“打开项目” **， 
导航到 FreeRTOS/Demo/AVR_Dx_Atmel_Studio 文件夹，然后打开 RTOS Demo 文件。

![图 10：Microchip  Studio 项目文件。](/media/2021/figure10-300x83.png)   
*图 10：Microchip  Studio 项目文件。*

在方案资源管理器 (Solution Explore)（导航）中， 
右键单击项目并选择**“属性” **，打开编译器配置。从中选择 AVR/GNU C 编译器 -> 优化项目。选中所有复选框， 
优化选为 -Os。

![图 11：项目属性。选择优化设置。](/media/2021/figure11-300x160.png)   
*图 11：项目属性。选择优化设置。*

在 **Debugging** 选项中，将**“调试级别”**设置为 -g2（默认级别）。

![图 12：项目属性。选择调试级别。](/media/2021/figure12-300x102.png)   
*图 12：项目属性。选择调试级别。*

对于**链接器** -> **优化**，选中“垃圾回收未使用部分”选项。该 
GUI 似乎包括最常见的 GCC 选项，但也可以手动指定其他选项。

![图 13：项目属性。已启用垃圾回收。](/media/2021/figure13-300x143.png)   
*图 13：项目属性。已启用垃圾回收。*


### 搜索结果

Microchip Studio 和 AVR-GCC 以及其他编译器都会生成一些警告。 
其中有些警告涉及完成超出变量支持宽度的移位， 
本文不作赘述。Microchip Studio 在编译器输出窗口中显示代码大小：

![图14：输出窗口显示的代码项目的内存大小。](/media/2021/figure14-300x30.png)   
*图 14：输出窗口显示的代码项目的内存大小。点击放大。*

警告：如果在程序代码标准 .text 段之外的其他段放置代码， 
则代码大小信息可能缺乏准确性。通过使用 avr-size 工具查看 ELF 输出文件， 
得出结论：代码主要使用 .text 段，由于这种方式的代码大小误差极小， 
所以较为合理。

**AVR-GCC**
| 演示 | 闪存大小 | SRAM 大小 |
| ------- | ---- | ---- |
| Blinky  | 8026 | 4309 |
| Minimal  | 12490 | 4420 |
| Full  | 15152 | 4555 |


## AVR 专用 IAR 嵌入式工作台

在 IAR EWAVR 中，使用工作区文件打开 FreeRTOS 移植项目。右键单击项目 
并选择**“选项” **，即可进行优化设置。GUI 选项有限， 
任何关键内容一览无余，因此简单易用。选择优化级别 
以及是否需要优化代码的大小或速度，然后选中所有复选框。

Porthardware.h 包含 FreeRTOSConfig.h ，但由于某种原因，编译器无法自行定位此文件， 
因此，必须指定编译代码的路径。这个解决方法极简单， 
但我原本希望代码能在开箱后就编译成功。

![图 15：项目选项。选择优化级别和其他优化选项。](/media/2021/figure15-300x269.png)   
*图 15：项目选项。选择优化级别和其他优化选项。*

在**“项目”**菜单中点击**“重新生成所有”**……

**IAR EWAVR **
| Demo： | 闪存大小 | SRAM 大小 |
| ------ | ---- | ---- |
| Blinky | 7278 | 4636 |
| Minimal | 11341 | 4728 |
| Full | 11921 | 4863 |


## 我并不是编译器专家……

并非每个人都是编译器方面的专家。所以，我联系了 Microchip’ 和 IAR 的编译专家， 
询问是否可以进一步改进移植的优化设置。这些优化 
设置可能坑许多用户并不熟悉，因此，我学以致用， 
希望能为那些需要将代码缩小至最低限度的人带来一些启发。


## Microchip 提供的专家建议

Microchip’的专家建议在 MPLAB XC8 编译器的“全局选项”中添加以下切换开关:

![图16：项目属性。在附加选项中添加专家优化。](/media/2021/figure16-300x170.png)   
*图 16：项目属性。在附加选项中添加专家优化。点击放大。*

这项功能极大改善了代码大小，降至 7.9% 至 10.6% ：

**MPLAB XC8 PRO 编译器（专家版） **
| Demo | 闪存大小 | SRAM 大小 | 改进 |
| ------ | ---- | ---- | ---- |
| Blinky | 6242 | 4271 | 8.7% |
| Minimal | 9426 | 4308 | 7.9% |
| Full | 11847 | 4332 | 10.6% |


## IAR 提供的专家建议

IAR 的专家建议在命令行选项中添加以下内容：

![图17 ：项目选项。在命令行选项中添加专家优化。](/media/2021/figure17-300x268.png)   
*图 17 ：项目选项。在命令行选项中添加专家优化。*

这项改进会使所有三个演示示例的代码大小减少约 200 字节， 
即指实现 1.5% 至 3.1% 的改进：

**IAR EWAVR（专家版）**
| Demo： | 闪存大小 | SRAM 大小 | 改进 |
| ------ | ---- | ---- | ---- |
| Blinky | 7056 | 4636 | 3.1% |
| Minimal | 11099 | 4728 | 2.1% |
| Full | 11739 | 4863 | 1.5% |


## 总结

我们的目标是找出 AVR Dx 系列在运行 FreeRTOS 时 
的内存消耗情况。因此， 
在 IAR 和 Microchip: 并未提供专家反馈的情况下，对比框中代码大小结果。

**AVR-GCC**
| Demo： | 闪存大小 | SRAM 大小 |
| ------ | ---- | ---- |
| Blinky | 8026 | 4309 |
| Minimal | 12490 | 4420 |
| Full | 15152 | 4555 |

**MPLAB XC8 PRO 版编译器**
| Demo： | 闪存大小 | SRAM 大小 |
| ------ | ---- | ---- |
| Blinky | 6836 | 4271 |
| Minimal | 10230 | 4308 |
| Full | 13255 | 4332 |

**MPLAB XC8 免费版编译器**
| Demo： | 闪存大小 | SRAM 大小 |
| ------ | ---- | ---- |
| Blinky | 9078 | 4287 |
| Minimal | 13840 | 4319 |
| Full | 16691 | 4338 |

**IAR EWAVR **
| Demo： | 闪存大小 | SRAM 大小 | 
| ----- | ---------- | --------- |
| Blinky | 7278 | 4636 |
| Minimal | 11341 | 4728 |
| Full | 11921 | 4863 |

无论演示示例如何， SRAM 消耗恒定不变， 
这一特征尤为突出。由于所有编译器皆兼容 4 KB 以上的 RAM ，因此，可以得出结论， 
用户需要 8 KB 或以上的设备。闪存消耗取决于演示示例。显然， 
需要更多闪存才能获得较大的演示代码。Full 演示示例编译为 12–13 KB 的程序内存（闪存）。 
这意味着选择 MCU 时， SRAM 正在驱动内存需求。由于这些设备在 
闪存和 SRAM 之间的比率为 8: 1，因此，需要 64 KB 的 AVR DA/DB 才能获得足够的 SRAM。有些选项 
是 AVR64DA48（位于 Curiosity Nano 开发板）或 AVR64DB32。最大的 
AVR DA/DB 设备配备 128 KB 的闪存和 16 KB 的 SRAM ，因此空间充足，可以容纳众多应用程序 
。也就是说， FreeRTOS 将根据所用线程数或多或少使用 SRAM ， 
因此 SRAM 消耗并非一成不变。

除了 AVR Dx 设备的移植外，megaAVR 0 系列 
MCU（即 ATmega1608/9、ATmega3208/9 和 ATmega4808/9）的移植也已发布。这些 MCU 在许多方面 
与传统的 AVR MCU 相似，但也具有 XMEGA 系列的元素。由于 FreeRTOS 
对 SRAM 有一定的需求，因此 ATmega480x 设备是一个不错的选择， 
因为它们有 6 KB 的 SRAM 和 48 KB 的闪存。较小系列的 SRAM 较小， 
因此需要对 FreeRTOS 配置进行一些调整来与之匹配。

在编译器方面，MPLAB XC8 PRO 版编译器的性能极佳，令人印象深刻。 
此编译器为 Blinky 和 Minimal 演示生成了较小代码，而使用开箱即用设置时， IAR EWAVR 在 Full 示例中表现更好 
。根据编译器专家的建议， 
MPLAB XC8 编译器在 Blinky 和 Minimal 演示中表现更强，生成的代码量更少（分别少 13% 
和 17.7%），而在 Full 演示中，IAR 
EWAVR 生成的代码量仅相差 0.9%，差距如此之小，所以我将其视为平局。详见下表。 
SRAM 消耗不受专家设置的影响；故得出结论： 
相较于 IAR EWAVR (8.5% 至 12.3%)，MPLAB XC8 编译器能够节省相当数量的 SRAM。

**MPLAB XC8 PRO 编译器（专家版）**
| Demo： | 闪存大小 | SRAM 大小 |
| ------ | ---- | ---- |
| Blinky | 6242 | 4271 | 
| Minimal | 9426 | 4308 | 
| Full | 11847 | 4332 | 

**IAR EWAVR（专家版）** 
| Demo： | 闪存大小 | SRAM 大小 | 
| ------ | ---- | ---- |
| Blinky | 7056 | 4636 |
| Minimal | 11099 | 4728 |
| Full | 11739 | 4863 |

**MPLAB XC8 编译器 vs.IAR EWAVR**
| Demo： | 闪存 | SRAM |
| ------ | ------ | ----- |
| Blinky | -13.0% | -8.5% |
| Minimal | -17.7% | -9.7% |
| Full | 0.9% | -12.3% |

如您所见， MPLAB XC8 PRO 版编译器和 IAR EWAVR 性能俱佳。对于大容量设计， 
选择一个商用编译器，迁移到内存较大的 MCU 时， 
可以节省成本。

很高兴看到 Microchip  为其最新 AVR MCU 创建 FreeRTOS 移植。以后我一定 
会留意基于 FreeRTOS 的 AVR MCU 项目。


## 致谢

用于 AVR MCU 的新 FreeRTOS 移植于 v10.3.1 发布；布加勒斯特的 Microchip’ 的 PIC® 
和 AVR MCU 应用程序团队以及 Amazon 的 FreeRTOS 团队做出重大贡献。感谢各位的辛苦付出 
。

感谢 Microchip  和 IAR 的编译器专家对编译器进行优化， 
使编译器的性能发挥到极致。


## 免责声明

此博文中的内容和意见属第三方作者的内容和意见，AWS 
对此帖子的内容或准确性概不负责。 


## 作者简介

![](https://secure.gravatar.com/avatar/cfa4d47b14862d65ab27765c400a75d8?s=200&d=mm&r=g)   
Jacob Lunn Lassen 荣获丹麦奥尔堡大学硕士学位。于 2000 年加入 Atmel 
的 AVR 应用团队，从事关键客户支持、电机控制、智能电池、EMC 研究和产品 
开发工作。他于 2016 年加入了 Microchip’ 的 PIC 和 AVR MCU 营销团队， 
目前从事产品定义、IoT 和功能安全方面的工作。  
[查看此作者的文章](../author/jacoblassen) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

