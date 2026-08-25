---
title: 使用 FreeRTOS 消息缓冲区进行简单的多核核心到核心通信
created: 2020-02-18 00:00:00.0 UTC
feature: blog
categories:
- 长期支持
authors:
- ribarry
relatedLinks:
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Richard Barry](../author/ribarry) 于 2020 年 2 月 18 日发布

FreeRTOS 下载包中的 [[STM32H745I](../../STM32H7_Dual_Core_AMP_RTOS_demo) 演示
提供了下面所描述的控制缓冲区方案的工作示例。]

在这篇文章中，我描述了如何
通过 [FreeRTOS 消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)实现基础、轻量级核心到核心通信的方案。
消息缓冲区是无锁循环缓冲区，
可以将不同大小的数据包从单个发送方传递到单个接收方。
消息缓冲区只传输数据，不强加任何
数据必须符合的格式或更高级别的协议。

下述用例中，发送和接收任务是在
非对称多处理器 (AMP) 配置中的多核微控制器 (MCU) 的不同内核
进行——这说明着每个内核只运行自己的 FreeRTOS 实例。唯一的
硬件要求（除了有一个以上的核心）是具有
一个核心可以在另一个核心中产生中断的能力，同时需具有
两个核心都可以访问的内存区域（共享内存）。消息缓冲区
放在上面所述共享内存中，
在每个核心中的应用程序知道该共享内存地址。见图  1。
理想情况下，还将有一个内存保护单元 (MPU)，以确保消息缓冲区只能
通过内核的 [消息
缓冲区 API](/Documentation/02-Kernel/04-API-references/09-Message-buffers/00-RTOS-message-buffer-API) 访问，并且最好将共享内存标记为不可缓存。

![AMP 多核配置中两个核心上的 rtos](/media/2019/multicore_amp_hardware_configuration.png)   
*图 1：硬件拓扑。点击放大。*

以下两个伪代码列表显示 API 函数的结构
用于从消息缓冲区发送和接收信息。可以看出，在这两种情况下，
调用任务可以选择性进入阻塞状态（因此不消耗
任何 CPU 周期）等待操作完成。

```c
xMessageBufferSend()
{
    /* If a time out is specified and there isn't enough
       space in the message buffer to send the data, then
       enter the blocked state to wait for more space. */
    if( time out != 0 )
    {
        while( there is insufficient space in the buffer &&
               not timed out waiting )
        {
            Enter the blocked state to wait for space in the buffer
        }
    }

    if( there is enough space in the buffer )
    {
        write data to buffer
        sbSEND_COMPLETED()
    }
}         
```
*用于将数据发送到流缓冲区的简化伪代码*


```c
xMessageBufferReceive()
{
    /* If a time out is specified and the buffer doesn't
       contain any data that can be read, then enter the
       blocked state to wait for the buffer to contain data. */
    if( time out != 0 )
    {
        while( there is no data in the buffer &&
               not timed out waiting )
        {
            Enter the blocked state to wait for data
        }
    }

    if( there is data in the buffer )
    {
        read data from buffer
        sbRECEIVE_COMPLETED()
    }
}              
```
*用于从流缓冲区读取数据的简化伪代码*
  

如果任务在 xMessageBufferReceive() 中进入阻塞状态以等待缓冲区装入数据， 
则将数据发送到缓冲区必须取消阻塞任务，以便完成运行。当  
xMessageBufferSend() 调用预处理宏 `sbSEND_COMPLETED()` 时，任务取消阻塞。

默认的 `sbSEND_COMPLETED` 实现方式是假设发送任务（或中断）和接收 
任务处于 FreeRTOS 内核相同实例的控制之下，并在同一个 MCU 核心上运行。 
在此 AMP 示例中，发送任务和接收任务由 
 FreeRTOS 内核的两个不同实例控制，并且在不同 MCU 核心上运行，因此默认的 `sbSEND_COMPLETED` 实现 
