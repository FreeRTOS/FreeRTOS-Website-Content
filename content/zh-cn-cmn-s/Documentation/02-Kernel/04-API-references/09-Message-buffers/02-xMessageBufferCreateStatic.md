---
title: "xMessageBufferCreateStatic, xMessageBufferCreateStaticWithCallback"
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
MessageBufferHandle_t xMessageBufferCreateStatic(
                          size_t xBufferSizeBytes,
                          uint8_t *pucMessageBufferStorageArea,
                          StaticMessageBuffer_t *pxStaticMessageBuffer );

MessageBufferHandle_t xMessageBufferCreateStaticWithCallback(
                          size_t xBufferSizeBytes,
                          uint8_t *pucMessageBufferStorageArea,
                          StaticMessageBuffer_t *pxStaticMessageBuffer,
                          StreamBufferCallbackFunction_t pxSendCompletedCallback,
                          StreamBufferCallbackFunction_t pxReceiveCompletedCallback );
```

使用静态分配的内存创建新的[消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example)。消息 
缓冲区会在每次发送和接收操作完成后执行回调。使用 
xMessageBufferCreateStatic() API 创建的消息缓冲区共享相同的发送和接收完成回调函数，这些回调函数使用 
sbSEND_COMPLETED() 和 sbRECEIVE_COMPLETED() 宏定义。使用 
xMessageBufferCreateStaticWithCallback() API 创建的消息缓冲区可以拥有各自独特的发送和接收完成
回调函数。请参阅 [xMessageBufferCreate() and xMessageBufferCreateWithCallback()](/Documentation/02-Kernel/04-API-references/09-Message-buffers/01-xMessageBufferCreate) 
了解使用动态分配内存的对应版本。

[configSUPPORT_STATIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_static_allocation) 必须在 FreeRTOSConfig.h 中设置为 1， 
xMessageBufferCreateStatic() 才可用。此外，configUSE_SB_COMPLETED_CALLBACK 必须在 
FreeRTOSConfig.h 中设置为 1，xMessageBufferCreateStaticWithCallback() 才可用。

通过在构建中包含 FreeRTOS/source/stream_buffer.c 源文件 
来启用消息缓冲区功能（因为消息缓冲区使用流缓冲区）。


**参数：**

- *xBufferSizeBytes*

  pucMessageBufferStorageArea 参数所指向的缓冲区的大小（单位：字节）。当消息写入消息缓冲区时，
  同时也会写入额外的 sizeof（size_t）字节以存储消息的长度。 
  sizeof( size_t ) 在 32 位架构上的大小通常是 4 个字节，因此在大多数 32 位架构中，10 字节的消息将占用 14 字节的 
  消息缓冲区空间。可以存储在消息缓冲区的最大字节数实际上是 (xBufferSizeBytes - 1)。
  
- *pucMessageBufferStorageArea*

  必须指向一个大小至少为 xBufferSizeBytes + 1 的 uint8_t 数组。将消息写入消息缓冲区时， 
  实际上是将消息复制到这个数组。

- *pxStaticMessageBuffer*

  必须指向一个 StaticMessageBuffer_t 类型的变量，它将用于保存消息缓冲区的数据结构体。

- *pxSendCompletedCallback*

  消息写入消息缓冲区时调用的回调函数。如果参数为 NULL，
  则使用 sbSEND_COMPLETED 宏所提供的默认实现。发送完成回调函数必须
  具有 StreamBufferCallbackFunction_t 定义的原型，即：

  ```c
  void vSendCallbackFunction( MessageBufferHandle_t xMessageBuffer,  
                              BaseType_t xIsInsideISR,  
                              BaseType_t * const pxHigherPriorityTaskWoken );  
  ```

- *pxReceiveCompletedCallback*

  从消息缓冲区读取消息时调用的回调函数。如果参数为 NULL，
  则使用 sbRECEIVE_COMPLETED 宏所提供的默认实现。接收完成回调函数必须
  具有 StreamBufferCallbackFunction_t 定义的原型，即：

  ```c
  void vReceiveCallbackFunction( MessageBufferHandle_t xMessageBuffer,  
                                 BaseType_t xIsInsideISR,  
                                 BaseType_t * const pxHigherPriorityTaskWoken );  
  ```

**返回：**

如果成功创建了消息缓冲区，那么将返回一个所创建消息缓冲区的句柄。如果 
pucMessageBufferStorageArea 或 pxStaticMessageBuffer 为 NULL，则返回 NULL。


**用法示例：**

```c
/* Used to dimension the array used to hold the messages. The available  
 * space will actually be one less than this, so 999. */  
#define STORAGE_SIZE_BYTES 1000  

/* Defines the memory that will actually hold the messages within the message  
 * buffer. Should be one more than the value passed in the xBufferSizeBytes  
 * parameter. */  
static uint8_t ucMessageBufferStorage[ STORAGE_SIZE_BYTES ];  
static uint8_t ucMessageBufferWithCallbackStorage[ STORAGE_SIZE_BYTES ];  

/* The variable used to hold the message buffer structure. */
StaticMessageBuffer_t xMessageBufferStruct;  
StaticMessageBuffer_t xMessageBufferWithCallbackStruct;  

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

void MyFunction( void )  
{  
MessageBufferHandle_t xMessageBuffer, xMessageBufferWithCallback;  

    /* Create a message buffer that uses the functions defined  
     * using the sbSEND_COMPLETED() and sbRECEIVE_COMPLETED()  
     * macros as send and receive completed callback functions. */  
    xMessageBuffer = xMessageBufferCreateStatic( sizeof( ucMessageBufferStorage ),  
                                                 ucMessageBufferStorage,  
                                                 &xMessageBufferStruct );  

                                 
    /* Create a message buffer that uses the functions  
     * vSendCallbackFunction and vReceiveCallbackFunction as send  
     * and receive completed callback functions. */  
    xMessageBufferWithCallback = xMessageBufferCreateStaticWithCallback(   
                                     sizeof( ucMessageBufferWithCallbackStorage ),  
                                     ucMessageBufferWithCallbackStorage,  
                                     &xMessageBufferWithCallbackStruct,  
                                     vSendCallbackFunction,  
                                     vReceiveCallbackFunction );

    /* As neither the pucMessageBufferStorageArea or pxStaticMessageBuffer  
     * parameters were NULL, xMessageBuffer and xMessageBufferWithCallback  
     * will not be NULL, and can be used to reference the created message  
     * buffers in other message buffer API calls. */  

    /* Other code that uses the message buffers can go here. */  
}  
```
