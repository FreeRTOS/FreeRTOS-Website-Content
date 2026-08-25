---
title: "下载 FreeRTOS"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 如何下载 FreeRTOS
relatedLinks:
  - title: FreeRTOS 版本说明
    link: /Documentation/04-Roadmap-and-release-note/02-Release-notes/00-Release-history
  - title: FreeRTOS GitHub 存储库
    link: https://github.com/FreeRTOS
customStrings:
  - id: 0
    value: FreeRTOS 202406.05 LTS
  - id: 1
    value: "[数据包](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/04-FreeRTOS-libraries-and-3rd-party-tools/#freertos-source-code-organisation) 内含 FreeRTOS LTS 库，其中包含 FreeRTOS 内核和 IoT 库，没有示例项目。请参阅 [LTS 库页面](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries)，了解更多详情。您也可以从 [GitHub](https://github.com/FreeRTOS/FreeRTOS-LTS) 获取源代码。"
  - id: 4
    value: FreeRTOS 内核入门
  - id: 5
    value: "了解如何选择 FreeRTOS 内核移植，如何选择并构建预配置示例以演示内核功能，以及如何查找其他实用内核文档。<br/>[了解更多](FreeRTOS-quick-start-guide)"
  - id: 6
    value: FreeRTOS-Plus 库入门
  - id: 7
    value: "FreeRTOS-Plus 库针对 FreeRTOS 内核实现了附加功能，适用于资源受限的设备。FreeRTOS-Plus-TCP TCP/IP 堆栈经过优化，可以搭配 FreeRTOS 内核使用。此类别中的一些库可与多线程一起使用，也可不与多线程一起使用。FreeRTOS-Plus 库对 FreeRTOS RTOS 内核具有依赖性。<br/>[了解更多](/Documentation/03-Libraries/02-FreeRTOS-plus/01-Introduction)"
  - id: 8
    value: FreeRTOS Core 库入门
  - id: 9
    value: "FreeRTOS Core 库可实现基于开放标准的连接、安全性和相关功能，适用于构建连接到云端的基于微控制器的智能设备。与 FreeRTOS-Plus 库不同，FreeRTOS Core 库除了标准 C 库之外没有其他依赖项，因此不依赖 FreeRTOS RTOS 内核。<br/>[了解更多](/Documentation/03-Libraries/03-FreeRTOS-core/01-Introduction)"
  - id: 10
    value: AWS IoT 库入门
  - id: 11
    value: "AWS IoT 库提供用于连接到 AWS IoT 服务的客户端，包括安全的 over-the-air 更新功能。此类别中的所有库都适用于构建基于微控制器的 IoT 设备。另请参阅[AWS IoT 参考集成](aws-reference-integrations)。<br/>[了解更多](iot-libraries)"
  - id: 12
    value: Quick Connect 板入门
  - id: 13
    value: "Quick Connect 板是我们与合作伙伴制造商联合生产的，开箱即用，5 分钟之内即可连接到云端。您只需要一台计算机、特定于板的数据线和 WiFi 网络，无需 AWS 等云服务账户。连接成功后，即可查看微控制器传感器的数据，然后按照教程添加新的传感器和执行器控件。<br/>[了解更多](/Why-FreeRTOS/Quick-connect)"
  - id: 14
    value: AWS 参考集成入门
  - id: 15
    value: "AWS 参考集成是预集成的 FreeRTOS 项目，已移植到基于微控制器的评估板上，可用来演示端到端云连接。AWS 参考集成有助于节省数月的开发工作并缩短上市时间。<br/>[了解更多](aws-reference-integrations)"
  - id: 16
    value: FreeRTOS Labs 入门
  - id: 17
    value: "FreeRTOS Labs 包括目前正在开发但尚未准备发布的库，以及可能发展成为 FreeRTOS 产品的实验项目和库。<br/>[了解更多](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction)"
  - id: 18
    value: FreeRTOS 论坛
  - id: 19
    value: "与 FreeRTOS 社区和 Amazon Web Services (AWS) 互动并获取支持。<br/>[了解更多](https://forums.freertos.org/)"
  - id: 20
    value: 常见问题
  - id: 21
    value: "常见问题 <br/>[了解更多](/Why-FreeRTOS/FAQs)"
---

欢迎下载最新版 FreeRTOS 和长期支持 (LTS) 包，如下所示。 

