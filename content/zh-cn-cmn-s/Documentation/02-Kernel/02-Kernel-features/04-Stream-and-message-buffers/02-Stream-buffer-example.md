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

通过流缓冲区，可以将字节流从中断服务程序传递到任务，
也可以将其从一项任务传递到另一项任务。字节流可以是任意长度，不一定
有开头或结尾。可以一次写入任意数量的字节，
也可以一次读取任意数量的字节。数据通过复制的方式传递：数据由发送方复制到缓冲区中，
然后由接收方从缓冲区中读取。

与大多数其他 FreeRTOS 通信原语不同，流缓冲区针对单读取器单写入器场景进行了优化，
例如可将数据从中断服务程序传递到任务，
或从双核 CPU 上的一个微控制器内核传递到另一个微控制器内核。

要启用流缓冲区功能，可以在构建中纳入 FreeRTOS/source/stream_buffer.c
源文件。

流缓冲区实现使用[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)。因此，
调用将调用任务置于阻塞状态的流缓冲区 API 函数可以更改
调用任务的通知状态和值。

**重要提示**：与其他 FreeRTOS 对象都不同的是，流缓冲区的实现
（[消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example)的实现也是如此，因为消息缓冲区是建立在流缓冲区之上的）
假定只有一项任务或中断会写入缓冲区（写入器），
而且只会从缓冲区（读取器）中读取一项任务或中断。可以写入和读取不同的任务或中断，这样是安全的，
但与其他 FreeRTOS 对象不同，
拥有多个不同的写入器或多个不同的读取器是不安全的。如果有多个不同的写入器，
则应用程序编写者必须将对写入 API 函数
（例如 [xStreamBufferSend()](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/03-xStreamBufferSend)）的每次调用置于临界区内，并将发送阻塞时间设置为 0。
同样，如果有多个不同的读取器，则应用程序编写者必须
将对读取 API 函数（例如 [xStreamBufferReceive()](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/05-xStreamBufferReceive)）的每次调用置于临界区内，
并将接收阻塞时间设置为 0。

### 入门指南

**FreeRTOS/Demo/Common/Minimal/StreamBufferInterrupt.c** 源文件
提供了经过大量注释的示例，说明如何使用流缓冲区将数据
从中断服务程序传递到任务。

有关流缓冲区相关 API 函数的列表，请参阅用户文档的[流缓冲区部分](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)，
许多示例中都包含演示所使用函数的代码片段。

## 阻塞读取和触发级别

[xStreamBufferReceive()](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/05-xStreamBufferReceive) 用于从 RTOS
任务的流缓冲区中读取数据。[xStreamBufferReceiveFromISR()](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/06-xStreamBufferReceiveFromISR)) 用于
从中断服务程序 (ISR) 的流缓冲区中读取数据。

xStreamBufferReceive() 允许指定阻塞时间。在任务使用 xStreamBufferReceive() 从恰好为空的流缓冲区中读取数据时，
如果指定了非零阻塞时间，
则该任务将进入阻塞状态（因此不会消耗任何 CPU 时间，且其他任务可以运行），
直到流缓冲区中有指定数量的数据可用，或者阻塞时间到期。在等待数据的任务
从阻塞状态中移除之前，流缓冲区中需要有一定数量的数据可用，
这个数据量称为流缓冲区的触发级别。例如：

- 如果任务在读取触发级别为 1 的空流缓冲区时被阻塞，
  则向缓冲区写入单个字节或任务的阻塞时间到期时，
  该任务将被解除阻塞。
- 如果任务在读取触发级别为 10 的空流缓冲区时被阻塞，
  则在流缓冲区至少包含 10 个字节或任务的阻塞时间到期之前，
  该任务将不会被解除阻塞。

如果读取任务的阻塞时间在达到触发级别之前过期，那么该任务仍将
接收实际可用的字节数。

**注意：**

- 不可将触发级别设置为 0。如果试图
  将触发级别设置为 0，实际上使用的触发级别为 1。

- 也不可将触发级别指定为大于
  流缓冲区大小的值。

