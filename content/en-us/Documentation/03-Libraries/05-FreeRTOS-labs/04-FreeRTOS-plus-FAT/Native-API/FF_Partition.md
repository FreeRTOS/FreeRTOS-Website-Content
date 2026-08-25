---
title: "FF_Partition()"
description: FreeRTOS+FAT FF_Partition API documentation
---
[FreeRTOS-Plus-FAT Native API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_format.h
```c
FF_Error_t FF_Partition( FF_Disk_t *pxDisk, FF_PartitionParameters *pxFormatParameters );
```

The media is the physical device on which files are stored. Examples of
 media suitable for use in an embedded file system include SD cards,
 solid state disks, NOR flash memory chips, NAND flash chips, and RAM
 chips.

Media cannot be used to hold a FreeRTOS-Plus-FAT file system until it has
 been [partitioned](http://en.wikipedia.org/wiki/Disk_partitioning).

Partitioning divides the media into multiple units, each of which is
 called a partition. Each partition can then be [formatted](FF_Format)
 to hold its own file system.

How the media is to be partitioned is described by a structure of type
 FF_PartitionParameters, which is shown below. A single partition that
 fills all available space on the media can be created by simply leaving
 the structure's xSizes and xPrimaryCount members at zero.


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
*The FF_PartitionParameters and associated types*


## Parameters

+ *pxDisk*

  The FF_Disk_t structure that describes the media being partitioned.

+ *FF_FormatParameters*

  A pointer to a structure that describes how the media will be partitioned.

## Returns

If the media is successfully partitioned then FF_ERR_NONE is returned.
If the media could not be partitioned then an error code is returned.
FF_GetErrMessage() converts error codes into error descriptions.

## Example usage

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
*Using the FF_Partition() and FF_Format() functions to partition the disk, then format a partition*