[常见问题](/Why-FreeRTOS/FAQs/Github-repository-structure-and-versioning/#how-are-freertos-git-repositories-structured)部分解释了单个库和库包之间的区别， 
并提供了[各个库存储库的链接](/Why-FreeRTOS/FAQs/Github-repository-structure-and-versioning/#how-do-i-obtain-and-use-individual-freertos-libraries)。

```jsx
<InfoBlock
  title="0"
  content="1"
  variant="download-primary"
  version="202406.05"
/>
```

如需查看[已知问题和安全更新](#当前版本的已知问题)等信息，请跳转至页面底部。


## 安全更新

请参阅[安全更新](/security/security_updates.html)页面。


## 后续步骤

FreeRTOS 的开发活动已从 SVN 迁移到 GitHub，现可直接 
在我们的 [GitHub 组织](https://github.com/FreeRTOS)页面上找到。从 GitHub 下载 
[之前版本](https://github.com/FreeRTOS/FreeRTOS/releases) 的 FreeRTOS，可以是标准 
zip (.zip) 文件，也可以是自解压 zip (.exe) 文件。解压源代码，同时确保不改动 
文件夹结构。请阅读以下文档，以了解目录结构 
并快速入门！

```jsx
<InfoBlock 
  title="4"
  content="5"
/>
<InfoBlock 
  title="6"
  content="7"
/>
<InfoBlock 
  title="8"
  content="9"
/>
<InfoBlock 
  title="10"
  content="11"
/>
<InfoBlock 
  title="12"
  content="13"
/>
<InfoBlock 
  title="14"
  content="15"
/>
<InfoBlock 
  title="16"
  content="17"
/>
<InfoBlock 
  title="18"
  content="19"
/>
<InfoBlock 
  title="20"
  content="21"
/>
```

  
## 安全更新

请参阅[安全更新](/Security/03-Vulnerabilities)页面。

## 升级说明

* [从 FreeRTOS V10.4.6 升级到 V10.5.0](/Documentation/04-Roadmap-and-release-note/02-Release-notes/08-FreeRTOS-V10.5.0)
* [从 FreeRTOS V10.4.5 升级到 V10.4.6](/Documentation/04-Roadmap-and-release-note/02-Release-notes/07-FreeRTOS-V10.4.6)
* [从 FreeRTOS V10.4.4 升级到 V10.4.5](/Documentation/04-Roadmap-and-release-note/02-Release-notes/06-FreeRTOS-V10.4.5)
* [从 FreeRTOS V10.3.0 升级到 V10.4.x](/Documentation/04-Roadmap-and-release-note/02-Release-notes/05-FreeRTOS-V10.4.x)
* [从 FreeRTOS V10.2.1 升级到 V10.3.0](/Documentation/04-Roadmap-and-release-note/02-Release-notes/04-FreeRTOS-V10.3.0)
* [升级到 FreeRTOS 版本 10](/Documentation/04-Roadmap-and-release-note/02-Release-notes/03-FreeRTOS-V10)
* [升级到 FreeRTOS 版本 9](/Documentation/04-Roadmap-and-release-note/02-Release-notes/02-FreeRTOS-V9)
* [从 FreeRTOS V7.x.x 升级到 FreeRTOS V8.x.x](/Documentation/04-Roadmap-and-release-note/02-Release-notes/01-FreeRTOS-V8)


## 当前版本的已知问题

### 遗留问题

#### Coldfire V2 CodeWarrior 移植

Coldfire V2 CodeWarrior 代码无法在基于 Eclipse 的最新 CodeWarrior 工具中运行。修复方法 
已发布在[支持论坛](https://forums.freertos.org/t/starting-a-simple-task/5743)（第 4 个帖子）， 
并将在适当的时候纳入主版本。


#### Coldfire V1 CodeWarrior 移植

Coldfire V1 CodeWarrior 项目无法自动更新到更高版本的 CodeWarrior， 
除非先从 FreeRTOS/源目录中删除所有不必要的文件。 
有关详细信息，请参阅[此支持帖](https://forums.freertos.org/t/project-from-scrap-problems-mcf51cn/653)。 


#### MSP430 CrossWorks 和 GCC 演示

CrossWorks 演示尚未更新，无法使用 CrossWorks V2.0 或更高版本。GCC 演示尚未更新， 
无法使用最新版本的 MSPGCC 编译器。


#### AVR32 演示

目前无法构建 AVR32 的 IAR Embedded Workbench 演示 
（如果使用的是较新版本的 IAR 工具链）。该问题由编译器头文件中的宏名称更改导致。 


#### Silicon Labs SDCC 移植

很遗憾，这些移植不适用于最新版本的编译器。目前来看，生成该移植的编译器版本相当陈旧， 
这在移植文档页面上有说明。

