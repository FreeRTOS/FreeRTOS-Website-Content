---
title: 通过 FreeRTOS 为 Cortex-M 设备提供安全的 OTA 更新
created: 2021-07-14 00:00:00.0 UTC
feature: blog
categories:
- 长期支持
authors:
- arm-author
relatedLinks:
- title: FreeRTOS 简介
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Shebu Varghese Kuriakose](../author/arm-author) 发表于 2021 年 7 月 14 日

IoT 设备在各细分市场得到快速采用，正成为网络攻击的主要目标。 
大量针对 IoT 设备的攻击是 
因设备部署后缺乏软件更新或更新过程不安全所致。网络攻击者经常利用过时软件组件中的漏洞 
来控制设备。软件更新有助于及时修复新发现的漏洞， 
从而有效应对持续不断的威胁。

手动更新软件通常难以扩展，不适用于 IoT 设备群，因为它们可能需要频繁更新， 
并且用户难以直接接触到设备。Over-the-Air (OTA) 更新通常用于 
更新 IoT 设备。使用蜂窝或互联网连接无线部署更新，即可远程完成 OTA 更新 
。凭借此方法，无需直接接触设备，并且可以大规模集中管理 
对数百万台设备的更新。

IoT 设备支持安全 OTA 更新的一个主要障碍在于， 
将 OTA 应用程序集成到 IoT 生态系统的过程过于复杂。这是由于硬件平台种类繁多， 
其存储、更新和映像身份验证机制各不相同。PSA 认证框架旨在 
简化 IoT 开发者在安全方面的工作，使其更容易实现目标。PSA 认证定义了 10 项安全目标，其中一项 
就是安全更新。PSA 认证框架中的 PSA 固件更新规范 
有助于实现这一目标。

本博文探讨了 FreeRTOS 设备如何利用 PSA 固件更新规范在 Cortex-M 设备上无缝启用安全 OTA 更新 
。本博文首先介绍了 PSA 固件更新规范， 
然后介绍了参考实现 Trusted Firmware-M 如何与 Cortex-M 设备上现有的 FreeRTOS 
OTA 代理集成以执行安全 OTA 更新。目前已在 Arm v8-M 参考平台 MuscaB1e 上 
完成一个示例实现。


## PSA 固件更新 - 标准更新接口

