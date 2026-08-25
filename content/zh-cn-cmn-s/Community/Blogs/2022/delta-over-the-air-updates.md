---
title: Delta Over-the-Air 更新
date: 2022 年 1 月 12 日
feature: blog
categories:
- 长期支持
authors:
- pvyawaha
---
<p className="tips">
  <span className="display-6">⚠️ 已弃用</span>
  <span className="content">
    本文使用的 AWS IoT OTA 库现已弃用。对于新设计，我们建议使用 [模块化 Over-the-Air 更新](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates)，它用更小的、可组合的库取代了单体式 OTA Agent。云端 OTA 流程（AWS IoT 控制台和 OTA 更新管理器服务）保持不变——只有设备端的库发生了变化。
  </span>
</p>

随着接入云端的嵌入式设备与日俱增，通过 Over-the-Air (OTA) 方式更新设备软件的功能变得日益重要。 
OTA 更新利于操作员 
大规模、快速、可靠地将安全补丁程序应用于已部署设备内并添加新功能， 
而无需费钱费事地请技术人员去处理。

虽然所有连接设备解都从 OTA 中获益，但是诸如 LoRaWAN 
和 NB- IoT 之类的低带宽网络则面临更多挑战。这些网络受到带宽的严重限制， 
如果需要向这类设备传送大型固件（或其他）映像，则进行 OTA 更新 
的成本高昂。对于接入耗电较高的 Wi-Fi 和蜂窝网络的电池供电设备而言， 
无线传送大尺寸映像也是一个问题——无线设备关闭越早， 
电池的续航时间就越长。因此，可见引入 
减小映像传输大小的机制，对这两个用例都是有益的。这篇博文 
则描述了此类机制——Delta Over-the-Air 更新。不同于向设备 
发送固件映像， Delta Over-the-Air 更新只发送 
实际已发生变化的映像部分。


## Delta Over-the-Air 更新使用二进制差异

Delta Over-the-Air 更新可以降低 OTA 的大小， 
方法是：仅发送设备上当前运行的固件与新固件之间的二进制差异（二进制差异）， 
而非发送完整固件映像。向设备发送 
二进制差异作为补丁程序文件。然后，在设备上运行的补丁程序库会重建 
来自补丁文件的新固件映像和设备上已有的固件。下述 
两个组件是二进制差异机制的主要部分：


* **Diff Utility**：开发人员在其 PC 上运行此实用程序，以 
  计算当前固件与新固件之间的二进制差值。 
  将此差值作为补丁文件通过无线方式发送到设备。
* **Patching Library**：补丁程序库在设备上运行， 
  并从补丁文件和设备当前固件上重建 
  新固件。

下图显示了更新设备或设备机群上的固件的过程 
（其中设备使用 Delta Over-the-Air 更新）：

![](/media/2021/firmware-update-process.png)

可用的二进制差异算法包括 [bsdiff](https://www.daemonology.net/bsdiff/)、[xdelta](http://xdelta.org/)、[jojodiff](http://jojodiff.sourceforge.net/)  
和 [courgette](https://www.chromium.org/developers/design-documents/software-updates-courgette)。该 
应用程序编写者可自由选择最适合其应用程序的算法。在 
选择二进制差异算法时需要牢记内存要求、性能和增量图像的大小 
。


## 使用 AWS IoT OTA 库执行 Delta Over-the-Air 更新

[AWS IoT OTA 库](https://github.com/aws/ota-for-aws-iot-embedded-sdk)在设备上运行，并管理 
新可用更新通知的接收、更新下载和所收到更新的加密验证 
。此库可用于 Delta Over-the-Air 更新。AWS 
IoT OTA 库要求应用程序提供以下接口的实现方式：

* MQTT 接口
* HTTP 接口
* OS 接口（操作系统接口）
* PAL 接口（平台抽象层接口）

![](/media/2021/delta-update-library.png)

唯一需要更新以支持 Delta Over-the-Air 更新的组件是 OTA PAL。更 
具体地说，OTA PAL 的 `OtaPalCloseFile_t` 函数必须调用补丁程序库， 
以便从补丁文件和当前固件上重建新固件图像。

以下伪代码表示 `OtaPalCloseFile_t` 函数的实现示例，此函数支持 
Delta Over-the-Air 更新：

![](/media/2021/otapalclosefile.png)


## 入门指南

从[此示例](https://github.com/FreeRTOS/Labs-Project-Espressif-Demos)入手，其中使用 
[jojodiff](http://jojodiff.sourceforge.net/) 实用程序和 [janpatch](https://github.com/janjongboom/janpatch)  
库在 Espressif 的 ESP32 system-on-chip (SoC) 上显示 Delta Over-the-Air 更新。 
运行此示例的逐步说明参见[此处](https://github.com/FreeRTOS/Labs-Project-Espressif-Demos/blob/main/README#getting-started)。


## 结论

Delta Over-the-Air (OTA) 更新减少了在带宽受限或电池供电的网络设备上更新 OTA  
的时间、成本和耗电量。如果目前使用的是 AWS IoT 
OTA 库，要获得这些优势，可以在相关函数（负责将接收到的映像写入设备的非易失性存储器） 
中添加打补丁阶段。有几种 
可用的补丁算法，每种算法在资源需求、 
处理速度、映像尺寸缩小程度等方面都各有优劣。


## 作者简介

![](https://secure.gravatar.com/avatar/4ae57ecc6122ef1c1844135bab3e9310?s=200&d=mm&r=g)   
Prasad 是 Amazon Web Services 的软件开发工程师，专注于开发各类库， 
为边缘设备实现 IoT 连接。加入 AWS 之前，他曾开发低功率网络 
堆栈和嵌入式软件，用于车载信息娱乐系统、蜂窝调制解调器和工业分析仪器 
。  
[查看此作者的文章](../author/pvyawaha) 


FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

