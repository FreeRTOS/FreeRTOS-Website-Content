---
title: "FreeRTOS V10"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 路线图和版本说明
description: 关于 FreeRTOS V10 的信息
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


### 向后兼容性

FreeRTOS V10 包含一份新的源文件 stream_buffers.c，
并且出于一致性考虑，已将 StackMacros.h 头文件重新命名为 stack_macros.h。
但是，**V10 是 FreeRTOS V9.x.x 的直接替代品**，
因为新的源文件仅用于启用新功能，
而且 V10 还提供了两版头文件，一版采用旧名称，另一版则采用新名称。
stack_macros.h 仅在 FreeRTOS 内核代码内部使用。


### 流缓冲区和消息缓冲区简介

FreeRTOS V10 包含两项重要新功能：[流缓冲区和消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)。

流缓冲区是一种进程间通信 (IPC) 原语，
针对只有一个读取器和一个写入器的场景进行了优化，
例如将数据流从中断服务程序 (ISR) 发送到 RTOS 任务，
或从一个处理器核心发送到另一个处理器核心。

消息缓冲区基于流缓冲区构建。流缓冲区发送
连续的字节流，而消息缓冲区则发送长度不一的离散消息
。


### 其他变更

请参阅[变更历史记录](/Documentation/04-Roadmap-and-release-note/02-Release-notes/00-Release-history)，获取有关新移植
以及其他增强功能的更多详情。
  