流缓冲器的触发级别是在[创建](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/01-xStreamBufferCreate)时设置的，
可以使用 [xStreamBufferSetTriggerLevel()](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/10-xStreamBufferSetTriggerLevel) API 函数进行更改。

## 阻塞写入

[xStreamBufferSend()](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/03-xStreamBufferSend)) 用于将数据从 RTOS
任务发送到流缓冲区。[xStreamBufferSendFromISR()](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/04-xStreamBufferSendFromISR)) 用于将数据
从中断服务程序 (ISR) 发送到流缓冲区。

在任务使用 xStreamBufferSend()
写入恰好已满的流缓冲区时，如果指定了非零阻塞时间，则该任务
将进入阻塞状态（因此不消耗任何 CPU 时间，且其他任务可以
运行），直到流缓冲区中出现可用空间，或者
阻塞时间到期。

## 发送和接收完整回调

[另请参阅[关于使用消息缓冲区进行双核心-核心间通信的博文。](/Community/Blogs/2020/simple-multicore-core-to-core-communication-using-freertos-message-buffers)]

流缓冲区和消息缓冲区会在每次发送和接收操作完成后执行回调：

- 使用 xStreamBufferCreate() 和 xMessageBufferCreate() API 函数
  （及其静态分配的等效函数）创建的流缓冲区和消息缓冲区共享相同的回调函数，可使用
  sbSEND_COMPLETED() 和 sbRECEIVE_COMPLETED() 宏定义这些回调函数。以下各节会详细介绍这些宏。

- 使用 xStreamBufferCreateWithCallback() 和 xMessageBufferCreateWithCallback() API 函数
  （及其静态分配的等效函数）创建的流缓冲区和消息缓冲区各自具有独特的回调函数。

### sbSEND_COMPLETED()（和 sbSEND_COMPLETED_FROM_ISR()）

sbSEND_COMPLETED() 是将数据写入流缓冲区时（在 FreeRTOS API 函数内部）调用的宏，
该流缓冲区使用 xStreamBufferCreate() 或 xStreamBufferCreateStatic()
API 创建。它需要一个参数，即已更新的流缓冲区的句柄。

默认情况下（即应用程序编写者未提供自己的宏实现），
sbSEND_COMPLETED() 会检查流缓冲区上是否存在等待数据的阻塞任务；
如果存在，则将该任务从阻塞状态中移除。

应用程序编写者可以通过
在 FreeRTOSConfig.h 中提供自己的 sbSEND_COMPLETED() 实现来更改此默认行为。此操作非常适用于
使用流缓冲区在多核处理器上的核心之间传递数据。在
这种情况下，可以实现 sbSEND_COMPLETED() 以在其他 CPU 核心中生成中断，
然后中断服务程序可以使用
xStreamBufferSendCompletedFromISR() API 函数检查是否存在等待数据的任务，
并在必要时解除阻塞。

FreeRTOS/Demo/Common/Minimal/MessageBufferAMP.c 源文件提供了
详细说明该场景的示例。

如果您需要每个流缓冲区都有自己的“发送完成”行为，
请使用 xStreamBufferCreateStaticWithCallback() 或 xStreamBufferCreateStaticWithCallback() API 函数
创建流缓冲区。

### sbRECEIVE_COMPLETED()（和 sbRECEIVE_COMPLETED_FROM_ISR()）

sbRECEIVE_COMPLETED() 是 sbSEND_COMPLETED() 的接收等效函数。在
从流缓冲区读取数据时，会（在 FreeRTOS API 函数内部）调用此函数
。默认情况下（即应用程序编写者未提供自己的宏实现），
该宏会检查流缓冲区上是否存在等待缓冲区内空间可用的阻塞任务；
如果存在，则将该任务
从阻塞状态中移除。

与 sbSEND_COMPLETED() 一样，应用程序编写者
可以通过
在 FreeRTOSConfig.h 中提供替代实现来更改 sbRECEIVE_COMPLETED() 的默认行为。如果您需要每个流缓冲区都有自己的“接收完成”行为，
请使用 xStreamBufferCreateWithCallback() 或 xStreamBufferCreateStaticWithCallback() API 函数
创建流缓冲区。
