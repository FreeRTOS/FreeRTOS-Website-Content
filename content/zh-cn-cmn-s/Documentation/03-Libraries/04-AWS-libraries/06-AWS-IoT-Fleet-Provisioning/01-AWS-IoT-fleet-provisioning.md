---
title: AWS IoT Fleet Provisioning
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 库
description: AWS IoT fleet provisioning 库简介
relatedLinks:
  - title: Fleet provisioning Github 存储库
    link: https://github.com/aws/Fleet-Provisioning-for-AWS-IoT-embedded-sdk
externalLinks:
  - title: AWS IoT Fleet Provisioning 库
    link: https://aws.github.io/Fleet-Provisioning-for-AWS-IoT-embedded-sdk/v1.1.0/
---

## 引言

您可利用 AWS Fleet Provisioning 库使用唯一证书预置 IoT 设备队列， 
并使用 AWS IoT Core 
的[队列预置功能将设备注册到 AWS IoT Core](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html)。 
使用 Fleet Provisioning 有两种方法： 
[通过声明预置](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html#claim-based) 
和[通过受信任的用户预置](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html#trusted-user)。 
这样，您便能够使用制造设备凭证或新生成的凭证。除标准 C 库以外， 
该库不依赖于其他库， 
因此可以与任何 MQTT 库一起使用。 

此库已通过代码质量检查， 
包括验证函数的 [GNU 复杂性](https://www.gnu.org/software/complexity/manual/complexity.html)分数均未超过 8 分， 
以及检查 
代码与 [MISRA 编码标准](https://www.misra.org.uk/)中强制性规则的偏差。与 MISRA C:2012 指南的偏差记录在 
[MISRA 偏差](https://github.com/aws/Fleet-Provisioning-for-AWS-IoT-embedded-sdk/blob/main/MISRA.md)中。 
此库还 
使用 [Coverity 静态分析](https://scan.coverity.com/)进行了静态代码分析， 
以及使用 [CBMC 自动推理工具](https://www.cprover.org/cbmc/)验证内存安全性。


此库根据 
[MIT 开源许可证](https://github.com/aws/Fleet-Provisioning-for-AWS-IoT-embedded-sdk/blob/main/LICENSE)发布。

**AWS IoT Fleet Provisioning 的代码大小（通过 ARM Cortex-M 的 GCC 生成的示例）**

| 文件 | 使用 -O1 优化 | 使用 -Os 优化 |
| --- | --- | --- |
| fleet_provisioning.c | 1.0K | 0.9K |
| 总估计值 | 1.0K | 0.9 K |
