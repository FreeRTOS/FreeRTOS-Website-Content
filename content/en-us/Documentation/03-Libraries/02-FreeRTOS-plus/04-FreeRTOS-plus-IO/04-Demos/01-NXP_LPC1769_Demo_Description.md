---
title: FreeRTOS-Plus-IO and FreeRTOS-Plus-CLI Demos
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Using the [LPCXpresso Base Board BSP](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_IO/BSP/NXP/LPCXpresso-LPC1769-Base-Board)


## Introduction

This page describes two demo applications that use FreeRTOS-Plus-IO and FreeRTOS-Plus-CLI on
the [LPCXpresso Base Board BSP](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_IO/BSP/NXP/LPCXpresso-LPC1769-Base-Board). The second demo integrates
lwIP and FatFS to provide a Telnet "like" command line interface to files stored on an SD card.

These demos are very comprehensive; simpler code snippets can be found on
the [quick examples](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/02-Quick-examples) page, and on most of the FreeRTOS-Plus-IO
and FreeRTOS-Plus-CLI documentation pages.

These demos use the standard FreeRTOS Cortex-M3 GCC port. It is important that users wishing
to use this port without FreeRTOS-Plus-IO first consult the port documentation to gain an understanding of
the interrupt configuration settings required to use the FreeRTOS interrupt nesting model.
The [FAQ that documents the most common mistakes made](/Why-FreeRTOS/FAQs/Troubleshooting) when using a multitasking
kernel on a Cortex-M device is a good place to start.


## FreeRTOS-Plus-IO and FreeRTOS-Plus-CLI demo 1 functionality

![FreeRTOS-Plus-IO and FreeRTOS-Plus-CLI being used to create a command console on a UART and use I2C, SPI and GPIO peripherals](/media/2018/FreeRTOS_UART_Command_Console_SPI_I2C_GPIO.jpg)
*Relevant Jumper Configuration*

Jumpers must be set correctly! Relevant jumper settings are pictured below.

![Jumper settings on the LPCXpresso base board for the correct SPI and I2C configuration](/media/2018/FreeRTOS_IO_CLI_Demo_1_Jumper1.jpg)

![Jumper settings on the LPCXpresso base board for the correct OLED display configuration](/media/2018/FreeRTOS_IO_CLI_Demo_1_Jumper2.jpg)

![Jumper settings on the LPCXpresso base board for the correct 7-segment display configuration](/media/2018/FreeRTOS_IO_CLI_Demo_1_Jumper3.jpg)

If you are using the ISP bootloader, so have J62 set, then  you must also remove J54 (may only be applicable
to Rev B  base boards).

In this demo, [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI) and
FreeRTOS-Plus-IO are used to create the following examples:


**Command Console**

+ FreeRTOS-Plus-IO and FreeRTOS-Plus-CLI are used to create a command  console. UART3 is used for input
  and output.

+ The FreeRTOS-Plus-IO  [zero copy transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/08-Zero_Copy_Transfer_Mode) is used to transmit
  characters, and the interrupt  driven [character queue transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/10-Character_Queue_Transfer_Mode)
  is used to receive characters.

+ Six commands are registered with FreeRTOS-Plus-CLI. These are run-time-stats, task-stats, echo-parameters,
  echo-3-parameters, create-task and delete-task.

+ Enter "run-time-stats" in the command console to see the amount of time each task has spent in the
  Running state since it was created.

+ Enter "task-stats" in the command console to see a snapshot of task state information - including stack
  high water mark data.

+ Enter "echo-parameters" followed by one or more command line parameters to see the (variable) number
  of parameters echoed back. This command demonstrates defining and implementing commands that can take
  any number of parameters.

+ Enter "echo-3-parameters" followed by three command line parameters to see the (fixed) number of parameters
  echoed back. This command demonstrated defining and implementing commands that expect an exact number of
  parameters.

+ Enter "create-task" followed by a single numeric parameter to create a task that accepts the entered
  number as its task parameter. The task will print (to the command console) the parameter value when
  it starts executing. The "task-stats"  command can be used to see the additional task running.

+ Enter "delete-task" to delete the task that was created using the "create-task" command.

+ As delivered, UART3 is set to 115200 baud, no start bits, 8 data bits and 1 stop bit. On the base board,
  UART3 is routed via a UART to USB converter, to the micro USB connector marked X3.  **The terminal program
  used to connect to the target must be configured  to send line ends with line feeds. Release 1 of the
  featured demo required the terminal program to echo typed characters locally, release 2 does not.**


**Display Driver**

+ FreeRTOS-Plus-IO is used to implement an OLED display driver.  The I2C2 peripheral is used for output,
  so the base board jumpers must be set to configured the OLED for I2C operation.