PSA 固件更新[规范](https://developer.arm.com/documentation/ihi0093/0000) 定义了 
一组标准的固件更新接口，可供更新应用程序和云连接器客户端 
使用。这些接口不仅可提供足够的灵活性，在各式各样的 IoT SoC 架构 
和不同的信任模型上高效实现，还独立于 
与设备通信所使用的协议以及向设备传递更新的媒介。

以下为定义的一组接口。

| PSA FWU API | 功能 |
| --- | --- |
| psa_fwu_query () | 查询映像信息，如已安装、已拒绝和候选映像的状态 |
| psa_fwu_write () | 将候选映像写入其暂存区 |
| psa_fwu_install () | 开始安装映像 |
| psa_fwu_request_reboot () | 触发平台重启以应用经过身份验证的新映像 |
| psa_fwu_request_rollback () | 回滚最近应用的更新 |
| psa_fwu_accept () | 指示最近应用的更新是否正常运行。 |

更新应用程序可以调用这些接口来查询当前映像的状态，存储、验证 
并最终安装新映像。

Trusted Firmware-M (TF-M) 是 Cortex-M 设备的 PSA 认证参考实现，实现了 
这些接口。如此一来，更新应用程序就可以在启用 TF-M 的 Cortex-M 设备上 
使用这些接口。 


## Trusted Firmware-M 和安全启动

Trusted Firmware-M (TF-M) 为基于 Armv8-M 架构的处理器 
（例如 Cortex-M55、Cortex-M33 和 Cortex-M23 处理器）和双核 Cortex-M 设备 
实现了安全处理环境 (SPE)。TF-M 提供符合 PSA 认证指南的参考实现，可加快 [PSA 认证](http://psacertified.org/) 设备的 
开发速度，已在多个 
Cortex-M [平台](https://ci-builds.trustedfirmware.org/static-files/vUfxJmnEhNuLhSAYNUVk46JxWug8yDk5bJz0Clfj2rsxNjE5MTc1MjA3NTMxOjk6YW5vbnltb3VzOmpvYi90Zi1tLWJ1aWxkLWRvY3MtbmlnaHRseS9sYXN0U3RhYmxlQnVpbGQvYXJ0aWZhY3Q=/trusted-firmware-m/build/docs/user_guide/html/platform/ext/index.html) 
（例如 NXP LPC55S69、ST STM32L5、Infineon PSoC64、Nordic nrf5340、nrf9160 和 Nuvoton M2351、M2354）上启用。 
FreeRTOS 与 TF-M 运行时服务集成，可确保 Cortex-M 设备的安全， 
如[此处](https://freertos.org/2020/07/security-for-arm-cortex-m-devices-with-freertos.html) 所述。 
FreeRTOS 已获得 PSA 1 级认证，这可确保基本安全原则已纳入 
可供 OEM 应用程序开发者利用的系统软件之中。 

![](/media/2021/trusted-firmware-m-300x110.png)   
*图 1：Cortex-M 设备安全处理环境中的 Trusted Firmware-M 示意图。
PSA 功能 API 可以由非安全处理环境（RTOS 和应用程序）使用*

TF-M 提供的一项重要功能是安全启动，可确保仅在设备上 
运行授权软件。该功能至关重要，确保设备在现场部署后即可联网并更新软件 
。开源社区项目 [MCUboot](https://github.com/mcu-tools/mcuboot)
可用作 TF-M 的安全引导加载程序。引导加载程序通过哈希和数字签名对运行时映像进行身份验证， 
具体方式是使用 MCUboot 映像中的映像密钥或在 SoC 中配置的映像密钥。

除 PSA 加密、存储和认证安全运行时服务以外，TF-M 还在安全处理环境中以安全服务的形式实现了 
PSA 固件更新 (PSA FWU) 接口（图 1）。 
这些接口会暴露给非安全处理环境 (NSPE)，由更新应用程序 
使用。反过来，PSA FWU 服务依赖 TF-M 安全启动 (MCUboot)  
来验证新映像，并在成功验证后将其部署为活动映像。

在完成 FreeRTOS 和 TF-M 集成 
（[如前所述](/Community/Blogs/2020/security-for-arm-cortex-m-devices-with-freertos)）的基础上，PSA FWU 
安全服务已与 FreeRTOS 集成，具体内容如下节所述。 


## TF-M 与 FreeRTOS OTA 集成

FreeRTOS 提供了 [OTA 代理库](https://docs.aws.amazon.com/freertos/latest/userguide/ota-agent-library.html)， 
可供 FreeRTOS 设备接收并部署来自 AWS IoT 的固件更新。得益于此，IoT 
设备（搭载 FreeRTOS）可以应用 OTA 更新。该库还定义了一组 OTA 平台抽象层 (PAL) API， 
需要由集成该库的供应商来实现。每个 Cortex-M 芯片平台都需要 
提供 OTA PAL API 的实现，方能启用 OTA 代理。 

我们提供了一种 OTA PAL API 的实现，可通过 TF-M 在 Cortex-M 设备上进行安全固件更新 
。该 API 实现使用 PSA 功能 API，包括上文探讨的 PSA FWU API 和 
PSA 加密 API。

下表显示了 [PSA 功能 API](https://www.psacertified.org/getting-certified/functional-api-certification/) 
（在 OTA PAL API 中使用）。

| OTA PAL API | PSA 功能 API |
| --- | --- |
| prvPAL_Abort | psa_fwu_abort<br/>  |
| prvPAL_CreateFileForRx | 无 |
| prvPAL_CloseFile | psa_fwu_query  psa_asymmetric_verify |
| prvPAL_WriteBlock | psa_fwu_write |
| prvPAL_ActivateNewImage | psa_fwu_install  psa_fwu_request_reboot |
| prvPAL_ResetDevice | psa_fwu_request_reboot |
| prvPAL_SetPlatformImageState | psa_fwu_accept |

上述使用 PSA 功能 API 的 OTA PAL API 实现可在 
所有启用 TF-M 的 Cortex-M 平台上作为通用实现。这样就无需每个 Cortex-M 平台 
都开发和维护 OTA PAL API 的实现。安全处理环境 
（包括由 TF-M 提供的安全启动）可确保在平台上安全完成 OTA 更新 
。

已在 Arm Musca-B1e 平台上构建使用 TF-M OTA PAL 的 OTA 代理的示例实现。 
TF-M OTA PAL 通过 PSA 功能 API 使用 TF-M 的固件更新服务。该实现 
可以连接到 AWS IoT，接收新固件映像，进行身份验证并部署映像。下图 2 显示了 
该实现。有关 TF-M OTA PAL 和 FreeRTOS 实现的更多信息， 
请查看[此处](https://github.com/Linaro/freertos-ota-pal-psa/tree/0b6db7d7cc0260fbb1e54a26ad6ff25cdcde3697) 的 GitHub 文件夹 ota_pal_psa。 

![](/media/2021/enabling-secure-ota-300x155.png)   
*图 2：通过 OTA 代理、OTA PAL 实现以及 TF-M 集成启用来自 AWS IoT 服务的安全 OTA 更新示意图*


## 使用 TF-M 和 FreeRTOS 简化 Cortex-M 上的 OTA 更新

OTA 是 IoT 设备部署后保持安全的 
基本构建块。[NIST 8259A](https://www.nist.gov/news-events/news/2020/06/security-iot-device-manufacturers-nist-publishes-nistirs-8259-and-8259a) 
和 [EN 303 645](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/02.01.01_60/en_303645v020101p.pdf) 
概述了网络安全最佳实践和提高 IoT 设备安全标准的共同基准。与 
PSA 认证一样，这些指南要求设备支持软件和固件更新机制。 
IoT 设备制造商发现，由于底层硬件平台的多样性和复杂性，大规模启用 OTA 颇具挑战 
。采用 TF-M OTA PAL 和 TF-M 可以化繁为简， 
确保 FreeRTOS Cortex-M 设备在其生命周期内无缝且安全地更新，从而利用 
芯片和系统软件中的安全功能。请访问 FreeRTOS 参考集成 
（位于 [Github](https://github.com/aws/amazon-freertos/tree/main/libraries/abstractions/) 上） 
和[可信固件](https://www.trustedfirmware.org/projects/tf-m/)，详细了解 TF-M 
OTA PAL 和 TF-M 实现。


## 作者简介

![](https://secure.gravatar.com/avatar/db732371ff8ea1e00013619782acc940?s=200&d=mm&r=g)   
Shebu Varghese Kuriakose 是 Arm 开源软件集团软件技术管理总监 
兼可信固件项目委员会主席。Shebu 致力于推动 Trusted Firmware-M 开发路线图， 
并与芯片供应商、RTOS 和工具生态系统开展合作。  
[查看此作者的文章](../author/arm-author) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

