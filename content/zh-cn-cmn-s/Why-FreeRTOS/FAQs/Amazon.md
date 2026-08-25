---
title: FreeRTOS 常见问题- Amazon
created: 2018-09-20 00:00:00.0 UTC
description: 关于 FreeRTOS 和 Amazon 的常见问题
---


## 为什么 Amazon 要接管 FreeRTOS?

[Amazon Web Services](https://aws.amazon.com/) 提供
超过 100 种 [云托管服务](https://aws.amazon.com/application-hosting/benefits/)，
拥有数以百万计的客户，范围覆盖各行各业。越来越多的
AWS 服务因物联网 (IoT) 应用程序而诞生，
为[连接互联网的设备提供连接和管理服务](https://aws.amazon.com/iot/)。

设备制造商将基于 MCU 的设备连接到云端，
对其产品和业务模式进行创新。但是，需要花时间先将
这种连接所需的安全和连接组件
构建到设备的软件中，然后才能开始创新。相当一部分
连接的 MCU 设备已经运行了 FreeRTOS 内核，因此 Amazon
选择为 FreeRTOS 项目提供所需资源
将其产品扩展到完全集成的安全和连接库，并确保
这些库在未来很长时间内可以得到开发和支持。因此，
减少了 FreeRTOS 开发人员在库集成上花费的时间，而把更多的时间放在
创新上。

为了确保使用寿命， Amazon 还确保
大 FreeRTOS 生态系统强大，让所有 FreeRTOS 内核用户都受益，而不仅仅是
那些将设备连接到互联网的用户。我们会继续
为未来新架构新增功能和支持。同时，我们一如既往地欢迎
用户反馈。

另请参阅常见问题[“我必须是 AWS 客户才能使用 FreeRTOS 吗？”。](#必须是-amazon-web-sevice-aws-客户才能使用-freertos-吗) 
[“我可以使用 FreeRTOS 连接到任何云服务吗？”](#我可以使用-freertos-连接到任何云服务吗)。


## 必须是 Amazon Web Sevice (AWS) 客户才能使用 FreeRTOS 吗？

不，FreeRTOS 库
是根据免费开源 [MIT 许可](/Documentation/03-Libraries/01-Library-overview/04-Licensing)条款提供的。这
意味着它们可以不受限制地用于任何目的。


## 我可以使用 FreeRTOS 连接到任何云服务吗？

是的。另请参阅常见问题 [“我必须是 AWS 客户才能使用 FreeRTOS 吗？”](#必须是-amazon-web-sevice-aws-客户才能使用-freertos-吗)。


## Amazon 是否也将 FreeRTOS 内核作为独立组件进行投资？

是的。FreeRTOS 内核的首个版本于
Amazon Web Services (AWS) 的管理下发布，版本为 [FreeRTOS V10.0.0 ](/Documentation/04-Roadmap-and-release-note/02-Release-notes/03-FreeRTOS-V10)，
包含新功能和更简单的许可。


## Amazon 是否拆分了 FreeRTOS？

否。Amazon 将继续投资开发 FreeRTOS 内核。
