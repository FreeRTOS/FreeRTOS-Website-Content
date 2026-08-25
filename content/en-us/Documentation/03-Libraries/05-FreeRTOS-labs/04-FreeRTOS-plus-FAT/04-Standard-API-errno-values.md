---
title: "Reference: errno values"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## Standard API errno Values

#### [[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)]

The FreeRTOS-Plus-FAT file system's standard API uses the same errno values
as used by the standard C library. File related functions in standard C library return 0 for pass,
and -1 for fail. If -1 is returned then the reason for the failure is
stored in a variable called errno, which must be inspected separately.

Similarly, FreeRTOS-Plus-FAT's standard API returns 0 for and -1 for fail, and maintains an errno variable
for each RTOS task. A task can retrieve its errno value by calling stdioGET\_ERRNO(). The error codes
returned by stdioGET\_ERRNO() are defined in \<projdefs.h\> files and are listed below.

| **Value** | **Constant**                     | **Description**                               |
| --------- | -------------------------------- | --------------------------------------------- |
| 0         | pdFREERTOS\_ERRNO\_NONE          | No such file or directory                     |
| 2         | pdFREERTOS\_ERRNO\_ENOENT        | No such file or directory                     |
| 5         | pdFREERTOS\_ERRNO\_EIO           | I/O error                                     |
| 6         | pdFREERTOS\_ERRNO\_ENXIO         | No such device or address                     |
| 9         | pdFREERTOS\_ERRNO\_EBADF         | Bad file number                               |
| 11        | pdFREERTOS\_ERRNO\_EAGAIN        | No more processes                             |
| 11        | pdFREERTOS\_ERRNO\_EWOULDBLOCK   | Operation would block                         |
| 12        | pdFREERTOS\_ERRNO\_ENOMEM        | Not enough core                               |
| 13        | pdFREERTOS\_ERRNO\_EACCES        | Permission denied                             |
| 14        | pdFREERTOS\_ERRNO\_EFAULT        | Bad address                                   |
| 16        | pdFREERTOS\_ERRNO\_EBUSY         | Mount device busy                             |
| 17        | pdFREERTOS\_ERRNO\_EEXIST        | File exists                                   |
| 18        | pdFREERTOS\_ERRNO\_EXDEV         | Cross-device link                             |
| 19        | pdFREERTOS\_ERRNO\_ENODEV        | No such device                                |
| 20        | pdFREERTOS\_ERRNO\_ENOTDIR       | Not a directory                               |
| 21        | pdFREERTOS\_ERRNO\_EISDIR        | Is a directory                                |
| 22        | pdFREERTOS\_ERRNO\_EINVAL        | Invalid argument                              |
| 28        | pdFREERTOS\_ERRNO\_ENOSPC        | No space left on device                       |
| 29        | pdFREERTOS\_ERRNO\_ESPIPE        | Illegal seek                                  |
| 30        | pdFREERTOS\_ERRNO\_EROFS         | Read only file system                         |
| 42        | pdFREERTOS\_ERRNO\_EUNATCH       | Protocol driver not attached                  |
| 50        | pdFREERTOS\_ERRNO\_EBADE         | Invalid exchange                              |
| 79        | pdFREERTOS\_ERRNO\_EFTYPE        | Inappropriate file type or format             |
| 89        | pdFREERTOS\_ERRNO\_ENMFILE       | No more files                                 |
| 90        | pdFREERTOS\_ERRNO\_ENOTEMPTY     | Directory not empty                           |
| 91        | pdFREERTOS\_ERRNO\_ENAMETOOLONG  | File or path name too long                    |
| 95        | pdFREERTOS\_ERRNO\_EOPNOTSUPP    | Operation not supported on transport endpoint |
| 105       | pdFREERTOS\_ERRNO\_ENOBUFS       | No buffer space available                     |
| 109       | pdFREERTOS\_ERRNO\_ENOPROTOOPT   | Protocol not available                        |
| 112       | pdFREERTOS\_ERRNO\_EADDRINUSE    | Address already in use                        |
| 116       | pdFREERTOS\_ERRNO\_ETIMEDOUT     | Connection timed out                          |
| 119       | pdFREERTOS\_ERRNO\_EINPROGRESS   | Connection already in progress                |
| 120       | pdFREERTOS\_ERRNO\_EALREADY      | Socket already connected                      |
| 125       | pdFREERTOS\_ERRNO\_EADDRNOTAVAIL | Address not available                         |
| 127       | pdFREERTOS\_ERRNO\_EISCONN       | Socket is already connected                   |
| 128       | pdFREERTOS\_ERRNO\_ENOTCONN      | Socket is not connected                       |
| 135       | pdFREERTOS\_ERRNO\_ENOMEDIUM     | No medium inserted                            |
| 138       | pdFREERTOS\_ERRNO\_EILSEQ        | An invalid UTF-16 sequence was encountered    |
| 140       | pdFREERTOS\_ERRNO\_ECANCELED     | Operation cancelled                           |

Native API errno Values

---

#### [[FreeRTOS-Plus-FAT Native API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)]

The file system's native API has a more sophisticated error code system, and returns error codes directly
from its API functions. Error codes used by native APIs are defined in \<ff\_error.h\>.
