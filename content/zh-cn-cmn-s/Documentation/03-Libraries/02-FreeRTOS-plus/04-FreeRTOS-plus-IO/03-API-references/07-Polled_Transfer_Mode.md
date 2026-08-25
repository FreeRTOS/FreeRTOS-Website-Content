---
title: 轮询传输模式
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[FreeRTOS-Plus-IO 传输模式](FreeRTOS_IO_Transfer_Modes)]


### 数据方向

轮询模式可以与 FreeRTOS_read() 和 FreeRTOS_write() 同时使用。


### 描述

在轮询模式下，数据传输通过忙等待外围设备状态位来执行，不使用
中断。

**轮询传输模式**

- **优点**

  - 非常易于使用的模型

  - 在大多数情况下，FreeRTOS_read() 或 FreeRTOS_write() 操作仅在所有数据分别读取或写入后
    才返回。

  - FreeRTOS-Plus-IO 驱动程序无需 RAM 即可缓冲数据。

- **缺点**

  - 执行读取或写入操作的任务在操作期间一直处于 
    [“就绪”或“正在运行”](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states/)状态，
    即便没有待执行操作，也是如此，
    这是因为外围设备的状态位自上次轮询以来没有变化。因此，
    轮询任务会浪费 CPU 时间，影响另一项本可以立即执行处理作业的任务
    。

  - 没有内置的互斥方法。如果多项任务需要访问同一外围设备，
    应用程序编写者必须确保任务之间的互斥（例如使用互斥锁）。

  - 目前尚无法更改读取或写入超时。

打开外围设备时默认启用轮询模式。退出轮询模式后，
并非所有外围设备都支持重新进入轮询模式。

除非发生错误，否则轮询写入操作仅在所有字节均已写入外围设备后才会返回
。

除非发生错误，否则轮询读取操作仅在从外围设备读取到请求的字节数后才会返回
。


### 用法示例

```c
/* FreeRTO+IO includes. */
#include "FreeRTOS_IO.h"

void vAFunction( void )
{
/* The Peripheral_Descriptor_t type is the FreeRTOS-Plus-IO equivalent of a descriptor. */
Peripheral_Descriptor_t xOpenedPort;
BaseType_t xBytesTransferred;

    /* Open the SPI port identified in the board support package as using the
       path string "/SPI2/". The second parameter is not currently used and can
       be set to anything, although, for future compatibility, it is recommneded
       that it is set to NULL. */
    xOpenedPort = FreeRTOS_open( "/SPI2/", NULL );

    if( xOpenedPort != NULL )
    {
        /* xOpenedPort now contains a valid descriptor that can be used with
           other FreeRTOS-Plus-IO API functions.

           Peripherals default to using Polled mode for both reads and writes, so
           the following FreeRTOS_write() call will write 10 bytes from the
           ucBuffer array to the SPI2 peripheral. The ucBuffer declaration is not
           shown, and assumed to be outside of this example function. */
        xBytesTransferred = FreeRTOS_write( xOpenedPort, ucBuffer, 10 );

        /* As polled mode is being used, xBytesTransferred should be 10, unless
           an error occurred. */
        configASSERT( xBytesTransferred == 10 );

        /* The transfer mode has not been changed, so the following read will
           also use polled mode. It will read 10 bytes into ucBuffer. */
        xBytesTransferred = FreeRTOS_read( xOpenedPort, ucBuffer, 10 );

        /* Again, as polled mode is used, the call to FreeRTOS_read() will have
           returned all of the 10 requested bytes unless an error occurred. */
        configASSERT( xBytesTransferred == 10 );
    }
    else
    {
        /* The port was not opened successfully. */
    }
}
```

