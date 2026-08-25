---
title: 中断驱动的零拷贝传输模式
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[FreeRTOS-Plus-IO 传输模式](FreeRTOS_IO_Transfer_Modes)]


### 数据方向

中断驱动的零拷贝传输模式可以与 FreeRTOS_write() 一起使用。


### 描述

ioconfigUSE_ZERO_COPY_TX 必须在 [FreeRTOSIOConfig.h](FreeRTOS_Plus_IO_Configuration) 设置为 1 
以使零拷贝传输模式可用。还必须在同一配置文件中
为正在使用的外设明确启用该功能。

当选择零拷贝传输模式时，FreeRTOS_write() 不会直接向外设写入字节
。相反，要写入的字节总数和指向第一个字节的指针
都存储在 FreeRTOS-Plus-IO 驱动程序中。然后，外设的中断服务程序
使用这些值执行实际写入操作。字节从提供的缓冲区直接被拷贝到外围设备的
寄存器，而不存储在任何中间队列或缓冲区中。

FreeRTOS-Plus-IO 驱动程序可以创建和管理互斥锁，
以确保一次只能有一个任务执行零拷贝写入。在任务开始零拷贝写入之前，必须先获得互斥锁。使用
[FreeRTOS_ioctl()](FreeRTOS_ioctl) 调用和 ioctlOBTAIN_WRITE_MUTEX 请求代码获取
互斥锁。必须检查 FreeRTOS_ioctl()的返回值，以确定是否成功获取了互斥锁
（在调用 FreeRTOS_write() 之前检查）。如果通过非互斥锁持有者的任务调用 FreeRTOS_write() ，调用将失败
。

