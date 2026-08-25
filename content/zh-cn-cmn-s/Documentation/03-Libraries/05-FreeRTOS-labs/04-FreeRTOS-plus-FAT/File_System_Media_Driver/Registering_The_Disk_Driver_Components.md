---
title: "用嵌入式文件系统注册驱动器组件"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[创建 FreeRTOS-Plus-FAT 媒体驱动程序](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)


FreeRTOS-Plus-FAT 需要了解媒体驱动器使用的组件，
包括驱动器的读写函数以及 IO 管理器。所选
FF_RegisterBlockDevice() 函数正是用于此目的。

以下示例大致描述了
由 FreeRTOS-Plus-FAT 的 RAM 磁盘驱动程序使用的 prvRegisterDisk() 函数。
prvRegisterDisk() 由 RAM 磁盘驱动程序的初始化函数调用，并演示如何
使用 FF_RegisterBlockDevice()。如需完整版本，请参阅文件
ff_ramdisk.c 文件，此文件位于
FreeRTOS-Plus/Source/FreeRTOS-Plus-FAT/portable/common 目录
下。

```c
static BaseType_t prvRegisterDisk( FF_Disk_t *pxDisk )
{
FF_Error_t xError;
BaseType_t xReturn;

    /* Register the read/write access functions and the IO manager with the file
       system. pxDisk is also registered as a parameter that will be passed to the
       read and write functions when they are called. */
    xError = FF_RegisterBlockDevice( pxDisk->pxIOManager,
                                     ramSECTOR_SIZE,
                                     prvWriteRAM,
                                     prvReadRAM,
                                     ( void * ) pxDisk );

    if( FF_isERR( xError ) != pdFALSE )
    {
        xReturn = pdFAIL;
    }
    else
    {
        /* Record that the disk has been successfully registered. */
        pxDisk->xStatus.bIsRegistered = pdTRUE;
        xReturn = pdPASS;
    }

    return xReturn;
}

```
*使用 FreeRTOS-Plus-FAT 嵌入式文件系统注册媒体驱动程序所用的组件*
