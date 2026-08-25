---
title: "xMessageBufferCreate, xMessageBufferCreateWithCallback"
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
MessageBufferHandle_t xMessageBufferCreate( size_t xBufferSizeBytes );

MessageBufferHandle_t xMessageBufferCreateWithCallback( 
                          size_t xBufferSizeBytes,
                          StreamBufferCallbackFunction_t pxSendCompletedCallback,
                          StreamBufferCallbackFunction_t pxReceiveCompletedCallback );
```

创建使用动态分配内存的新[消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example)。消息 
缓冲区会在每次发送和接收操作完成后执行回调。使用 
`xMessageBufferCreate()` API 创建的消息缓冲区共享相同的发送和接收完成回调函数，这些回调函数使用 
`sbSEND_COMPLETED()` 和 `sbRECEIVE_COMPLETED()` 宏定义。使用 
`xMessageBufferCreateWithCallback()` API 创建的消息缓冲区可以拥有各自独特的发送和接收完成回调 
函数。请参阅 `xMessageBufferCreateStatic()` 和 `xMessageBufferCreateStaticWithCallback()` 
获取使用静态分配内存（在编译时分配的内存）的相应版本。

[configSUPPORT_DYNAMIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_dynamic_allocation) 必须 
在 FreeRTOSConfig.h 中设置为 1 或未定义，`xMessageBufferCreate()` 才可用。此外，`configUSE_SB_COMPLETED_CALLBACK` 
必须在 FreeRTOSConfig.h 中设置为1，`xMessageBufferCreateWithCallback()` 才可用。

通过在构建中包含 FreeRTOS/source/stream_buffer.c 源文件 
来启用消息缓冲区功能（因为消息缓冲区使用流缓冲区）。


**参数：**

- *xBufferSizeBytes*

  消息缓冲区在任何时候能够容纳的字节（而非消息）总数。当消息写入消息缓冲区时， 
  同时也会写入额外的 `sizeof( size_t )` 字节以存储消息的长度。 `sizeof( size_t )` 
  sizeof( size_t ) 在 32 位架构上的大小通常是 4 个字节，因此在大多数 32 位架构中，10 字节的消息将占用 14 字节的 
  消息缓冲区空间。
  
- *pxSendCompletedCallback*

  消息写入消息缓冲区时调用的回调函数。如果参数为 NULL， 
  则使用 `sbSEND_COMPLETED` 宏所提供的默认实现。发送完成回调函数必须
  具有由 `StreamBufferCallbackFunction_t` 定义的原型，即：

  ```c
  void vSendCallbackFunction( MessageBufferHandle_t xMessageBuffer,  
                              BaseType_t xIsInsideISR,  
                              BaseType_t * const pxHigherPriorityTaskWoken );  
  ```

- *pxReceiveCompletedCallback*

  从消息缓冲区读取消息时调用的回调函数。如果参数为 NULL， 
  则使用 `sbRECEIVE_COMPLETED` 宏所提供的默认实现。接收完成回调函数必须 
  具有由 `StreamBufferCallbackFunction_t` 定义的原型，即：

  ```c
  void vReceiveCallbackFunction( MessageBufferHandle_t xMessageBuffer,  
                                 BaseType_t xIsInsideISR,  
                                 BaseType_t * const pxHigherPriorityTaskWoken );  
  ```


**返回：**

- 如果返回 NULL，则说明因为没有足够的堆内存可供 FreeRTOS 
  分配消息缓冲区的数据结构体和存储区域，所以无法创建消息缓冲区。 
  
- 如果返回非 NULL 值，则表示消息 
  缓冲区已成功创建，返回值应该作为所创建消息缓冲区的句柄来存储。


**用法示例：**

```c
void vSendCallbackFunction( MessageBufferHandle_t xMessageBuffer,  
                            BaseType_t xIsInsideISR,  
                            BaseType_t * const pxHigherPriorityTaskWoken )  
{  
    /* Insert code here which is invoked when a message is written to  
     * the message buffer.  
     * This is useful when a message buffer is used to pass messages between  
     * cores on a multicore processor. In that scenario, this callback  
     * can be implemented to generate an interrupt in the other CPU core,  
     * and the interrupt's service routine can then use the  
     * xMessageBufferSendCompletedFromISR() API function to check, and if  
     * necessary unblock, a task that was waiting for message. */  
}  

  
void vReceiveCallbackFunction( MessageBufferHandle_t xMessageBuffer,  
                               BaseType_t xIsInsideISR,  
                               BaseType_t * const pxHigherPriorityTaskWoken )  
{  
    /* Insert code here which is invoked when a message is read from a message  
     * buffer.  
     * This is useful when a message buffer is used to pass messages between  
     * cores on a multicore processor. In that scenario, this callback  
     * can be implemented to generate an interrupt in the other CPU core,  
     * and the interrupt's service routine can then use the  
     * xMessageBufferReceiveCompletedFromISR() API function to check, and if  
     * necessary unblock, a task that was waiting to send message. */  
}  

  
void vAFunction( void )  
{  
    MessageBufferHandle_t xMessageBuffer, xMessageBufferWithCallback;  
    const size_t xMessageBufferSizeBytes = 100;  

    /* Create a message buffer that can hold 100 bytes and uses the  
     * functions defined using the sbSEND_COMPLETED() and  
     * sbRECEIVE_COMPLETED() macros as send and receive completed  
     * callback functions. The memory used to hold both the message  
     * buffer structure and the data in the message buffer is  
     * allocated dynamically. */  
    xMessageBuffer = xMessageBufferCreate( xMessageBufferSizeBytes );  

    if( xMessageBuffer == NULL )  
    {  
        /* There was not enough heap memory space available to create the  
         * message buffer. */  
    }  
    else  
    {  
        /* The message buffer was created successfully and can now be used. */  
    }  

    /* Create a message buffer that can hold 100 bytes and uses the  
     * functions vSendCallbackFunction and vReceiveCallbackFunction  
     * as send and receive completed callback functions. The memory  
     * used to hold both the message buffer structure and the data  
     * in the message buffer is allocated dynamically. */  
    xMessageBufferWithCallback = xMessageBufferCreateWithCallback(   
                                     xMessageBufferSizeBytes,  
                                     vSendCallbackFunction,  
                                     vReceiveCallbackFunction );  

    if( xMessageBufferWithCallback == NULL )  
    {  
        /* There was not enough heap memory space available to create the  
         * message buffer. */  
    }  
    else  
    {  
        /* The message buffer was created successfully and can now be used. */  
    }  
}  
```
