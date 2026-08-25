---
title: "FreeRTOS 流缓冲区和消息缓冲区"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 流缓冲区和消息缓冲区
relatedLinks:
  - title: API 引用 - 流缓冲区
    link: /Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API/
  - title: API 引用 - 消息缓冲区
    link: /Documentation/02-Kernel/04-API-references/09-Message-buffers/00-RTOS-message-buffer-API/
---

[**自 FreeRTOS V10.0.0 开始支持此功能**](/Documentation/04-Roadmap-and-release-note/02-Release-notes/01-FreeRTOS-V8)

## 简介

流缓冲区指的是 [RTOS 任务](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/00-Tasks-and-co-routines/)
到 RTOS 任务以及中断到任务的通信原语。与其他大多数 FreeRTOS 通信原语不同，流缓冲区
针对单个读取者单个写入者场景进行了优化，例如
将数据从中断服务程序传递到任务，或在双核 CPU 上从一个微控制器核心传递到另一个核心。数据
通过复制的方式传递：数据由发送者复制到缓冲区中，然后由读取者复制出缓冲区。

流缓冲区传递连续的字节流。消息缓冲区传递大小可变但离散的消息。
消息缓冲区使用流缓冲区进行数据传输。

**重要提示**：与其他 FreeRTOS 对象都不同的是，流缓冲区的
实现（[消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example)的实现也是如此，
因为消息缓冲区构建在流缓冲区之上）假定只有一个任务或
中断会写入缓冲区（写入者），
并且只有一个任务或中断将从缓冲区读取（读取者）。写入者和读取者可以是不同的任务或中断，这样是安全的，
但不同于
其他 FreeRTOS 对象，具有多个写入者或读取者
并不安全。如果有多个不同的写入者，
则应用程序编写者必须将每个
编写 API 函数的调用（如 [xStreamBufferSend()](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/03-xStreamBufferSend)）放在临界区中，
并以 0 为发送阻塞时间。同样，
如果存在多个不同的读取者，那么应用程序编写者必须将
每个读取 API 函数的调用（如 [xStreamBufferReceive()](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/05-xStreamBufferReceive)）
放在临界区中，并以 0 为接收阻塞时间。

### 延伸阅读

以下页面更详细地描述了流缓冲区和消息缓冲区，
还举例说明如何利用这些缓冲区分别实现中断到任务的通信以及处理器核心到处理器核心的通信。

[有关流缓冲区的更多信息......](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example)

[有关消息缓冲区的更多信息......](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example)

[使用消息缓冲区进行内核到内核通信的博客......](/Community/Blogs/2020/simple-multicore-core-to-core-communication-using-freertos-message-buffers)
