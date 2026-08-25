---
title: "FreeRTOS LTS 路线图"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 发展路线图
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS 初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---

此页面介绍了我们的长期支持 (LTS) 版本路线图中每个库的状态。此页面上列出的所有库
都已经或正在进行重构，
以满足[以下](#lts-代码质量检查表)所述的模块化和代码质量标准。库满足标准后将被移动到主 FreeRTOS 下载中
（每个库也有[自己的 Github 存储库](https://github.com/FreeRTOS)）。当所有库
都在主 FreeRTOS 下载中时，将以长期支持的方式发布这些库和 FreeRTOS 内核。

## LTS 状态

**最后更新时间：2020/11/10**

| 库 | 阶段 |
| ------- | ----- |
| [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP) | 在主 [下载](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)中 |
| [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)（适合任何 TCP/IP 堆栈） | 在主 [下载](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)中 |
| [corePKCS11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11) | 在主 [下载](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)中 |
| [coreJSON](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/01-coreJSON) | 在主 [下载](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)中 |
| [AWS IoT Device Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow) | 在主 [下载](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)中 |
| OTA                                                        | 正在进行中                                                                                                  |
| HTTPS                                                      | 正在进行中                                                                                                  |
| AWS IoT Jobs                                               | 正在进行中                                                                                                  |

## LTS 代码质量检查表

| #   | 类别                   | 检查事项 |
| --- | -------------------------- | ------ |
| 1   | 复杂性评分 | 所有函数的 [GNU Complexity](https://www.gnu.org/software/complexity/manual/complexity.html) 评分小于等于 8 |
| 2   | 编码标准 | 所有函数符合 [MISRA 编码标准](/Documentation/02-Kernel/06-Coding-guidelines/02-FreeRTOS-Coding-Standard-and-Style-Guide/#coding-standard--misra-compliance) |
| 3   | 静态检查 | 所有代码都将使用 [Coverity](https://scan.coverity.com/) 进行静态检查 |
| 4   | 函数返回 | 所有函数都有一个单独的出口点 |
| 5   | 代码测试 | 所有代码都会进行广泛的单元测试。将使用 Gcov 报告来报告测试覆盖范围，每个库将有扩展功能测试。 |
| 6   | 要求文档 | 所有库都有记录要求，可能包括资源要求、列出所有依赖项和移植要求（如适用） |
| 7   | 设计文档 | 所有库都具有设计文档，可能包括应用程序和云接口、状态机和同步（如适用）。 |
| 8   | 编译器警告 | 当使用 gcc -Wall -Wextra 编译器选项时，代码的编译不会产生任何编译器警告。 |
