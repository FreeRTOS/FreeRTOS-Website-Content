---
title: Using FreeRTOS-Plus-Trace
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


### Introduction

FreeRTOS-Plus-Trace has two components:

* Trace Recorder Source Files:

  The trace recorder is responsible for collecting trace data and runs on the target hardware as part
  of your RTOS application. It is provided as C source code in the main FreeRTOS .zip file download.

  The examples on this website use a 'snapshot' record of data for off-line analysis.  FreeRTOS-Plus-Trace
  provides a 'streaming' recorder which will back the recorded data.

* FreeRTOS-Plus-Trace PC Application:

  Trace recordings are viewed in the Tracealyzer application available from [Percepio's website](https://percepio.com/tracealyzer/download-tracealyzer/)

This page provides quick start instructions only. Refer to the help menu in the FreeRTOS-Plus-Trace
application for more detailed information and the [Percepio](https://percepio.com/) website for detailed
information.

Steps to trace enable your RTOS application:

1. [Add the trace recorder source files into your RTOS project](#add-the-trace-recorder-source-files-into-your-rtos-project)
2. [Update your application to initialise the trace, then start and stop a trace recording](#update-your-application-to-initialise-the-trace-then-start-and-stop-a-trace-recording)
3. [Extract a snapshot trace recording from the target for viewing in FreeRTOS-Plus-Trace](#extract-a-trace-recording-from-the-target-for-viewing-in-freertos-plus-trace)

 
### Add The Trace Recorder Source Files Into Your RTOS Project

![](/media/2018/trace_source_files.png)
*The trace recorder source files viewed in the project that builds the FreeRTOS-Plus-Trace
[Win32 simulator demo](Free_RTOS_Plus_Trace_CLI_Example)*

[![](/media/2018/include_file.png)](/media/2018/include_file.png)
*Inclusion of trcKernelPort.h in the same project. (Click to enlarge).*
 
1. Add *trcKernelPort.c* to the build project.  To use the snapshot recorder add *trcSnapshotRecord* to
   the project, or to use the streaming recording add *trcStreamingConfig.h* to the project.

2. Add /FreeRTOS-Plus/Source/FreeRTOS-Plus-Trace/include to the compiler's include path.

3. Create a trcConfig.h configuration file by editing a copy of the template provided
   in `FreeRTOS-Plus/Source/FreeRTOS-Plus-Trace/config`. *trcConfig.h* file used by an example in zip
   file download. Full instructions are provided in the comments within the header file itself.

4. To use the snapshot recorder create a trcSnapshotConfig.h configuration file by editing a copy of
   the template provided in FreeRTOS-Plus/Source/FreeRTOS-Plus-Trace/config, or editing a trcSnapshotConfig.h
   file used by an example in the FreeRTOS zip file download. Again, full instructions are provided in the
   comments within the header file itself. Alternatively, to use the streaming recorder, create a trcStreamingConfig.h
   header file by editing a copy of the template provided within the same directory.

5. Set configUSE\_TRACE\_FACILITY to 1 in FreeRTOSConfig.h.

6. Include the trcRecorder.h header file at the bottom of your project's FreeRTOSConfig.h configuration file.

Depending on the port in use it may also be necessary to define the TRACE\_ENTER\_CRITICAL\_SECTION()
and TRACE\_EXIT\_CRITICAL\_SECTION() macros. A #error in the source files will inform you if this is the
case, and provide further instruction.

Also depending on the port and development environment it may be necessary to use the pre-processor
to prevent the configuration file from being included from assembly files. For example, in IAR this
can be done as follows...

```c
/* The IAR C compiler automatically defines __ICCARM__. */
#ifdef __ICCARM__
    #include "trcKernelPortFreeRTOS.h"
#endif
```
*Preventing the RTOS trace header file from being included from assembly files when using the IAR compiler*

...and in MPLAB it can be achieved as follows:


```c
/* The MPLAB assembler automatically defines __LANGUAGE_ASSEMBLY. */
#ifndef __LANGUAGE_ASSEMBLY
    #include "trcKernelPortFreeRTOS.h"
#endif
```
*Preventing the RTOS trace header file from being included from assembly files when using the MPLAB compiler*


###  Update Your Application to Initialise the Trace, Then Start and Stop a Trace Recording

The trace recorder is initialised by calling vTraceEnable(). The trace recorder must be initialized **before**
any FreeRTOS API functions are called, so it is recommended to call vTraceEnable( TRC\_INIT) at the top of main().

To start a recording call vTraceStart(). To stop a recording call vTraceStop(). It is not necessary to
stop a recording before extracting the recorded data.


###  Extract a Trace Recording from the Target for Viewing in FreeRTOS-Plus-Trace

If the snapshot recorder is used (as opposed to the streaming), then the recorded data is stored within
the target hardware.  The recorded data is stored within the target hardware's RAM in a variable called
RecorderData, which itself is pointed to by a variable called RecorderDataPtr. To view a snapshot, it is
necessary to dump the contents of the targets RAM to a disk file, from where it can be opened using
FreeRTOS-Plus-Trace's File menu. The RAM that is saved to a file only needs to contain the RecorderData
variable - it can start and end at any memory address because FreeRTOS-Plus-Trace will automatically
find the recording within the saved data.

Most debuggers are able to save RAM contents to a file, and the FreeRTOS-Plus-Trace help file provides
instructions on using the **IAR**, **ST-Link**, Rowley **CrossStudio**, Keil **uVision**, and
Renesas **HEW** tools. There are a few other environments that have direct built-in or plug-in FreeRTOS-Plus-Trace
support. These are listed below.

* J-Link Users (all build environments and targets)

  If you are using a **J-Link** debug interface then the recorded data can be retrieved directly from
  within FreeRTOS-Plus-Trace using the J-Link menu.

* Atmel Studio

  If you are using **Atmel Studio 6** then Atmel's MemoryLogger extension, available from the Atmel
  Gallery, automatically detects the path to FreeRTOS-Plus-Trace, if installed, and gives you a single-click
  upload and refresh. You can use the extension while debugging, and optionally get an automatic refresh
  of the trace data each time the MCU is halted.

* MPLAB X

  If you are using **MPLAB X** then an MPLAB plug-in allows you to save the recorded data to disk so
  it can be opened from within FreeRTOS-Plus-Trace.

  To install the plug-in into MPLAB X:

  1. Extract the .nbm file from the provided zip file.
  2. In MPLAB, select Tools-\>Plugins, then in the Plugins dialog, select the Downloaded tab and then click Add Plugins...".
  3. Select org-percepio-freertostraceplugin.nbm from the zip file.
  4. Restart MPLAB and enable the plugin by selecting Tools-\>Embedded-\>FreeRTOS-Plus-Trace Plugin.

* Eclipse

  Finally, although Eclipse does not (yet) have built in support, as there are so many Eclipse users it
  is worth highlighting how to dump RAM to a disk in that environment. This is demonstrated in the image
  below (LPCXpresso shown in the image).

  ![](/media/2018/RTOS_Eclipse_Dump.png)
  *Using the memory export facility in Eclipse to save the RAM that contains RecorderData to a disk file*
