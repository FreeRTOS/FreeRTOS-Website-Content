---
title: "Creating a Media Driver: The FF_Disk_t Structure"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[Creating a FreeRTOS-Plus-FAT Media Driver](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Creating_a_file_system_media_driver)

FreeRTOS-Plus-FAT stores information that is common to all media types in a
structure of type FF\_Disk\_t. Media drivers can extended the FF\_Disk\_t structure
to include additional information that is specific to the media in use.
For example,
the [initialisation function used by FreeRTOS-Plus-FAT's RAM disk driver](Media_Driver_Initialisation)
extends the FF\_Disk\_t structure to include a pointer to the RAM buffer used as the disk.

The pxIOManager member of the FF\_Disk\_t structure is created by
calling [FF\_CreateIOManager()](FF_CreateIOManager).

It is advisable to clear the entire structure to zero after it has been
allocated - that way the media driver will be compatible with future
FreeRTOS-Plus-FAT versions, in which the FF\_Disk\_t structure may include
additional members.

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
*The FF\_Disk\_t structure*
