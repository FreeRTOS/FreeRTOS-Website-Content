---
title: 安全漏洞
date: 2022 年 1 月
---

## 安全更新

下表列出了 FreeRTOS 在过去三年中的安全更新
以及相应的[通用漏洞披露](https://cve.mitre.org/) (CVE) 
编号。要报告安全问题， 
请访问[AWS 漏洞报告](https://aws.amazon.com/security/vulnerability-reporting/)。

**安全问题**
| **创建日期** | **严重程度** | **FreeRTOS 库**  | **CVE**  | **最低补丁版本** |
| ---------------- | ------------ | --------------------- | -------- | --------------------------- |
| 2026 年 5 月 15 日       | 高         | coreMQTT                         | [CVE-2026-8686](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-8686) | [coreMQTT V5.0.1](https://github.com/FreeRTOS/coreMQTT/releases/tag/V5.0.1)
| 2026 年 4 月 29 日       | 高         | FreeRTOS+TCP                     | [CVE-2026-7426](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-7426) | [FreeRTOS-Plus-TCP V4.4.1](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/releases/tag/V4.4.1) [FreeRTOS-Plus-TCP V4.2.6](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/releases/tag/V4.2.6)
| 2026 年 4 月 29 日       | 中         | FreeRTOS+TCP                     | [CVE-2026-7425](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-7425) | [FreeRTOS-Plus-TCP V4.4.1](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/releases/tag/V4.4.1) [FreeRTOS-Plus-TCP V4.2.6](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/releases/tag/V4.2.6)
| 2026 年 4 月 29 日       | 高         | FreeRTOS+TCP                     | [CVE-2026-7424](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-7424) | [FreeRTOS-Plus-TCP V4.4.1](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/releases/tag/V4.4.1) [FreeRTOS-Plus-TCP V4.2.6](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/releases/tag/V4.2.6)
| 2026 年 4 月 29 日       | 中         | FreeRTOS+TCP                     | [CVE-2026-7423](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-7423) | [FreeRTOS-Plus-TCP V4.4.1](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/releases/tag/V4.4.1) [FreeRTOS-Plus-TCP V4.2.6](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/releases/tag/V4.2.6)
| 2026 年 4 月 29 日       | 中         | FreeRTOS+TCP                     | [CVE-2026-7422](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-7422) | [FreeRTOS-Plus-TCP V4.4.1](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/releases/tag/V4.4.1) [FreeRTOS-Plus-TCP V4.2.6](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/releases/tag/V4.2.6)
| 2025 年 10 月 10 日      | 中         | FreeRTOS+TCP                     | [CVE-2025-11618](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-11618) | [FreeRTOS-Plus-TCP V4.3.4](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/releases/tag/V4.3.4)
| 2025 年 10 月 10 日      | 中         | FreeRTOS+TCP                     | [CVE-2025-11617](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-11617) | [FreeRTOS-Plus-TCP V4.3.4](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/releases/tag/V4.3.4)
| 2025 年 10 月 10 日      | 中         | FreeRTOS+TCP                     | [CVE-2025-11616](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-11616) | [FreeRTOS-Plus-TCP V4.3.4](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/releases/tag/V4.3.4)
| 2025 年 6 月 4 日        | 高         | FreeRTOS+TCP                     | [CVE-2025-5688](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-5688) | [FreeRTOS-Plus-TCP V4.3.2](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/releases/tag/V4.3.2)
| 2024 年 6 月 17 日       | 严重     | FreeRTOS+TCP                     | [CVE-2024-38373](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-38373) | [FreeRTOS-Plus-TCP V4.1.1](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/releases/tag/V4.1.1)
| 2023 年 11 月 29 日       | 高         | FreeRTOS 内核                  | 仅增强功能                                                               | [FreeRTOS 内核 V10.6.2](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/V10.6.2)                                                                                                                                         |
| 2022 年 9 月 16 日       | 高         | FreeRTOS 内核（仅 MPU 移植） | 仅增强功能                                                               | [FreeRTOS 内核 V10.5.0](https://github.com/FreeRTOS/FreeRTOS-Kernel/releases/tag/V10.5.0)                                                                                                                                 |
| 2021 年 9 月 10 日       | 高         | FreeRTOS+TCP                     | 仅增强功能                                                               | [FreeRTOS-Plus-TCP V2.3.4](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/blob/V2.3.4/README.md) [FreeRTOS-Plus-TCP V2.3.2-LTS-Patch-2](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/releases/tag/V2.3.2-LTS-Patch-2)       |
| 2021 年 11 月 17 日       | 高         | FreeRTOS 内核                  | [CVE-2021-43997](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-43997) | [FreeRTOS 内核 v10.4.6](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/V10.4.6/History.txt)‡、[FreeRTOS 内核 v10.4.3-LTS-Patch-2](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/V10.4.3-LTS-Patch-2/History.txt) |
| 2021 年 5 月 3 日       | 严重     | FreeRTOS 内核                  | [CVE-2021-32020](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-32020) | [FreeRTOS 内核 v10.4.3](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/V10.4.3/History.txt)†                                                                                                                            |
| 2021 年 4 月 22 日       | 严重     | FreeRTOS 内核                  | [CVE-2021-31572](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-31572) | [FreeRTOS 内核 v10.4.3](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/V10.4.3/History.txt)†                                                                                                                            |
| 2021 年 4 月 22 日       | 严重     | FreeRTOS 内核                  | [CVE-2021-31571](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-31571) | [FreeRTOS 内核 v10.4.3](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/V10.4.3/History.txt)†                                                                                                                            |

†FreeRTOS 内核 v10.4.3（不包括）之前的所有版本

‡从 v10.2.0（包括） 到 v10.4.6（不包括）的 FreeRTOS 内核版本



