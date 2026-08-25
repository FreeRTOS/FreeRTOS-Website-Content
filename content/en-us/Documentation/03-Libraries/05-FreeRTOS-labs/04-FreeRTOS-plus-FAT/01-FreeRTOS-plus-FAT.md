---
title: FreeRTOS-Plus-FAT
---
DOS Compatible Embedded FAT File System


**NOTE**:
FreeRTOS-Plus-FAT is a [FreeRTOS Labs](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction) project. It is fully functional,
and quite mature, but as an originally acquired (rather than authored) product it does not necessarily
meet our production code or testing standards. It is available from
the [Lab-Project-FreeRTOS-FAT](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-FAT) repository on GitHub.


FreeRTOS-Plus-FAT is an open source, thread aware and scalable FAT12/FAT16/FAT32 DOS/Windows
compatible embedded FAT file system which was recently acquired
by [Real Time Engineers ltd.](/Why-FreeRTOS/Support-options) for
use with and without the RTOS.

FreeRTOS-Plus-FAT is already used in commercial products, and is the file system
used in the [FTP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/06-FTP-server)
and [HTTP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/07-HTTP-web-server)
server examples that are documented on
the [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP) pages.


The [standard C library style API](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)
includes a thread local errno value, and the lower level native API
provides a rich set of detailed error codes.

We are currently working hard on improving the embedded file system's
documentation, adding additional scalability options, and updating the
source code to ensure it conforms with our strict coding standards.
We encourage you to download FreeRTOS-Plus-FAT to try the embedded FAT file
system for yourself while we continue this work.

**Why use FreeRTOS-Plus-FAT**

+ Fully thread aware
+ Scalable
+ Optional long file name support
+ Optional directory name hashing for speed
+ FAT12, FAT16 and FAT32 support
+ Task specific working directories
+ Task specific errno support
+ Additional comprehensive error reporting
+ Standard and comprehensive API
+ Supported technology
