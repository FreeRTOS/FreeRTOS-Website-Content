---
title: "ff_fwrite()"
description: FreeRTOS+FAT ff_fwrite API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
size_t ff_fwrite( const void *pvBuffer, size_t xSize, size_t xItems, FF_FILE * pxStream );
```
Writes data to the current read/write position within an open file in the
 embedded FAT file system. The read/write position is incremented by the number
 of bytes written.


## Parameters 
+ *pvBuffer*

  A pointer to the source of the data to be written to the file.

+ *xSize*

  The size in bytes of each item being written to the file.

+ *xItems*

  The number of items to write to the file. The size of each item is set by the
   xSize parameter.

+ *pxStream*

  A pointer to the file to which the data is being written. This is the same
  pointer that was returned from the call to ff_fopen() used to originally
  open the file.

## Returns

 The number of items actually written to the file is returned. The number of
 items written to the file will only equal the number of bytes written to the
 file when the item size is 1. The size of each item is set by the xSize 
 parameter.

 If the number of items written to the file is less than the xItems value then the task's
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)
 is set to indicate the reason. A task can obtain its errno value using the
 [stdioGET_ERRNO()()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API function.
 

## Example usage

The example provided on the [ff_fopen()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_fopen) documentation page shows how ff_fwrite() is used.
