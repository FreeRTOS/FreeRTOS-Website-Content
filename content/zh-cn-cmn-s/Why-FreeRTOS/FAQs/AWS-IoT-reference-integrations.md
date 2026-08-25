---
title: FreeRTOS 常见问题 - AWS IoT 参考集成
created: 2018-09-20 00:00:00.0 UTC
description: 有关 FreeRTOS AWS IoT 参考集成的常见问题
---

## 如何将基于微控制器的主板添加到 FreeRTOS.org  [IoT 参考集成](/Documentation/03-Libraries/04-AWS-libraries/09-AWS-reference-integrations)页面？

要将您的主板加入 AWS IoT 参考集成页面， 
请按照 [AWS 设备认证程序](https://aws.amazon.com/partners/dqp/)中列出的认证流程操作。在认证程序中， 
您需要验证您的 FreeRTOS 移植、提交验证结果 
并在 [AWS 合作伙伴设备目录]中列出您的主板。(https://devices.amazonaws.com/) 认证合格后，您的主板将在 
FreeTOS.org IoT 参考集成页面中列出。


## 如果要使用 AWS IoT 功能，我该如何开始使用 FreeRTOS LTS 库？

您可以通过克隆 GitHub 的单个存储库， 
或从 FreeRTOS.org 中的 IoT 参考集成开始，将单个库更新到 FreeRTOS LTS 库，来构建您的项目。 
一些 IoT 参考集成已与 FreeRTOS LTS 库预先集成， 
您可以通过标签 “使用 FreeRTOS YYYYMM.XX LTS 库”来识别它们。选取后， 
您会进入 AWS 合作伙伴设备目录。您可以在其中查看参考集成中使用的 LTS 库的列表， 
以及特定基于 MCU 的主板的入门指南。
