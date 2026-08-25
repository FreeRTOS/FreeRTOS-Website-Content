---
title: File Related Command Line Interface
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP and FreeRTOS-Plus-FAT Examples](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_FAT_demo_projects#Free_TCPIP_FAT_examples)

The UDP [command line interface example](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/UDP_CLI)
includes commands that allow files to be viewed, accessed and manipulated, as described in the
table below.

The commands are implemented in /FreeRTOS-Plus/Demo/Common/FreeRTOS\_Plus\_CLI\_Demos/File-releated-CLI-commands.c.

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
