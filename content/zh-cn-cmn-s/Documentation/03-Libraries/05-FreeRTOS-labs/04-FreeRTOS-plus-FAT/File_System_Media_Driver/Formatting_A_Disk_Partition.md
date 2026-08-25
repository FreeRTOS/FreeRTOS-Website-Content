---
title: 格式化分区
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[创建 FreeRTOS-Plus-FAT 媒体驱动程序](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)


媒体分区必须先进行格式化，然后才能使用。
FF_Format() 函数即可实现此目的。

以下示例大致描述了
由 FreeRTOS-Plus-FAT 的 RAM 磁盘驱动程序使用的 prvFormatPartition() 函数。
prvFormatPartition() 由 RAM 磁盘的初始化函数调用，并演示了如何使用
FF_Format() 函数。如需完整版本，请参阅文件 ff_ramdisk.c
（位于 FreeRTOS-Plus/Source/FreeRTOS-Plus-FAT/portable/common 目录下）
。

```c
static BaseType_t prvFormatPartition( FF_Disk_t *pxDisk, BaseType_t xPartitionToFormat )
{
BaseType_t xReturn;
FF_Error_t xError;

    /* Format the disk, trying FAT16 with small clusters. */
    xError = FF_Format( pxDisk->pxIOManager, xPartitionToFormat, pdTRUE, pdTRUE );
    if( FF_isERR( xError ) != pdFALSE )
    {
        xReturn = pdFAIL;
    }
    else
    {
        xReturn = pdPASS;
    }

    return xReturn;
}

```
*格式化分区*
