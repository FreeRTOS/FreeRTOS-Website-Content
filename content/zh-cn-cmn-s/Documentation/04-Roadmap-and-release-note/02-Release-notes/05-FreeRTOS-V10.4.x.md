---
title: "从 FreeRTOS V10.3.0 升级到 V10.4.x"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 路线图和版本说明
description: 关于从 FreeRTOS V10.3.0 升级到 V10.4.x 的信息
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS 简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---


### 关于未来版本控制的说明：

到目前为止，FreeRTOS zip 文件版本都带有所含内核的版本号。
例如，FreeRTOSv10.4.0\.zip 表示所含的 FreeRTOS 内核为 10.4.0 版。然而，内核并不是
zip 文件中包含的唯一单独进行版本控制的库，而且在今后的版本中，
zip 文件中库的数量会不断增加。因此，为了更好地反映 zip 文件实际上包含了集成在一起的一系列库，
今后的版本将使用日期戳版本
而不是内核版本。


### 向后兼容性

FreeRTOS V10.4.0 是 FreeRTOS V10.3.x 的直接替代品，适用于
除支持内存保护单元 (MPU) 以外的所有移植。请参阅记录 FreeRTOS MPU
移植[的页面了解升级信息](/Security/04-FreeRTOS-MPU-memory-protection-unit#upgrading-to-FreeRTOS-10.4.0)。

Tracealyzer 用户须知：FreeRTOS V10.4.0 中的任务通知功能
向后兼容 FreeRTOS V10.3.x 中的功能，但跟踪记录宏除外。Tracealyzer 用户需要
将其跟踪记录器代码更新为 FreeRTOS V10.4.0 版本中提供的代码，
并在其 trcConfig.h 文件中将 TRC_CFG_FREERTOS_VERSION 设置为 TRC_FREERTOS_VERSION_10_4_0。

请参阅[变更历史记录](/Documentation/04-Roadmap-and-release-note/02-Release-notes/00-Release-history)，
了解有关新移植和其他增强功能的详细信息。


### 功能增强

#### 直达任务通知增强

在 FreeRTOS V10.4.0 版本前，
每个任务只有单条[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)。
从 FreeRTOS V10.4.0 开始，每个任务都有[用户可定义的任务通知数组](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configtask_notification_array_entries)。

### 其他变更

#### 影响巨大的 Linux 移植变更

William Davy 提供的旧版 Linux FreeRTOS 移植已变更为
David Vrabel 提供的增强型移植。新版本修复了长期存在调度器错误，
即上下文切换过程中两个任务可能同时执行。请参阅  [Linux 模拟器文档](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Linux/FreeRTOS-simulator-for-Linux)
了解更多信息。


#### 格式化变更

代码格式化现已自动化，以增加
Git 中的协作开发。自动格式化代码与
原来的格式化惯例不尽相同。值得注意的是，现已使用空格
代替制表符。
