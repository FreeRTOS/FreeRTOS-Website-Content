---
title: 在格式化之前对媒体进行分区
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[创建一个 FreeRTOS-Plus-FAT 媒体驱动程序](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)


必须将媒体分成一个或多个分区，然后才能
用必要的嵌入式 FAT 文件系统结构体进行格式化。所选
FF_Partition() 函数正是用于此目的。

以下示例大致描述了
由 FreeRTOS-Plus-FAT 的 RAM 磁盘驱动程序使用的 prvPartitionDisk() 函数。
此函数由 RAM 磁盘的初始化函数调用，并演示如何调用 FF_Partition()。
如需完整版本，请参阅文件 ff_ramdisk.c
（位于 FreeRTOS-Plus/Source/FreeRTOS-Plus-FAT/portable/common 目录下）
。

```c
/* Initial sectors to be kept free. */
#define ramHIDDEN_SECTOR_COUNT		8

/* The number of primary partitions on the disk. */
#define ramPRIMARY_PARTITIONS		1

static BaseType_t prvPartitionDisk( FF_Disk_t *pxDisk )
{
FF_FormatParameters xPartition;
FF_Error_t xError;
BaseType_t xReturn;

    /* Start with the FF_FormatParameters structure cleared to zero. */
    memset( &xPartition, '�', sizeof( xPartition ) );

    /* Fill in the structure's members as necessary. */
    xPartition.ulSectorCount = pxDisk->ulSectorCount;
    xPartition.ulHiddenSectors = ramHIDDEN_SECTOR_COUNT;
    xPartition.xPrimaryCount = ramPRIMARY_PARTITIONS;

    /* Partition the disk. */
    xError = FF_Partition( pxDisk->pxIOManager, &xPartition );

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
*将媒体分区，准备好格式化*
