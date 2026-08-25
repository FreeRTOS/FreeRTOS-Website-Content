---
title: FreeRTOS and Reliance Edge Demo
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

**Using the Fail Safe File System with the FreeRTOS Windows Port**


[![Tuxera Logo](/media/2021/tuxera_logo.png)](https://www.tuxera.com/)
[![fail safe embedded file system](/media/2021/Reliance_Edge_logo.png)](https://www.tuxera.com/products/reliance-edge/)
[Download the Reliance Edge Developer's Guide](https://www.tuxera.com/resources/reliance-edge-developers-guide/)
[Evaluate now!](Fail_Safe_Embedded_File_System_demo)
[License Information](safety_critical_embedded_file_system_license)
[Watch the video](https://www.youtube.com/watch?v=KITEPryc1jI)


<blockquote>
    <span class="content">
        "Our products are used from the bottom of the ocean, to the depths
        of space, and from the factory floor, to your hip pocket"
    </span>
    <span class="attribution">Ken Whitaker, Tuxera</span>
</blockquote>

<blockquote>
    <span class="content">
        "Tuxera's family of Reliance fail safe file systems have
        delivered proven reliability in hundreds of millions of devices."
    </span>
    <span class="attribution">Kerri McConnell, Tuxera</span>
</blockquote>

<blockquote>
    <span class="content">
        "The design goals and implementation of Reliance Edge
        means it is no ordinary file system. Reliance Edge will
        be a valuable resource for our users, so we are happy to
        accept it as an official FreeRTOS-Plus component."
    </span>
    <span class="attribution">Richard Barry, Amazon Web Services Inc.</span>
</blockquote>


This page presents a project that runs FreeRTOS and Datalight's Reliance
edge fail safe file system in a Windows environment.

The FreeRTOS Windows port provides a convenient and non embedded target
specific evaluation platform. It allows FreeRTOS, and some FreeRTOS-Plus
components, to be executed on a standard Windows computer, using
feature rich and free development tools. However, unlike when FreeRTOS
is executed on real embedded hardware, the Windows port does not exhibit
true real time behaviour.

## Source Code and Project Files

The project described on this page is located in the following folder of
the main [FreeRTOS .zip file download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS):
FreeRTOS-Plus/Demo/FreeRTOS\_Plus\_Reliance\_Edge\_and\_CLI\_Windows\_Simulator


## Target Hardware

The project creates a RAM disk using
the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW).
The Windows port provides a convenient evaluation platform, but it
does not exhibit real time behaviour. Simulated time might be slower than real time.


## Compiler / Tool Chain

The project is pre-configured to build with
the [free Express edition of Microsoft Visual C++](http://www.microsoft.com/visualstudio/eng/products/visual-studio-express-products)
(MSVC). MSVC Express Edition 2010 was used.


## Functionality

The demo:

1. Creates and formats a RAM disk.

2. Creates then reads back a set of example files in the root directory of the RAM disk.

3. Creates sub-directories.

4. Creates then reads back a set of example files from the created sub-directories.

5. Creates a command console (using [FreeRTOS-Plus-CLI](../FreeRTOS_Plus_CLI/FreeRTOS_Plus_Command_Line_Interface))
   that implements the commands described below:

   |  Command and parameters  |  Description  |
   | --- | --- |
   | *dir \<filename\>* |  Lists the files in the named directory  |
   | *type \<filename\>* |  Prints file contents to the terminal  |
   | *append \<filename\>*  |  Appends data to a file (creating the file if it does not exist)  |
   | *del \<filename\>* |  Deletes a file or directory  |
   | *copy \<source file\> \<dest file\>* |  Copies \<source file\> to \<dest file\>  |
   | *create \<filename\>* |  Creates an empty file  |
   | *mkdir \<filename\>* |  Creates an empty directory  |
   | *rename \<source file\> \<dest file\>* |  Rename \<source file\> to \<dest file\>  |
   | *link \<source file\> \<dest file\>* |  Create hard link \<dest file\> pointing at \<source file\>  |
   | *stat \<filename\>* |  Show file information  |
   | *statfs* |  Show file system information  |
   | *format* |  Re-formats the file system volume. ALL FILES WILL BE DELETED!  |
   | *transact* |  Commits a Reliance Edge transaction point  |
   | *transmaskget* |  Retrieves the Reliance Edge automatic transaction mask  |
   | *transmaskset \<hex mask\>* |  Sets the Reliance Edge automatic transaction mask  |
   | *abort* |  Rolls back all changes not part of the last transaction point  |
   | *test-fs* |  Executes file system tests. ALL FILES WILL BE DELETED!  |


## Command Console Input and Output

The command console is accessed from a UDP terminal.
See the [Usage Instructions](#usage-instructions) section below.


## Build Instructions

1. The demo application is available in the main [FreeRTOS .zip file download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/).

2. Open the Visual Studio solution file FreeRTOS\_Plus\_Reliance\_Edge\_with\_CLI.sln
   from within the Visual Studio IDE. The solution file is located
   in the "FreeRTOS-Plus/Demo/FreeRTOS\_Plus\_Reliance\_Edge\_and\_CLI\_Windows\_Simulator"
   directory.

3. Select "Build Solution" from the IDE's Build menu (or press F7)
   to build the application.


## Debug Instructions

In Visual Studio, press F10 to start a debug session and break on entry to main().

The same host computer is used to build the application, debug the application,
and (because the FreeRTOS Win32 port is used) run the application.
There are no special debugging instructions.


## Usage Instructions

1. The demo application creates a set of files and directories on
   a RAM disk, outputting information to the Windows console as it goes.

   ![The output generated when the fail safe file system files and directories are created](/media/2018/safety_critical_file_system_console_output.jpg)
   *The output generated in the Windows console when the fail safe embedded file system demo application starts*

2. A local UDP connection is used to connect to the FreeRTOS-Plus-CLI
   command line interface. The Windows TCP/IP stack is used
   instead of FreeRTOS-Plus-TCP to ensure
   the demo remains focused on the file system. A demo application
   that uses the FreeRTOS Windows port and FreeRTOS-Plus-TCP to create
   a command console [is available in the FreeRTOS-Plus-TCP section of this website](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP).

   Free dumb terminal programs that are suitable for connecting to
   the command line interface using UDP include [YAT](https://sourceforge.net/projects/y-a-terminal/)
   and [Hercules](http://www.hw-group.com/products/hercules/index_en.html).

   The standard localhost IP address (127.0.0.1) can be used because
   both the (simulated) demo application and the UDP terminal execute
   on the same computer. FreeRTOS-Plus-CLI listens for characters
   arriving on UDP port 5001 and sends its output to UDP port 5002.
   The required terminal configuration is shown below.

   ![Settings required to the safety critical file system demo](/media/2018/yat_settings_to_connect_to_the_safety_critical_file_system_demo.jpg)
   *Configuring the YAT terminal to communication with the FreeRTOS-Plus-CLI command line interface*

3. Type "help" to see a list of registered commands.

   ![Viewing safety critical file system related RTOS commands](/media/2018/view_safety_critical_file_system_commands.png)
   *Type "help" in the UDP terminal to see a list of registered commands*

4. Experiment with the file system commands! A sample session is shown below.

   ![running safety critical file system RTOS commands](/media/2018/running_safety_critical_file_system_commands_in_yat.png)
   *Running safety critical file system commands in the YAT terminal*