+ The example demonstrates the I2C port being used in both the [polled](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/07-Polled_Transfer_Mode)
  and interrupt driven [zero copy](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/08-Zero_Copy_Transfer_Mode) transfer modes.


**Serial EEPROM Interface**

+ FreeRTOS-Plus-IO is used to write to, then read back from, an EEPROM that is connected to the I2C2
  peripheral.

+ The example demonstrates the I2C port being used in the [polled](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/07-Polled_Transfer_Mode)
  and interrupt driven [zero copy](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/08-Zero_Copy_Transfer_Mode) transfer modes to write to the
  EEPROM, and the polled and interrupt driven [circular buffer](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/09-Circular_Buffer_Transfer_Mode)
  transfer modes to read back from the EEPROM.


**7-Segment Display**

+ This time FreeRTOS-Plus-IO is used with an SSP peripheral that is configured in SPI mode.
  The [polled transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/07-Polled_Transfer_Mode) is used to periodically write an
  incrementing number to a 7-segment display.


**GPIO**

+ FreeRTOS software timers are used to periodically toggle  the multi-coloured LEDs.


---

## FreeRTOS-Plus-IO and FreeRTOS-Plus-CLI demo 2 functionality

![FreeRTOS-Plus-IO and FreeRTOS-Plus-CLI being used to create a command console on a telnet socket to access a file system. A web server is also created.](/media/2018/FreeRTOS_File_System_Telnet_Web_Server.jpg)
*Relevant Jumper Configuration*

Jumpers must be set correctly! Relevant jumper settings are pictured below. **Note the settings in the first
picture are different to those shown for Demo 1!**

![Jumper settings on the LPCXpresso base board for the correct SPI and I2C configuration demo 2](/media/2018/FreeRTOS_IO_CLI_Demo_2_Jumper1.jpg)

![Jumper settings on the LPCXpresso base board for the correct OLED display configuration demo 2](/media/2018/FreeRTOS_IO_CLI_Demo_1_Jumper2.jpg)

![Jumper settings on the LPCXpresso base board for the correct 7-segment display configuration demo 2](/media/2018/FreeRTOS_IO_CLI_Demo_1_Jumper3.jpg)

If you are using the ISP bootloader, and so have J62 set, then you must also remove J54 (may only be
applicable to Rev B  base boards).

