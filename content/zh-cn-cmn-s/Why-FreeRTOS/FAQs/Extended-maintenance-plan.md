---
title: "FreeRTOS 常见问题-什么是 FreeRTOS 延长维护计划 (EMP) ？"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 有关 FreeRTOS 延长维护计划 (EMP) 的常见问题
---


## 什么是 FreeRTOS 延长维护计划 (EMP)？

由 Amazon Web Services (AWS) 提供的 FreeRTOS 延长维护计划 (EMP)， 
可在最初的 LTS 期过期后 10 年内，为您所选择的 FreeRTOS Long Term Support (LTS) 版本提供安全补丁和关键错误修复服务 
[](/Community/Blogs/2021/freertos-aws-reference-integrations-now-include-freertos-202012-01-lts-libraries)。有了 FreeRTOS EMP，您的基于 FreeRTOS 的
长寿命设备可以依赖一个具有功能稳定性的版本， 
并在您的订阅期限内获得安全更新。你可以及时收到 FreeRTOS 库即将发布补丁的通知，因此您 
可以计划在物联网 (IoT) 设备上部署安全补丁。在当前 
LTS 期结束之前，您可以使用您的 AWS 帐户订阅延长维护计划，并 
每年续订，以覆盖产品生命周期或直到您准备过渡到新的 FreeRTOS 
版本为止。FreeRTOS EMP 适用于属于 FreeRTOS LTS 的库。 



## 我为什么要使用 FreeRTOS EMP ？

FreeRTOS EMP 可帮助您在订阅期间维护基于 FreeRTOS的设备。它能够为您 
节省操作系统的升级成本，同时减少无法及时更新设备的风险。它 
在功能稳定的 FreeRTOS LTS 版本上提供安全补丁和关键错误修复，因此您无需 
为升级到最新的 FreeRTOS 版本而产生开发、测试和 QA 成本。更新设备涉及 
项目规划、发布准备测试和 over-the-air (OTA) 更新调度以部署关键修复。 
FreeRTOS EMP 通过及时通知即将发布的补丁和 
就融合问题提供支持。 



##  FreeRTOS EMP 的主要特色是什么？

| 特色 | 说明 | 为什么这很重要？ |
| --- | --- | --- |
| 功能稳定性 | 获取多年来保持相同功能集的 FreeRTOS 库。 | 使用稳定的 FreeRTOS 代码库来节省产品生命周期的升级成本。 |
\| API 稳定性\|获取多年来保持稳定 API 的 FreeRTOS 库。\|
\|关键修复\|在您选择的 FreeRTOS 库上接收安全补丁和关键错误[^1]修复。安全补丁有助于在产品生命周期内确保您的 IoT 设备的安全。\|
\|补丁通知\|及时收到即将发布的补丁通知。\|及时了解安全补丁有助于您主动规划补丁部署。\|
\|灵活的订阅计划\|将维护时间延长一年或更长时间。\|继续将您的年度订阅续订更长时间，以在整个设备生命周期内保持同一版本，或在更新到最新 FreeRTOS 版本之前争取更短的时间。\|


[^1]: A 关键错误是由 AWS 确定为影响受影响的 
库的功能的缺陷，并且没有合理的解决办法。

AWS 将通过 [AWS 支持](https://aws.amazon.com/premiumsupport/)向 FreeRTOS EMP 客户提供技术支持。 
AWS 支持不包括在 FreeRTOS EMP 订阅中。您可以跟踪问题（例如， 
与 AWS 账户、账单或错误相关的问题）或 
根据您的 AWS 支持计划与技术专家取得联系（有关补丁集成等问题）。


## 在哪里可以找到定价和入门相关信息？

请访问 AWS 上的 [FreeRTOS 网页](https://aws.amazon.com/freertos/) 了解更多信息。
