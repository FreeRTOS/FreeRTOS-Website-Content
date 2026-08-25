---
title: "创建媒体驱动器：驱动器初始化函数"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[创建一个 FreeRTOS-Plus-FAT 媒体驱动程序](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)]


![](/media/2018/disk_driver_initialisation_function.png)
*媒体驱动程序的初始化函数中执行的操作（可选步骤）*

媒体驱动程序初始化函数必须分配 [FF_Disk_t](FF_Disk_t)
结构体，以供媒体使用。

FF_Disk_t 结构体包含指向 FF_IOManager_t 结构体的指针。
FF_IOManager_t 结构体的创建需调用 [FF_CreateIOManager()](FF_CreateIOManager)。

为方便起见，媒体驱动程序还可以
择性在媒体上[挂载分区](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_Mount)
然后[将挂载的分区添加到 FreeRTOS-Plus-FAT 的虚拟文件系统中](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_FS_Add)。
在初始化函数内执行这两个可选步骤后，
应用程序编写者便无需显式执行这些步骤。右图
显示了执行这些可选步骤的媒体驱动程序的
初始化函数。


#### 工作示例

以下示例大致描述了
FreeRTOS-Plus-FAT RAM 磁盘驱动程序使用的媒体驱动程序初始化函数。如需包含更多错误检查的
完整版本，请参阅
/FreeRTOS-Plus/Source/FreeRTOS-Plus-FAT/portable/common/ff_ramdisk.c。


```c
/* The size of each sector on the disk. */
#define ramSECTOR_SIZE                512UL

/* Only a single partition is used. Partition numbers start at 0. */
#define ramPARTITION_NUMBER            0

/*
In this example:
 - pcName is the name to give the disk within FreeRTOS-Plus-FAT's virtual file system.
 - pucDataBuffer is the start of the RAM buffer used as the disk.
 - ulSectorCount is effectively the size of the disk, each sector is 512 bytes.
 - xIOManagerCacheSize is the size of the IO manager's cache, which must be a
 multiple of the sector size, and at least twice as big as the sector size.
*/
[FF_Disk_t](FF_Disk_t) *FF_RAMDiskInit( char *pcName,
                          uint8_t *pucDataBuffer,
                          uint32_t ulSectorCount,
                          size_t xIOManagerCacheSize )
{
FF_Error_t xError;
[FF_Disk_t](FF_Disk_t) *pxDisk = NULL;
FF_CreationParameters_t xParameters;

    /* Check the validity of the xIOManagerCacheSize parameter. */
    [configASSERT](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)( ( xIOManagerCacheSize % ramSECTOR_SIZE ) == 0 );
    configASSERT( ( xIOManagerCacheSize >= ( 2 * ramSECTOR_SIZE ) ) );

    /* Attempt to allocated the [FF_Disk_t](FF_Disk_t) structure. */
    pxDisk = ( FF_Disk_t * ) pvPortMalloc( sizeof( FF_Disk_t ) );

    if( pxDisk != NULL )
    {
        /* It is advisable to clear the entire structure to zero after it has been
           allocated - that way the media driver will be compatible with future
           FreeRTOS-Plus-FAT versions, in which the FF_Disk_t structure may include
           additional members. */
        memset( pxDisk, '�', sizeof( FF_Disk_t ) );

        /* The pvTag member of the FF_Disk_t structure allows the structure to be
           extended to also include media specific parameters. The only media
           specific data that needs to be stored in the FF_Disk_t structure for a
           RAM disk is the location of the RAM buffer itself - so this is stored
           directly in the FF_Disk_t's pvTag member. */
        pxDisk->pvTag = ( void * ) pucDataBuffer;

        /* The signature is used by the disk read and disk write functions to
           ensure the disk being accessed is a RAM disk. */
        pxDisk->ulSignature = ramSIGNATURE;

        /* The number of sectors is recorded for bounds checking in the read and
           write functions. */
        pxDisk->ulNumberOfSectors = ulSectorCount;

        /* Create the IO manager that will be used to control the RAM disk -
           the FF_CreationParameters_t structure completed with the required
           parameters, then passed into the [FF_CreateIOManager()](FF_CreateIOManager) function. */
        memset (&xParameters, '�', sizeof xParameters);
        xParameters.pucCacheMemory = NULL;
        xParameters.ulMemorySize = xIOManagerCacheSize;
        xParameters.ulSectorSize = ramSECTOR_SIZE;
        xParameters.fnWriteBlocks = prvWriteRAM;
        xParameters.fnReadBlocks = prvReadRAM;
        xParameters.pxDisk = pxDisk;

        /* The driver is re-entrant as it just accesses RAM using memcpy(), so
           xBlockDeviceIsReentrant can be set to pdTRUE. In this case the
           semaphore is only used to protect FAT data structures, and not the read
           and write function. */
        xParameters.pvSemaphore = ( void * ) xSemaphoreCreateRecursiveMutex();
        xParameters.xBlockDeviceIsReentrant = pdTRUE;

        pxDisk->pxIOManager = [FF_CreateIOManger](FF_CreateIOManager)( &xParameters, &xError );

        if( ( pxDisk->pxIOManager != NULL ) && ( FF_isERR( xError ) == pdFALSE ) )
        {
            /* Record that the RAM disk has been initialised. */
            pxDisk->xStatus.bIsInitialised = pdTRUE;

            /* Create a partition on the RAM disk. NOTE! The disk is only
               being partitioned here because it is a new RAM disk. It is
               known that the disk has not been used before, and cannot already
               contain any partitions. Most media drivers will not perform
               this step because the media will already been partitioned and
               formatted. */
            xError = prvPartitionAndFormatDisk( pxDisk );

            if( FF_isERR( xError ) == pdFALSE )
            {
                /* Record the partition number the FF_Disk_t structure is, then
                   mount the partition. */
                pxDisk->xStatus.bPartitionNumber = ramPARTITION_NUMBER;

                /* Mount the partition. */
                xError = FF_Mount( pxDisk, ramPARTITION_NUMBER );
            }

            if( FF_isERR( xError ) == pdFALSE )
            {
                /* The partition mounted successfully, add it to the virtual
                   file system - where it will appear as a directory off the file
                   system's root directory. */
                [FF_FS_Add](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_FS_Add)( pcName, pxDisk->pxIOManager );
            }
        }
        else
        {
            /* The disk structure was allocated, but the disk's IO manager could
               not be allocated, so free the disk again. */
            FF_RAMDiskDelete( pxDisk );
            pxDisk = NULL;
        }
    }

    return pxDisk;
}

```
*媒体驱动程序初始化函数的概述*
