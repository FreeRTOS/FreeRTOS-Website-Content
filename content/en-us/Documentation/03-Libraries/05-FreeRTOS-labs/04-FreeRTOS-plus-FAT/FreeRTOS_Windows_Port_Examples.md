---
title: FreeRTOS-Plus-FAT Examples
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

The FreeRTOS-Plus-FAT examples described below are included in the 'comprehensive' demo project that
is [described on the FreeRTOS-Plus-TCP pages](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator).
The demo project can be built and executed using free development tools and in
a Windows environment.

Examples:

- [Creating a Disk](#creating-a-disk)
- [Creating, Writing and Reading Files](#creating-writing-and-reading-files)
- [File Related CLI Commands](#file-related-cli-commands)
- [FTP and HTTP Servers](#ftp-and-http-servers)

---

#### Creating a Disk

The [main.c](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)
source file includes a function called prvCreateDiskAndExampleFiles(),
which calls FF_RAMDiskInit().

FF_RAMDiskInit() is the [initialisation function](File_System_Media_Driver/Media_Driver_Initialisation)
for FreeRTOS-Plus-FAT's RAM disk media driver. It demonstrates how to [partition](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_Partition)
a disk, [format](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_Format)
a partition, [mount](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_Mount)
the formatted partition, and [add the mounted partition](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_FS_Add)
to the FreeRTOS-Plus-FAT virtual file system. The mounted partition appears
as /ram.


#### Creating, Writing and Reading Files

prvCreateDiskAndExampleFiles() also calls vCreateAndVerifyExampleFiles() which demonstrates the use
of [ff\_fread()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_fread), [ff\_fwrite()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_fwrite), [ff\_fgetc()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_fgetc)
and [ff\_fputc()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_fputc).

The files and directories created by prvCreateDiskAndExampleFiles()
can be viewed and manipulated using both the FTP server example
and the UDP command line interface (information on both of these below).


#### File Related CLI Commands

The UDP [command line interface example](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/UDP_CLI)
includes commands that allow files to be viewed, accessed and manipulated, as described in the
following table:

| Command             | Description                                                |
| ------------------- | ---------------------------------------------------------- |
| dir                 | View a directory listing                                   |
| cd \<path>          | Change the current working directory (CWD) to \<path>      |
| del \<file>         | Delete \<file>                                             |
| rmdir \<path>       | Remove the directory \<path> - the directory must be empty |
| type \<file>        | Display the contents of \<file>.                           |
| copy \<src> \<dest> | Copy the file \<src> to the file \<dest>                   |
| pwd                 | Print the working directory                                |

![Accessing the embedded FAT file system through the command line interface](/media/2018/File_System_Commands.png)
*Accessing the file system through the command line interface*


#### FTP and HTTP Servers

Both the [FTP example](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/06-FTP-server)
and the [HTTP example](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/07-HTTP-web-server)
use FreeRTOS-Plus-FAT as the file
system.
