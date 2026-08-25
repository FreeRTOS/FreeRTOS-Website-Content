---
title: Formatting a Partition
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[Creating a FreeRTOS-Plus-FAT Media Driver](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)


A media partition must be formatted before it can be used. The
FF\_Format() function is used for this purpose.

As an example, below is the outline of the prvFormatPartition() function
used by FreeRTOS-Plus-FAT's RAM disk driver. prvFormatPartition() is called by
the RAM disk's initialisation function and demonstrates how to use the
FF\_Format() function. See the file ff\_ramdisk.c in the
FreeRTOS-Plus/Source/FreeRTOS-Plus-FAT/portable/common directory
for the full version.

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
*Formatting a Partition*
