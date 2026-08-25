---
title: "Posix/Linux Simulator Demo for FreeRTOS using GCC"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

The FreeRTOS port documented on this page allows FreeRTOS to run on Linux just as the
 [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW) (often
 referred to as the FreeRTOS Windows simulator) has always allowed FreeRTOS to run on Windows. The port was contributed by David
 Vrabel, and inspired by William Davy's original 2008 Linux port.

The implementation of the port layer uses POSIX threading, so the port is also referred to as the POSIX port. It should not be confused
 with the [FreeRTOS-Plus-POSIX library](/Documentation/03-Libraries/05-FreeRTOS-labs/03-FreeRTOS-plus-POSIX/00-FreeRTOS-Plus-POSIX) – they do completely opposite things.
 FreeRTOS-Plus-POSIX provides a POSIX threading wrapper for the native FreeRTOS API that enables applications written using the POSIX API
 to run on FreeRTOS, whereas the Linux/POSIX FreeRTOS port enables FreeRTOS applications to run on POSIX operating systems.

Just like the Windows port, the FreeRTOS Linux port provides a convenient environment in which you can
 experiment with FreeRTOS and develop FreeRTOS applications intended for later porting to real embedded hardware - but FreeRTOS applications
 that use the Linux port will not exhibit real-time behaviour.

---

#### IMPORTANT! Notes on using the Posix/Linux Simulator Demo for FreeRTOS

*Please read all the following points before using the simulator demo.*

