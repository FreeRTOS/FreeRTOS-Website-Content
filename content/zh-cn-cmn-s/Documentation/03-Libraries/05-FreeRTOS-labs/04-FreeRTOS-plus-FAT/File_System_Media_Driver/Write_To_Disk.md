---
title: "创建媒体驱动程序：写入扇区"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[创建一个 FreeRTOS-Plus-FAT 媒体驱动程序](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)]


每个 FreeRTOS-Plus-FAT 媒体驱动程序都需要一个函数来
将扇区写入存储嵌入式文件系统的媒体。写入函数的实际作用取决于媒体类型
。例如，
如果媒体是 RAM 磁盘，则可以使用 memcpy() 将数据写入 RAM，
但如果媒体是 SD 卡，则卡的命令接口将
必须通过 MMC 或 SPI 外围设备驱动器使用。


### 写入函数

写入函数可以使用任何名称，但必须具备以下原型：

```c
int32_t FFWrite( uint8_t *pucSource,      /* Source of data to be written. */
                 uint32_t ulSectorNumber, /* The first sector being written to. */
                 uint32_t ulSectorCount,  /* The number of sectors to write. */
                 FF_Disk_t *pxDisk );     /* Describes the disk being written to. */

```
*用于写入媒体的函数的原型，该媒体可保留嵌入式文件系统*

以下示例大致描述了
FreeRTOS-Plus-FAT RAM 磁盘驱动器中使用的读取函数。完整版本包含输入参数检查，
位于
/FreeRTOS-Plus/Source/FreeRTOS-Plus-FAT/portable/common/ff_ramdisk.c。

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
*RAM 磁盘驱动器使用的写入函数（为清晰起见，未显示输入参数检查*）
