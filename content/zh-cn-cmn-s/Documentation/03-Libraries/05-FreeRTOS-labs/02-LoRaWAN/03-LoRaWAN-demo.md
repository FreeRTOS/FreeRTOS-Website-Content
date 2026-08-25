---
title: 针对 LoRaWAN 演示的 FreeRTOS 支持
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


**注意**：针对 LoRaWAN 演示项目的 FreeRTOS 支持位于 FreeRTOS-Labs。此演示虽然功能齐全， 
但正在进行优化或重构，以提高内存使用率、增强模块性、完善说明文档、提升演示可用性或测试覆盖率 
。它位于 
GitHub 上的 [Lab-Project-FreeRTOS-LoRaWAN](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-LoRaWAN) 存储库， 
与 Labs 项目的主下载文件分隔开。 

如上所述， A 类提供最节能的通信模式并且可实现最长的电池寿命 
。上行和下行链路消息可以已确认（需要另一方 
的 ACK）或未确认（无需 ACK）。下图 3a 和 3b 展示了 
已确认的上行链路和下行链路的序列。如需了解有关详细说明，请参阅 
 [LoRaWAN 1.0.3](https://lora-alliance.org/wp-content/uploads/2020/11/lorawan1.0.3.pdf) 规范的第 18 节。 

[\![](/media/2020/Figure-3a.png)](/media/2020/Figure-3a.png)   
*图 3a：已确认数据消息的上行链路时序图（来源：LoRa 联盟）点击放大。*

[\![](/media/2020/Figure-3b.png)](/media/2020/Figure-3b.png)   
*图 3b：已确认数据消息的下行链路时序图（来源：LoRa 联盟）点击放大。*

此页上的演示描述了 A 类应用程序的工作示例。它会生成 A 类应用程序 
任务，该任务定期发送上行链路消息， 
并遵循 [LoRaWAN 地区参数](https://resources.lora-alliance.org/technical-specifications/rp002-1-0-4-regional-parameters)定义的链路公平访问策略。 
上行链路消息在已确认或未确认模式下均可发送。成功启用上行链路后， 
任务将等待下行链路消息或任何其他来自 MAC 层的事件。它将通过下行链路 
收到的帧负载和移植写入控制台。如果 MAC 层显示有其他下行链路消息挂起， 
或有出于控制目的需要发送的上行链路，它会立即发送空白上行链路消息。 
如果 MAC 层检测到帧丢失，它会触发再入网流程来重置帧计数器。 
处理完所有下行链路数据和事件后，任务将恢复休眠状态直到下一个传输周期。

MAC 层到应用程序的所有事件都使用轻量级任务通知发送。LoRaWAN 允许 
将服务器的多个请求捎带到上行链路消息中。这些请求的响应 
由应用程序接收，以便使用队列。如果应用程序想要在发送上行链路有效负载之前 
同时读取接收到的多个有效负载，也会存在下行链路队列。 


## 低功率模式

A 类设备通信的一个重要功能是，应用程序在其生命周期的大部分时间 
休眠，因而消耗的功率更少。通过 
FreeRTOS [无滴答空闲功能](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)可以为演示启用低功率模式。通过为 
`portSUPPRESS_TICKS_AND_SLEEP()` 宏提供板特定的实现并将 `configUSE_TICKLESS_IDLE`  
设置为 FreeRTOSConfig.h 中的适当值可以启用无滴答空闲模式。启用无滴答模式允许 MCU 在任务处于空闲时休眠， 
但由无线电或其他定时器事件中的中断唤醒。


## 入门指南

此博客文章描述了演示所需的硬件：

* Nordic NRF52840 开发套件
* Semtech sx1262mb2cas（带天线）
* [LoRa Raspberry Pi 网关](https://www.sparkfun.com/products/15336)（[开始使用](https://cdn.sparkfun.com/assets/3/0/d/e/2/Get_Start_with_RAK2245_Pi_HAT_V2.4R.pdf) 
  并将网关连接至 The Things Network——本页面未介绍）


### 支持的平台

| 供货商 | MCU | LoRa Radio Shield | IDE |
| ------ | --- | ----------------- | --- |
| Nordic | [NRF52840-DK](https://www.nordicsemi.com/Software-and-Tools/Development-Kits/nRF52840-DK) | [sx1262mb2cas](https://www.semtech.com/products/wireless-rf/lora-transceivers/sx1262mb2cas) | [Segger Embedded Studio (SES)](https://www.segger.com/downloads/embedded-studio) |
| STMicroeletronics | [STM32-L4](https://www.st.com/en/microcontrollers-microprocessors/stm32l4-series.html) | [sx1276MB1LAS](https://www.semtech.com/products/wireless-rf/lora-transceivers/sx1276mb1las) | [STM32 系統工作台](https://www.st.com/en/development-tools/sw4stm32.html) |


## 快速设置

###  设备硬件设置 (Nordic NRF52840 + Semtech SX126x Mbed Radio)

图 4 所示为 Nordic NRF52480 开发套件，图 5 所示为 Semtech SX126x LoR 无线电收发器的 Mbed 屏蔽板 
。

[\![](/media/2020/Figure-4.png)](/media/2020/Figure-4.png)   
*图 4：Nordic NRF52840-DK 板  点击放大。*

[\![](/media/2020/Figure-5.png)](/media/2020/Figure-5.png)   
*图 5：Semtech SX126x LoRa 无线电收发器  点击放大。*

该套件与 Arduino UNO 版本 3 标准兼容，顶部可以堆叠 
SX126x 屏蔽板，如图 6 所示。Nordic MCU 运行 FreeRTOS 和 LoRa MAC 层， 
它通过 SPI、GPIO 和 UART 接口与 LoRa 无线电收发器通信。

[\![](/media/2020/Figure-6-right-scaled.jpg)](/media/2020/Figure-6-right-scaled.jpg)   
*图 6 Nordic NRF52840-DK 板和 Semtech SX126x LoRa 组合 点击放大。*


###  设置 IDE

* [下载支持 ARM 的最新 Segger Embedded studio IDE](https://www.segger.com/downloads/embedded-studio/)
* 安装支持 ARM IDE 的Embedded studio IDE。


###  下载并查看代码

- [使用 Git 存储库设置 SSH](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account)。

- 下载[存储库](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-LoRaWAN.git)以及相关存储库：

  ```c
  git clone --recurse-submodules https://github.com/FreeRTOS/Lab-Project-FreeRTOS-LoRaWAN.git  
  ```

- FreeRTOS LoRaWAN 实现使用略有修补的 LoRaMac-Node 4.4.4 版本。补丁 
  用于公开无线电 HAL 回调，以通知无线电中断事件。要应用补丁程序，请执行以下操作： 

  ```c
  cd Lab-Project-FreeRTOS-LoRaWAN  

  git apply --whitespace=fix FreeRTOS-LoRaMac-node-v4_4_4.patch  
  ```

- 通过以下路径打开 Segger Embedded Studio 中的解决方案： 
  `demos/classA/Nordic_NRF52/classa_demo.emProject`

  [\![](/media/2020/Figure-7.png)](/media/2020/Figure-7.png)   
  *图 7 Segger IDE 展示 A 类演示项目  点击放大。*


###  在 The Things Network (TTN) 上注册设备

在终端设备能通过 The Things Network (TTN) 沟通之前，请按照 
[步骤](https://www.thethingsnetwork.org/docs/devices/registration.html)  将其注册到应用程序 
。


### 设置激活凭据

Over the Air Activation (OTAA) 和 Activation By Personalization (ABP) 方法要求在设备中配置 Device EUI、Join EUI 以及必要的密钥 
。对于生产用例，我们强烈 
建议您通过安全元件预先配置这些凭据。为了支持预先配置的凭据， 
用户需要使用 LoRaMac-node 提供的接口 secure-element.h 提供安全元件的实现 
。不同安全元件的引用实现位于 
LoRaMac-node 存储库。 

所提供的示例使用基于软件的安全元件。凭据可以通过 getter 函数， 
从内存位置或闪存检索。默认情况下，示例将凭据硬编码为静态常量变量 
。以下步骤描述了如何设置这些变量的值。

* 打开文件 `demos/classA/common/credentials.c`，根据演示的激活类型 
  配置全局变量。注意：这些参数是以十六进制值数组的形式提供，其中以大端字节顺序表示字节 
  。

* 对于 Over The Air Activation (OTAA)：
  + 将变量 devEUI 设置为全局唯一的 8 字节 Device EUI。
  + 将变量 joinEUI 设置为 8 字节 Join EUI。
  + 将 appKey 设置为 16 字节的预共享网络密钥。

* 对于 Activation By Personalization (ABP)：
  + 将变量 devEUI 设置为全局唯一的 8 字节 Device EUI。
  + 将变量 joinEUI 设置为 8 字节 Join EUI。
  + 将变量 appSessionKey 和 nwkSessionKey 设置为 16 字节的预共享会话密钥。
  + 将 END_DEVICE_ADDR 设置为预先分配的 24 位 NET ID。

  ```c
  /**  
   * @brief Device EUI needed for both OTAA and ABP activation.  
   */  
  static const uint8_t devEUI[ 8 ] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };  
    
  /**  
   * @brief JOIN EUI needed for both OTAA and ABP activation.  
   */  
  static const uint8_t joinEUI[ 8 ] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };  
    
  /**  
   * @brief App key required for OTAA activation.  
   */  
  static const uint8_t appKey[ 16 ] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };  
  ```

* 注释或删除以 #error 开头的行 

  ```c
  #error "Please configure DEV EUI, Join EUI and App key to run the demo using OTAA"  
              
  ```


### 设置 LoRaWAN 区域

* 选择示例区域时，也会根据 
  [LoRaWAN 地区参数](https://resources.lora-alliance.org/technical-specifications/rp002-1-0-4-regional-parameters)指南为 LoRaMAN 选择频率计划和其他参数 
  。默认情况下，示例设置为连接到 US915 区域

* 若要为示例选择其他区域，请前往 A 类任务 `demos/classA/common/classa_task.c` 
  并使用适当的区域类型更新 LORAWAN_REGION。示例：

  ```c
  #define LORAWAN_REGION         ( LORAMAC_REGION_US915 )  

  ```

各个区域的枚举列表位于头文件 LoRaMac-node/src/mac/LoRaMac.h 中 


### 构建并运行代码

* 连接您的 nrf52840-dk。
* 在 SES 的 Build 菜单中，选择 Build classa_demo。下文图 8 显示了 IDE 调试终端中的 UART 
  输出
* 在 SES 的 Debug 菜单中，选择 Go。设备将在调试模式下闪烁并运行演示。程序的开头有一个断点 
  。准备就绪后，便可以继续执行。

[\![](/media/2020/Figure-8.png)](/media/2020/Figure-8.png)   
*图 8 Segger IDE 显示构建完成  点击放大。*


###  加入该设备

* 在初始化 LoRaWAN 堆栈后，设备发送加入请求。 

  [\![](/media/2020/Figure-9.png)](/media/2020/Figure-9.png)   
  *图 9 TTN 控制台显示中断设备加入请求  点击放大。*

* 图 10 中的 TTN 控制台显示从 LNS 将加入请求发送回网关，然后再发送 
  到终端设备。

  [\![](/media/2020/Figure-10.png)](/media/2020/Figure-10.png)   
  *图 10 TTN 控制台显示终端设备 Join Accept  点击放大。*

* 图 11 中的终端设备调试控制台显示已接收 Join accept，并且设备成功完成 加入过程 
  。终端设备获得 `Device Address`，然后将其用于所有上行链路 
  和下行链路通信。 

  [\![](/media/2020/Figure-11.png)](/media/2020/Figure-11.png)   
  *图 11 Segger IDE 显示通过设备地址分配完成加入流程  点击放大。*


### 发送上行链路数据

LoRaWAN A 类通信允许设备在成功激活后随时发送上行链路数据。 
但是，连接到 LoRaWAN 网络的设备应遵循针对特定区域定义的占空比限制和公平访问策略 
。该策略限制数据包大小或发送时间以及允许传输的占空比 
。想要了解关于占空比限制和公平访问策略的更多信息， 
请参阅[此处](https://www.thethingsnetwork.org/docs/lorawan/duty-cycle.html)。

FreeRTOS 的 A 类设备演示任务按照以占空比间隔为基础配置的间隔发送 2 字节的周期性上行链路数据 
。以下是该设备在 TTN 上发送和接收的数据包的屏幕截图：


* 如图 12 所示，该设备在每个 TX-RX 周期发送 2 字节的 `0xFEED` 上行链路数据包。数据包 
  以未确认模式发送，这意味着不会收到这些数据包的 ACK。（注意：如需更改为已确认 
  模式，请在 `demos/classA/common/classa_task.c` 中设置以下配置）。

  ```c
  #define LORAWAN_CONFIRMED_SEND                 ( 1 )  

  ```

  [\![](/media/2020/Figure-12.png)](/media/2020/Figure-12.png)   
  *图 12：Segger IDE 显示设备成功发送上行链路数据  点击放大。*

* 图 13 显示由 TTN 控制台接收的数据包以及接收元数据，诸如网关 RSSI、SNR 
  。 

  [\![](/media/2020/Figure-13.png)](/media/2020/Figure-13.png)   
  *图 13 TTN 控制台显示终端设备上行链路以及接收元数据  点击放大。*


### 接收下行链路数据

对于 LoRaWAN A 类设备通信，设备仅在每条上行链路消息后打开接收插槽。对于 
来自 TTN 控制台的设备，可以将下行链路数据包排入队列。LNS 为设备选择网关， 
并将数据包排入网关队列。设备在成功发送下一个上行链路数据包后接收下行链路数据包 
。

* 若要将 TTN 的下行链路数据包排入队列，请进入应用程序页面，然后点击您的应用程序。 
  点击注册设备选项卡，然后选择要向其发送下行链路数据包的设备。 
  。如图 14 所示，在设备页面的下行链路选项卡下，将有效负载排入下行链路队列。（图 
  14 显示 2 字节的 `0xC0DE` 有效负载，该有效负载以未确认模式排入 `FPort 2` 队列。）

  [\![](/media/2020/Figure-14.png)](/media/2020/Figure-14.png)   
  *图 14 TTN 控制台调度下行链路  点击放大。*

* 在 A 类设备操作模式下，TTN 网络服务器调度下行链路数据， 
  然后在接收到来自设备的下一个上行链路数据包时将下行链路数据发送到该设备。

  [\![](/media/2020/Figure-15.png)](/media/2020/Figure-15.png)
  *图 15 TTN 控制台调度下行链路  点击放大。*

* 如图 16 所示，终端设备在下一条上行链路之后在两个接收窗口中的一个 `FPort 2` 上接收下行链路数据 `0xC0DE` 
  ：

  [\![](/media/2020/Figure-16.png)](/media/2020/Figure-16.png)   
  *图 16 Segger IDE 显示为终端设备接收的下行链路数据  点击放大。*
