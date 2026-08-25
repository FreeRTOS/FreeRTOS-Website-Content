---
title: 代码质量与安全相关文章
description:
feature: full
featureLinks:
  - title: FreeRTOS-Plus-TCP 库现在更加稳健和安全
    link: /Community/Blogs/2022/the-freertos-plus-tcp-library-is-now-more-robust-and-secure
    description: 在从事 FreeRTOS Labs IPv6 项目的同时，我们不忘继续提高 FreeRTOS-Plus-TCP 库的稳健性、安全性和模块化标准。今天，我们很高兴推出专为实现此目的而开发的 FreeRTOS-Plus-TCP V3.0.0 库。FreeRTOS-Plus-TCP V3.0.0 新增了全面的单元测试，覆盖所有代码行和分支，并经过了渗透测试……
    author: Toshiyanger Walling
    date: 2022 年 8 月 9 日
    tags: [质量-安全]
  - title: FreeRTOS is now SESIP Level 3 certified
    link: /Community/Blogs/2024/freertos-is-now-sesip-level3-certified
    description: FreeRTOS has achieved certification for the Security Evaluation Standard for IoT Platforms (SESIP™) Assurance Level 3. Primarily used in embedded system processors, FreeRTOS remains one of the top choices among developers, supported by a community that has been collaborating for over 21 years...
    author: Aniruddha Kanhere
    date: 09 Oct 2024
    tags: [quality-security]
---


```jsx
<CategoryPage />
```


* [推出三个精选 FreeRTOS IoT 集成以提升 IoT 应用程序安全性](../2022/introducing-three-featured-freertos-iot-integrations-for-more-secure-iot-applications) 
  本帖由 [Lucio Di Jasio](../author/luciodj) 于 2022 年 5 月 9 日发布 我们很高兴地宣布推出三个精选 FreeRTOS 
  IoT 集成。这些集成是与我们的合作伙伴 Espressif、NXP 和 STMicroelectronics 合作开发的。 
  每个项目都展示了最新的 FreeRTOS 和 AWS 嵌入式 C SDK 长期支持 (LTS) 库的用法， 
  以及最新的微控制器架构功能，从而提高了 
  安全性和模块化水平[…]   
  [阅读更多……](../2022/introducing-three-featured-freertos-iot-integrations-for-more-secure-iot-applications)

* [通过 FreeRTOS](/Community/Blogs/2021/secure-ota-updates-for-cortex-m-devices-with-freertos) 为 Cortex-M 设备提供安全的 OTA 更新 
  本帖由 [Shebu Varghese Kuriakose](../author/arm-author) 于 2021 年 7 月 14 日发布 IoT 设备在各个细分市场迅速普及， 
  并成为网络攻击的主要目标。对 
  IoT 设备的攻击有很大一部分是由于软件投入使用后缺少软件更新或 
  更新不安全所致。网络攻击者经常针对过时的软件组件漏洞来 
  控制[...]   
  [阅读更多……](/Community/Blogs/2021/secure-ota-updates-for-cortex-m-devices-with-freertos)

* [为什么 SESIP™ 认证对 FreeRTOS 至关重要](/Community/Blogs/2021/why-sesip-certification-for-freertos-matters) 
  本帖由 [Richard Elberger](../author/elberger) 于 2021 年 3 月 1 日发布 FreeRTOS 现已通过 
  IoT 平台安全评估标准 (SESIP™) 保证级别 2 的认证。FreeRTOS 在大多数情况下 
  是在嵌入式系统处理器上运行的软件。开发人员在构建 FreeRTOS 应用程序的同时 
  也在参与一个合作 18 年以上且不断壮大的社区，这一现象前所未有。虽然 
  主要[...]   
  [阅读更多……](/Community/Blogs/2021/why-sesip-certification-for-freertos-matters)

* [使用形式化方法验证 OTA 协议](/Community/Blogs/2020/using-formal-methods-to-validate-ota-protocol) 
  本帖由 [Murali Talupur](../author/talupur) 于 2020 年 12 月 14 日发布 AWS FreeRTOS 是一款实时操作系统， 
  用于在 IoT 设备上运行，使这类设备可以与 AWS 服务轻松、可靠地进行交互。该 
  Over the Air (OTA) 更新功能可以快速、可靠地更新装有安全修补程序的设备 
  。OTA 库，是整体 OTA 功能的一部分[…]   
  [阅读更多……](/Community/Blogs/2020/using-formal-methods-to-validate-ota-protocol)

* [通过 FreeRTOS](/Community/Blogs/2020/security-for-arm-cortex-m-devices-with-freertos) 确保 Arm Cortex-M 设备的安全 
  本帖由 [Shebu Varghese Kuriakose](../author/arm-author) 于 2020 年 7 月 17 日发布 
  确保微控制器的安全非常具有挑战性，部分原因在于这些设备缺乏由硬件强制实施的安全域。创建两个安全域 
  通常需要两个微处理器，每个微处理器都有一个单独的内存保护单元 (MPU)。随 
  Armv8-M 架构一起引入的 Arm TrustZone 
  可在单个 Cortex-M 处理器上实现两个安全处理环境（请参阅在 Armv8-M 微控制器上使用 FreeRTOS）。一旦 [...]   
  [阅读更多......](/Community/Blogs/2020/security-for-arm-cortex-m-devices-with-freertos)

* [确保 FreeRTOS 的内存安全第 2 部分](/Community/Blogs/2020/ensuring-the-memory-safety-of-freertos-part-2) 
  本帖由 [Nathan Chong](../author/ncchong) 于 2020 年 5 月 7 日发布。在第 1 部分中，我们讨论了 FreeRTOS 如何解决 
  安全问题的一个重要来源：--- 缓冲区溢出 ---， 
  解决方法是确保 TCP/IP、ARP、DHCP、DNS 和 FreeRTOS-Plus-TCP TCP/IP 堆栈中解析的 HTTPS 标头的内存安全。我们介绍了 
  如何使用自动推理技术、软件模型检测，以及[…]   
  [阅读更多……](/Community/Blogs/2020/ensuring-the-memory-safety-of-freertos-part-2)

* [确保 FreeRTOS 的内存安全第 1 部分](/Community/Blogs/2020/ensuring-the-memory-safety-of-freertos-part-1) 
  本帖由 [Nathan Chong](../author/ncchong) 于 2020 年 2 月 18 日发布 FreeRTOS 
  是专为资源受限设备设计的实时操作系统，包括物联网 (IoT) 中的各种设备。 由于这些 
  设备属于资源受限型设备，无法像较大型的操作系统一样， 
  能够利用各类硬件机制来保护系统免受外部干扰。 在这些小型设备上， 
  安全取决于较简单的内存保护、具有执行优先级的硬件[…]   
  [阅读更多……](/Community/Blogs/2020/ensuring-the-memory-safety-of-freertos-part-1)


