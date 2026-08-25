---
title: "Standard API errno Values"
description: FreeRTOS+FAT errno API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

The FreeRTOS-Plus-FAT file system's standard API uses the same errno values
as used by the standard C library. File related functions in standard C library return 0 for pass, and -1 for fail. If -1 is returned then the reason for the failure is
stored in a variable called errno, which must be inspected separately.

Similarly, FreeRTOS-Plus-FAT's standard API returns 0 for and -1 for fail, and maintains an errno variable
for each RTOS task. A task can retrieve its errno value by calling stdioGET_ERRNO(). The error codes returned by stdioGET_ERRNO() are defined in `projdefs.h` files and are listed below.

|  |  |  |
| --- | --- | --- |
| **Value** | **Constant** | **Description** |
| 0 | pdFREERTOS_ERRNO_NONE | No such file or directory |
| 2 | pdFREERTOS_ERRNO_ENOENT | No such file or directory |
| 5 | pdFREERTOS_ERRNO_EIO | I/O error |
| 6 | pdFREERTOS_ERRNO_ENXIO | No such device or address |
| 9 | pdFREERTOS_ERRNO_EBADF | Bad file number |
| 11 | pdFREERTOS_ERRNO_EAGAIN | No more processes |
| 11 | pdFREERTOS_ERRNO_EWOULDBLOCK | Operation would block |
| 12 | pdFREERTOS_ERRNO_ENOMEM | Not enough core |
| 13 | pdFREERTOS_ERRNO_EACCES | Permission denied |
| 14 | pdFREERTOS_ERRNO_EFAULT | Bad address |
| 16 | pdFREERTOS_ERRNO_EBUSY | Mount device busy |
| 17 | pdFREERTOS_ERRNO_EEXIST | File exists |
| 18 | pdFREERTOS_ERRNO_EXDEV | Cross-device link |
| 19 | pdFREERTOS_ERRNO_ENODEV | No such device |
| 20 | pdFREERTOS_ERRNO_ENOTDIR | Not a directory |
| 21 | pdFREERTOS_ERRNO_EISDIR | Is a directory |
| 22 | pdFREERTOS_ERRNO_EINVAL | Invalid argument |
| 28 | pdFREERTOS_ERRNO_ENOSPC | No space left on device |
| 29 | pdFREERTOS_ERRNO_ESPIPE | Illegal seek |
| 30 | pdFREERTOS_ERRNO_EROFS | Read only file system |
| 42 | pdFREERTOS_ERRNO_EUNATCH | Protocol driver not attached |
| 50 | pdFREERTOS_ERRNO_EBADE | Invalid exchange |
| 79 | pdFREERTOS_ERRNO_EFTYPE | Inappropriate file type or format |
| 89 | pdFREERTOS_ERRNO_ENMFILE | No more files |
| 90 | pdFREERTOS_ERRNO_ENOTEMPTY | Directory not empty |
| 91 | pdFREERTOS_ERRNO_ENAMETOOLONG | File or path name too long |
| 95 | pdFREERTOS_ERRNO_EOPNOTSUPP | Operation not supported on transport endpoint |
| 105 | pdFREERTOS_ERRNO_ENOBUFS | No buffer space available |
| 109 | pdFREERTOS_ERRNO_ENOPROTOOPT | Protocol not available |
| 112 | pdFREERTOS_ERRNO_EADDRINUSE | Address already in use |
| 116 | pdFREERTOS_ERRNO_ETIMEDOUT | Connection timed out |
| 119 | pdFREERTOS_ERRNO_EINPROGRESS | Connection already in progress |
| 120 | pdFREERTOS_ERRNO_EALREADY | Socket already connected |
| 125 | pdFREERTOS_ERRNO_EADDRNOTAVAIL | Address not available |
| 127 | pdFREERTOS_ERRNO_EISCONN | Socket is already connected |
| 128 | pdFREERTOS_ERRNO_ENOTCONN | Socket is not connected |
| 135 | pdFREERTOS_ERRNO_ENOMEDIUM | No medium inserted |
| 138 | pdFREERTOS_ERRNO_EILSEQ | An invalid UTF-16 sequence was encountered |
| 140 | pdFREERTOS_ERRNO_ECANCELED | Operation cancelled |

 
Native API errno Values
-----------------------
[FreeRTOS-Plus-FAT Native API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)


The file system's native API has a more sophisticated error code system, and returns error codes directly from its API functions. Error codes used by native APIs are defined in `ff_error.h`.
