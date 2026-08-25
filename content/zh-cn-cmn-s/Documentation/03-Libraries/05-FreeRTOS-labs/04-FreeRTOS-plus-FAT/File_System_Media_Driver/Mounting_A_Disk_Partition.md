---
title: 挂载格式化分区
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[创建 FreeRTOS-Plus-FAT 媒体驱动程序](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)

分区格式化后，可使用
FF_Mount() 函数实现此目的。

以下示例大致描述了
由 FreeRTOS-Plus-FAT 的 RAM 磁盘驱动程序使用的 prvMountPartition() 函数。
prvMountPartition() 由 RAM 磁盘的初始化函数调用，并演示了如何使用
FF_Mount() 函数。完整版本请参阅
ff_ramdisk.c 文件，此文件位于
FreeRTOS-Plus/Source/FreeRTOS-Plus-FAT/portable/common 目录
下。

```c
static BaseType_t prvMountPartition( FF_Disk_t *pxDisk, BaseType_t xPartitionToMount )
{
FF_Error_t xError;
BaseType_t xReturn;

    /* Record the partition number the FF_Disk_t structure is managing. */
    pxDisk->xStatus.bPartitionNumber = xPartitionToMount;

    /* Mount the partition. */
    xError = FF_Mount( pxDisk->pxIOManager, xPartitionToMount );

    if( FF_isERR( xError ) == pdFALSE )
    {
        /* Record that the partition is now mounted. */
        pxDisk->xStatus.bIsMounted = pdTRUE;
        xReturn = pdPASS;
    }
    else
    {
        xReturn = pdFALSE;
    }

    return xReturn;
}

```
*挂载分区*


### 将分区添加至虚拟文件系统

FreeRTOS-Plus-FAT 实现了虚拟文件系统，
其中每个挂载的分区都显示为一个目录。使用
ff_fs_add() 函数将挂载的分区添加至虚拟文件系统。
