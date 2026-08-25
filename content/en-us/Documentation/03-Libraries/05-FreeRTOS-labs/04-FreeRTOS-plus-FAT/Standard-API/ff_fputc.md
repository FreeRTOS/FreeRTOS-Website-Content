---
title: "ff_fputc()"
description: FreeRTOS+FAT ff_fputc API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_fputc( int iChar, FF_FILE * pxStream );	
```
Write a single byte to an open file in the embedded FAT file system.

The read/write position is incremented by one.

Passing a char in an int may not seem optimal, but the ff_fputc()
 prototype conforms to the standand and expected stdio fputc() 
 function prototype.

## Parameters 

+ *iChar*
  
  The value written to the file. The value is converted to an unsigned char 
   (8-bit) before it is written.

+ *pxStream* 
  
  A pointer to the file to which the character is being written. This is the
   same pointer that was returned from the call to ff_fopen() used to 
   originally open the file.

## Returns

On success the byte written to the file is returned. If any other value
 is returned then the byte was not written to the file and the task's
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)
 will be set to indicate the reason. A task can obtain its errno value using the
 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API function.

## Example usage 

```c
void vSampleFunction( char *pcFileName, int32_t lNumberToWrite )
{
    FF_FILE *pxFile;
    const int iCharToWrite = 'A';
    int iCharWritten;
    int32_t lBytesWritten;

    /* Open the file specified by the pcFileName parameter for writing. */
    pxFile = ff_fopen( pcFileName, "w" );

    /* Write 'A' to the file the number of times specified by the
       lNumberToWrite parameter. */
    for( lBytesWritten = 0; lBytesWritten < lNumberToWrite; lBytesWritten++ )
    {
        /* Write the byte. */
        iCharWritten = ff_fputc( iCharToWrite, pxFile );

        /* Was the character written to the file successfully? */
        if( iCharWritten != iCharToWrite )
        {
            /* The byte could not be written to the file. */
            break;
        }
    }

    /* Finished with the file. */
    ff_fclose( pxFile );
}
```
*Example use of the ff_fputc() API function*
