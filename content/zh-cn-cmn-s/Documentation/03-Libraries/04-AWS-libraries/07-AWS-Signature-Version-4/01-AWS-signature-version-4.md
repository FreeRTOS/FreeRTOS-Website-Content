---
title: AWS 签名第 4 版
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 库
description: AWS IoT 签名第 4 版库简介
relatedLinks:
  - title: 签名第 4 版 Github 存储库
    link: https://github.com/aws/SigV4-for-AWS-IoT-embedded-sdk
externalLinks:
  - title: AWS SigV4 库
    link: https://aws.github.io/SigV4-for-AWS-IoT-embedded-sdk/v1.2.0/
---


## 引言

AWS 签名第 4 版 (SigV4) 库是用于生成身份验证标头和签名的独立库，
符合
[AWS 签名第 4 版本](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html)
签名过程的规范。此库可以用于应用程序与
需要使用 HTTP 进行 SigV4 身份验证的 AWS 服务进行交互。此库不依赖
标准 C 库以外的任何库。


此库已通过代码质量检查，包括验证没有函数的
[GNU 复杂度](https://www.gnu.org/software/complexity/manual/complexity.html)分数超过 8 并
检查是否偏离了
[MISRA 编码标准](https://www.misra.org.uk/)中的强制性规则。偏离 MISRA C:2012 指南的情况
记录在
[MISRA 偏离](https://github.com/aws/SigV4-for-AWS-IoT-embedded-sdk/blob/main/MISRA.md)中。
此库还
使用 [Coverity 静态分析](https://scan.coverity.com/)开展静态代码分析，并通过
[CBMC 自动推理工具](https://www.cprover.org/cbmc/)验证内存安全。

此库可自由使用，并根据
[MIT 开源许可证](https://github.com/aws/SigV4-for-AWS-IoT-embedded-sdk/blob/main/LICENSE)发布。


**AWS SigV4 库的代码大小（通过 ARM Cortex-M 的 GCC 生成的示例）**

| 文件 | 使用 -O1 优化 | 使用 -Os 优化 |
| --- | --- | --- |
| sigv4.c | 5.2K | 4.4K |
| sigv4_quicksort.c | 0.4K | 0.3K |
| 总估计值 | 5.6K | 4.7K |
