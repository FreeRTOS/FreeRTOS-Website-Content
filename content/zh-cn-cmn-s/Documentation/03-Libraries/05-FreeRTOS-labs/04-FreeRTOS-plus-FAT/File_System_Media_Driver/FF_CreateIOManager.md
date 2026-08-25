---
title: "FF_CreateIOManager()"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[创建一个 FreeRTOS-Plus-FAT 媒体驱动程序](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)]

ff_ioman.h

```c
FF_IOManager_t *FF_CreateIOManger( FF_CreationParameters_t *pxParameters, FF_Error_t *pxError );

```

FreeRTOS-Plus-FAT [媒体驱动程序](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)
将所有媒体类型通用的信息存储在
[FF_Disk_t](FF_Disk_t) 类型的结构体中。
FF_Disk_t 结构体的 pxIOManager 成员引用了一个称为
输入/输出管理器（IO 管理器，或简称为 IOMAN）的对象。IO
管理器负责缓冲和缓存
文件和目录信息等。

FF_CreateIOManager() 创建一个 IO 管理器对象。

参数被传递到 FF_CreationParameters_t 结构体中的 FF_CreateIOManager
。

FF_CreationParameters_t 结构体的 pvSemaphore 成员必须通过调用
[xSemaphoreCreateRecursiveMutex()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/08-xSemaphoreCreateRecursiveMutex)
FreeRTOS API 函数来创建。

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
       basically a pointer back to the FF_Disk_t structure that contains the IO
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
*FF_CreationParameters_t 结构体*


**参数：**

+ *pxParameters*

  FF_CreationParameters_t 类型的结构体，定义了正在创建的 IO 管理器。

+ *pxError*

  用于传递错误代码。


**返回：**

如果 IO 管理器创建成功，则返回一个指向创建的 IO 管理器的指针，
并将 *pxError 设置为 FF_ERR_NONE。
如果 IO 管理器未创建成功，则返回 NULL，并将 *pxError 设置为错误代码
。FF_GetErrMessage() 可将错误代码转换为错误描述。


**用法示例：**

记录[如何创建 FreeRTOS-Plus-FAT](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)
媒体驱动程序的页面也演示了如何使用 FF_CreateIOManger() 函数
。
