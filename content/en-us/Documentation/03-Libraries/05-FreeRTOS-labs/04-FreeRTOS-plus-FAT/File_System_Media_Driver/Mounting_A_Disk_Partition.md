---
title: Mounting a Formatted Partition
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[Creating a FreeRTOS-Plus-FAT Media Driver](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)

Once a partition has been formatted it can be mounted. The
FF\_Mount() function is used for this purpose.

As an example, below is the outline of the prvMountPartition() function
used by FreeRTOS-Plus-FAT's RAM disk driver. prvMountPartition() is called by
the RAM disk's initialisation function and demonstrates how to use the
FF\_Mount() function. See the file
ff\_ramdisk.c in the
FreeRTOS-Plus/Source/FreeRTOS-Plus-FAT/portable/common directory
for the full version.

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
*Mounting a Partition*


### Adding a Partition to the Virtual File System

FreeRTOS-Plus-FAT implements a virtual file system, in which each mounted
partition appears as a directory. Mounted partitions are added to the
virtual file system using the ff\_fs\_add() function.
