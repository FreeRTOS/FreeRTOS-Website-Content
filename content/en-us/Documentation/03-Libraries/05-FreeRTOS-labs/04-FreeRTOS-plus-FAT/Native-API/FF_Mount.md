---
title: "FF_Mount()"
description: FreeRTOS+FAT FF_Mount API documentation
---
[FreeRTOS-Plus-FAT Native API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

 
ff_ioman.h
```c
FF_Error_t FF_Mount( FF_Disk_t *pxDisk, BaseType_t xPartitionNumber );
```

The media is the physical device on which files are stored. Examples of
 media suitable for use in an embedded file system include SD cards,
 solid state disks, NOR flash memory chips, NAND flash chips, and RAM
 chips.
 
Partitioning divides the media into multiple units, each of which is
 called a partition. A partition cannot be used to hold a FreeRTOS-Plus-FAT
 file system until it has been formatted.
 
Formatted partitions must be 
 [mounted](http://en.wikipedia.org/wiki/Mount_%28computing%29) before they
 can be used with the FreeRTOS-Plus-Fat [standard API](FF_Format).

## Parameters 

+ *pxDisk* 

  The FF_Disk_t structure that holds the formatted partition to be mounted.

+ *xPartitionNumber* 

  The number of the partition on the media to mount. Partition numbers start from 0.


## Returns

If the partition was successfully mounted then FF_ERR_NONE is returned.

If the partition could not be mounted then an error code is returned.

FF_GetErrMessage() converts error codes into error descriptions.

## Example usage 

The [page that documents how to create a FreeRTOS-Plus-FAT media driver](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/File_System_Media_Driver/Media_Driver_Initialisation)
also demonstrates how to use the FF_Mount() function.
