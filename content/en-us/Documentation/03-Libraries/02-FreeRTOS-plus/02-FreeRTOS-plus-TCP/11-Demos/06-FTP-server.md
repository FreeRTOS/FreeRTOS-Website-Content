---
title: FTP Server Example
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP and FreeRTOS-Plus-FAT Examples](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_FAT_demo_projects#Free_TCPIP_FAT_examples)

**Note:** This demo has a dependency on the FreeRTOS-Plus-FAT code base and is
therefore currently only available in the FreeRTOS Labs download.

Not all demo projects will include this example. If this example is
included in a demo project then it may be necessary to set
mainCREATE_FTP_SERVER to 1 at the top of
the project's main.c source file to include the example in the
build.

This example uses FreeRTOS-Plus-TCP to implement an FTP server that accesses
files from a file system implemented by FreeRTOS-Plus-FAT. Some demo projects
store files on a RAM disk, while others store files on non-volatile media
such as an SD card. Some projects even mount both a RAM disk and an
SD card within the same virtual file system.

If an example uses a RAM disk then a set of example files are created on
the RAM disk after it is mounted.

**NOTE**: Performance will be limited when using the FreeRTOS Windows port.

The FTP server can be accessed using a standard FTP client, such as [FileZilla](https://filezilla-project.org/). To connect:

- Enter the IP address or hostname of the FTP server as the host (the FTP
  server is the target running FreeRTOS-Plus-TCP).
- Enter "anonymous" as the username.
- Leave the password blank.

![](/media/2018/viewing_the_ram_disk_in_FileZilla_FTP_client.png)  
_Viewing the example files on the RAM disk in the FileZilla FTP client_
