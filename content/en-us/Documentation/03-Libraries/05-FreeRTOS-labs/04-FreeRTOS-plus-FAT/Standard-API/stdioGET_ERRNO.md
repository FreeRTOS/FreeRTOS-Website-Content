---
title: "stdioGET_ERRNO()"
description: FreeRTOS+FAT stdioGET_ERRNO API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
static portINLINE int stdioGET_ERRNO( void );
```

File related functions in the standard C library often return 0 for pass,
and -1 for fail. If -1 is returned then the reason for the failure is
stored in a variable called errno, which must be inspected separately.

FreeRTOS-Plus-FAT's standard stdio style interface maintains an errno variable
for each RTOS task. static portINLINE() returns the errno value for the calling
task.

Notes:
* The file system's C library style API uses the same errno values
  as used by the standard C library. These 
  [are documented on a separate page](errno).

* The file system's native API
  has a more sophisticated error code system, and  returns error codes directly from its API functions.

## Example usage

```c
void vAFunction( FF_FILE *pxFile, long lOffset, int iWhence )
{
    int iReturned;

    /* Attempt to seek a file using the parameters passed into this function. */
    iReturned = ff_fseek( pxFile, lOffset, iWhence );

    if( iReturned == 0 )
    {
        /* The call to ff_fseek() passed. */
    }
    else
    {
        /* The call to ff_fseek() failed. Obtain the errno to see why. */
        iReturned = stdioGET_ERRNO();

        if( iReturned == pdFREERTOS_ERRNO_ESPIPE )
        {
            /* The seek position was illegal - outside of the file's space. */
        }
        else if( iReturned == pdFREERTOS_ERRNO_EINVAL )
        {
            /* The value of iWhence was not legal. */
        }
    }
}
```
*Example use of the stdioGET_ERRNO() API function*
