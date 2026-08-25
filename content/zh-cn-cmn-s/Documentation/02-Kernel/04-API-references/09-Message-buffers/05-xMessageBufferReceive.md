---
title: xMessageBufferReceive()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 消息缓冲区 API](/Documentation/02-Kernel/04-API-references/09-Message-buffers/00-RTOS-message-buffer-API)]

message_buffer.h

```c
size_t xMessageBufferReceive( MessageBufferHandle_t xMessageBuffer,
                              void *pvRxData,
                              size_t xBufferLengthBytes,
                              TickType_t xTicksToWait );
```

从 RTOS [消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example)接收离散消息。消息长度可变，
并且从缓冲区中复制出来。

**注意**：与其他 FreeRTOS 对象都不同的是，流缓冲区的实现
（消息缓冲区的实现也是如此，因为消息缓冲区是建立在流缓冲区之上的）
假定只有一个任务或中断将写入
缓冲区（写入器），只有一个任务或中断会从
缓冲区读取（读取器）。写入和读取
不同的任务或中断是安全的，但与其他 FreeRTOS 对象不同，
有多个不同的写入或多个不同的读取是不安全的。如果
有多个不同的写入器，那么应用程序写入器必须
将每个调用放置到临界区中的一个写入 API 函数（如 xStreamBufferSend()）中，
并使用发送阻塞时间 0。同样，如果有多个不同的读取器，
那么应用程序写入器必须把对读取 API 函数（如 xStreamBufferReceive()）的每个调用放在一个临界区内，
并使用接收阻塞时间 0。

使用 xMessageBufferReceive () 从任务中的消息缓冲区读取数据。 
使用 [xMessageBufferReceiveFromISR()](/Documentation/02-Kernel/04-API-references/09-Message-buffers/06-xMessageBufferReceiveFromISR) 从中断服务程序（ISR）的消息缓冲区读取数据
。

通过在构建中包含 FreeRTOS/source/stream_buffer.c 源文件
来启用消息缓冲区功能（因为消息缓冲区使用流缓冲区）。


**参数：** 

- *xMessageBuffer*

  消息缓冲区的句柄，正在接收的信息来自该消息缓存区。

- *pvRxData*

  指向缓冲区的指针，接收到的信息将被复制到该缓冲区中。

- *xBufferLengthBytes*

  由 pvRxData 参数指向的缓冲区的长度。这用于设定
  可接收信息的最大长度。如果 xBufferLengthBytes 空间不足，无法保存下一条消息，
  那么消息将保留在消息缓冲区中，并且将返回 0。

- *xTicksToWait*

  在调用 xMessageBufferReceive() 时，如果消息缓冲区为空，
  则任务应保持阻塞状态等待消息的最长时间。
  如果 xTicksToWait 为零并且消息缓冲区为空，则 xMessageBufferReceive() 将立即返回。阻塞时间
  的单位为滴答周期，因此，它代表的绝对时间取决于
  滴答频率。pdMS_TO_TICKS() 可用于将以毫秒为单位的时间
  转换为以滴答为单位的时间。将 xTicksToWait 设置为 portMAX_DELAY 将
  导致任务无限期等待（不超时），前提是 INCLUDE_vTaskSuspend 在
  FreeRTOSConfig.h 中设置为 1。任务处于“阻塞”状态时不会占用任何 CPU 时间。


**返回：** 

从消息缓冲区读取的消息的长度（以字节为单位）
（如有）。如果在消息写入之前，xMessageBufferSend() 调用超时，
则返回零。如果消息长度大于
xBufferLengthBytes，则消息将保留在消息缓冲区中，
同时返回零。


**用法示例：**

```c
void vAFunction( MessageBuffer_t xMessageBuffer )
{
uint8_t ucRxData[ 20 ];
size_t xReceivedBytes;
const TickType_t xBlockTime = pdMS_TO_TICKS( 20 );

    /* Receive the next message from the message buffer. Wait in the Blocked
       state (so not using any CPU processing time) for a maximum of 100ms for
       a message to become available. */
    xReceivedBytes = xMessageBufferReceive( xMessageBuffer,
                                            ( void * ) ucRxData,
                                            sizeof( ucRxData ),
                                            xBlockTime );

    if( xReceivedBytes > 0 )
    {
        /* A ucRxData contains a message that is xReceivedBytes long. Process
           the message here.... */
    }
}
```
