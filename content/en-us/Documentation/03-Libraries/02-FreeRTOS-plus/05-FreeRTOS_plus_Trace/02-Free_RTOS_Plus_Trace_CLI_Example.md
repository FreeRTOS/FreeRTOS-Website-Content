---
title: FreeRTOS-Plus-Trace and FreeRTOS-Plus-CLI Demo
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Percepio View for FreeRTOS
    link: /Documentation/03-Libraries/02-FreeRTOS-plus/05-FreeRTOS_plus_Trace/01-Percepio_View
  - title: Tracealyzer™
    link: /Documentation/03-Libraries/02-FreeRTOS-plus/05-FreeRTOS_plus_Trace/00-FreeRTOS_Plus_Trace
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


Using the [FreeRTOS Win32 Simulator](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)


## Download

The example presented on this page is available in the following directory
of the official [FreeRTOS zip file download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS):

FreeRTOS-Plus/Demo/FreeRTOS\_Plus\_CLI\_with\_Trace\_Windows\_Simulator


## Introduction

This page describes a simple FreeRTOS example that runs in the
FreeRTOS Win32 simulator.
Using the simulator makes it easy to
evaluate FreeRTOS-Plus-CLI and FreeRTOS-Plus-Trace on a standard desktop PC, using
free development tools, and without the
need to connect any external hardware.

To keep everything as simple as possible, the FreeRTOS-Plus-CLI command line
interface is accessed through a UDP socket on the default Windows
loopback IP address of 127.0.0.1. Using the loopback adaptor allows the
demo to be used on a single computer, and without a live network connection.

The following commands are implemented:

+ *trace*

  The trace command is used to start and stop the trace recording. FreeRTOS-Plus-CLI will only process
  the command if it is entered with exactly one parameter.  To start a FreeRTOS-Plus-Trace recording
  enter: "trace start" To stop a FreeRTOS-Plus-Trace recording enter: "trace stop" When a trace stops,
  results in the trace buffer are automatically saved to the hard disk of the host computer. Instructions
  on viewing the trace are provided further down this page.

+ *echo\_parameters*

  This demonstrates how to create and implement a command that accepts a variable number of parameters.
  FreeRTOS-Plus-CLI will not check the number of supplied parameters, and the implementation of the command
  simply echos parameter back, one at a time. For example, if the user enters: "echo\_parameters one two
  three four" Then the generated out will be: The parameters were: 1: one 2: two 3: three 4: four

+ *echo\_3\_parameters*

  This demonstrates how to create a command that takes an exact number of parameters. The command will not
  be accepted by FreeRTOS-Plus-CLI unless exactly three parameters are supplied. When the command is accepted,
  the implementation of the command echos all three parameters in a similar manner to the echo\_parameters
  command detailed above.

+ *run-time-stats*

  [Displays a table](/Documentation/02-Kernel/02-Kernel-features/08-Run-time-statistics), each row of which shows the amount of time a single
  task has spent in the running state. That is, how much execution time has been allocated to each task.
  Both absolute and relative values are displayed, although the absolute times have no units when using
  the Windows simulator.


## Demo Functionality

Two tasks and a single queue are used to generate a simple execution
pattern that can be viewed in the FreeRTOS-Plus-Trace graphical interface.

A low priority queue send task repeatedly sends a message to the queue.
A higher priority queue receive task repeatedly attempts to read a
message from the queue, blocking on the queue read operation when no
messages are available. An explanation of the resultant execution
pattern is provided below.

A trace monitoring task is also created that prints out a message
when it determines that the status of the trace recorder has changed
since it last executed.

It should be noted that, because the Windows simulator is being used,
the timing information displayed while the application is running, and
recorded in the trace log, have no meaningful units.


## Building and executing the demo

