---
title: "FF_Format()"
description: FreeRTOS+FAT FF_Format API 文档
---
[FreeRTOS-Plus-FAT 原生 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)


ff_format.h
```c
FF_Error_t FF_Format( FF_Disk_t *pxDisk,
                    BaseType_t xPartitionNumber,
                    BaseType_t xPreferFAT16,
                    BaseType_t xSmallClusters );
```

媒体是用于存储文件的物理设备。适用于
 嵌入式文件系统的媒体包括 SD 卡、
 固态磁盘、NOR 闪存芯片、NAND 闪存芯片和 RAM
 芯片。

要想媒体可存放 FreeRTOS-Plus-FAT 文件系统，必须
 将其[分区](FF_Partition)。

将媒体划分为多个单元，每个单元
 称为一个分区。各分区经过格式化之后
 方可存放文件系统。分区可以通过外部方式格式化
 （例如，通过 Windows 系统格式化 SD 卡），也可以使用 FF_Format()
 函数进行格式化。

FF_Format() 会动态确定要使用的 FAT 类型和
 簇大小。簇大小与簇数相关，而簇数
 则与 FAT 类型相关。可以通过 xPreferFAT16 和 xSmallClusters 参数
 指定首选项。例如，对于小型 RAM 磁盘，
 将这两个参数都设置为 true 以使用具有小簇的 FAT16，
 对于大型 SD 卡，将这两个参数都设置为 false
 以使用具有大簇的 FAT32。大簇的访问速度较快， 
 而小簇浪费的空间较少，因为它们在文件末尾会有较少 
 未使用的块。

## 参数 

+ *pxDisk* 

  FF_Disk_t 结构体，描述包含要格式化的分区的媒体。

+ *xPartitionNumber* 

  媒体上要格式化的分区的编号，从 0 开始。

+ *xPreferFAT16* 

  如果可能，设置为 pdTRUE 以使用 FAT16，否则使用 FAT32。

+ *xSmallClusters* 

  如果可能，设置为 pdTRUE 以使用小簇，否则使用大簇。设置为 pdFALSE 时， 
  将尽可能选择最大的簇。实际大小取决于使用的 FAT 类型。

## 返回

如果媒体格式化成功，则返回 FF_ERR_NONE。

如果媒体无法格式化，则返回错误代码。

FF_GetErrMessage() 可将错误代码转换为错误描述。


## 用法示例 
```c
#define HIDDEN_SECTOR_COUNT     8  
#define PRIMARY_PARTITIONS      1  
#define PARTITION_NUMBER        0  
  
static FF_Error_t prvPartitionAndFormatDisk( FF_Disk_t *pxDisk )  
{  
    FF_PartitionParameters xPartition;  
    FF_Error_t xError;  
  
    /* Media cannot be used until it has been partitioned. In this  
       case a single partition is to be created that fills all available space - so  
       by clearing the xPartition structure to zero. */  
    memset( &xPartition, 0x00, sizeof( xPartition ) );  
    xPartition.ulSectorCount = pxDisk->ulNumberOfSectors;  
    xPartition.ulHiddenSectors = HIDDEN_SECTOR_COUNT;  
    xPartition.xPrimaryCount = PRIMARY_PARTITIONS;  
    xPartition.eSizeType = eSizeIsQuota;  
  
    /* Perform the partitioning. */  
    xError = FF_Partition( pxDisk, &xPartition );  
  
    /* Print out the result of the partition operation. */  
    FF_PRINTF( "FF_Partition: FF_Format: %sn", FF_GetErrMessage( xError ) );  
  
    /* Was the disk partitioned successfully? */  
    if( FF_isERR( xError ) == pdFALSE )  
    {  
        /* The disk was partitioned successfully. Format the first partition. */  
        xError = FF_Format( pxDisk, ramPARTITION_NUMBER, pdTRUE, pdTRUE );  
  
        /* Print out the result of the format operation. */  
        FF_PRINTF( "FF_RAMDiskInit: FF_Format: %sn", FF_GetErrMessage( xError ) );  
    }  
  
    return xError;  
}  
  
```
*使用 FF_Partition() 和 FF_Format() 函数对磁盘进行分区，然后格式化分区*
