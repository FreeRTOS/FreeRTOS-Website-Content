---
title: "FreeRTOS™ 内核"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 内核简介
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS 简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS 初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---

[市场领先](https://www.embedded.com/wp-content/uploads/2019/11/EETimes_Embedded_2019_Embedded_Markets_Study.pdf)以及 
事实上的标准和跨平台 [RTOS](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/01-RTOS-fundamentals) 
内核

FreeRTOS 是我们与世界领先的芯片公司历时 18 年合作开发的成果， 
这是一款适用于微控制器和小型微处理器的市场领先实时操作系统。 
FreeRTOS 通过 MIT 开源许可免费分发，包括一个内核和一组不断丰富的库， 
适用于各行各业。FreeRTOS 注重可靠性、可访问性和易用性， 
每 170 秒就被下载一次。    
  
  
## 您知道吗？

- FreeRTOS 每 170 秒就被下载一次（2019 年平均下载频次）。

- **自 2011 年首次纳入 [EETimes 嵌入式市场](https://www.embedded.com/electronics-blogs/embedded-market-surveys/4458724/2017-Embedded-Market-Survey)
  调查名单以来，FreeRTOS 每次都位列榜首。**

- 与其他同类商品相比，FreeRTOS 的_**项目风险更低**_，_**总拥有成本也更低**_，原因如下：
    
  - 得到[全面支持](https://forums.freertos.org)，并有文档记录。
  - 虽然大多数人在将产品推向市场时甚至从未联系过我们，但他们非常踏实放心，因为他们知道自己 
    可随时切换到[完全免责的商业许可](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/04-Licensing#optional-freertos-commercial-licensing)（提供专门支持）。

- 一些 FreeRTOS 移植[不会完全禁用中断](/Documentation/02-Kernel/03-Supported-devices/02-Customization#kernel_priority)。

- 为严格控制质量并避免知识产权归属的不确定性， 
  [我们已将 FreeRTOS 官方代码与社区贡献的代码分开。](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party)

- FreeRTOS 采用无滴答模式，[直接支持低功耗应用程序](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)。

- FreeRTOS 简单易用：只需 3 个 RTOS 移植通用的源文件 
  和 1 个微控制器专用的源文件即可，其 API 的设计也很简单直观。

- RL78 移植可在不到 4K 字节的 RAM 中创建 13 项任务、2 个队列和 4 个软件定时器！
    

## 为什么使用 FreeRTOS？

<blockquote>
    <span className="content">
“现在我几乎可以肯定地说，FreeRTOS 经历的‘同行评审’要远多于市面上其他的 RTOS 
。我曾在多个项目中使用 FreeRTOS，其中一个项目采用多处理器环境， 
使用的处理器超过 64 个，需要可靠地运行数月。RTOS 核心表现非常出色。试着使用 FreeRTOS 看看吧。”
    </span>
<span className="attribution">John Westmoreland</span>
</blockquote>

**FreeRTOS 集合了所有优点：**FreeRTOS 真正免费，得到全方位[支持](https://forums.freertos.org)， 
即使在商业应用中也是如此。 
[FreeRTOS 采用 MIT 开源许可](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/04-Licensing)， 
不要求您公开专有知识产权。在使用 FreeRTOS 将产品推向市场时，您无需告知我们， 
更无需支付费用，成千上万的人都是这样做的。如果您希望获得额外支持， 
或者您的法律团队需要额外的书面保证或赔偿， 
我们随时都可以为您提供[简单且低成本的商业升级路径](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/04-Licensing#optional-freertos-commercial-licensing)。 
请尽管放心，您随时都可选择走商业路线。

为什么 FreeRTOS 是您开发下一个应用程序的明智选择？原因如下 - FreeRTOS……

- 提供统一且独立的解决方案，适用于多种不同的架构和开发工具。
- 可靠性众所周知。姐妹项目 SafeRTOS 所执行的活动提供了额外的信心保证。
- [功能丰富](/Why-FreeRTOS/highlighted-features)且仍在持续积极开发中。
- 占用的 ROM 和 RAM 较少，处理开销也较低。RTOS 内核二进制映像通常 
  介于 6K 到 12K 字节之间。
- 非常简单易用，RTOS 内核的核心仅包含 
  在 [3 个 C 文件](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)中。 
  .zip 文件下载内容中包含的大多数文件仅与演示应用程序有关。
- 对商业应用完全免费 
  （详情请参阅[许可条件](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/04-Licensing)） 
  。
- 以 OPEN**RTOS** 的形式提供商业许可、专业支持和移植服务
  （由我们的合作伙伴 [WITTENSTEIN High Integrity Systems](https://www.highintegritysystems.com) 提供） 。
- 可迁移至 [Safe**RTOS**](https://www.highintegritysystems.com)，提供 
  医疗、汽车和工业领域的认证。
- 用户群非常庞大，且仍在不断壮大。
- 每个移植都包含一个预配置示例。无需明白如何设置项目，只需下载和编译即可！
- 拥有优秀、活跃并受到广大用户监督的免费[支持论坛](https://forums.freertos.org)。
- 确保随时为您提供商业支持。
- 提供丰富的文档。
- 易于扩展、简单易用。
- FreeRTOS 可为那些不适合或无法在 eCOS、嵌入式 Linux 
  （或实时 Linux）甚至 uCLinux 上开发的应用程序提供更小巧、更简单的实时处理系统。
