---
title: xMessageBufferReceiveFromISR()
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
size_t xMessageBufferReceiveFromISR( MessageBufferHandle_t xMessageBuffer,
                                     void *pvRxData,
                                     size_t xBufferLengthBytes,
                                     BaseType_t *pxHigherPriorityTaskWoken );
```

中断安全版本的 API 函数，用于
从[消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example)接收离散消息。消息长度可变，
从缓冲区中复制出来。

**注意**：与其他 FreeRTOS 对象都不同的是，流缓冲区的实现
（消息缓冲区的实现也是如此，因为消息缓冲区是建立在流缓冲区之上的）
假定只有一个任务或中断将写入
缓冲区（写入器），只有一个任务或中断会从
缓冲区读取（读取器）。写入和读取
不同的任务或中断是安全的，但与其他FreeRTOS对象不同，
有多个不同的写入或多个不同的读取是不安全的。如果
有多个不同的写入器，那么应用程序写入器必须
将每个调用放置到临界区中的一个写入 API 函数（如 xStreamBufferSend()）中，
并使用发送阻塞时间 0。同样，如果有多个不同的读取器，
那么应用程序写入器必须把对读取 API 函数（如 xStreamBufferReceive()）的每个调用放在一个临界区内，
并将接收阻塞时间设置为0。

使用 [xMessageBufferReceive()](/Documentation/02-Kernel/04-API-references/09-Message-buffers/05-xMessageBufferReceive) 从任务的消息缓冲区读取数据。使用
xMessageBufferReceiveFromISR () 从中断服务程序 (ISR) 的消息缓冲区
读取数据。

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

- *pxHigherPriorityTaskWoken*

  （这是一个可选参数，可以设置为 NULL。）消息缓冲区上可能会有一个任务被阻塞，
  等待空间变为可用。调用 xMessageBufferReceiveFromISR()
  可以腾出空间，从而使正在等待空间的任务脱离阻塞状态。
  如果调用 xMessageBufferReceiveFromISR () 导致任务结束阻塞状态，并且
  被解除阻塞的任务的优先级高于当前正在执行的任务（被中断的任务），那么
  xMessageBufferReceiveFromISR() 将从内部把 *pxHigherPriorityTaskWoken 设置为 pdTRUE。如果
  如果 xMessageBufferReceiveFromISR() 将此值设置为 pdTRUE，那么通常应在
  退出中断之前执行上下文切换。这将确保中断直接返回优先级最高的就绪状态任务。 
  在将 *pxHigherPriorityTaskWoken 传递给函数之前，
  应将其设置为 pdFALSE。有关示例，请参阅下面的代码示例。


**返回：** 

从消息缓冲区读取的消息的长度（如有），以字节为单位。


**用法示例：**

```c
/* A message buffer that has already been created. */
MessageBuffer_t xMessageBuffer;

void vAnInterruptServiceRoutine( void )
{
uint8_t ucRxData[ 20 ];
size_t xReceivedBytes;
BaseType_t xHigherPriorityTaskWoken = pdFALSE;  /* Initialised to pdFALSE. */

    /* Receive the next message from the message buffer. */
    xReceivedBytes = xMessageBufferReceiveFromISR( xMessageBuffer,
                                                  ( void * ) ucRxData,
                                                  sizeof( ucRxData ),
                                                  &xHigherPriorityTaskWoken );

    if( xReceivedBytes > 0 )
    {
        /* A ucRxData contains a message that is xReceivedBytes long. Process
           the message here.... */
    }

    /* If xHigherPriorityTaskWoken was set to pdTRUE inside
       xMessageBufferReceiveFromISR() then a task that has a priority above the
       priority of the currently executing task was unblocked and a context
       switch should be performed to ensure the ISR returns to the unblocked
       task. In most FreeRTOS ports this is done by simply passing
       xHigherPriorityTaskWoken into taskYIELD_FROM_ISR(), which will test the
       variables value, and perform the context switch if necessary. Check the
       documentation for the port in use for port specific instructions. */
    taskYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
```
