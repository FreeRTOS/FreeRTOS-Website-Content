---
title: Creating and Verifying Files
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[FreeRTOS-Plus-TCP and FreeRTOS-Plus-FAT Examples](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_FAT_demo_projects#Free_TCPIP_FAT_examples)


When a RAM disk is created it is empty, so [FreeRTOS-Plus-FAT demo projects](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_FAT_demo_projects)
that use a RAM
disk create a set of example files on the disk after it has been created.
The example files are created, and also verified, by calling the vCreateAndVerifyExampleFiles()
function.

vCreateAndVerifyExampleFiles() is implemented
in /FreeRTOS-Plus/Demo/Common/FreeRTOS\_Plus\_FAT\_Demos/CreateAndVerifyExampleFiles.c,
its implementation can serve as a useful reference.
