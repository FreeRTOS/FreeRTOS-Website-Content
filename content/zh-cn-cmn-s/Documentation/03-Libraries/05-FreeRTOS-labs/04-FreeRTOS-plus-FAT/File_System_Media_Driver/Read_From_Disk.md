---
title: "创建媒体驱动程序：读取扇区"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[创建一个 FreeRTOS-Plus-FAT 媒体驱动程序](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)]

每个 FreeRTOS-Plus-FAT 媒体驱动程序都需要一个函数来
从存储嵌入式文件系统的媒体中读取扇区。读取函数的
实际工作方式取决于媒体类型。例如，如果
媒体是 RAM 磁盘，则可以使用 memcpy() 从 RAM 读取数据，
但如果媒体是 SD 卡，则卡的命令接口
必须通过 MMC 或 SPI 外围驱动器使用。


### 读取函数

读取函数可以具有任何名称，但必须具有以下原型:

```c
int32_t prvFFRead( uint8_t *pucDestination, /* Destination for data being read. */
                   uint32_t ulSectorNumber, /* Sector from which to start reading data. */
                   uint32_t ulSectorCount,  /* Number of sectors to read. */
                   FF_Disk_t *pxDisk );     /* Describes the disk being read from. */

```
*用于从媒体读取扇区的函数的原型，该媒体可保留嵌入式文件系统*

示例大致描述了
FreeRTOS-Plus-FAT RAM 磁盘驱动程序中使用的读取函数。完整版本包含输入参数检查，
可在 /FreeRTOS-Plus/Source/FreeRTOS-Plus-FAT/portable/common/ff_ramdisk.c 中找到。


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
*RAM 磁盘驱动程序使用的读取函数（为清晰起见，未显示输入参数检查）*
