---
title: "库和第三方工具"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 内核简介
relatedLinks:
  - title: FreeRTOS 库概述
    link: /Documentation/03-Libraries/01-Library-overview/01-All-libraries/
  - title: LTS 库
    link: /Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries/

previous:
  title: 构建您的首个项目
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project/
next:
  title: FreeRTOS plus AWS 解决方案
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/05-FreeRTOS-plus-AWS-solutions/
---

## 引言

下列所有库均基于 [MIT（开源）许可](https://opensource.org/licenses/MIT)，
专为资源受限的设备（如微控制器和小型微处理器）而设计。
FreeRTOS Core 和适用于 AWS 的 FreeRTOS 库除了标准 C 库之外，
没有任何其他依赖项，它们甚至不依赖于 RTOS。

## FreeRTOS 源代码组织

共有两种类型的存储库：**单库**存储库和**软件包存储库**。
所有单库存储库均包含库的源代码，不含任何构建项目
或示例。软件包存储库包含多个库，并且可能包含
用于演示库使用方法的预配置项目。

虽然软件包存储库包含多个库，但不包含这些库的副本，
而是以
[git 子模块](https://git-scm.com/book/en/v2/Git-Tools-Submodules)的形式引用所含的库。使用子模块可确保
每个库都有唯一的事实来源。

单个库的 git 存储库在两个 GitHub 组织间拆分。含有
FreeRTOS 特定库的存储库（如 FreeRTOS-Plus-TCP）或通用库（如 coreMQTT 等
跨云库，因其适用于任何 MQTT代理）位于 
[FreeRTOSGitHub 组织中](https://www.github.com/FreeRTOS)。含有 AWS IoT 特定库的存储库
（如 AWS IoT over-the-air 更新客户端）位于
[AWSGitHub 组织中](https://github.com/AWS)。下图为该结构体的演示。

![](/media/2021/gsv-faq-image1.png)

## 主流 FreeRTOS 库

[查看所有库](/Documentation/03-Libraries/01-Library-overview/01-All-libraries)

### FreeRTOS-Plus 库

FreeRTOS-Plus 库实现了 FreeRTOS 内核的附加功能。与 FreeRTOS core 库不同，
FreeRTOS-Plus 库对 FreeRTOS RTOS 内核具有 依赖性。

[**FreeRTOS-Plus-TCP**](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)

基于套接字的轻量级线程感知 TCP/IP 堆栈
同时支持 IPv4 和 IPv6 以及多接口和多端点。

[**FreeRTOS-Plus-CLI**](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)

能使您的应用程序高效处理命令行输入。

[**FreeRTOS-Plus-IO** \[已弃用\]](/FreeRTOS-Plus/FreeRTOS_Plus_IO/FreeRTOS_Plus_IO.html)

向应用程序添加 open()、read()、write()、ioctl() 外设接口。

### FreeRTOS Core 库

实现基于开放标准的连接性、安全性和相关功能的库。这些库适用于
构建连接到云端的基于微控制器的智能设备。与 FreeRTOS-Plus 库不同（参见上文），
FreeRTOS Core 库除了标准 C 库没有其他依赖项，因此 FreeRTOS Core 库
不依赖 FreeRTOS RTOS 内核。

[**coreMQTT**](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)

适用于 IoT 用例的轻量级 [MQTT 客户端](https://mqtt.org/)实现。coreMQTT Agent
库（见下文）可创建线程安全 Agent。

[**coreMQTT Agent**](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/01-coreMQTT-agent)

用于 coreMQTT 库的线程安全 Agent（或守护进程）。coreMQTT Agent 包括 coreMQTT 库。

[**CoreHTTP**](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/01-coreHTTP)

轻量级部分 [HTTP 客户端](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol)
实现——适用于 IoT 用例。

[**coreSNTP**](/Documentation/03-Libraries/03-FreeRTOS-core/05-coreSNTP/01-coreSNTP)

coreSNTP 库提供简单网络时间协议 (SNTP) 客户端，
以便设备同步其系统时钟。

[**传输接口**](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface)

描述 Core 应用程序协议使用的网络传输独立接口， FreeRTOS
如 coreMQTT 和 coreHTTP。

[**coreJSON**](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/01-coreJSON)

轻量级部分 JSON 解析器，执行 [ECMA-404 JSON 标准](https://www.json.org/json-en.html)。

[**corePKCS #11**](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11)

[PKCS #11](https://en.wikipedia.org/wiki/PKCS_11) 是开放标准加密 API 层（OASIS 标准），
可对密钥存储、加密对象的 get/set 属性进行抽象。

[**FreeRTOS 蜂窝接口库**](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/01-Cellular-interface)

提供适用于 FreeRTOS 的 LTE [CAT M-1 蜂窝接口](https://en.wikipedia.org/wiki/LTE-M)。下载内容
中包含示例。

### 适用于 AWS IoT 的 FreeRTOS 库

为 AWS IoT 特定的增值云服务实现客户端的库，包括 over the air (OTA) 更新服务。这些
库适用于构建连接到 AWS IoT 云端的基于微控制器的智能设备。与 FreeRTOS
core 库一样，除了标准 C 库，它们不依赖于其他任何东西，因此也不依赖于 FreeRTOS
RTOS 内核。

[**AWS IoT OTA**](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates)

管理 IoT 设备固件更新的通知、下载和验证的库。

[**AWS IoT Device Shadow**](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow)

管理连接至 AWS IoT 的设备的持久虚拟表示形式的库。

[**AWS IoT Jobs**](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/01-AWS-IoT-jobs)

向连接的 IoT 设备通知任务（如 OTA 更新）的服务。

[**AWS IoT Device Defender**](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender)

监控连接设备的安全指标。

[**AWS IoT Fleet Provisioning**](/Documentation/03-Libraries/04-AWS-libraries/06-AWS-IoT-Fleet-Provisioning/01-AWS-IoT-fleet-provisioning)

预配没有设备证书的新 IoT 设备。

[**AWS 签名版本 4**](/Documentation/03-Libraries/04-AWS-libraries/07-AWS-Signature-Version-4/01-AWS-signature-version-4)

生成符合 AWS
签名版本 4 签名流程的签名和授权标头。

### FreeRTOS Lab 库

FreeRTOS Labs 项目具有实用性，但同时欠完整，或具实验性，
或仅为开放源社区提供。每个 Labs 库的文档页面上的横幅
描述了适用于该库的标准。

[**LoRaWAN**](/Documentation/03-Libraries/05-FreeRTOS-labs/02-LoRaWAN/01-LoRaWAN-library)

包含可构建项目和文档文章，演示如何在
FreeRTOS 上使用 [LoRaWAN](https://lora-alliance.org/about-lorawan/)。

[**FreeRTOS-Plus-POSIX**](/Documentation/03-Libraries/05-FreeRTOS-labs/03-FreeRTOS-plus-POSIX/00-FreeRTOS-Plus-POSIX)
FreeRTOS 内核原生 API 的 POSIX 线程包装器。实现了
[POSIX 线程 API](https://en.wikipedia.org/wiki/POSIX_Threads) 的子集。

[**FreeRTOS-Plus-FAT**](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/01-FreeRTOS-plus-FAT)

线程感知 FAT 文件系统---具有可选的长文件名、缓存
和目录名称哈希等特性。

[**FreeRTOS MCUBoot**](/Documentation/03-Libraries/05-FreeRTOS-labs/05-FreeRTOS-MCUBoot)

MCUBoot 是可配置的安全引导加载程序，
由多个行业领导者维护，支持软件映像的加密验证
。

[**Delta Over-the-Air 更新**](/Community/Blogs/2022/delta-over-the-air-updates)
Delta Over-the-Air 更新可以降低 OTA 的大小，
方法是仅发送二进制差异。

## FreeRTOS 合作伙伴关系

FreeRTOS 具有一个丰富且不断发展的生态系统，
其中含有附加和补充产品，如跟踪工具、预集成软件包、
库和商用 RTOS 产品，
为您提供额外价值。

### 半导体

FreeRTOS 与半导体制造商合作，
共同为特定微控制器和微处理器
提供参考实现。参考实现通常
在半导体合作伙伴的工具链中提供。
[了解更多](/Partners/Semiconductor)

### 培训和咨询

FreeRTOS 与培训公司合作，
帮助您使用 FreeRTOS 的产品团队和个人以快速、有条理的方式加速 FreeRTOS 开发
。

FreeRTOS 与咨询公司合作，
帮助您的嵌入式开发人员朝着正确的方向快速启动，
甚至可以提供基于 FreeRTOS 的整个产品。
[了解更多](/Partners/Training)

### 软件

FreeRTOS 与独立软件供应商 (ISV) 合作，
提供整个软件库，
使您的项目和整个 FreeRTOS 许可或业界测试的打包发行版能够实现交钥匙功能
。
[了解更多](/Partners/Software#partners)

### 安全认证和商业许可

作为 FreeRTOS 的战略合作伙伴，WITTENSTEIN high integrity systems
提供安全认证和商业许可版本的 FreeRTOS
库。
[了解更多](/Partners/Software#safety-critical)
