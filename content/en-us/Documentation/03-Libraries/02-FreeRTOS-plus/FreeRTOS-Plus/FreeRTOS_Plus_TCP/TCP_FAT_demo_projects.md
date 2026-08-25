---
title: FreeRTOS-Plus-TCP and FreeRTOS-Plus-FAT Examples
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


FreeRTOS-Plus-FAT is a [FreeRTOS Labs](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction) project. It is fully functional,
and quite mature, but as an originally acquired (rather than authored) product it does not necessarily
meet our production code or testing standards. It is available from
the [Lab-Project-FreeRTOS-FAT](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-FAT) repository on GitHub.


## Introduction

[![](/media/2018/video_still_tcp_fat_190K.jpg)](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP-IP_In_190K_RAM_Video)
*Video demonstrating many of the standard RTOS TCP/IP and FAT
file system demos ([listed below](#functionality)) running simultaneously
in less than 190K bytes of RAM*

FreeRTOS-Plus-TCP and FreeRTOS-Plus-FAT are provided with pre-configured demo
projects that allow the middleware components to build and run 'out of the box'. The links below
describe how to locate and use the demo projects.

[The demo that uses the FreeRTOS Windows port](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator) provides a completely free and
feature rich environment for both evaluating and developing FreeRTOS-Plus-TCP and
FreeRTOS-Plus-FAT applications, using free tools, and without the need to purchase any special
hardware.


### Target Specific Pre-configured Projects

* [Windows demo](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator) - using free tools
* [Xilinx Zynq dual core ARM Cortex-A9 demo](TCPIP_FAT_Examples_Xilinx_Zynq)
* [Atmel SAM4E ARM Cortex-M4F demo](TCPIP_FAT_Examples_Atmel_SAM4E)
* [ST STM32F4 ARM Cortex-M4F demo](TCP-IP_FAT_Examples_ST_STM32F407) (using internal RAM only!)


### Functionality

The pre-configured demo projects run multiple examples. A description of each example, along with instructions
for including the example in the build, are provided on the links below.
Not all the examples are included in all the demo projects - although
all are included in the [demo project that uses the FreeRTOS Windows port](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator).

Available examples

* FreeRTOS-Plus-TCP UDP sockets examples

  1. [Command line interface using a UDP socket](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/UDP_CLI)
  2. [Basic UDP clients communicating with basic UDP servers (standard and zero copy)](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/UDP_client_server)
  3. [Using FreeRTOS\_select()](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/using_select)
  4. [UDP echo clients](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/UDP_Echo_Clients)
  5. [Sending FreeRTOS-Plus-TCP log messages to a UDP port](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/UDP_Logging)

* FreeRTOS-Plus-TCP TCP sockets examples

  1. [TCP echo clients (Rx and Tx performed in the same RTOS task)](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_Echo_Clients)
  2. [TCP echo clients (Rx and Tx performed in separate RTOS tasks)](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_Echo_Clients_Separate)
  3. [TCP echo server](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_Echo_Server)

* FreeRTOS-Plus-TCP and FreeRTOS-Plus-FAT web (HTTP) and FTP examples

  1. [FTP server](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/06-FTP-server)
  2. [HTTP web server](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/07-HTTP-web-server)

* FreeRTOS-Plus-FAT

  1. [Creating and verifying a set of example files](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/creating_and_verifying_files)
  2. [Basic stdio API tests](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/basic_stdio_API_tests)
  3. [Creating a disk](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/creating_a_disk)
  4. [File system command line interface](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/file_related_cli_commands)


![Logging messages produced by the free RTOS TCP/IP stack](/media/2018/udp_logging_output.jpg)
*The output produced by the [UDP logging example](UDP_Logging)*
