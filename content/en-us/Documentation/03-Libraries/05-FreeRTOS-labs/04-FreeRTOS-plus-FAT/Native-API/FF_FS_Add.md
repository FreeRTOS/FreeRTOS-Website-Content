---
title: "FF_FS_Add()"
description: FreeRTOS+FAT FF_FS_Add API documentation
---
[FreeRTOS-Plus-FAT Native API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_sys.h
```c
BaseType_t FF_FS_Add( const char *pcPath, FF_Disk_t *pxDisk );
```

Adds a mounted partition to the FreeRTOS-Plus-FAT virtual file system, where
it will appear as a directory off the file system's root directory.
 

## Parameters 

+ *pcPath* 

  The name used for the partition within the virtual file system. For example,
  if pcPath is "/SDCard" then the partition will appear as /SDCard in the 
  file system's root directory.

  pcPath must be an absolute path that starts with a forward slash (/).

+ *pdDisk* 

  The FF_Disk_t structure used to access and manage the partition being added
   to the file system.


## Returns

If the partition was successfully added to the FreeRTOS-Plus-FAT virtual file
system then 1 is returned, otherwise 0 is returned.
 
