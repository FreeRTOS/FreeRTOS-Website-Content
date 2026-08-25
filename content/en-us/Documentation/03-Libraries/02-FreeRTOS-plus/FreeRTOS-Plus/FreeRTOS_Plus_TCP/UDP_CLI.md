---
title: FreeRTOS-Plus-CLI Input and Output Using a UDP Socket
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP and FreeRTOS-Plus-FAT Examples](TCP_FAT_demo_projects#Free_TCPIP_FAT_examples)


Not all demo projects will include this example. If this example is
included in a demo project then it may be necessary to set
mainCREATE\_UDP\_CLI\_TASKS to 1 at the top of the project's
main.c source file to include the CLI in the build.

The example creates a [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI) command console that uses a UDP port for its input and output.

Free dumb terminal programs that are suitable for connecting to
the command line interface using UDP include [YAT](https://sourceforge.net/projects/y-a-terminal/)
and [Hercules](http://www.hw-group.com/products/hercules/index_en.html).

To connect to the CLI configure the dumb terminal to connect to the
target's hostname (or IP address) as the IP address, 5001 as the remote port, and 5002
as the local port. The default hostname is "RTOSDemo". The required
configuration is shown in the image below.

As always with FreeRTOS-Plus-CLI - type "help" in the command console to see
a list of registered commands.

![Free RTOS command line interface](/media/2018/yat-settings-for-udp-cli.png)
*Required Configuration to Connect Using YAT*

![Accessing the embedded FAT file system through the command line interface](/media/2018/File_System_Commands.png)
*Accessing the file system through the command line interface*
