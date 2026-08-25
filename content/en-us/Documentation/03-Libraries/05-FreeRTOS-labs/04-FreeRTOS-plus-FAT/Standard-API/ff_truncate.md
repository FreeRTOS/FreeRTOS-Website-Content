---
title: "ff_truncate()"
description: FreeRTOS+FAT ff_truncate API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h

```c
FF_FILE *ff_truncate( const char * pcFileName, long lTruncateSize );
```

Opens a file for writing, pointing to the end of the file,
 then truncates the file’s length to lTruncateSize.

If the file was longer than lTruncateSize then the data past lTruncateSize
 is discarded.

If the file was shorter than lTruncateSize then new data added to the end
 of the file is set to 0.

When ff_truncate() is called, writing in the opened file is done at the end.
 So, after opening the file with ff_truncate(),
 [ff_fseek()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_fseek) or
 [ff_rewind()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_rewind)
 can be called to write at any desired location.


## Parameters

+ *pcFileName*

  A pointer to a standard null terminated C string that holds the name of the file being opened and truncated. 
  The file name can include a relative path to the file.

+ *lTruncateSize*

  The length, in byte, to which the file's length will be set.


## Returns

If the length of the file was successfully set to lTruncateSize then a
pointer to the opened file is returned.

If the length of the file was not successfully set to lTruncateSize 
 then NULL is returned, the file will remain closed, and the task's
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno) is set to indicate the reason. A task can obtain 
 its errno value using the [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API function.


## Example usage

```c
void vSampleFunction( char *pcFileName, long lLength )  
{  
    FF_FILE *pxFile;  
  
    /* Open and truncate the file specified by the pcFileName parameter. */  
    pxFile = ff_truncate( pcFileName, lLength );  
  
    if( pxFile == NULL )  
    {  
        /* The file could not be opened, or the file could not be truncated. */  
    }  
    else  
    {  
        /* The file was opened and the file length was set. */  
  
        /*  
         * The file can be accessed here.  
         */  
      
        /* Close the file when it is no longer required. */  
        ff_fclose( pxFile );  
    }  
}  
```
*Example use of the ff_truncate() API function*