1. Ensure Microsoft Visual C++ is installed.
   The [free Express version](https://visualstudio.microsoft.com/vs/community/)
   can be used.

2. The Visual C++ solution file is called FreeRTOS\_Plus\_CLI\_with\_Trace.sln, and is
   located in the FreeRTOS-Plus/Demo/FreeRTOS\_Plus\_CLI\_with\_Trace\_Windows\_Simulator
   directory of the download. Double click the file to open Visual C++, or alternatively
   open the file from within the Visual C++ IDE.

   ![The RTOS project viewed inside the compiler development tool](/media/2018/RTOS_project_viewed_in_dev_tool_editor.png)
   <br />
   *The RTOS project viewed in the Visual C++ IDE*

   Within the solution explorer:

   * The source files that implement the demo application are listed in the Demo App Source folder.
   * The source files that implement the FreeRTOS-Plus-CLI functionality are listed in the
     FreeRTOS-Plus/FreeRTOS-Plus-CLI folder.
   * The source files that implement the FreeRTOS-Plus-Trace recorder functionality are listed in the
     FreeRTOS-Plus/FreeRTOS-Plus-Trace folder.
   * The source files that implement the RTOS functionality are listed in the FreeRTOS folder.

3. Build, then execute, the project. (F7 will build the project, and F5 will execute the project).


## Accessing the Command Console

The command console uses a UDP socket on IP address 127.0.0.1 and port 5001 to receive command
line input, and a UDP socket on the same IP address and port 5002 for output. A UDP console
program, such as the [free YAT utility](http://sourceforge.net/projects/y-a-terminal/),
can be used as a UDP interface. Note that 127.0.0.1 is the loopback IP address, so
a live network connection is not required.

![The required UDP command console configuration](/media/2018/YAT-console-configuration.jpg)
<br />
*The required YAT terminal settings*


## Creating a FreeRTOS-Plus-Trace Recording

To create a trace recording:

1. Test the UDP connection between the UDP terminal and the running
   application by running the "task-stats" and "run-time-stats"
   commands.

2. Start the trace recorder by entering the "trace start"
   command in the UDP terminal. Leave the
   recording running for approximately five to ten seconds, then end the
   recording by entering the "trace stop" command.

   ![Screen capture after the RTOS trace has been started and stopped from the console](/media/2018/command-line-input-and-output.jpg)
   <br />
   *Screen capture after the RTOS trace has been started and stopped from the UDP console*


## Viewing the Trace Recording in FreeRTOS-Plus-Trace

To open and view the trace recording:

1. [Download FreeRTOS-Plus-Trace](http://percepio.com/tz/freertostrace/)
   from the Percepio web site if you do not already have it installed.

2. Open the trace file from within the FreeRTOS-Plus-Trace application.
   The trace file will have been saved as
   FreeRTOSPlusTrace.dump in the directory that contains
   the Visual Studio project.

3. The trace data will be displayed in the main FreeRTOS plus
   trace window. Scroll the trace display down until you notice
   "Tx" and "Rx" markers on the left side of the screen. These are
   the times during which the queue send and queue receive tasks
   were executing respectively. Zooming in on that region will
   result in a display similar to the screen shot below. Note that
   the screen shot has all the visibility filters ticked, not all
   of which are available in the free FreeRTOS-Plus-Trace edition.

   ![Viewing the RTOS trace in FreeRTOS-Plus-Trace](/media/2018/Viewing-the-RTOS-trace-in-FreeRTOS-Trace.jpg)
   <br />
   *Viewing the recorded RTOS trace in FreeRTOS-Plus-Trace with explanatory annotation*

   The image above has been annotated with some green numbers to highlight
   points of interest. Referring to the image above:

   1. At (1) the CLI task is running. In a real scenario, on real
      hardware, the CLI task need only execute when there is input
      to process. In this simulated environment, the TCP/IP stack cannot
      be allowed to block, so the CLI task is always available to the
      scheduler.
   2. At (2) the Tx task (the queue send task) unblocks because it is
      time for it to send another message to the queue. The Tx task
      pre-empts the CLI task.
   3. At (3) the Tx task calls xQueueSend() to send a message to the
      queue named DemoQ. The higher priority Rx task (the queue receive task) was blocked
      on the queue, waiting for a message to arrive, so it now unblocks and
      pre-empts the Tx task.
   4. At (4) the Rx task calls xQueueReceive() again, but the queue is
      once more empty so the Rx task re-enters the Blocked state (signified by the
      red colour of the xQueueReceive() label in the trace view) allowing
      the Tx task to enter the Running state again.
   5. At (5) the Tx task calls vTaskDelayUntil() to enter the Blocked
      state until once again it is time for it to send a message to
      the queue.
   6. At (6) the idle task is running.


## Going Further

This simple example has only demonstrated the basic functionality. The
FreeRTOS-Plus-Trace download contains a much more comprehensive FreeRTOS
Windows simulator project, along with pre-recorded example trace log files.
Visit [the Percepio Website](http://percepio.com/tz/freertostrace/) for more
information.
