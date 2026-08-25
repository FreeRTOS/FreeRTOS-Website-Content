---
title: "Creating a Media Driver: Writing Sectors"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[Creating a FreeRTOS-Plus-FAT Media Driver](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)]


Each FreeRTOS-Plus-FAT media driver requires a function that writes sectors
to the media on which the embedded file system is stored. How the write
functions actually work is dependent on the media type. For example, if
the media is a RAM disk then data can be written to the RAM using memcpy(),
but if the media is an SD card then the card's command interface will
have to be used via an MMC or SPI peripheral driver.


### The Write Function

The write function can take any name, but must have the following prototype:

```c
int32_t FFWrite( uint8_t *pucSource,      /* Source of data to be written. */
                 uint32_t ulSectorNumber, /* The first sector being written to. */
                 uint32_t ulSectorCount,  /* The number of sectors to write. */
                 FF_Disk_t *pxDisk );     /* Describes the disk being written to. */
```
*The prototype of a function used to write to the media that holds the embedded file system*

As an example, below is the outline of the write function used by the
FreeRTOS-Plus-FAT RAM disk driver. The full version contains input parameter
checking, and can be found in
/FreeRTOS-Plus/Source/FreeRTOS-Plus-FAT/portable/common/ff\_ramdisk.c.

```c
/* Each sector is 512 bytes. */
#define ramSECTOR_SIZE    512

static int32_t prvWriteRAM( uint8_t *pucSource,
                            uint32_t ulSectorNumber,
                            uint32_t ulSectorCount,
                            FF_Disk_t *pxDisk )
{
uint8_t *pucDestination;

    /* The FF_Disk_t structure describes the media being accessed. Attributes that
       are common to all media types are stored in the structure directly. The pvTag
       member of the structure is used to add attributes that are specific to the media
       actually being accessed. In the case of the RAM disk the pvTag member is just
       used to point to the RAM buffer being used as the disk. */
    pucDestination = ( uint8_t * ) pxDisk->pvTag;

    /* Move to the start of the sector being written. */
    pucDestination += ( ramSECTOR_SIZE * ulSectorNumber );

    /* Copy the data to the disk. As this is a RAM disk data can be copied
       using memcpy(). */
    memcpy( ( void * ) pucDestination,
            ( void * ) pucSource,
            ( size_t ) ( ulSectorCount * ramSECTOR_SIZE ) );

    return FF_ERR_NONE;
}
```
*The write function used by the RAM disk driver - for clarity input parameter checking is not shown*
