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

[[流缓冲区和消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)]

[**自 FreeRTOS V10.0.0 开始支持此功能**](/Documentation/04-Roadmap-and-release-note/02-Release-notes/01-FreeRTOS-V8)

## 引言

消息缓冲区允许长度可变的离散消息从中断服务程序传递至
一个任务，或从一个任务传递至另一个任务。例如，长度为 10、20 和 123 字节的消息
都可以在同一个消息缓冲区写入或读取
。与使用[流缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example)不同的是，
长度为 10 个字节的消息只能作为 10 个字节的消息读取，而不能
以单独的字节读取。消息缓冲区构建在流缓冲区之上（即它们使用
流缓冲区实现）。

数据通过复制的方式在消息缓冲区中传递：数据由发送方复制到
缓冲区中，然后由接收方从缓冲区中读取。

另请参阅 [configMESSAGE_BUFFER_LENGTH_TYPE](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configmessage_buffer_length_type)
配置参数的定义。

与大多数其他 FreeRTOS 通信原语、流缓冲区不同，
消息缓冲区针对单读取器单写入器场景进行了优化，例如可将数据从中断服务程序传递到任务，
或从双核 CPU 上的一个微控制器内核传递到另一个微控制器内核。

要启用消息缓冲区功能，可以在构建中纳入 FreeRTOS/source/stream_buffer.c
源文件。

消息缓冲区实现使用[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)。因此，
调用将调用任务置于阻塞状态的消息缓冲区 API 函数可以更改
调用任务的通知状态和值。

**重要提示**：与其他 FreeRTOS 对象都不同的是，流缓冲区的实现
（[消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example)的实现也是如此,
因为消息缓冲区是建立在流缓冲区之上的）
假定只有一项任务或中断会写入缓冲区（写入器），而且只会从缓冲区（读取器）中
读取一项任务或中断。可以写入和读取不同的任务或中断，这样是安全的，
但与其他 FreeRTOS 对象不同，拥有多个不同的写入器或多个不同的读取器是不安全的。
如果有多个不同的写入器，则应用程序编写者必须将对写入
API 函数（例如 [xStreamBufferSend()](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/03-xStreamBufferSend)）的每次调用置于临界区内，
并将发送阻塞时间设置为 0。同样，如果有多个不同的读取器，则应用程序编写者必须
将对读取 API 函数（例如 [xStreamBufferReceive()](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/05-xStreamBufferReceive)）的每次调用置于临界区内，
并将接收阻塞时间设置为 0。

## 入门指南

**FreeRTOS/Demo/Common/Minimal/MessageBufferAMP.c** 源文件
提供了经过大量注释的示例，说明如何使用消息缓冲区将可变长度数据
从多核 MCU 的一个 MCU 核心传递到另一个 MCU 核心。这是一个相当
高级的场景，但创建消息缓冲区，向缓冲区发送和从缓冲区接收的机制
与更简单的单核场景中的机制是相同的，
与演示不同，
此场景不需要覆盖 [sbSEND_COMPLETE()](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example#send-complete-and-receive-complete-callbacks) 宏。

有关消息缓冲区相关 API 函数的列表，请参阅用户文档的[消息缓冲区部分](/Documentation/02-Kernel/04-API-references/09-Message-buffers/00-RTOS-message-buffer-API)，
许多示例中都包含演示所使用函数的代码片段。

## 设置消息缓冲区大小

要使消息缓冲区能够处理可变大小的消息，在将消息写入消息缓冲区之前，需将每条消息的长度
写入消息缓冲区（通过 FreeRTOS API 函数在内部完成）。
长度存储在变量中，其类型由 configMESSAGE_BUFFER_LENGTH_TYPE 常量
（位于 FreeRTOSConfig.h 中）设置。如果未定义，则 configMESSAGE_BUFFER_LENGTH_TYPE 默认为 size_t 类型。
在 32 位架构中，size_t 通常为 4 字节。比如，
将 10 字节的消息写入消息缓冲区时，实际上会占用 14 字节的缓冲区空间。
configMESSAGE_BUFFER_LENGTH_TYPE 为 4 字节。同样，将 100 字节的消息写入消息缓冲区时，
实际上会占用 104 字节的缓冲区空间。

## 阻塞读取和写入

[xMessageBufferReceive()](/Documentation/02-Kernel/04-API-references/09-Message-buffers/05-xMessageBufferReceive)) 用于从 RTOS 任务的消息缓冲区读取数据。
[xMessageBufferReceiveFromISR()](/Documentation/02-Kernel/04-API-references/09-Message-buffers/06-xMessageBufferReceiveFromISR)) 用于
从中断服务程序(ISR) 的消息缓冲区读取数据。[xMessageBufferSend()](/Documentation/02-Kernel/04-API-references/09-Message-buffers/03-xMessageBufferSend)) 用于
将数据发送到 RTOS 任务的消息缓冲区。[xMessageBufferSendFromISR()](/Documentation/02-Kernel/04-API-references/09-Message-buffers/04-xMessageBufferSendFromISR))
用于将数据发送到中断服务程序 (ISR) 的消息缓冲区。

在任务使用 xMessageBufferReceive()  从恰好为空的消息缓冲区中读取数据时，
如果指定了非零阻塞时间，则该任务将进入阻塞状态（因此不会消耗任何 CPU 时间，
且其他任务可以运行），直到消息缓冲区中出现可用数据，或者阻塞时间到期。

在任务使用 xMessageBufferSend() 写入恰好已满的消息缓冲区时，
如果指定了非零阻塞时间，则该任务
进入阻塞状态（因此它不会消耗任何 CPU 时间，且其他任务可以运行）
直到消息缓冲区中出现可用空间，或者阻塞时间
到期。

## 发送并接收完整宏

由于消息缓冲区是基于流缓冲区构建的，因此 sbSEND_COMPLETE() 和 sbRECEIVE_COMPLETE() 宏的行为
与[流缓冲区页面](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example)描述的行为完全相同。
