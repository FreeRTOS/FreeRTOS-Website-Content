---
title: "ff_stat()"
description: FreeRTOS+FAT ff_stat API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_stat( const char *pcFileName, FF_Stat_t *pxStatBuffer );
```
Populates an FF_Stat_t with information about a file. FF_Stat_t contains the following fields:

+ st_dev 

  The Device ID of the device containing the file.

+ st_ino

  The file's serial number.

+ st_mode

   If the file is a directory then st_mode will be set toFF_IFDIR. Otherwise st_mode will be set to FF_IFREG (regular).

+ st_nlink 

  Number of hard links to the fileHard coded to 1.

+ st_uid

  User ID of file

+ st_gid

  Group ID of the file

+ st_rdev

   Device ID

+ st_size

   The size of the file in bytes. ff_stat() cannot be used toobtain the size of an open file.

+ st_atime 

  The time the file was last accessed. Only available if FF_TIME_SUPPORT is set to 1 in FreeRTOSFATConfig.h.

+ st_mtime 

  The time the file was last modified. Only available if FF_TIME_SUPPORT is set to 1 in FreeRTOSFATConfig.h.

+ st_ctime 

  The time the status of the file last changed. Only available if FF_TIME_SUPPORT is set to 1 in FreeRTOSFATConfig.h.

## Parameters

+ *pcFileName*

  A pointer to a standard null terminated C string that holds the name of the file on which stat information 
  is being retrieved. The file name can include a relative path to the directory.

+ *pxStatBuffer*

  A pointer to the FF_Stat_t to fill with information on the file.


## Returns

+ If the stat structure was populated with information about the file then zero is returned.

+ If the stat structure could not be populated with information about the file then -1 is returned 
  and the task's [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)
  is set to indicate the reason. A task can obtain its errno value using the
  [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
  API function.


## Example usage

```c
long lGetFileLength( char *pcFileName )  
{  
    FF_Stat_t xStat;  
    long lReturn;  
  
    /* Find the length of the file with name pcFileName. */  
    if( ff_stat( pcFileName, &xStat ) == 0 )  
    {  
        lReturn = xStat.st_size;  
    }  
    else  
    {  
        /* Could not obtain the length of the file. */  
        lReturn = -1;  
    }
    return lReturn;  
}
```
*Example use of the ff_stat() API function*
