---
title: Partitioning the Media Prior to Formatting
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[Creating a FreeRTOS-Plus-FAT Media Driver](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)


The media must be divided into one or more partitions before it can be
formatted with the necessary embedded FAT file system structures. The
FF\_Partition() function is used for this purpose.

As an example, below is the outline of the prvPartitionDisk() function
used by FreeRTOS-Plus-FAT's RAM disk driver. prvPartitionDisk() is called by
the RAM disk's initialisation function and demonstrates how to call FF\_Partition().
See the file ff\_ramdisk.c in the
FreeRTOS-Plus/Source/FreeRTOS-Plus-FAT/portable/common directory
for the full version.

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
*Partitioning the Media, Ready for Formatting*
