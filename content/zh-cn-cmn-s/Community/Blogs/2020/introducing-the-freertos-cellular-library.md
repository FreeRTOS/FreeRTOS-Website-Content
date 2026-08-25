---
title: FreeRTOS 蜂窝网库简介
created: 2020-12-14 00:00:00.0 UTC
feature: blog
categories:
- 长期支持
authors:
- luciodj
relatedLinks:
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

由[ Lucio Di Jasio ](../author/luciodj)于 2020 年 12 月 14 日发布

我们很高兴介绍一个新的 FreeRTOS 库的预览，该库旨在简化 
IoT 应用程序的开发，而这些应用程序可通过[蜂窝 LTE-M 技术](https://en.wikipedia.org/wiki/LTE-M)连接至云端。 
LTE-M，也称为 Cat-M1，是一种由 [3GPP](http://www.3gpp.org/) 开发的低成本 LPWAN 技术, 
属于 LTE 标准第 13 版的一部分，同时也是 
广义 [5G 技术](https://en.wikipedia.org/wiki/5G)集合的组成部分。它也是 
 [NB-IoT](https://en.wikipedia.org/wiki/Narrowband_IoT) 的补充技术，但它速度更快，具备 1 Mbps 的上传和下载 
速度，以及更低的延迟。因此它非常适合许多命令和控制应用程序。默认情况下， 
所有 LTE-M 蜂窝调制解调器向后兼容 4G 技术（如 CAT1），并且会在 
必要时回退到 3G 和 2G，以保证连接。 


## 使蜂窝 IoT 应用易于开发

大多数蜂窝模块的串行端口都实现标准（ASCII - AT 命令）接口，适合用于 
大多数微控制器和 FreeRTOS 应用程序。然而各个微控制器供应商实现串行 
接口 (UART) 的方式略有不同，不同蜂窝模块供应商的命令集（最初由 3GPP 标准定义） 
也存在细微区别，以展现其产品的最佳（或独特）功能 
。因此，如果没有做过特定硬件的实现，开发者没有简易快捷的办法采用蜂窝技术， 
而且大量的精力浪费在重新实现每个微控制器和模块对的串行接口上 
。 

FreeRTOS 蜂窝网库帮助解决了这一问题。蜂窝网库分离了模块命令 
序列化和解析模块答复所需的重复、未区分的代码，提供了一个简单 
且统一的[应用程序编程接口 (API)](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/01-Cellular-interface)。这种统一 
接口使开发人员能够专注于应用程序逻辑， 
加快开发进度，并提供整洁、可信赖的代码基础。使用蜂窝网库 API 的 
应用程序将可以在不同供应商和型号的蜂窝调制解调器之间自由移植。目前， 
 FreeRTOS 蜂窝网库支持以下常见蜂窝 
调制解调器：[Quectel BG96](https://www.quectel.com/product/bg96.htm)、[Sierra Wireless HL7802](https://www.sierrawireless.com/products-and-solutions/embedded-solutions/products/hl7802/)、 
和 [U-Blox Sara-R4](https://www.u-blox.com/en/product/sara-r4-series)。


## 构建 IoT 堆栈

[FreeRTOS](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) 提供了专为 IoT 应用程序设计的网络堆栈。通用连接 
技术（如以太网、Wi-Fi 和 BLE）已与此堆栈集成，一系列 
使用常见微控制器和无线模块的电路板也在 
 [FreeRTOS 参考集成](https://devices.amazonaws.com/search?page=1&sv=freerto)中获得支持。新的 
蜂窝网库提供传输层以适配该堆栈，以便与 
其他 TCP 套接字连接选项通用。

![图 1：使用蜂窝网库的免费 RTOS IoT 应用程序堆栈](/media/2020/Figure-1-Cellular-Blog.png)


## 开发和测试蜂窝网 IoT 应用程序

得益于 FreeRTOS IoT 库的常见堆栈设计和灵活性（如 coreMQTT、coreHTTP、 
corePKCS11 等等），现在可以将原本为其他无线连接解决方案设计的 IoT 应用程序轻松地快速迁移 
到蜂窝技术。此外， 
也能更快设计和测试新的蜂窝网 IoT 应用程序， 
方法是使用 [FreeRTOS Windows 模拟器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW) 
和 [Linux (POSIX) 模拟器](https://freertos.org/FreeRTOS-simulator-for-Linux.html)。事实上，我们 
创建了一个新的 [FreeRTOS Lab 存储库](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo)， 
其中包含三个 (Visual Studio) 项目。这个存储库基于 FreeRTOS Windows 模拟器，仅需一台笔记本电脑 
和一个评估套件就可以运行最初支持的三个调制解调器中的任意一个。您可以在 
 FreeRTOS 蜂窝演示[入门指南](../../cellular-demo)获取更多有关设置调制解调器和构建演示的信息。

此外，三个新的 FreeRTOS 参考集成已经通过认证。这些集成基于 FreeRTOS 202011.00 版本 
库并使用以下工具包： 
 [STM32L4+ Discovery board](https://devices.amazonaws.com/detail/a3G0h0000087pwWEAQ/STM32L4+-Discovery-Kit-IoT-Node)、 
 [STMODLTE](https://www.st.com/content/st_com/en/products/evaluation-tools/solution-evaluation-tools/communication-and-connectivity-solution-eval-boards/steval-stmodlte.html)、 
Sierra Wireless [Sensor Hub AWS Kit](https://www.richardsonrfpd.com/Products/Product/SENSORHUB-AWS#) 
（采用 Sierra Wireless HL7802 模块）、 
Nuvoton - [NuMaker IoT M487 主板](https://devices.amazonaws.com/detail/a3G0h000000Tg9cEAC/NuMaker-IoT-M487) 
和 Quectel [RFBG96 适配器](https://www.nuvoton.com/board/rf-bg96a/)。您可以在 
[AWS 合作伙伴设备目录](https://devices.amazonaws.com/search?conn=lte-m&kw=LTE&page=1)中找到它们。 


## FreeRTOS 蜂窝网库反响

新 FreeRTOS 蜂窝网库的反响令我们感到兴奋，这个库是我们根据 
 FreeRTOS 合作伙伴、客户和嵌入式开发人员社区的反馈而构建。以下是我们的合作伙伴想说的话…… 

<blockquote>
  <span className="content">
  将 u-blox LTE-M 和 NB-IoT 模块与 FreeRTOS 蜂窝网库集成，进一步扩大了我们 
  对客户的承诺。这些客户开发连接到 AWS 云服务的安全 IoT 和边缘设备。” 
  </span>
  <span className="attribution">
  Harald Kröll，u-blox 产品经理 
  </span>
</blockquote>

<blockquote>
  <span className="content">
  “我们对 FreeRTOS 蜂窝网库（支持 STM32L4+ Discovery Kit IoT Node 和 Quectel BG96’s STEVAL-STMODLTE）的发布感到很高兴。 
  我们的客户将获益匪浅，他们在开发 
  蜂窝 IoT 应用程序时能节省大量的时间和精力。” 
  </span>
  <span className="attribution">
  Andre Dostie，STMicroelectronics, Inc. 美洲微控制器部门 IoT 应用总监
  </span>
</blockquote>

<blockquote>
  <span className="content">
  "我们很高兴能继续与 AWS 进行长期合作。BG96 蜂窝模块，已经获得 AWS  
  IoT Core 认证，被纳入 AWS 合作伙伴设备目录，现在集成到 FreeRTOS 蜂窝网 中， 
  使我们的客户更加快捷地连接到 AWS 云。”
  </span>
  <span className="attribution">
  Alexander Bufalino，Quectel Wireless Solutions 营销副总裁
  </span>
</blockquote>

<blockquote>
  <span className="content">
  “我们很高兴看到 AWS 推出的 FreeRTOS 蜂窝网库可随时支持我们的 HL7802  
  模块，以满足我们共同客户的需求，并加快开发创新 IoT 应用程序， 
  以连接到 AWS 云。” 
  </span>
  <span className="attribution">
  Ashish Syal，Sierra Wireless 首席工程师
  </span>
</blockquote>


## 总结

您可以在[此处](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/01-Cellular-interface)找到更多关于 FreeRTOS 蜂窝网库的更多信息。我们将 
继续为新调制解调器和常见调制解调器增加蜂窝接口的实现，我们也欢迎您 
为扩展调制解调器目录和改进库功能做出贡献。了解 
更多详细信息，请参阅[蜂窝网库移植指南](../../cellular-porting-guide)。敬请期待……

FreeRTOS 是一款 MIT 授权的、适用于微控制器的开源实时操作系统， 
让您可以轻松地编写、部署、保护、连接和管理低功耗的小型边缘设备。

您可以下载源代码开始使用 
（下载地址：[FreeRTOS.org](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) 或 [GitHub](https://github.com/freertos/freertos) ()）， 
同时了解 FreeRTOS 及其库和演示的更多信息，详情请见  
[FreeRTOS 用户指南](/Documentation/03-Libraries/02-FreeRTOS-plus/01-Introduction)。
 

## 作者简介

![](https://secure.gravatar.com/avatar/9938f7b242eb47e5e8c3f41e0e927283?s=200&d=mm&r=g)   
Lucio 是 Amazon Web Services 的产品经理。过去 20 年里，他在半导体行业 
担任过各种技术和营销职务。作为一个富有见解的高产作者，他发表了 
许多关于嵌入式控制应用程序编程的文章和技术书籍。热爱 
飞行的他又获得了 FAA 和 EASA 私人飞行员执照。  
[查看此作者的文章](../author/luciodj) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

