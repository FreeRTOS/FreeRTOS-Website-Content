---
title: "ff_filelength()"
description: FreeRTOS+FAT ff_filelength API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
size_t ff_filelength( FF_FILE *pxStream );
```
Return the length in bytes of a file that has been opened for reading.

## Parameters 
 - *pxStream*

  A pointer to the file being queried. This will be the same pointer returned
   by [ff_fopen()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_fopen)
   when the file was originally opened.

## Returns
If the length of the file was successfully obtained then the file's length
 is returned.

If the length of the file could not be obtained then 0 is returned and the task's
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)
 is set to indicate the reason. The length of a file can only be obtained if the file is open
 for reading and the file's length fits in a variable of type size_t.
