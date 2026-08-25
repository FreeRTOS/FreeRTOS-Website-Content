---
title: "创建媒体驱动程序：FF_Disk_t 结构体"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[创建 FreeRTOS-Plus-FAT 媒体驱动程序](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)

FreeRTOS-Plus-FAT 将所有媒体类型共有的信息存储在
FF_Disk_t 类型的结构体中。媒体驱动程序可以扩展 FF_Disk_t 结构体，
以包含特定于正在使用的媒体的其他信息。
例如，
[FreeRTOS-Plus-FAT 的 RAM 磁盘驱动程序使用的初始化函数](Media_Driver_Initialisation)
可扩展 FF_Disk_t 结构体，以包含指向用作磁盘的 RAM 缓冲区的指针。

要创建 FF_Disk_t 结构体的 pxIOManager 成员，
请调用 [FF_CreateIOManager()](FF_CreateIOManager)。

建议在分配后将整个结构体清零，
以确保媒体驱动程序与未来的
FreeRTOS-Plus-FAT 版本兼容，其中 FF_Disk_t 结构体可能包含
其他成员。

```c
/* Structure that contains fields common to all media drivers, and can be
   extended to contain additional fields to tailor it for use with a specific media
   type. */
struct xFFDisk
{
    struct
    {
        /* Flags that can optionally be used by the media driver to ensure the
           disk has been initialised, registered and mounted before it is accessed. */
        uint32_t bIsInitialised : 1;
        uint32_t bIsRegistered : 1;
        uint32_t bIsMounted : 1;
        uint32_t spare0 : 5;

        /* The partition number on the media described by this structure. */
        uint32_t bPartitionNumber : 8;
        uint32_t spare1 : 16;
    } xStatus;

    /* Provided to allow this structure to be extended to include additional
       attributes that are specific to a media type. */
    void *pvTag;

    /* Points to input and output manager used by the disk described by this
       structure. */
    FF_IOManager_t *pxIOManager;

    /* The number of sectors on the disk. */
    uint32_t ulNumberOfSectors;

    /* Field that can optionally be set to a signature that is unique to the
       media. Read and write functions can check the ulSignature field to validate
       the media type before they attempt to access the pvTag field, or perform any
       read and write operations. */
    uint32_t ulSignature;
};

typedef struct xFFDisk FF_Disk_t;

```
*FF_Disk_t 结构体*
