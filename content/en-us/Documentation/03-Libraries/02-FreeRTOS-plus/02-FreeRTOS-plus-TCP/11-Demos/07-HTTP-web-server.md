---
title: HTTP Web Server Example
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
mainCREATE_HTTP_SERVER to 1 at the top of
the project's main.c source file to include the example in the
build.

This example uses FreeRTOS-Plus-TCP to implement a basic web (HTTP) server that accesses
files from a file system implemented by FreeRTOS-Plus-FAT. Some demo projects
store files on a RAM disk, while others store files on non-volatile media
such as an SD card.

The base directory used by the web server is set by the configHTTP_ROOT
constant in FreeRTOSConfig.h.
If a RAM disk is used then a default and very basic HTML file called "freertos.html"
is created in the base directory after it is mounted.
The [FTP server](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/06-FTP-server) can be used to overwrite the
default HTML file with different web content.

**NOTE**: Performance will be limited when using the FreeRTOS Windows port.

[![](/media/2018/viewing_the_default_web_page.png)](/media/2018/viewing_the_default_web_page.png)
_Viewing the default web page served by the FreeRTOS-Plus-TCP web server (Click to enlarge)_