In this demo, [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI),
FreeRTOS-Plus-IO, [lwIP](http://savannah.nongnu.org/projects/lwip),
 and [FatFS](http://elm-chan.org/fsw/ff/00index_e.html) are used to create the following examples. **NOTE:
 An SD card  must be inserted for this demo to run!**.


**SD Card MMC Driver for FAT File System**

+ A FAT compatible file system is hosted on an SD card that uses an SPI interface. The FreeRTOS-Plus-IO
  API is used with an SSP peripheral to provide the necessary input and output. FatFS is used to provide the
  file system functionality.

+ The example demonstrates files being written to and read from the SD card using all the
  available  [FreeRTOS-Plus-IO transfer modes](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes). The file name is
  used to indicate the mode being  used when the file was created, and 20 files are created using each
  mode.

+ The files can be listed and manipulated  using FreeRTOS-Plus-CLI - see below.


**Telnet "like" Command Console**

+ FreeRTOS-Plus-CLI creates a command  console on the standard telnet TCP/IP port (port 23). The lwIP sockets
  API is used to provide the TCP/IP implementation.

+ The command console uses the telnet port number, and can be accessed using a standard telnet client,
  but it is not a full telnet server.

+ The example uses a static IP address that is configured using the configIP\_ADDR0-configIP\_ADDR3 constants
  defined in FreeRTOSConfig.h.

+ Five commands are registered with FreeRTOS-Plus-CLI. These are dir, copy and del to manipulate the
  file system (see above), and run-time-stats and task-stats to view FreeRTOS task information.

+ Enter "dir" in the command console to see a file system directory listing.

+ Enter "del \<filename\>" in the command console to delete a file from the SD card.

+ Enter "copy \<source\_file\> \<destination\_file\>" in the command console to copy a file.

+ Enter "run-time-stats" in the command console to see the amount of time each task has spent in the Running
  state since it was created.

+ Enter "task-stats" in the command console to see a snapshot of task state information - including stack
  high water mark data.

+ **The terminal program used to connect to the target must be configured to send line ends with line
  feeds and echo typed characters locally.**


**A web Server**

+ The lwIP raw API is used to create a simple web server. The web server uses server side includes (SSI)
  to display task state and  run time information.


**GPIO**

+ FreeRTOS software timers are used to periodically toggle  the multi-coloured LEDs.


### Source and project files download link

All the source files required to build both projects are contained
in [a single zip file](http://interactive.freertos.org/attachments/token/xupqqaau9ixtslj/?name=LPC1769_FreeRTOS_Plus_Featured_Demo_002.zip).


### Hardware platform and software tools

Both demos are configured to run on the LPCXpresso LPC1769 CPU board fitted to an LPCXpresso base board.
The [LPCXpresso IDE](https://www.nxp.com/design/design-center/development-boards-and-designs/lpcxpresso-boards:LPCXPRESSO-BOARDS) is used to build, flash, and debug the
application.


### Build Instructions

1. Start the [LPCXpresso IDE](https://www.nxp.com/design/design-center/development-boards-and-designs/lpcxpresso-boards:LPCXPRESSO-BOARDS). Create a new workspace, or
   select an existing workspace when prompted.

2. Select "Import" from the IDE "File" menu, then select "Existing Projects Into Workspace", as shown below,
   before clicking "Next".

   ![Selecting Existing Project Into Workspace in the LPCXpresso IDE](/media/2018/LPCXpresso_Existing_Project_Into_Workspace.jpg)
   *Selecting "Existing Projects Into Workspace" in the Import dialogue box*

3. Click the "Select Archive File" radio button, **ensure the "Copy projects into workspace" check box
   is checked**, then navigate to and select the zip file downloaded in step one.

   The dialogue box will list a number of project files. Ensure all the projects are selected, then click
   finish. The import process will attempt to create some files more than once - resulting in a dialogue
   box being displayed that warns of the potential for files to be overwritten. When this happens, simply
   select the "No to all" option.

   ![All the projects need to be imported.](/media/2018/LPCXpresso_Selecting_All_Projects.jpg)
   *Ensure each project is checked as all the projects are required to build the application.*

4. The imported projects will appear in the LPCXpresso IDE's project explorer window. To build demo 1,
   select "FreeRTOS-Plus-Demo-1" in the project explorer, then select "Build Project" from the IDE
   "Project" menu. Building FreeRTOS-Plus-Demo-1 will result in all its dependent projects being built too.

    Likewise, to build project 2, select "FreeRTOS-Plus-Demo-2" in the project window before selecting
    "Build Project" from the IDE "Project" menu.

   ![Building project 1 by selecting FreeRTOS-Plus-Demo-1 then selecting Build Project.](/media/2018/Building_Project_1.jpg)
   *Selecting "Build Project" with FreeRTOS-Plus-Demo-1 selecting in the project explorer*


### Connecting the hardware and starting a debug session

After the project has been built successfully:

1. Connect a USB cable between the USB socket on the LPCXpresso base board and the host computer. Only after
   this first connection has been made, connect a second USB cable between the debug USB socket on the
   LPCXpresso CPU board and the host computer. **Note:** This sequence seems to be important in order for
   a debug session to be started successfully.

2. Each demo requires slightly different jumper settings. The jumper settings are pictured next to the demo
   descriptions above. Ensure the jumpers are set correctly for the selected demo, and, if Demo 2 is selected,
   also ensure an SD card has been inserted into the relevant connector on the base board (the demo will not
   run without it!).

3. Click the debug speed button in the LPCXpresso IDE to start a debug session.

   ![The debug speed button in the LPCXpresso IDE](/media/2018/Debug-speed-button.jpg)
   *The location of the debug speed button in the LPCXpresso IDE*


### Navigating the projects and directories

The workspace contains the following five projects:

+ CMSISv2p00\_LPC17xx

  This is the standard CMSIS library provided by NXP for the LPC17xx family  of microcontrollers.

+ lpc17xx.cmsis.driver.library

  This is the peripheral driver library provided by NXP for the LPC17xx family of microcontrollers. It
  is used, in part, by the FreeRTOS-Plus-IO LPC17xx port layer. It contains very few modifications from
  the code distributed by NXP themselves.

+ FreeRTOS-Products

  This contains the FreeRTOS real time kernel, FreeRTOS-Plus-CLI and FreeRTOS-Plus-IO code, organised
  into three separate respective directories. Note that this project is  not actually built directly -
  the source code it contains is just referenced by the two demo application projects. The demo projects
  reference the files using workspace relative paths - which is why the projects will only build when
  they are located in the workspace directory.

+ FreeRTOS-Plus-Demo-1

  This project contains the demo 1 application code itself - which in turn uses source files from the
  FreeRTOS-Products directories.

+ FreeRTOS-Plus-Demo-2

  This project contains the demo 2 application code itself, including the FatFS and lwIP source files.
  The project also uses source files from the FreeRTOS-Products directories.


### Software component licensing

FreeRTOS-Plus-IO and FreeRTOS-Plus-CLI are supplied under their respective open
source [licenses](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/05-FreeRTOS_Plus_IO_License).

lwIP and FatFS are third party open source products, supplied under their own license terms.
