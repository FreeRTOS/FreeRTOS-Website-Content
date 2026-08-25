---
title: "FF_Partition()"
description: FreeRTOS+FAT FF_Partition API 文档
---
[FreeRTOS-Plus-FAT 原生 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_format.h
```c
FF_Error_t FF_Partition( FF_Disk_t *pxDisk, FF_PartitionParameters *pxFormatParameters );
```

媒体是用于存储文件的物理设备。适用于
 嵌入式文件系统的媒体包括 SD 卡、
 固态磁盘、NOR 闪存芯片、NAND 闪存芯片和 RAM
 芯片。

要想媒体可存放 FreeRTOS-Plus-FAT 文件系统，必须
 将其[分区](http://en.wikipedia.org/wiki/Disk_partitioning)。

将媒体划分为多个单元，每个单元
 称为一个分区。各分区经过[格式化](FF_Format)之后
 方可存放文件系统。

媒体的分区方式
 由 FF_PartitionParameters 类型的结构体进行描述，如下所示。若要创建一个用于填充媒体上所有可用空间的分区，
 只需
 将结构体的 xSizes 和 xPrimaryCount 成员保留为零。


```c
typedef enum _FF_SizeType  
{  
    /* xSizes within the FF_PartitionParameters structure are specified as a  
       quotum (the sum of all xSizes is free, all disk space will be allocated). */  
    eSizeIsQuota,  
    
    /* xSizes within the FF_PartitionParameters structure are specified as a  
       percentage of the total disk space (the sum of all xSizes must be <= 100%) */  
    eSizeIsPercent,  
    
    /* xSizes within the FF_PartitionParameters structure are specified as a  
       number of sectors (the sum of all xSizes must be < ulSectorCount). */  
    FF_Size_Sectors,  
    } eSizeType_t;  
    
    typedef struct _FF_PartitionParameters  
    {  
    /* The total number of sectors on the media, including hidden/reserved  
       sectors. */  
    uint32_t ulSectorCount;  
    
    /* The number of sectors to keep free. */  
    uint32_t ulHiddenSectors;  
    
    /* The number of sectors to keep between partitions. */  
    uint32_t ulInterSpace;  
    
    /* The size of each partition - how the sizes are specified depends on the  
       value of eSizeType. */  
    BaseType_t xSizes[ FF_MAX_PARTITIONS ];  
    
    /* The number of primary partitions to create. */  
    BaseType_t xPrimaryCount;  
    
    /* How the values within the xSizes array are specified. */  
    eSizeType_t eSizeType;  
} FF_PartitionParameters;
```
*FF_PartitionParameters 和相关类型*


## 参数

+ *pxDisk*

  描述被分区的媒体的 FF_Disk_t 结构体。

+ *FF_FormatParameters*

  指向描述如何对媒体进行分区的结构体的指针。

## 返回

如果媒体分区成功，则返回 FF_ERR_NONE。
如果无法对媒体进行分区，则返回错误代码。
FF_GetErrMessage() 可将错误代码转换为错误描述。

## 用法示例

```c
#define HIDDEN_SECTOR_COUNT 8  
#define PRIMARY_PARTITIONS 1  
#define PARTITION_NUMBER 0  
  
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
