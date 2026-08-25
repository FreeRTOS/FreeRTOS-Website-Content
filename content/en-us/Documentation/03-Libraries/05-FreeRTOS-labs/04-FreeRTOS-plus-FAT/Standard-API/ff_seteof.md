---
title: "ff_seteof()"
description: FreeRTOS+FAT ff_seteof API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_seteof( FF_FILE *pxStream );
```
Truncates a file to the file's current read/write position. The file must have previously been opened using
[ff_fopen()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_fopen)
 with the mode string set to "a" or "w".

## Parameters
+ *pxStream*

  The file being truncated.

## Returns

If the file was successfully truncated then zero is returned.

If the file could not be truncated then FF_EOF is returned and the task's 
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)
 is set to indicate the reason. A task can obtain its errno value using the
 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API function.

## Example usage

```c
void vSampleFunction( char *pcFileName, long lTruncatePosition )  
{  
    FF_FILE *pxFile;  
    
    /* Open the file specified by the pcFileName parameter. */  
    pxFile = ff_fopen( pcFileName, "a" );  
    
    /* Move the current read/write position to the position specified by  
       the lTruncatePosition parameter. */  
    ff_fseek( pxFile, lTruncatePosition, FF_SEEK_SET );  
    
    /* Truncate the file so all data past the current file position is lost. */  
    if( ff_seteof( pxFile ) != FF_EOF )  
    {  
    /* The truncate failed. */  
    }  
    
    /* Finished with the file. */  
    ff_fclose( pxFile );  
}  
```
*Example use of the ff_seteof() API function*
