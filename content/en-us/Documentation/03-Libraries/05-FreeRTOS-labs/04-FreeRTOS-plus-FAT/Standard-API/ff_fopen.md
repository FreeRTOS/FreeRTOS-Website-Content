---
title: "ff_fopen()"
description: FreeRTOS+FAT ff_fopen API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
FF_FILE *ff_fopen( const char *pcFile, const char *pcMode );	
```
Opens a file in the embedded FAT file system.

## Parameters 
+ *pcFile*

  A pointer to a standard null terminated C string that holds the name of the file being opened. The string can include a relative path.

+ *pcMode*

  A string that sets the mode in which the file is opened. 
  Valid strings include:

  - "r": Open the file for reading only.

  - "r+": Open the file for reading and writing.

  - "w": Open a file for reading and writing. If the file already exists it 
    will be truncated to zero length. If the file does not already exist it 
    will be created.

  - "a" Open a file for writing. If the file already exists then new data 
    will be appended to the end of the file. If the file does not already
    exist it will be created.

  - "a+": Open a file for reading and writing. If the file already exists
    then new data will be appended to the end of the file. If the file does
    not already exist it will be created. Files are always opened in binary mode.

## Returns
If the file was opened successfully then a pointer to the file is
 returned.

If the file could not be opened then NULL is returned and the task's
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)
 is set to indicate the reason. A task can obtain its errno value using the
 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API function.

## Example usage 
```c
BaseType_t xCopyFile( char *pcSourceFileName, char *pcDestinationFileName )
{
    FF_FILE *pxSourceFile, *pxDestinationFile;
    size_t xCount;
    uint32_t ucBuffer[ 50 ];

    /* Open the source file in read only mode. */
    pxSourceFile = ff_fopen( pcSourceFileName, "r" );

    if( pxSourceFile != NULL )
    {
        /* Create or overwrite a writable file. */
        pxDestinationFile = ff_fopen( pcDestinationFileName, "w+" );

        if( pxDestinationFile != NULL )
        {
            for( ;; )
            {
                /* Read sizeof( ucBuffer ) bytes from the source file into a buffer. */
                xCount = ff_fread( ucBuffer, 1, sizeof( ucBuffer ), pxSourceFile );

                /* Write however many bytes were read from the source file into the
                   destination file. */
                ff_fwrite( ucBuffer, xCount, 1, pxDestinationFile );

                if( xCount < sizeof( ucBuffer ) )
                {
                    /* The end of the file was reached. */
                    break;
                }
            }

            /* Close the destination file. */
            ff_fclose( pxDestinationFile );
        }

        /* Close the source file. */
        ff_fclose( pxSourceFile );
    }
}
```
*Example use of the ff_fopen() API function to open or create a file*