无法执行（每个 FreeRTOS 内核实例仅了解其控制下的任务）。AMP 场景 
因此需要覆盖 `sbSEND_COMPLETED` 宏（可能还包括 `sbRECEIVE_COMPLETED` 宏， 
参见下文）。执行覆盖操作时只需在项目的  
[FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 文件中提供您自己的实现。重新实现的 `sbSEND_COMPLETED()` 宏可以轻松地触发  
另一个 MCU 核心中的中断。然后，中断处理程序（ISR 
在一个核心中触发，在另外一个核心中执行）必须完成任务，否则 
`sbSEND_COMPLETE` 实现将默认完成任务，即在任务等待从现已包含数据的消息缓冲区 
接收数据时取消任务阻塞。ISR 取消任务阻塞是通过将消息缓冲区的 
句柄作为参数传递至 `xMessageBufferSendCompletedFromISR()` 函数。此序列由 
图 2 中的编号箭头所示，其中发送和接收任务在不同的 MCU 核心上：

1. 接收任务尝试从空消息缓冲区读取，并进入阻塞状态以等待 
   数据抵达。
2. 发送任务将数据写入消息缓冲区。
3. `sbSEND_COMPLETED()` 在正在执行接收任务的核心中触发中断。
4. 中断服务程序调用 `xMessageBufferSendCompletedFromISR()` 以取消接收任务的阻塞， 
   而接收任务现在可以从缓冲区读取消息，因为缓冲区不再为空。

![AMP 多核配置中两个核心上的 rtos](/media/2019/multicore_amp_single_message_buffer.png)   
*图 2：编号箭头对应于上面的编号列表，描述通过消息缓冲区传输一个
数据项。**点击放大**。*

在只有一个消息缓冲区时，很容易将消息缓冲区的句柄传递到 `xMessageBufferSendCompletedFromISR()`， 
但请考虑存在两个或更多消息缓冲区的情况： 
此时 ISR 必须首先确定哪个消息缓冲区包含数据。如果消息缓冲区数量较少，可以通过 
多种方式来确定。例如：

* 如果硬件允许，那么每个消息缓冲区可以使用不同的中断线， 
  它保持中断服务程序和消息缓冲区之间的一对一映射。
* 中断服务程序可以简单查询每个消息缓冲区，以确定其中是否包含数据。 
* 多个消息缓冲区可以被单个消息缓冲区替换，后者传递两个元数据 
  （消息是什么，其预期接收方是什么）以及实际数据。

然而，这些技术不足以处理存在大量或未知数量消息缓冲区的情况： 
在这种情况下，可扩展的解决方案是引入一个单独的控制消息缓冲区。如 
下文代码所示，`sbSEND_COMPLETED()` 使用控制消息缓冲区，将包含数据的消息缓冲区的句柄 
传递入中断服务程序。

```c
/* Added to FreeRTOSConfig.h to override the default implementation. */
#define sbSEND_COMPLETED( pxStreamBuffer ) vGenerateCoreToCoreInterrupt( pxStreamBuffer )

/* Implemented in a C file. */
void vGenerateCoreToCoreInterrupt( MessageBufferHandle_t xUpdatedBuffer )
{
    size_t BytesWritten;

    /* Called by the implementation of sbSEND_COMPLETED() in FreeRTOSConfig.h.
       If this function was called because data was written to any message buffer 
       other than the control message buffer then write the handle of the message
       buffer that contains data to the control message buffer, then raise an
       interrupt in the other core. If this function was called because data was
       written to the control message buffer then do nothing. */
    if( xUpdatedBuffer != xControlMessageBuffer )
    {
        BytesWritten = xMessageBufferSend(  xControlMessageBuffer,
                                            &xUpdatedBuffer,
                                            sizeof( xUpdatedBuffer ),
                                            0 );

        /* If the bytes could not be written then the control message buffer
           is too small! */
        configASSERT( BytesWritten == sizeof( xUpdatedBuffer );

        /* Generate interrupt in the other core (pseudocode). */
        GenerateInterrupt();
    }
}            
```
*使用控制消息缓冲区时 sbSEND_COMPLETED() 的实现。*

然后 ISR 读取控制消息缓冲区以获得句柄，之后 
将句柄作为参数传入 xMessageBufferSendCompletedFromISR()。请参阅下列代码列表。

```c
void InterruptServiceRoutine( void )
{
MessageBufferHandle_t xUpdatedMessageBuffer;
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* Receive the handle of the message buffer that contains data from the
       control message buffer. Ensure to drain the buffer before returning. */
    while( xMessageBufferReceiveFromISR( xControlMessageBuffer,
                                         &xUpdatedMessageBuffer,
                                         sizeof( xUpdatedMessageBuffer ),
                                         &xHigherPriorityTaskWoken )
                                           == sizeof( xUpdatedMessageBuffer ) )
    {
        /* Call the API function that sends a notification to any task that is
           blocked on the xUpdatedMessageBuffer message buffer waiting for data to
           arrive. */
        xMessageBufferSendCompletedFromISR( xUpdatedMessageBuffer,
                                            &xHigherPriorityTaskWoken );
    }

    /* Normal FreeRTOS "yield from interrupt" semantics, where
       xHigherPriorityTaskWoken is initialised to pdFALSE and will then get set to
       pdTRUE if the interrupt unblocks a task that has a priority above that of
       the currently executing task. */
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}      
```
*使用控制消息缓冲区时 ISR 的实现。*

图 3 显示了使用控制消息缓冲区时的序列。这里的编号项目同样与 
图中的编号箭头相关：

1. 接收任务尝试从空消息缓冲区读取，并进入阻塞状态以 
   等待数据抵达。
2. 发送任务将数据写入消息缓冲区。
3. `sbSEND_COMPLETED()` 将包含数据的消息缓冲区的句柄发送至控制 
   消息缓冲区。
4. `sbSEND_COMPLETED()` 在正在执行接收任务的核心中触发中断。
5. 中断服务程序读取消息缓冲区的句柄（该句柄 
   包含来自控制消息缓冲区的数据），然后将句柄传入 `xMessageBufferSendCompletedFromISR()` API 函数 
   以取消阻塞接收任务，该任务现在可以从缓冲区读取数据，因为缓冲区不再为空。

![AMP 多核配置中两个核心中的 rtos](/media/2019/multicore_amp_multiple_message_buffer.png)   
*图 3：编号箭头对应于上面的编号列表，它描述了如何利用控制消息缓冲区，通过众多消息缓冲区的一个传递
一个数据项，以便 ISR 
了解哪个消息缓冲区包含数据。*

到目前为止，我们只考虑了发送任务必须对接收任务取消阻塞的情况。如果 
消息缓冲区可以用于核心到核心的通信，则需要考虑接收消息如何 
取消发送消息的阻塞。如需完成这一操作，可以覆盖 
 `sbRECEIVE_COMPLETED()` 的实现，覆盖方法与已经为 `sbSEND_COMPLETED()` 描述的方式完全相同。

在所有这些情况下，确保任务不会在 
一个消息队列中无限期阻塞（以防出现中断丢失的情况）是一种不错的防御性编程实践，并应总是将消息队列完全排空， 
而不是假定每个中断有一条消息。


## 作者简介

![](https://secure.gravatar.com/avatar/2197982f95321bd156e6f3b3fa184b92?s=200&d=mm&r=g)   
Richard Barry 于 2003 年创立了 FreeRTOS 项目，花了十多年时间通过其公司 
Real Time Engineers Ltd 开发并推广 FreeRTOS 。现在他仍在继续改进 FreeRTOS， 
但已加入 Amazon Web Services 的更大团队担任首席工程师。Richard 毕业时荣获实时系统计算的 
一等学位，还因对嵌入式技术开发的贡献而被授予 
荣誉博士学位。Richard 还直接参与创办了几家 
公司，并撰写了几本书籍。  
[查看此作者的文章](../author/ribarry) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

