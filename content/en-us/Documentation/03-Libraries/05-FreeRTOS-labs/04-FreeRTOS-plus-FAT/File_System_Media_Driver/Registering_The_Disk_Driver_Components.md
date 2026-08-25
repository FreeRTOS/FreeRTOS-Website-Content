---
title: "Registering the Driver's Components with the Embedded File System"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[Creating a FreeRTOS-Plus-FAT Media Driver](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)


FreeRTOS-Plus-FAT needs to be aware of the components used by the media driver,
including the driver's read and write functions, and the drivers IO manager. The
FF\_RegisterBlockDevice() function is used for this purpose.

As an example, below is the outline of the prvRegisterDisk() function
used by FreeRTOS-Plus-FAT's RAM disk driver. prvRegisterDisk() is called by
the RAM disk driver's initialisation function, and demonstrates how
FF\_RegisterBlockDevice() is used. See the file
ff\_ramdisk.c in the
FreeRTOS-Plus/Source/FreeRTOS-Plus-FAT/portable/common directory
for the full version.

```c
static BaseType_t prvRegisterDisk( FF_Disk_t *pxDisk )
{
FF_Error_t xError;
BaseType_t xReturn;

    /* Register the read/write access functions and the IO manager with the file
       system. pxDisk is also registered as a parameter that will be passed to the
       read and write functions when they are called. */
    xError = FF_RegisterBlockDevice( pxDisk->pxIOManager,
                                     ramSECTOR_SIZE,
                                     prvWriteRAM,
                                     prvReadRAM,
                                     ( void * ) pxDisk );

    if( FF_isERR( xError ) != pdFALSE )
    {
        xReturn = pdFAIL;
    }
    else
    {
        /* Record that the disk has been successfully registered. */
        pxDisk->xStatus.bIsRegistered = pdTRUE;
        xReturn = pdPASS;
    }

    return xReturn;
}
```
*Registering the components used by the media driver with the FreeRTOS-Plus-FAT embedded file system*
