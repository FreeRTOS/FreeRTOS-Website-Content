---
title: "Creating a Media Driver: Reading Sectors"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[Creating a FreeRTOS-Plus-FAT Media Driver](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)]

Each FreeRTOS-Plus-FAT media driver requires a function that reads sectors
from the media on which the embedded file system is stored. How the read
functions actually work is dependent on the media type. For example, if
the media is a RAM disk then data can be read from the RAM using memcpy(),
but if the media is an SD card then the card's command interface will
have to be used via an MMC or SPI peripheral driver.


### The Read Function

The read function can have any name, but must have the following prototype:

```c
int32_t prvFFRead( uint8_t *pucDestination, /* Destination for data being read. */
                   uint32_t ulSectorNumber, /* Sector from which to start reading data. */
                   uint32_t ulSectorCount,  /* Number of sectors to read. */
                   FF_Disk_t *pxDisk );     /* Describes the disk being read from. */
```
*The prototype of a function used to read sectors from the media holding the embedded file system*

As an example, below is the outline of the read function used by the
FreeRTOS-Plus-FAT RAM disk driver. The full version contains input parameter
checking, and can be found in /FreeRTOS-Plus/Source/FreeRTOS-Plus-FAT/portable/common/ff\_ramdisk.c.


```c
/* Each sector is 512 bytes. */
#define ramSECTOR_SIZE    512

static int32_t prvReadRAM( uint8_t *pucDestination,
                           uint32_t ulSectorNumber,
                           uint32_t ulSectorCount,
                           FF_Disk_t *pxDisk )
{
uint8_t *pucSource;

    /* The FF_Disk_t structure describes the media being accessed. Attributes that
 are common to all media types are stored in the structure directly. The pvTag
 member of the structure is used to add attributes that are specific to the media
 actually being accessed. In the case of the RAM disk the pvTag member is just
 used to point to the RAM buffer being used as the disk. */
    pucSource = ( uint8_t * ) pxDisk->pvTag;

    /* Move to the start of the sector being read. */
    pucSource += ( ramSECTOR_SIZE * ulSectorNumber );

    /* Copy the data from the disk. As this is a RAM disk data can be copied
 using memcpy(). */
    memcpy( ( void * ) pucDestination,
            ( void * ) pucSource,
            ( size_t ) ( ulSectorCount * ramSECTOR_SIZE ) );

    return FF_ERR_NONE;
}
```
*The read function used by the RAM disk driver - for clarity input parameter checking is not shown*
