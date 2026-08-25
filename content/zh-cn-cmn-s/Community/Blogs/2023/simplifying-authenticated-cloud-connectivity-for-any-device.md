---
title: 简化任何设备的身份验证云连接
date: 2023 年 12 月 14 日
feature: blog
authors:
  - ribarry
---
简介
------------


[精选 FreeRTOS IoT 参考集成](/Documentation/03-Libraries/08-Featured-integrations/06-STM32-Expresslink) 
演示了如何将 [ FreeRTOS 库的长期支持 (LTS) 版本](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries)
与硬件强制安全集成，以帮助创建安全的云连接设备。这篇博客介绍了如何使用 
执行 
[AWS IoT ExpressLink 
规范](https://aws.amazon.com/iot-expresslink/)（以下简称 "ExpressLink"）的 Wi-Fi 和蜂窝连接模块，即使在太小而无法运行软件库的微控制器 (MCU) 上 
也能实现相同的结果。



ExpressLink 简化了连接的设备软件，减少了 RAM 和 ROM 占用空间。它还大规模简化了硬件设计、 
制造和设备登录。登录是指设备首次开机时 
将设备连接到正确的云帐户的过程。


IoT 设备通常使用主机 MCU 来运行应用软件，并使用单独的通信模块来访问 Wi-Fi、 
蓝牙或蜂窝网络。一些通信模块不仅仅管理无线网络， 
还提供更高级别的协议，例如 TCP/IP 堆栈。但更常见的是， 
安全认证云通信所需的所有软件都与应用软件链接，并在主机 MCU 上运行。图 1 中的橙色框 
代表通常用于创建安全云连接的库。



[![设备到云 IoT 安全连接所需的典型库集](/media/2023/typical-library-set.png)](/media/2023/typical-library-set.png)
  

**图 1：设备到云 
 IoT 安全连接所需的典型库集**

在图 1 中：


* MQTT 是一种应用层协议，通常用于与云托管服务器进行通信。
* TLS 与用于保护 HTTPS 连接的传输层安全协议相同。
* 密钥管理和安全存储模块保护用于身份验证 
 和加密的私钥。
* 配置是用于向设备分配私钥和唯一身份的机制， 
 这在扩展生产时具有挑战性。


在图 2 中，您可以看到主机微控制器在 Wi-Fi 
或蜂窝模块连接到网络的帮助下执行此功能。



[![在主机微控制器上执行安全和连接软件](/media/2023/executing-security-and-connectivity.png)](/media/2023/executing-security-and-connectivity.png)
  

**图 2：在 
 a 主机微控制器上执行安全和连接软件**

使用操作系统 (OS) 将复杂的功能封装到称为任务的自主执行线程中， 
简化了库（橙色）和应用程序代码（绿色）之间的接口。例如， 
图 3 使用实时操作系统 (RTOS) 将 MQTT 协议和更复杂的 over-the-air 
(OTA) 更新状态机封装到它们自己的任务中，我们将其称为代理（或守护进程）任务。精心设计的 
代理易于重用且线程安全。它们使应用程序代码变得更简单， 
因为现在在代理中运行的功能不再需要设计到应用程序软件的控制流中。代理 
还隐藏低级库依赖项，图 3 仅将其显示为“中间件库”。



[![使用多线程简化接口](/media/2023/using-multithreading.png)](/media/2023/using-multithreading.png)
  

**图 3 - 使用多线程简化接口**

代理是一种有用的简化，但是 ExpressLink 更进一步， 
通过将安全性和连接功能从主机 MCU 移至连接模块，极大地简化了操作。 
ExpressLink 规范还要求 ExpressLink 模块和主机 MCU 都具有 OTA 更新功能 
。


使用 ExpressLink 消除了应用程序编写者配置或构建库的需求， 
甚至无需学习简化的代理 API。将所有这些功能从主机 MCU 卸载， 
显著降低了 MCU 的 ROM 和 RAM 要求。ExpressLink 还取消了加密固件的验证， 
减少了主机 MCU 的计算需求。


ExpressLink 通过强制硬件支持的加密和身份验证密钥安全存储来进一步简化硬件设计， 
同时也减轻了 MCU 硬件的要求。



[![在通信模块上执行安全和连接软件](/media/2023/executing-security-and-connectivity.2.png)](/media/2023/executing-security-and-connectivity.2.png)
  

**图 4：在 
  通信模块上执行安全和连接软件**

ExpressLink 规范定义了一个 AT 命令集。要从主机 MCU 使用该命令集， 
只需要一个 UART 驱动程序即可。通过自动化的登录过程，您只需在串口上写入字符串 "AT+connect"， 
即可在首次开机时创建一个 TLS 加密和认证连接， 
与正确的云账户建立连接，而无需将机密信息提供给设备的制造供应链 
。


有一个 [FreeRTOS IoT参考 
集成利用 ST 的 I-Cube-ExpressLink](../../featured-freertos-iot-integration-using-aws-iot-expresslink) 将大型和小型 MCU 连接到 AWS。在此参考集成中， 
最小的 MCU 是 STM32G0，它有 32K 的程序空间和 8K 的 RAM。
