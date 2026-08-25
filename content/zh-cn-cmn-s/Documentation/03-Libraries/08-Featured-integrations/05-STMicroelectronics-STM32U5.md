---
title: "精选 FreeRTOS IoT 集成 "
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

#### 针对 STM32U5 Arm Cortex-M33 MCU

*这种精选参考集成为您提供了极大的灵活性，使您可以调整其功能并利用
您的硬件功能。或者，为了简单起见，也可以考虑 
[ExpressLink 精选集成](06-STM32-Expresslink)。*


## 引言

此演示展示了如何将模块化 FreeRTOS 软件与硬件强制的安全集成，
帮助创建更安全的云连接应用程序。这些项目
预配置为在 [B-U585-IOT02A](https://www.st.com/en/evaluation-tools/b-u585i-iot02a.html)
IoT discovery 开发套件上运行，此套件包含 [STM32U5](https://www.st.com/en/microcontrollers-microprocessors/stm32u5-series.html)
微控制器 (MCU)。

STM32U5 是一款 Arm® Cortex®-M33 MCU，
采用 [Arm TrustZone 技术](https://www.arm.com/technologies/trustzone-for-cortex-m)，
利用 CPU 内置的硬件强制隔离来保护关键的安全代码和数据。有两个项目，
一个未启用 TrustZone，另一个已启用 TrustZone。MCU 还提供内置安全功能，本演示中使用了其中一些功能，
例如安全启动、安全存储和
[真随机数生成器](https://en.wikipedia.org/wiki/Hardware_random_number_generator) (TRNG)。STM32U5
已获得 [PSA 3 级](https://www.psacertified.org/getting-certified/silicon-vendor/overview/level-3/)
和 [SESIP 3 级](https://www.trustcb.com/iot/sesip/)独立认证。

[\![B-U585-IOT02A 开发套件](/media/2022/b-u585-iot02a.jpeg) B-U585-IOT02A discovery kit](https://www.st.com/en/evaluation-tools/b-u585i-iot02a.html)


## 安全功能和函数演示

### 通过隔离关键的安全固件和数据来降低攻击的可能性

从正常的应用程序固件和数据中隔离安全关键组件有助于
降低[攻击的可能性](https://developer.arm.com/documentation/100690/0201/Security-of-TrustZone-technology-for-Armv8M-against-different-attack-scenarios)。
启用 TrustZone 的项目
利用 [ARM 可信固件 M](https://www.trustedfirmware.org/projects/tf-m/) (TF-M)，
采用 [Arm TrustZone 技术](https://developer.arm.com/documentation/100690/0201/Arm-TrustZone-technology)，
并隔离非安全处理环境 (NSPE) 中运行的代码
与安全处理环境 (SPE) 中运行的代码。

在启用 TrustZone 的项目中，安全环境中运行以下服务，这些服务对系统安全至关重要，
详见[精选 FreeRTOS 集成](01-Featured-integrations)页面：

* 安全启动
* 私钥和秘密存储
* 加密操作（如密钥生成和签名）

其余应用程序、FreeRTOS 内核以及其他任务，如 OTA 和 MQTT 代理
在非安全环境中运行。OTA 库与安全的 TF-M 固件更新
API 互动，以安装新映像。

STM32CubeIDE 为 TrustZone 项目提供构建支持，该项目生成两个独立的
安全的和非安全的二进制文件，两个文件通过独立密钥分别签名和验证。


### 确保设备身份和机密信息的安全

确保[传输层安全 (TLS)](https://en.wikipedia.org/wiki/Transport_Layer_Security) 通信安全
通信要求发送器和接收器
通过确定其身份进行认证。设备的唯一私钥及其对应的
客户端证书用于识别和认证设备。私钥必须予以
保密，防止未经授权的访问和通信。

设备 [ECDSA](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm) 公钥/私钥
对是使用内置的符合 [NIST SP 800-90B](https://en.wikipedia.org/wiki/NIST_SP_800-90B) 的
TRNG 生成的，以确保唯一性。密钥对用于生成 TLS 客户端证书。密钥对和
证书存储在 TF-M 内的内部可信存储中，私钥创建时随附了一个标志，
可阻止将其从 SPE 导出。私钥生成和验证操作是通过调用
[ARM PSA 加密 API ](https://armmbed.github.io/mbed-crypto/html/)执行的，
允许对存储在安全存储中的密钥执行加密操作，且与在非安全环境中运行的应用程序隔离。


### 通过双向验证保障 TLS 通信的安全

设备与 AWS IoT Core MQTT 代理之间的通信
使用 [TLS 版本 1.2](https://en.wikipedia.org/wiki/Transport_Layer_Security#TLS_1.2) 进行加密。
请参阅 [AWS IoT 中的传输安全](https://docs.aws.amazon.com/iot/latest/developerguide/transport-security.html)，
了解详情。[ARM PSA 加密 API](https://armmbed.github.io/mbed-crypto/html/) 允许 TLS 代码在 NSPE 中运行，
而无需直接访问 TLS 客户端证书的相关私钥。


### 确保 over-the-air 更新 (OTA) 的安全

STM32U5 平台具有双库闪存，总容量为 2 兆字节。可用闪存
内存分为两个库，每个大小为 1 MB ，其中一个库用于当前固件
映像，第二库用于为新的固件映像分段。内存的每个库
进一步分割成安全区和非安全区，带有独立的读写
保护闪存区域，用于安全端存取。

启用 TrustZone 的项目的固件更新通过将 FreeRTOS OTA
库与 [PSA 可信固件更新 API](https://developer.arm.com/documentation/ihi0093/0000)
作为 PAL 集成来实现。安全和非安全可执行文件会分别进行更新。防回滚保护和信任根验证
验证在不可更改（不可变）的 BL2 引导程序中完成。

安全映像分区和非安全映像分区各分为主要和次要
插槽。新映像最初被下载、验证并分段到次要插槽中
。在新映像安装后的下一次重置时，引导加载程序将
交换主要插槽中运行的当前映像与次要插槽中新映像。交换时
一次复制几个块，同时使用草稿区作为临时缓冲区。交换完成且
签名验证成功后，新映像启动并执行健全性测试
。这些测试包括成功连接到 AWS IoT 和防回滚保护
的版本升级验证。如果测试成功，新映像将得到确认，而
次要插槽中的旧映像被擦除，以防止回滚。如果测试失败，引导加载程序将回滚到
就映像，让系统返回已知的良好状态。


### 防回滚保护

防回滚保护可防止设备降级到
由于安全问题已被弃用的软件旧版本。防回滚保护
通过 MCUboot 和
TF-M [安全计数器](https://tf-m-user-guide.trustedfirmware.org/design_docs/booting/tfm_secure_boot.html)
实现来完成。

对于每个安全区和非安全区，更新必须具有安全计数器值，
这个值大于或等于相关区域的当前安全计数器值。
在固件更新期间，如果一个映像的安全计数器值低于当前映像的
安全计数器值，会导致更新被拒，此时引导加载程序将恢复
该区域的前一个映像。固件成功更新后，安全计数器值
递增。


### 内存安全证明

“核心” FreeRTOS 库符合记录的代码质量标准，包括
在每个代码签入时运行的内存安全证明。


## 演示入门

演示使用 Wi-Fi 连接到 AWS IoT，然后使用 [coreMQTT-Agent](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) 库
发布开发板上可用的环境和运动传感器数据。这些库
展示了如何将 [OTA](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates) 服务用于 FreeRTOS、[Device Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow)
和 [Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) AWS
IoT 服务。源代码示例、功能列表以及演构建和运行操作说明请参见
[FreeRTOS/iot-reference-stm32u5 GitHub 存储库](https://github.com/FreeRTOS/iot-reference-stm32u5)。
