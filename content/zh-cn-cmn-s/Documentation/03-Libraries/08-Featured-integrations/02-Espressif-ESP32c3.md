---
title: "精选 FreeRTOS IoT 集成 "
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

#### 针对使用数字签名外设的 Espressif ESP32-C3 RISC-V MCU

*您可以利用此精选参考集成灵活调整其功能，同时利用您的硬件功能。
或者，为了简单起见，也可以考虑 
[ExpressLink 精选集成](06-STM32-Expresslink)。*


## 引言

本页记录的演示项目演示了如何集成模块化 FreeRTOS 软件
和硬件强制安全，帮助创建更安全的云连接应用程序。该项目已预配置为在
[ESP32-C3-DevKitM-1](https://www.espressif.com/en/products/devkits) IoT 开发板上运行，其中包括
一个 [ESP32-C3](https://www.espressif.com/en/products/socs/esp32-c3) 微控制器 (MCU)。


ESP32-C3 是一款单核 [RISC-V](https://en.wikipedia.org/wiki/RISC-V) MCU，具有 Wi-Fi 和蓝牙
5 (LE) 连接功能，还配备
[数字签名 (DS)](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/api-reference/peripherals/ds.html)
外设和[HMAC](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/api-reference/peripherals/hmac.html)
（基于哈希的消息验证码）外设，以增强设备身份安全。


ESP32-C3 上的 [Secure Boot](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/security/secure-boot-v2.html)
有助于确保只在设备上运行受信任的软件，
而且[闪存加密](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/security/flash-encryption.html)
可将 ESP32-C3 片外闪存内容转换为秘密形式（加密）来保护信息，
如果没有正确转换成原始结构（解密），
就无法理解其内容。

[\![](/media/2022/ESP32-C3-DevKitM-1.png) ESP32-C3-DevKitM-1](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/hw-reference/esp32c3/user-guide-devkitm-1.html)


## 已证明的安全最佳实践

### 防止未经授权的软件在设备上运行

确保设备仅使用原始设备制造商 (OEM) 信任的软件启动，
有助于确保设备的安全。Secure Boot 阻止设备运行任何未经授权（如未签名）的代码；
它会检查每个正在启动的软件是否受 OEM 信任。此演示使用
Espressif 的 [Secure Boot V2](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/security/secure-boot-v2.html)。
ESP32-C3 的 Secure Boot 包含一级引导程序（存储在不可更改的 ROM 中）和二级引导程序
。一级引导程序加载二级引导程序，而二级引导程序又加载应用程序二进制文件。
二级引导程序和应用程序二进制文件通过 [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem) 私钥
来签名。使用该私钥对引导程序映像签名可确保映像
在签名后不被篡改，因为如果遭到篡改，则将无法使用对应的公钥完成
签名验证。


该 RSA 私钥必须保密，因为恶意行为者如果获取秘钥，可以使用密钥提供
未经授权的二进制文件。RSA 私钥在 OEM 场所（可以是
安全构建机器或远程签名服务器）的设备外部生成并存储，并且永远不会被设备访问。对应的
公钥存储在附加到引导程序和应用程序映像上的签名块中。公钥的
哈希值存储在 [eFuse](https://en.wikipedia.org/wiki/EFuse)。

eFuse 只能编程一次，并提供以不可更改的方式存储信息的方法。ESP32-C3 具有
许多 eFuse 块，OEM 可以使用这些块存储系统和安全参数。每个签名块
除了包含公钥之外，还包含相应映像的签名。eFuse 中的公钥哈希值
用于验证映像签名块中的公钥是否有效。

Secure Boot 包含以下步骤：

1. 一级引导程序加载二级引导程序时，会验证二级引导程序的签名
   块和映像。映像验证包括将二级引导程序签名块中
   所嵌入公钥的哈希值与 eFuse 中所存储公钥的哈希值进行比较，以及使用公钥
   对引导程序映像的签名进行验证。如果验证成功，则执行二级引导程序。
1. 二级引导程序加载应用程序映像时，会同样按上述方式验证应用程序的签名
   块和映像。如果验证成功，则执行应用程序映像
   。请参阅
   ESP-IDF [Secure Boot V2 编程指南](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/security/secure-boot-v2.html)，
   了解更多详情。


### 确保设备身份和机密信息的安全

确保[传输层安全 (TLS)](https://en.wikipedia.org/wiki/Transport_Layer_Security) 通信安全要求
发送者和接收者通过建立标识来验证身份。设备的唯一私钥及其对应的
客户端证书用于识别和验证设备。该私钥必须保密，以防止未经授权的
访问和通信。ESP32-C3 之所以能够在安全 TLS 通信期间保护设备的身份，
是因为
[数字签名 (DS) 外设](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/api-reference/peripherals/ds.html)
允许在 TLS 连接中采用唯一的 [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem) 私钥，
同时对其进行保密，不让 DS 外设以外的软件访问。

为防止暴露，TLS 连接中使用的私钥
经过 [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) 加密并存储在闪存中，
并且只能由 DS 外设（即只能由硬件）读取。DS 外设利用
[基于哈希的消息验证码](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/api-reference/peripherals/hmac.html) (HMAC)
模块和 [eFuse](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/efuse.html)
生成加密私钥所需的密钥。HMAC 用于密钥派生，并反过来
利用选定的 eFuse 块作为输入密钥。eFuse 中的密钥是随机生成的 256 位
数值（在 OEM 的主机系统上生成），
[配置 DS 外设](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/api-reference/peripherals/ds.html#configure-the-ds-peripheral-for-a-tls-connection)操作期间由 OEM 刻录到选定的
eFuse 块中。请参阅
ESP-IDF [DS 外设编程指南](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/api-reference/peripherals/ds.html)
以及 [DS 技术参考手册](https://www.espressif.com/sites/default/files/documentation/esp32s2_technical_reference_manual_en.pdf#digsig)，
了解 DS 外设工作原理的详细描述。


### 通过双向验证保障 TLS 通信的安全

设备与 AWS IoT Core MQTT 代理之间的通信
使用 [TLS 版本 1.2](https://en.wikipedia.org/wiki/Transport_Layer_Security#TLS_1.2) 进行加密。
请参阅 [AWS 传输安全IoT](https://docs.aws.amazon.com/iot/latest/developerguide/transport-security.html)，了解详情。
该演示使用在 ESP32-C3 SoC 中集成的 DS 外设、加密闪存、HMAC 模块和 eFuse 来存储
和使用 [X.509](https://en.wikipedia.org/wiki/X.509) TLS 客户端证书及相关的 RSA 私钥。这些
用于使用 [coreMQTT/Documentation/03-Libraries/02-FreeRTOS-core/02-coreMQTT/00-coreMQTT) 库与 AWS IoT Core MQTT 代理建立 TLS 连接。


### 保障 over-the-air (OTA) 更新安全

为了能够远程修复安全漏洞和程序故障，该演示包括 Over the Air (OTA) 更新。该更新使用
适用于 FreeRTOS 的 [AWS IoT OTA 服务](https://docs.aws.amazon.com/freertos/latest/userguide/freertos-ota-dev.html)，服务中
包括 [AWS IoT 代码签名](https://docs.aws.amazon.com/signer/latest/developerguide/Welcome.html)。在
OTA 更新之前，必须使用私钥对固件映像进行数字签名，以确保更新来自可靠来源并且
未被篡改。私钥在 OTA 设置过程中生成并存储在
[AWS 证书管理器](https://aws.amazon.com/certificate-manager/) 中，只有 OEM 可以访问。
对应的公钥证书用于验证签名的映像，嵌入
在设备上运行的应用程序二进制文件中，因此无法更改。

ESP32-C3 上的 OTA 客户端软件使用 [AWS IoT OTA 库](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates)。收到
待处理的 OTA 更新通知时，设备会将新映像下载到 ESP32-C3 的辅助 OTA 闪存分区中。OTA 客户端
随后使用公钥证书对整个映像进行代码签名验证以确认作者，
并保证代码在签名后没有被篡改或
损坏。请参阅
ESP-IDF 的 [OTA 编程指南](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/ota.html)，
了解更多详情。


## 此演示使用的库

此演示使用：

* [ESP-IDF FreeRTOS 内核](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/freertos.html)，
  这是 Espressif 的  [FreeRTOS 内核](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel) 移植。
* [coreMQTT Agent](/Documentation/03-Libraries/02-FreeRTOS-core/03-coreMQTT-agent/01-coreMQTT-agent)，其中包括 [coreMQTT](/Documentation/03-Libraries/02-FreeRTOS-core/02-coreMQTT/00-coreMQTT)（具有
  [backOffAlgorithm](https://github.com/FreeRTOS/backoffAlgorithm)）。
* [coreJSON](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/01-coreJSON)
* [AWS IoT Over the Air (OTA)](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates)

“核心”库和“适用于 AWS 的 FreeRTOS”库符合 [LTS](/Community/Blogs/2021/freertos-aws-reference-integrations-now-include-freertos-202012-01-lts-libraries) 代码质量标准，
其中包括内存安全证明。


## 演示入门

访问 [FreeRTOS/iot-reference-esp32c3](https://github.com/FreeRTOS/iot-reference-esp32c3) GitHub 存储库，
立即体验。源代码示例、功能列表以及有关如何构建和运行演示的说明
都可以在存储库中找到。