零拷贝写入由 FreeRTOS-Plus-IO 中断服务程序执行。在开始
写操作的
FreeRTOS _write() 调用返回后的一段时间内，中断服务程序可能会继续访问正在写入的缓冲区。在中断服务程序完成写入操作之前，
不得重复使用或以任何方式破坏缓冲区。
为此，可使用 FreeRTOS_ioctl() [ioctlOBTAIN_WRITE_MUTEX](http:/FreeRTOS-Plus/FreeRTOS_Plus_IO/FreeRTOS_ioctl.html#ioctlOBTAIN_WRITE_MUTEX)
和 [ioctlWAIT_PREVIOUS_WRITE_COMPLETE](FreeRTOS_ioctl#ioctlWAIT_PREVIOUS_WRITE_COMPLETE)
请求代码。

持有互斥锁但不执行 FreeRTOS_write() 的任务
必须调用 FreeRTOS_ioctl()，并将请求代码设置为 ioctlRELEASE_WRITE_MUTEX，从而手动释放互斥锁。

中断服务程序和写互斥锁由 FreeRTOS-Plus-IO 代码实现，
应用程序写入器无需提供。


**中断驱动的零拷贝传输模式**

- **优点**

  - 可自动将调用任务设为 
    [阻塞](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states/)状态
    以等待写互斥锁可用。这样可以确保调用 FreeRTOS_write() 的任务
    只有在实际访问外设时才会占用 CPU 时间。

  - 对 FreeRTOS_write() 的调用会立即返回，
    允许调用任务在传输过程中执行其他操作。

  - 字节由中断服务程序直接从 FreeRTOS_write() 调用中
    作为参数提供的缓冲区移至外设寄存器。由于不需要额外的 RAM，
    也不需要额外的数据复制，因此这是一种非常高效的写入方法。

  - 使用写互斥锁意味着 FreeRTOS-Plus-IO 驱动程序内置了互斥功能。

- **缺点**

  - 使用模型更复杂。

ioctlUSE_ZERO_COPY_TX 请求代码用于调用 FreeRTOS_ioctl() 以配置外设
使用中断驱动的零拷贝传输模式进行写入。请注意，此请求代码将导致外设
启用中断，并且将外设的中断优先级设置为
最低。ioctlSET_INTERRUPT_PRIORITY 请求代码可用于
提升外设优先级（如有必要）。


### 用法示例

[FreeRTOS_write() API 函数文档页面](FreeRTOS_write)也提供了相关示例。

```c
/* FreeRTOS-Plus-IO includes. */
#include "FreeRTOS_IO.h"

void vAFunction( void )
{
/* The Peripheral_Descriptor_t type is the FreeRTOS-Plus-IO equivalent of a descriptor. */
Peripheral_Descriptor_t xOpenedPort;
BaseType_t xReturned;
const uint32_t ulMaxBlock100ms = ( 100UL / portTICK_PERIOD_MS );

    /* Open the SPI port identified in the board support package as using the
       path string "/SPI2/". The second parameter is not currently used and can
       be set to anything, although, for future compatibility, it is recommended
       that it is set to NULL. */
    xOpenedPort = FreeRTOS_open( "/SPI2/", NULL );

    if( xOpenedPort != NULL )
    {
        /***************** Configure the port *********************************/

        /* xOpenedPort now contains a valid descriptor that can be used with
           other FreeRTOS-Plus-IO API functions.

           Peripherals default to using Polled mode for both reads and writes.
           Change from the default to use the interrupt driven zero copy transfer
           mode for writing. The third FreeRTOS_ioctl() parameter is not used and
           can take any value - although it is recommended to set the value to NULL
           for future compatibility. A successful FreeRTOS_ioctl() call will return
           pdPASS, for simplicity, this example does not show the return value being
           checked. */
        FreeRTOS_ioctl( xOpenedPort, ioctlUSE_ZERO_COPY_TX, NULL );


        /***************** Use the port ***************************************/

        /* As the zero copy transfer mode is being used, the write mutex must
           be obtained before FreeRTOS_write() is called. The following call will
           attempt to obtain the mutex. If the mutex is not immediately available,
           then the calling task will be placed into the Blocked state to wait for
           it, but the task will not wait longer than 100ms. If the task is
           successful in obtaining the mutex in that time, FreeRTOS_ioctl() will
           return pdPASS, otherwise FreeRTOS_ioctl() will return pdFAIL. */
        xReturned = FreeRTOS_ioctl( xOpenedPort, ioctlOBTAIN_WRITE_MUTEX, ulMaxBlock100ms );

        if( xReturned == pdTRUE )
        {
            /* The mutex was successfully obtained, now a FreeRTOS_write() can
               be performed. This call will send 100 bytes from ucBuffer. ucBuffer
               is assumed to be defined outside of this function. */
            xReturned = FreeRTOS_write( xOpenedPort, ucBuffer, 100 );

            if( xReturned == 100 )
            {
                /* The write was successful BUT will not yet have completed. The
                   peripheral's interrupt service routine will be accessing ucBuffer,
                   but this task is free to do anything else it needs to do at this
                   point - provided the data in ucBuffer is not changed. */
            }
        }

        /* Some time later the task wants to update the data in ucBuffer, and
           perform another write. First it must ensure the previous write has
           completed. If it can successfully obtain the write mutex again then
           it knows it is safe to access ucBuffer. Again, a maximum block time of
           100ms is used. */
        xReturned = FreeRTOS_ioctl( xOpenedPort, ioctlOBTAIN_WRITE_MUTEX, ulMaxBlock100ms );

        if( xReturned == pdTRUE )
        {
            /* The mutex was obtained, so the task can go ahead and update the
               buffer. In this example, all it is going to do is clear it to zero. */
            memset( ucBuffer, 0, 100 );

            /* The task already holds the mutex, so can perform the write now. */
            xReturned = FreeRTOS_write( xOpenedPort, ucBuffer, 100 );

            /* Again - if at this point xReturned == 100, the write was successful,
               but will still be in progress. */
        }

        /* Before exiting the function, the task wants to ensure the write has
           completed, but this time it does not want to perform another write itself,
           so uses the ioctlWAIT_PREVIOUS_WRITE_COMPLETE request code in place of the
           ioctlOBTAIN_WRITE_MUTEX request code in a call to FreeRTOS_ioctl(). */
        FreeRTOS_ioctl( xOpenedPort, ioctlWAIT_PREVIOUS_WRITE_COMPLETE, ulMaxBlock100ms );
    }
}
```

