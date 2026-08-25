---
title: "FF_CreateIOManager()"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[Creating a FreeRTOS-Plus-FAT Media Driver](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)]

ff\_ioman.h

```c
FF_IOManager_t *FF_CreateIOManger( FF_CreationParameters_t *pxParameters, FF_Error_t *pxError );
```

FreeRTOS-Plus-FAT [media drivers](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)
store information that is common to all media types in a structure of
type [FF\_Disk\_t](FF_Disk_t).
The pxIOManager member of the FF\_Disk\_t structure references an object
called an input/output manager (IO Manager, or simply IOMAN). The IO
manager is responsible for, amongst other things, buffering and caching
both file and directory information.

FF\_CreateIOManager() creates an IO Manager object.

Parameters are passed into FF\_CreateIOManager() in an FF\_CreationParameters\_t
structure.

The pvSemaphore member of the FF\_CreationParameters\_t structure must be created by a call to
the [xSemaphoreCreateRecursiveMutex()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/08-xSemaphoreCreateRecursiveMutex)
FreeRTOS API function.

```c
typedef struct xFF_CREATION_PARAMETERS
{
    /* If the memory to use as the IO manager's cache is provided by the application
       writer then pass a pointer to the memory in pucCacheMemory. If the memory to
       use as the IO manager's cache is to be allocated by the IO manager then pass
       NULL in pucCacheMemory. */
    uint8_t *pucCacheMemory;

    /* The size of the cache memory. ulMemorySize is specified in bytes and must
       be a multiple of ulSectorSize. */
    uint32_t ulMemorySize;

    /* Sector size, which is the unit for reading from and writing to the disk.
       A sector size of 512 bytes is normal. */
    BaseType_t ulSectorSize;

    /* The [function used to write a sector to the disk](Write_To_Disk). */
    FF_WriteBlock_t fnWriteBlocks;

    /* The [function used to read a sector from the disk](Read_From_Disk). */
    FF_ReadBlock_t fnReadBlocks;

    /* The parameter to pass into the read sector and write sector functions -
       basically a pointer back to the FF\_Disk\_t structure that contains the IO
       manager. */
    FF_Disk_t *pxDisk;

    /* The semaphore used to protect the data structures on the media must be
       created using the [xSemaphoreCreateRecursiveMutex()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/08-xSemaphoreCreateRecursiveMutex) API function. */

    void *pvSemaphore;

    /* If the media driver is not re-entant then set xBlockDeviceIsReentrant to
       pdFALSE - in which case the semaphore will also be used to protect access to
       the media driver's read and write functions. */
    BaseType_t xBlockDeviceIsReentrant;

} FF_CreationParameters_t;
```
*The FF_CreationParameters_t structure*


**Parameters:**

+ *pxParameters*

  A structure of type FF\_CreationParameters\_t, which defines the IO manager being created.

+ *pxError*

  Used to pass out an error code.


**Returns:**

If the IO manager was created successfully then a pointer to the created
IO manager is returned and *pxError is set to FF\_ERR\_NONE.
If the IO manager was not created successfully then NULL is returned and *pxError is set to an error
code. FF\_GetErrMessage() converts error codes into error descriptions.


**Example usage:**

The page that documents [how to create a FreeRTOS-Plus-FAT](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)
media driver also demonstrates how to use the FF\_CreateIOManger()
function.
