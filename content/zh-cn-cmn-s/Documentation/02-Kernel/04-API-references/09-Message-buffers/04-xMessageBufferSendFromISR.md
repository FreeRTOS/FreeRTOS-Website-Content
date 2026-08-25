---
title: xMessageBufferSendFromISR()
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
size_t xMessageBufferSendFromISR( MessageBufferHandle_t xMessageBuffer,
                                  const void *pvTxData,
                                  size_t xDataLengthBytes,
                                  BaseType_t *pxHigherPriorityTaskWoken );
```

中断安全版本的 API 函数，
该函数向[消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example)发送离散消息。消息长度只要满足缓冲区可用空间即可，
消息会被复制到缓冲区中。

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
并使用阻塞时间 0。

使用 [xMessageBufferSend()](/Documentation/02-Kernel/04-API-references/09-Message-buffers/03-xMessageBufferSend) 往任务的消息缓冲区写入消息。xMessageBufferSendFromISR()用于
往中断服务程序 (ISR) 的消息缓冲区写入
数据。

通过将 FreeRTOS/source/stream_buffer.c 源文件包含在构建中
来启用消息缓冲区功能（因为消息缓冲区使用流缓冲区）。


**参数：** 

- *xMessageBuffer*

  要将消息发送到的消息缓冲区的句柄。

- *pvTxData*

  指向要复制到信息缓冲区的消息的指针。

- *xDataLengthBytes*

  消息长度。也就是从 pvTxData 复制到消息缓冲区的字节数。 
  当消息写入消息缓冲区时，还会额外写入 sizeof( size_t ) 字节
  以存储消息的长度。sizeof( size_t ) 在 32 位架构上通常为 4 字节，
  因此在大部分 32 位架构上将 xDataLengthBytes 设置为 20 时，会将消息缓冲区中的可用空间减少 24 字节
  （20 字节的消息数据和 4 字节用来保存消息长度）。

- *pxHigherPriorityTaskWoken*

  （这是一个可选参数，可以设置为 NULL。）消息缓冲区上可能会有一个任务被阻塞，
  等待数据。调用 xMessageBufferSendFromISR() 可以使数据可用，
  从而使正在等待数据的任务离开阻塞状态。如果调用
  xMessageBufferSendFromISR() 导致任务离开阻塞状态，并且
  被解除阻塞的任务的优先级高于当前正在执行的任务（被中断的任务），那么
  xMessageBufferSendFromISR() 将从内部把 \*pxHigherPriorityTaskWoken 设置为 pdTRUE。如果
  xMessageBufferSendFromISR() 将此值设置为 pdTRUE，那么通常应在
  退出中断之前执行上下文切换。这将确保中断直接返回到最高优先级的就绪状态任务。
  在将 \*pxHigherPriorityTaskWoken 传递给函数之前，
  应将其设置为 pdFALSE。有关示例，请参阅下面的代码示例。


**返回：** 

实际写入消息缓冲区的字节数。如果
消息缓冲区可用空间不足，无法存储消息，
则返回 0，否则返回 xDataLengthBytes。 


**用法示例：**

```c
/* A message buffer that has already been created. */
MessageBufferHandle_t xMessageBuffer;

void vAnInterruptServiceRoutine( void )
{
size_t xBytesSent;
char *pcStringToSend = "String to send";
BaseType_t xHigherPriorityTaskWoken = pdFALSE; /* Initialised to pdFALSE. */

    /* Attempt to send the string to the message buffer. */
    xBytesSent = xMessageBufferSendFromISR( xMessageBuffer,
                                            ( void * ) pcStringToSend,
                                            strlen( pcStringToSend ),
                                            &xHigherPriorityTaskWoken );

    if( xBytesSent != strlen( pcStringToSend ) )
    {
        /* The string could not be added to the message buffer because there was
           not enough free space in the buffer. */
    }

    /* If xHigherPriorityTaskWoken was set to pdTRUE inside
       xMessageBufferSendFromISR() then a task that has a priority above the
       priority of the currently executing task was unblocked and a context
       switch should be performed to ensure the ISR returns to the unblocked
       task. In most FreeRTOS ports this is done by simply passing
       xHigherPriorityTaskWoken into taskYIELD_FROM_ISR(), which will test the
       variables value, and perform the context switch if necessary. Check the
       documentation for the port in use for port specific instructions. */
    taskYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
```