* [Source code organisation](#source-code-organization)
* [The FreeRTOS Linux port demo application](#the-posixlinux-simulator-demos)
* [Building and running the Posix/Linux simulator demo for FreeRTOS](#building-the-posixlinux-simulator-demos)
* [GDB debugging tips](#gdb-debugging-tips)
* [Port-layer design description](#port-layer-design-description)
* [Known issues](#known-issues)
* [Common problems and solutions](#common-problems-and-solutions)

Also see the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting).

---

### Source Code Organization

The [FreeRTOS zip file download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) contains the source code for all the FreeRTOS ports and demo applications – so it contains many more files than are required to build and run the pre-configured demos that use the FreeRTOS Linux port. See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) page for information on the zip file's directory structure.

* The RTOS port layer for Linux (POSIX) is located in the `[FreeRTOS/Source/portable/ThirdParty/GCC/Posix](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/master/portable/ThirdParty/GCC/Posix)` directory.
* There are two demo projects: A Kernel only demo which is located in the  `[FreeRTOS/Demo/POSIX\_GCC](https://github.com/FreeRTOS/FreeRTOS/tree/master/FreeRTOS/Demo/Posix_GCC)` directory, and a networking demo which is located in the  `[FreeRTOS-Plus/Demo/FreeRTOS\_Plus\_TCP\_Echo\_Posix](https://github.com/FreeRTOS/FreeRTOS/tree/master/FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_Echo_Posix)` directory.

### The Posix/Linux Simulator Demos

#### `[Kernel Demo Project](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS/Demo/Posix_GCC)`

 This project demonstrates FreeRTOS kernel functionality using the Linux (POSIX) port. The project can be configured to run either a simple Blinky style demo (`BLINKY_DEMO`), or a more comprehensive style demo (`FULL_DEMO`) by setting the constant `mainSELECTED_APPLICATION`, which is defined at the top of  `[main.c](https://github.com/FreeRTOS/FreeRTOS/tree/master/FreeRTOS/Demo/Posix_GCC/main.c)`.

* Blinky Demo

If `mainSELECTED_APPLICATION` is set to `BLINKY_DEMO`, then `main()` will call `main_blinky()`, which is implemented in `[main\_blinky.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS/Demo/Posix_GCC/main_blinky.c)`. `main_blinky()` creates a very simple demo that includes two tasks, a software timer, and a queue. One task repeatedly sends the value 100 at a frequency of 200 milliseconds to the other task through the queue, while the timer sends the value 200 every 2000ms to the same queue. The receiving task prints out a message each time it receives either of the values from the queue.
* Full Demo

If `mainSELECTED_APPLICATION` is set to `FULL_DEMO`, then `main()` will call `main_full()`, which is implemented in `[main\_full.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS/Demo/Posix_GCC/main_full.c)`. The demo created by `main_full()` consists primarily of the standard demo tasks, which don't perform any particular functionality other than testing the RTOS port and demonstrating how the FreeRTOS API can be used.

The full demo includes a 'check' task that executes every (simulated) ten seconds, but has the highest priority to ensure it gets processing time. Its main function is to check that all the standard demo tasks are still operational. The check task maintains a status string that is output to the console each time it executes. If all the standard demo tasks are running without error, then the string contains "OK" and the current tick count. If an error has been detected, then the string contains a message that indicates which task reported the error.

#### `[Networking Demo Project](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_Echo_Posix)`

This project demonstrates networking on Linux using the [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP) TCP/IP stack. It re-uses the TCP echo client demo originally written for the demo that uses FreeRTOS-Plus-TCP with the Windows RTOS port.

 The TCP echo demo uses the FreeRTOS-Plus-TCP TCP/IP stack to connect and communicate with a
[standard TCP echo server](https://en.wikipedia.org/wiki/Echo_Protocol) on TCP port 7.
The FreeRTOS-Plus-TCP network interface for Linux uses libpcap to access the network.

 To configure the TCP/IP stack for use with the demo:

* Follow the instructions under the
 [Software Setup #1, Software Setup #2, and Software Setup #4 sections](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic)
 on the page that describes using FreeRTOS-Plus-TCP on Windows hosts (the steps under Software Setup #3 are not required).
* Set the constants `configECHO_SERVER_ADDR0` to `configECHO_SERVER_ADDR3`
 to the address of the echo server in `FreeRTOSConfig.h`.

It is common for TCP port 7 (the standard echo port) to be blocked by firewalls. If this is the case, then change the port number used by both the FreeRTOS application and the echo server to a high, but valid,
number, such as 50000. The port number used by the FreeRTOS application is set by the echoECHO\_PORT
constant in [TCPEchoClient\_SingleTasks.c](https://github.com/FreeRTOS/FreeRTOS/blob/master/FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_Echo_Posix/TCPEchoClient_SingleTasks.c).
If you create a TCP echo server using the `nc` command in Linux then the port number is set using the `-l` switch:

```c
$ sudo nc -l 7
```
On MacOS the echo server can be started by
```c
$ sudo nc -l -p 7
```
#### Network troubleshooting

[ARP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/06-ARP) responses may not get sent if the echo server is running on the same computer as the FreeRTOS demo, resulting in the demo not being able to connect to the echo server. If this is an issue, then run the echo server on a different computer than that on which the RTOS demo is executing.

### Building the Posix/Linux Simulator Demos

* Prerequisites (the output below shows the versions used during testing):
	1. gcc

	```c
	$ gcc --version
	gcc (GCC) 9.2.0
	```
	2. make

	```c
	$ make --version
	GNU Make 3.81
	Copyright (C) 2006  Free Software Foundation, Inc.
	```
	3. [libpcap](https://www.tcpdump.org/) (for networking support)

	```c
	$ version: libpcap-devel-1.5.3-11.x86_64
	```

	 To install on ubuntu run
	```c
	$ sudo apt-get install libpcap-dev
	```

	 To install on an rpm based system run
	```c
	$ sudo yum install libpcap-devel
	```
	 or
	```c
	$ sudo dnf install libpcap-devel
	```

	 To install on MacOS run
	```c
	$ brew install libpcap
	```

	 Alternatively, it is possible to install from [source](https://github.com/the-tcpdump-group/libpcap) -- follow the instructions at [INSTALL.md](https://github.com/the-tcpdump-group/libpcap/blob/master/INSTALL.md)
* Building the source code:
	1. Navigate to the Demo Directories at:
	 [Kernel Demo source](https://github.com/FreeRTOS/FreeRTOS/tree/master/FreeRTOS/Demo/Posix_GCC) or to [Networking Demo source](https://github.com/FreeRTOS/FreeRTOS/tree/master/FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_Echo_Posix)

	```c
	 $ cd FreeRTOS/Demo/Posix_GCC/
	```

	or
	```c
	 $ cd FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_Echo_Posix
	```
	2. To build run:
	```c
	$ make
	```
	3. To clean run:
	```c
	$ make clean
	```
* Running the Demo (check the instructions above on how to choose between the available demos):

	1. Navigate to the newly created "build" directory

	```c
	$ cd build
	```
	2. Run the Kernel demo (Blinky or Full)

	```c
	$ ./posix_demo
	```
	3. Run the Networking demo

		- Run an echo server on a different machine

			```c
			$ sudo nc -l 7
			```

	   - Run on your machine 


			```c
			$ sudo ./posix_tcp_demo
			```

### GDB Debugging Tips

This section assumes that you have installed, and are familiar with, [gdb](https://www.gnu.org/software/gdb/).
 You can find the gdb documentation [here](https://www.gnu.org/software/gdb/documentation/).

The port layer uses two process signals: `SIGUSR1`, and `SIGALRM`. If a pthread is not waiting on
 the signal, then GDB will pause the process when it receives the signal. GDB must be told to ignore (and not print) the
 signal `SIGUSR1` because it is received asynchronously by each thread. In GDB, enter:

```c
$ handle SIGUSR1 nostop noprint pass
```

 to ensure that debugging is not interrupted by the signals. See:

```c
$ man signal
```

for more information.

Alternatively, create a file in your home directory called `.gdbinit` and place the following two lines in it:

```c
handle SIGUSR1 nostop noignore noprint
handle SIGALRM nostop noignore noprint
```

When you add these two lines to the `.gdbinit` file, it tells GDB to not break on those signals.

There are three different timers available for use as the System tick: `ITIMER_REAL`, `ITIMER_VIRTUAL`
 and `ITIMER_PROF`. The default timer is `ITIMER_VIRTUAL` because it only counts when the process is
 executing in user space, so it will stop when a break-point is hit. `ITIMER_PROF` is equivalent to
 `ITIMER_VIRTUAL` but it includes the time spent executing system calls. `ITIMER_REAL` continues
 counting even when the process is not executing at all, so it represents real-time. `ITIMER_REAL` is the only
 usable option because the other timers don't tick unless the process is actually running. For that reason, if
 `nanosleep` is called in the IDLE task hook, the time reported by the non-real timers will hardly ever
 increase.

### Port-Layer Design Description

A simple implementation of a FreeRTOS Simulator would simply wrap the platform native threads, and all calls to switch Task
 contexts would call the OS suspend and resume thread API. This simulator uses the Posix condition variables and Signals to
 control the execution of the underlying Posix threads. Signals can be delivered to the threads asynchronously, so that they
 interrupt the execution of the target thread, while suspended threads wait on condition variables to resume.

Typically, when designing a multi-threaded process, we use multiple threads to allow for concurrent execution and to
 implement a degree of non-blocking on IO tasks. This simulator does not use the threads to achieve concurrent execution,
 but only to store the context of the execution. Signals, mutexes and condition variables are used to synchronize context
 switching, but ultimately, the decision to change the context is driven by the FreeRTOS scheduler.

When a new Task is created, a pthread is created as the context for the execution of that Task. The pthread immediately
 suspends itself, and returns the execution to the creator. When a pthread is suspended, it is waiting in a call to
 `pthread_cond_wait`, which is blocked until it receives a resume signal `pthread_cond_signal`.

FreeRTOS Tasks can be switched in two ways, co-operatively by calling `taskYIELD()` or pre-emptively as part
 of the RTOS system Tick. In this simulator, the Task contexts are switched by resuming the next task context (decided by the
 FreeRTOS Scheduler) and suspending the current context (with a brief handshake between the two).

The RTOS system tick is generated using an `ITIMER` and the signal is delivered (only to) the currently executing
 pthread. The RTPS system tick signal handler increments the tick count and selects the next RTOS task context. It resumes that thread and sends a
 signal to itself to suspend. The suspend is only processed when the TOS system tick signal handler exits, because signals are
 queued.

### Known Issues

`pthread_create` and `pthread_exit/cancel` are system intensive calls which can rapidly saturate the
 processing time.

If you call system and library functions that block (printf), this could cause the whole process to halt. If it is necessary
 to make system calls, all signals on that thread must be masked, then re-allowed after the system call finishes execution.
 Additional threads could be created to simulate interrupts, but signals should be masked in those threads as well, so that
 they do not receive signals and so would be scheduled to execute by the FreeRTOS scheduler and become part of the regular FreeRTOS
 tasks.

To prevent the process from stealing all of the Idle execution time of the Host OS, use `nano_sleep()`. It doesn't
 use any signals in its implementation but will abort from the sleep/suspend process immediately to service a signal.
 Therefore, the best way to use it is to set a sleep time longer than a FreeRTOS execution time-slice and call it from the
 Idle task so that the process suspends until the next tick.

### Common Problems and Solutions

#### Creating Threads

**Problem**

Creating external threads with `pthread_create` (for example: simulating interrupts) can affect how FreeRTOS schedules tasks, as the underlying RTOS port relies on the reception of some signals to operate. The created thread could receive the signal instead which causes the scheduler to hijack the thread from its intended purpose to serve FreeRTOS specific tasks. This can lead to crashes and even deadlocks.

**Solution**

When creating a thread with pthread\_create, signals should be blocked on that thread by adding something like the following to the body of the thread:

 `sigset_t set;

 sigfillset( &set );

 pthread_sigmask( SIG_SETMASK, &set, NULL );`

Alternatively, there exists a better, but non portable, solution by blocking signals before the thread is created:

`void * args;

 sigset_t set;

 pthread_t tid;

 pthread_attr attr;

 sigfillset( &set );

 pthread_attr_init( &attr );

 pthread_attr_setsigmask_np( &attr, &set );

 pthread_create( &tid, &attr, start_routine, args );`

#### Creating new tasks

RTOS tasks created with `[xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate)` pass their created stack into port.c to allow the pthread library to use that stack with pthread\_attr\_setstack. A limitation exists for the minimal stack size that can be created. This limitation is platform dependent and is equal to PTHREAD\_STACK\_MIN. As a result, pthread\_create() will create its own stack and just ignore the stack passed by FreeRTOS. Nothing bad will happen to the runtime system if this happens, but some users who use FreeRTOS debugging tools to display stack information or other FreeRTOS variables will notice some inconsistencies.

As a workaround, always pass a stack of size PTHREAD\_STACK\_MIN if the desired stack is less than PTHREAD\_STACK\_MIN when running on a Posix port.
