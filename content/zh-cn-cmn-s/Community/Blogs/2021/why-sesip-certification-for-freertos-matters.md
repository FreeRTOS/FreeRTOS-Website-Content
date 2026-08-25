---
title: 为什么 SESIP™ 认证对 FreeRTOS 至关重要
date: null
feature: blog
categories:
- 长期支持
authors:
- elberger
relatedLinks:
- title: FreeRTOS 简介
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Richard Elberger](../author/elberger) 发表于 2021 年 3 月 1 日

FreeRTOS 现已通过[认证](https://trustcb.com/iot/sesip/sesip-certificates/)， 
满足 [IoT 平台安全评估标准](https://globalplatform.org/specs-library/security-evaluation-standard-for-iot-platforms-sesip-v1-0-gp_fst_070/) 
(SESIP™) 保证级别 2 的要求。[FreeRTOS](../../index) 软件在大多数情况下 
可在嵌入式系统处理器上运行。开发者在构建 FreeRTOS 应用程序的同时加入 
合作 18 年以上且不断壮大的社区，这一现象前所未有。虽然 
FreeRTOS 的主要软件是[实时操作系统内核](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel)，但 FreeRTOS 提供了基础 
库，例如 [FreeRTOS-Plus-TCP](../../FreeRTOS-Plus/FreeRTOS_Plus_TCP/index)，这是一个强大、 
安全且不断完善的 TCP 库。FreeRTOS 还提供 IoT 应用程序协议库， 
如 [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)，帮助开发者自信且安全地连接到云端。 
FreeRTOS 是开源项目，随着社区的参与不断完善， 
逐渐成为构建嵌入式系统和解决方案的开发者的最佳选择。

在所有 FreeRTOS 项目中，安全是首要任务。FreeRTOS 
不断[通过各种内存安全证明](/Community/Blogs/2020/ensuring-the-memory-safety-of-freertos-part-1)提高覆盖率。 
如今，FreeRTOS 展现出充分的安全性，已经通过 
[IoT 平台安全评估标准 (SESIP™)](https://trustcb.com/iot/sesip/) 认证。 
SESIP™ 的基本宗旨源于 
业界通行的[通用标准](https://en.wikipedia.org/wiki/Common_Criteria) 框架。  通用标准 
是计算机安全认证的国际标准 (ISO/IEC 15408)。FreeRTOS 
已通过强大且严苛的社区的严格审查。SESIP™ 认证展示了 
我们对所有 FreeRTOS 应用程序开发者的安全性承诺（无论他们是否真的需要自行证明网络安全合规性）， 
同时帮助那些确实需要证明网络安全合规性的开发者， 
让他们的产品更快实现网络安全合规性。客户可以快速识别符合严格标准的 SESIP™ 认证 
应用程序。

用于认证测试的 [FreeRTOS 的 SESIP™ 项目](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-SESIP) 配置了 
[FreeRTOS 202012.00 LTS 库](https://github.com/FreeRTOS/FreeRTOS-LTS/tree/202012.00-LTS)， 
由 FreeRTOS 在 GitHub 上维护。本博客中的一些主题 
假设您已对特定 FreeRTOS 内核功能或库有所了解。如果对这些特定功能有任何疑问，请随时 
通过 [FreeRTOS 论坛](https://forums.freertos.org/) 与社区互动 
。

本博客列出了在认证过程中评估的 FreeRTOS 内核和相关 FreeRTOS 库的 
关键领域。第一部分介绍认证测试的假设条件。接下来的三个部分 
介绍主要测试领域。第五部分介绍希望获得 SESIP™ 认证的产品开发者 
可以享受的优势。


## 关于 FreeRTOS 内核和相关库的 SESIP™ 认证

SESIP™ 认证有五个保证级别，从 0 到 5。随着保证级别的提高， 
测试也更加复杂和严格。[GlobalPlatform™](https://globalplatform.org/sesip/) 
负责管理 [SESIP™ 的五个保证级别](https://trustcb.com/iot/sesip/)，而测试合作伙伴则负责执行 
测试。TrustCB™ 可为所有五个 SESIP™ 认证级别提供认证服务。FreeRTOS 
接受了 SESIP™ 2 级测试，其中包括为期两周的黑盒渗透测试 
。[Riscure](https://www.riscure.com/) 是一家经验丰富的安全测试实验室，能够执行 
SESIP™ 2 级所要求的独立测试。[TrustCB™](https://trustcb.com/) 会在确认测试结果后 
颁发证书。认证过程中会对以下方面进行测试和验证：平台身份和实例 
身份、over-the-air 固件更新、安全通信、隔离功能以及加密 
操作，测试针对的是评估目标 (TOE)，即接受测试的软件主体，包括 FreeRTOS 
内核和相关 IoT 库。 


## 环境假设

在对 FreeRTOS 
进行 SESIP™ 认证测试时，为了缩小测试参数的范围，需要做出一些环境假设。

第一项假设是平台仅部署在 
无需抵御物理攻击的环境中。TOE 必须具有内存保护单元 (MPU) 作为底层硬件。第二项假设是 
测试不会向 TOE 添加任何恶意代码。实际上，开发团队需要是可信的，必须实施 
开发团队规则，约束对 FreeRTOS 源代码的修改。最后一项假设 
是 Over-the-Air 固件更新 (FOTA) 功能 
使用 [AWS IoT OTA 更新管理器](https://docs.aws.amazon.com/freertos/latest/userguide/ota-manager.html)。 
FOTA 功能依靠集中式系统来传递命令和固件有效负载。集中式 
系统不在测试范围内，连接到集中式系统的设备才是测试对象。

基于以上假设，我们来看一下测试的前三大领域。


### 身份验证

规范指出，“用户只有 
在能够获得产品部件（应用程序和连接平台）的身份标识时，才能验证其拥有产品的安全性。” 源代码和配置管理是 
实现身份识别的常见机制。FreeRTOS 负责维护 FreeRTOS 
内核和相关库（在 [GitHub](https://github.com/FreeRTOS/FreeRTOS) 上）。Github 是 
使用 [Git 源代码控制系统](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control) 的在线系统。 
经过身份验证且获得授权的用户可对源代码控制系统进行修改。源代码控制 
系统会跟踪每次原子[提交](https://git-scm.com/docs/git-commit)， 
生成详尽的存储库[提交历史记录](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)。 
开发者通常将软件组件组织到各个存储库中，以便于管理和 
组合。同样，FreeRTOS 内核和每个库都是一个软件组件，并且拥有自己的 
存储库。

虽然构成软件组件的每个文件都有版本，但配置管理器 
会应用 git 源代码存储库[标签](https://git-scm.com/book/en/v2/Git-Basics-Tagging) 来简化 
特定时间点的连续源代码集所表示的内容。FreeRTOS 
为每个软件组件（由各个存储库表示）维护一份清单文件，该文件描述了 
FreeRTOS 内核和库的连续集合。FreeRTOS 将清单视为 
[长期支持 (LTS)](https://github.com/FreeRTOS/FreeRTOS-LTS/blob/202012-LTS/manifest.yml) 
和[非 LTS](https://github.com/FreeRTOS/FreeRTOS/blob/master/manifest.yml) 版本的身份验证工件。FreeRTOS 202012.00 
LTS 版本用于 TOE。

认证测试评估了源代码实践，发现实施者 
可以通过 LTS 清单文件验证其产品中包含的软件版本。应用程序开发团队 
必须在实施者值得信赖且不会修改 SESIP™ 
认证的 FreeRTOS 源代码的环境条件下进行操作。不妨考虑使 FreeRTOS 源代码不可变，因为修改 
源代码会使认证失效。

连接平台的身份验证涉及设备操作期间的运行时身份识别 
。这意味着开发者和操作人员可以通过标准 API 或结构体对运行时设备 
进行唯一标识。在本测试中，负责提供运行时身份 API 的库是 coreMQTT。 
具体而言，开发者根据应用程序需求初始化 
[MQTTConnectInfo](https://github.com/FreeRTOS/coreMQTT/blob/v1.1.0/source/include/core_mqtt_serializer.h#L133) 
结构体。IoT 设备连接到 MQTT 代理时，  
客户端 ID 必须具有唯一性，这是 
由 [MQTT v3.1.1 规范第 3.1 节第 3 段](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.pdf) 定义的行为。 
开发者必须实现一种机制，为每台设备唯一地初始化结构体 
成员 https://github.com/FreeRTOS/coreMQTT/blob/v1.1.0/source/include/core_mqtt_serializer.h#L148pClientIdentifier[]()， 
但是 coreMQTT 库提供了统一的 API 来确定运行时身份。


### 系统更新

借助 Over-the-Air 更新，无需召回设备或无需技术人员上门服务即可更新设备固件，从而降低成本 
。OTA 方法可快速解决在设备部署到现场后发现的安全漏洞和软件错误 
。更新内容会经过验证，以确保来自可信源， 
同时还会进行其他验证，如版本和兼容性检查。借助 FreeRTOS over-the-air (OTA) 客户端库， 
应用程序开发者能够管理最近可用更新的通知、下载更新 
并对固件更新执行加密验证。我们已讨论过如何验证 OTA 模型， 
详见之前一篇 
名为《[使用形式化方法验证 OTA 协议](/Community/Blogs/2020/using-formal-methods-to-validate-ota-protocol)》的博客。

OTA 的一个关键方面是采用集中式服务，在服务器端提供 
OTA 处理所需的安全和作业管理机制。不同的集中式服务可能会以不同的方式 
实现该功能。本博客前文提到了环境假设，即 AWS，更具体地说是 
OTA 更新管理器服务，可用作集中式服务。我们使用了 
[AWS IoT Over-the-air 更新库](https://github.com/aws/ota-for-aws-iot-embedded-sdk) 
（在实现 OTA 的设备端应用程序时），该库可与 OTA 更新管理器 
服务无缝集成。  


### 软件隔离

如果攻击者修改内存，则可能 
会在应用程序运行时对所有正在运行的任务产生负面影响，而软件隔离有助于防止这种情况的发生。软件隔离包含两个层面：硬件层面和 
软件层面。要进行软件隔离，硬件层面需要具有内存管理单元 (MMU) 或内存保护 
单元 (MPU)。软件层面，FreeRTOS 内核必须为具备上述硬件功能的架构提供移植版本， 
然后实现与 MMU 和 MPU 协同工作的功能。

在认证过程中，FreeRTOS 团队使用了 
[LPC54018 IoT 模块](https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/general-purpose-mcus/lpc54000-cortex-m4-/lpc54018-iot-module-for-the-lpc540xx-family-of-mcus:OM40007) 
（来自 [NXP™](https://www.nxp.com/)），该模块具有 MPU，因此符合硬件要求。满足 
软件隔离的要求并不困难，因为 FreeRTOS 已在针对 Cortex™-M 架构的移植中实现这项功能 
。隔离发生在 FreeRTOS 任务级别 ， 
因此实现者必须了解两种不同的 API。如需详细了解此主题， 
请参阅 [Gaurav Aggarwal 的博客](/Community/Blogs/2020/using-freertos-on-armv8-m-microcontrollers#FREERTOS_WITH_MPU) 中 
与 ARMv8-M 功能相关的内容。 


## 希望获得 SESIP™ 认证的人士可以享受的额外优势

对于希望自己的应用程序获得认证的开发者来说，SESIP™ 认证的一个强大优势在于 
该认证建立在软件和硬件依赖关系已经获得的 SESIP™ 认证的基础之上 
。这称为组合认证，是构建安全可信产品的 
强大工具。对于 IoT 设备来说，随着应用程序日益复杂， 
尤其是在使用软硬件堆栈以实现跨网络安全通信时，这种认证显得尤为重要。图 1 显示了 
应用程序进行认证时的理想情况。

![](/media/2021/blog_sesip_ideal.png)   
*图 1. 理想情况下，应用程序的所有底层组件（绿色部分）都能获得与应用程序所需级别
相同或更高级别的 SESIP™ 认证。*

应用程序进行 SESIP™ 认证时，理想情况是开发者将 TOE 集中在 
其能够直接控制的代码或硬件上。如果开发者选择 
未经过 SESIP™ 认证的软硬件，测试机构（例如 Riscure）需要 
对整个软硬件堆栈进行测试。例如，图 2 显示了 
因 FreeRTOS 内核修改而导致需要重新认证的情况。

![](/media/2021/blog_sesip_mod.png)   
*图 2. 应用程序开发团队修改 FreeRTOS 内核而致使认证失效的情况。*


### 下一步工作

我们简要介绍了如何获得 SESIP™ 2 级认证。下一步， 
建议深入研究在此认证过程中发挥作用的 API。OTA 
可为大规模部署 IoT 设备的所有人员提供出色的功能。确保运行时代码 
在内存中得到保护也同样重要。切记 LTS 和非 LTS 的清单描述了 
表示 FreeRTOS 及其库软件身份的连续软件集。如果 
希望新产品（基于已经获得 SESIP™ 认证的 FreeRTOS 构建）获得 SESIP™ 认证，请查看 
[GlobalPlatform™ 网站上的要求](https://globalplatform.org/sesip/)。接下来，根据清单文件开始使用 
FreeRTOS 及其库，以确保在今后的开发工作中 
享受认证带来的好处并持续符合相关要求。

祝您生活愉快，编程愉快！


## 作者简介

![](https://secure.gravatar.com/avatar/df55a46d5a2ea6b956a43b968ff57d3d?s=200&d=mm&r=g)   
Richard Elberger 是 Amazon Web Services 的首席 IoT 技术专家。他经常发表各种演讲，定期撰写文章， 
对嵌入式技术有着浓厚的兴趣和不懈的追求。他积极创作内容并建立社群，为全球 IoT 和 
云领域的从业人员提供交流和学习的平台。Richard 致力于维护并改进多个与 IoT 相关的开源 
项目（FreeRTOS、meta-aws、ThingPress），帮助客户构建并交付出色的 IoT 解决方案 
（在 AWS 上）。  
[查看此作者的文章](../author/elberger) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

