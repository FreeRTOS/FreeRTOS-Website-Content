---
title: FreeRTOS 内核 v10.4.0 现已可用
created: 2020-09-09 00:00:00.0 UTC
feature: blog
categories:
- 长期支持
authors:
- luciodj
relatedLinks:
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---



本帖由 [Lucio Di Jasio](../author/luciodj) 于 2020 年 9 月 9 日发布

FreeRTOS 内核 v10.4.0 现已可[下载](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)。新版本推出许多 
全新功能，例如直达任务通知功能改进、支持 
内存保护单元 (MPU) 的内核移植功能增强和全新的 Linux 移植。请参阅 
[变更历史](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/master/History.txt)，了解更多 
详情。

  
## 直达任务通知功能增强

在 FreeRTOS V10.4.0 之前的版本中，每项任务都有单一的[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)。 
从 FreeRTOS V10.4.0 起，每项任务现在可以使用 
一个[用户可定义的**任务通知数组](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configtask_notification_array_entries)， 
而且[任务通知 API](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/00-RTOS-task-notifications) 已通过新函数得以扩展。 
这些函数的后缀为 “Indexed”，以便在数组内的任何任务通知上运行。

Tracealyzer 用户须知：FreeRTOS V10.4.0 中的任务通知功能向后兼容 
 FreeRTOS V10.3.x 中的任务通知功能，但追踪记录宏除外。Tracealyzer 用户需要 
将其追踪记录器代码更新为 FreeRTOS V10.4.0 版本中提供的代码， 
并在其 trcConfig.h 文件中将 TRC_CFG_FREERTOS_VERSION 设置为 TRC_FREERTOS_VERSION_10_4_0。


## 改进的 MPU 支持（针对 AMRv7-M 和 ARMv8-M

FreeRTOS V10.4.0）中包括改进的[内存保护单元](../../FreeRTOS-MPU-memory-protection-unit) (MPU)  
支持，适用于 ARMv7-M (ARM Cortex-M3/4/7) 和 ARMv8-M (ARM Cortex-M23/33) RTOS 移植。此外， 
ARMv7-M MPU 移植现在支持拥有 16 个 MPU 区域的设备，而且 Tickless 空闲支持现已 
扩展到 ARMv8-M RTOS 移植。请参阅 
[MPU 支持文档页面](../../FreeRTOS-MPU-memory-protection-unit#upgrading-to-FreeRTOS-10.4.0)， 
了解重要的升级信息。


## 社区贡献的 Linux 移植变更

新的 POSIX 移植层允许 FreeRTOS 在 Linux 主机上运行，运行方式与 Windows 移植层允许 
FreeRTOS 在 Windows 主机上运行的方式相同。 

William Davy 提供的原始 Linux FreeRTOS 移植已替换为增强型移植， 
后者由 David Vrabel 提供。请参阅  [ Linux 模拟器文档页面](../../FreeRTOS-simulator-for-Linux)， 
了解更多信息。


## 向后兼容性

FreeRTOS V10.4.0 是 FreeRTOS V10.3.x 的直接替代品，适用于 
所有移植，[支持内存保护单元 (MPU) 的移植除外](../../FreeRTOS-MPU-memory-protection-unit#upgrading-to-FreeRTOS-10.4.0)。 

如需从先前的 FreeRTOS 内核版本更新项目，请参阅 
[升级至 FreeRTOSv10.4.0](../../FreeRTOS-V10.4.x) 页面。


## 作者简介

![](https://secure.gravatar.com/avatar/9938f7b242eb47e5e8c3f41e0e927283?s=200&d=mm&r=g)   
Lucio 是 Amazon Web Services 的产品经理。过去 20 年里，他在半导体行业 
担任过各种技术和营销职务。作为一个富有见解的高产作者，他发表了 
许多关于嵌入式控制应用程序编程的文章和技术书籍。热爱 
飞行的他又获得了 FAA 和 EASA 私人飞行员执照。    
[查看此作者的文章](../author/luciodj) 


FreeRTOS 论坛：获得来自专家的行业领先支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

