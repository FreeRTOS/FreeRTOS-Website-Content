---
title: "ff_fclose()"
description: FreeRTOS+FAT ff_fclose API documentation
---
[[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)]

ff_stdio.h
```c
int ff_fclose( FF_FILE *pxStream );;
```
Flushes then closes a file within the embedded FAT file system. 
 The file must have previously been opened using [ff_fopen()](ff_fopen).

## Parameters 
+ *pxStream*

  A pointer to the file being closed. This will be the same pointer returned by
   ff_fopen() when the file was originally opened.

## Returns
If the file was closed successfully then 0 is returned.

If the file could not be closed then -1 is returned and the task's
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)
 is set to indicate the reason. A task can obtain its errno value using the
 [stdioGET_ERRNO](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API function.

## Example usage 
The example provided on the [ff_fopen()](ff_fopen) documentation
page shows how ff_fclose() is used.
