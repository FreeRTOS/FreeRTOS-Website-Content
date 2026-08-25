---
title: "精选 FreeRTOS IoT 参考集成 "
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

#### 针对 NXP i.MX RT1060 MCU 和 EdgeLock® SE050 安全元件

## 引言

这些演示展示了如何将[长期支持 (LTS)](/Community/Blogs/2021/freertos-aws-reference-integrations-now-include-freertos-202012-01-lts-libraries) FreeRTOS  内核
和库与硬件强制安全集成，以创建更安全的云连接应用程序。
项目已预配置为在
[i.MX RT1060 评估套件](https://www.nxp.com/design/development-boards/i-mx-evaluation-and-development-boards/i-mx-rt1060-evaluation-kit:MIMXRT1060-EVK)
(i.MX RT1060-EVK) 上运行，搭载
[i.MX RT1060 Arm® Cortex®-M7 MCU](https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/i-mx-rt-crossover-mcus/i-mx-rt1060-crossover-mcu-with-arm-cortex-m7-core:i.MX-RT1060)
和 [EdgeLock® SE050 开发套件](https://www.nxp.com/products/security-and-authentication/authentication/edgelock-se050-development-kit:OM-SE050X)
(OM-SE050)，用于基于硬件的信任根。


[\![](/media/2022/imxrt1060-eval-kit.png)<br />i.MX RT1060 评估套件](https://www.nxp.com/design/development-boards/i-mx-evaluation-and-development-boards/i-mx-rt1060-evaluation-kit:MIMXRT1060-EVK)
[\![](/media/2022/edgelockse050-dev-kit.png)<br />EdgeLock® SE050 开发套件](https://www.nxp.com/products/security-and-authentication/authentication/edgelock-se050-development-kit:OM-SE050X) |


## 安全功能和函数演示

### 防止未经授权的软件在设备上运行

安全启动过程旨在确保在主板上运行的固件映像由
原设备制造商 (OEM) 完成加密签名 。代码签名使用 [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem) 密钥对完成
。密钥对中的私钥（仅 OEM 知道的密钥）用于对映像进行签名。公钥被编入设备程序中，
且可用于验证映像是否由私钥签名。

演示的启动过程分为三个阶段，
如[精选 FreeRTOS 集成](01-Featured-integrations)页面中所述。

![](/media/2022/NXPimxrt1060GRI.png)
图 1：安全架构

第一级引导加载程序内置在 i.MX RT1060 的 ROM 中，无法修改。第二级引导加载程序
来自开源项目 [MCUboot](https://www.mcuboot.com/)，作为可构建项目包含在
参考集成存储库中。第三级引导加载程序则是一个基于 FreeRTOS 构建的应用程序。存储库包含
多个应用程序项目，每个项目都演示了使用 AWS IoT 服务的不同方法。

第一级引导加载程序可以验证第二级引导加载程序的数字签名，并使用来自安全存储的公钥确定其是否值得
信任。第二级引导加载程序可验证应用程序映像上的签名
。通过此种方式，它可在运行应用程序之前为其建立信任。在
“为引导加载程序创建签名密钥”和“创建签名的应用程序映像”部分
（见[《入门指南》](https://github.com/FreeRTOS/iot-reference-nxp-rt1060/blob/main/GSG)）
详细说明了生成必要密钥、在 MCUboot 中嵌入公钥以及对应用程序可执行文件进行签名的步骤。

此外，还必须保护用于验证 MCUboot 的公钥。iMX RT1060 拥有一次性可编程 (OTP) 属性的
熔丝，以启用此功能。一组 OTP 熔丝可用于实现一个非常小的存储区域，该区域只能被编程一次
。该存储区可记录启动配置，包括用于验证代码签名的公共代码签名密钥的哈希值
。启动配置最初设置为“打开”模式，允许在设备上加载和运行任何代码。
一旦启动配置熔丝被编程为“关闭”模式，则只能运行 MCUboot 的签名映像，
且无法返回到打开模式。应在所有生产设备上执行此单向转换。

该打开配置十分便于开发，因此参考集成的入门指南解释了如何
签署固件映像，但仍保持了启动配置为打开状态。


### 确保设备身份和机密信息的安全

连接到 AWS IoT 的设备由 TLS 客户端证书使用私钥进行唯一标识，以防止设备
相互冒充。设备的唯一私钥必须保密，以防止未经授权的访问和
通信。EdgeLock SE050 是主处理器之外的外围设备，
用于为客户端证书及其相关联私钥实现安全存储系统。每个 SE050 都附带唯一的客户端证书，
相关联的私钥已完成编程。请参阅上文图 1 中的“设备证书和私钥”。SE050 不
包含用于读出私钥的接口，因此只有此单一设备才能证明其拥有客户端证书。

与私钥不同，客户端证书为公开信息，可从 SE050 中提取。入门指南
介绍了如何通过串行接口读取客户端证书，您需要执行此操作
才能为您的 AWS 帐户注册评估套件的身份。

确保[传输层安全 (TLS)](https://en.wikipedia.org/wiki/Transport_Layer_Security) 协议安全
要求客户端使用其关联的私钥证明其对客户端证书的所有权
。由于私钥仅限于 SE050，因此参考集成代码提供
[PKCS #11 API](https://en.wikipedia.org/wiki/PKCS_11) 的实现，
允许在 SE050 上执行所需的加密操作，
无需直接访问密钥。


### 通过双向验证保障 TLS 通信的安全

设备与 AWS IoT Core MQTT 代理之间的通信
使用 [TLS 版本 1.2](https://en.wikipedia.org/wiki/Transport_Layer_Security#TLS_1.2) 进行加密。
请参阅 [AWS IoT 中的传输安全](https://docs.aws.amazon.com/iot/latest/developerguide/transport-security.html)，
了解详情。该演示使用 EdgeLock SE050 安全元件，该元件附带唯一的
客户端证书和已编程的关联私钥。可以在不泄露私钥的情况下
检索客户端证书，并在 AWS IoT 进行注册，以与 AWS IoT coreMQTT 代理建立 TLS 连接
（使用 [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) 库）。


### Over the air (OTA) 更新

参考集成包括 Over the Air (OTA) 更新的演示，以启用安全漏洞和故障修复的远程补丁
。此演示使用
[适用于 FreeRTOS 的 AWS IoT OTA 服务](https://docs.aws.amazon.com/freertos/latest/userguide/freertos-ota-dev.html)，
通过云端部署新映像。[AWS IoT OTA 库](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates)中的 OTA 客户端软件
在后台任务中运行，并等待从云端接收新固件映像可用的通知。收到通知后，
设备会下载新映像，然后重新启动以运行新映像。

OTA 演示使用了参考集成的两项功能来提高稳健性和安全性：主次固件映像插槽
和经签名的 OTA 映像。

MCUboot 辅助启动加载程序将闪存分为三个区域。其中一个用于引导加载器本身，
另两个分别用作主次固件映像插槽。一次只有一个固件插槽处于活动状态。当 OTA 库
下载了新的固件映像，它会将更新存储在非活动插槽中，保持活动固件不变。
如果新固件映像出错（如代码签名验证失败），MCUboot 便可以返回到旧固件
。

除安全启动系统中的代码签名验证外，OTA 服务及其客户端库还为映像下载进程
添加了自己的代码签名和验证步骤。和用于验证安全启动映像的公钥一样，
用于验证 OTA 签名的公钥必须存储在每个 IoT 设备上，并且不可作
任何更改。参考集成代码显示了将此密钥存储于 SE0050 的方法。


### 内存安全防护

“核心” FreeRTOS 库符合在案的代码质量标准，且每个代码 check-in 时均会运行内存安全防护
。


## 演示应用程序的功能

参考集成包括通过 i.MX RT1060 以太网连接器连接到 AWS IoT Core MQTT 代理的演示应用程序
。应用程序可执行通用 IoT 设备功能，包括与云端交换 MQTT 信息，以及
使用适用于 FreeRTOS 的 AWS IoT OTA 服务下载和安装新固件
映像。


## 演示入门

此项目 Git 存储库根目录中的 README 文件提供了下载源代码的说明，
GSG 文件提供了有关如何构建和运行演示的逐步说明。访问
[FreeRTOS/iot-reference-nxp-rt1060 Git 存储库](https://github.com/FreeRTOS/iot-reference-nxp-rt1060)，
即可立即体验。
