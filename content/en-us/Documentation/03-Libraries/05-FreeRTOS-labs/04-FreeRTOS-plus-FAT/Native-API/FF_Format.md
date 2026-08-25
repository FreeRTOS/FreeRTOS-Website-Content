---
title: "FF_Format()"
description: FreeRTOS+FAT FF_Format API documentation
---
[FreeRTOS-Plus-FAT Native API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)


ff_format.h
```c
FF_Error_t FF_Format( FF_Disk_t *pxDisk,
                    BaseType_t xPartitionNumber,
                    BaseType_t xPreferFAT16,
                    BaseType_t xSmallClusters );
```

The media is the physical device on which files are stored. Examples of
 media suitable for use in an embedded file system include SD cards,
 solid state disks, NOR flash memory chips, NAND flash chips, and RAM
 chips.
 
Media cannot be used to hold a FreeRTOS-Plus-FAT file system until it has
 been [partitioned](FF_Partition).
 
Partitioning divides the media into multiple units, each of which is
 called a partition. Each partition can then be formatted
 to hold its own file system. A partition can be formatted externally
 (for example Windows can format an SD-card), or using the FF_Format()
 function.
 
FF_Format() will dynamically determine the FAT type and cluster size to
 use. The cluster size will relate to the cluster count, and the cluster
 count to the FAT type. The xPreferFAT16 and xSmallClusters parameters
 allow a preference to be specified. For example, for a small RAM disk
 set both parameters to true to use FAT16 with small clusters, and for a
 large SD-card set both parameters to false to use FAT32 with large
 clusters. Larger clusters can be accessed more quickly, whereas smaller 
 clusters waste less space as they will have fewer unused blocks at the 
 end of a file.

## Parameters 

+ *pxDisk* 

  The FF_Disk_t structure that describes the media that> contains the partition to be formatted.

+ *xPartitionNumber* 

  The number of the partition on the media to format. Partition numbers start from 0.

+ *xPreferFAT16* 

  Set to pdTRUE to use FAT16 if it is possible, otherwise use FAT32.

+ *xSmallClusters* 

  Set to pdTRUE to use small clusters if it is possible, otherwise use large clusters. When set to pdFALSE, 
  the largest possible cluster size will be selected. The actual size will depends on the FAT type in use.

## Returns

If the media is successfully formatted then FF_ERR_NONE is returned.

If the media could not be formatted then an error code is returned.

FF_GetErrMessage() converts error codes into error descriptions.
 

## Example usage 
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
*Using the FF_Partition() and FF_Format() functions to partition the disk, then format a partition*
