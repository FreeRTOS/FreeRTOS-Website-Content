---
title: "ff_fread()"
description: FreeRTOS+FAT ff_fread API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)


ff_stdio.h
```c
size_t ff_fread( void *pvBuffer, size_t xSize, size_t xItems, FF_FILE * pxStream );	
```

Reads data from the current read/write position within an open file in
 the embedded FAT file system. The read/write position is incremented by the
 number of bytes read.
 

## Parameters 

+ *pvBuffer* 
  
  A pointer to the buffer into which data read from the file will be placed.
   The buffer must be at least large enough to hold the number of bytes being
   read.

+ *xSize* 
  
  The size in bytes of each item being read from the file.

+ *xItems* 

  The number of items to read from the file. The size of each item is set by
  the xSize parameter.

+ *pxStream*

  A pointer to the file from which the data is being read. This is the same
   pointer that was returned from the call to ff_fopen() used to originally 
   open the file.

## Returns

The number of items actually read from the file
 is returned. The number of items read from the file will only equal the
 number of items read from the file when the item size is 1. The size of
 each item is set by the xSize parameter.
 

If the number of items read from the file is less than the xItems value
 then the task's [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)
 is set to indicate the reason. A task can obtain its errno value using the
 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API function.
 
## Example usage 

The example provided on the [ff_fopen()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_fopen) documentation page shows how ff_fread() is used.
