---
title: Basic stdio API tests
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[FreeRTOS-Plus-TCP and FreeRTOS-Plus-FAT Examples](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_FAT_demo_projects#Free_TCPIP_FAT_examples)


Some [FreeRTOS-Plus-FAT demo projects](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_FAT_demo_projects)
make use of the vStdioWithCWDTest() function to
perform some basic sanity tests on the embedded FAT file system, using
the standard stdio API.

vStdioWithCWDTest() is implemented
in /FreeRTOS-Plus/Demo/Common/FreeRTOS\_Plus\_FAT\_Demos/test/ff\_stdio\_tests\_with\_cwd.c,
its implementation can serve as a useful reference.
