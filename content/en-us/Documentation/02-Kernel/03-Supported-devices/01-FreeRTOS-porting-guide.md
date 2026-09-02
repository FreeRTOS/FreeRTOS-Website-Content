---
title: "Creating a New FreeRTOS Port"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: Beginner's guide to FreeRTOS
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: Download FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FAQs
    link: /Why-FreeRTOS/FAQs
---


***You do not need to read or understand this page if using one of the many existing ports and demo applications!***


Porting FreeRTOS to a completely different and as yet unsupported microcontroller is not a trivial task. The aim of this 
page is to describe the house keeping preliminaries required to get a new port started.

Each port is moderately unique and very dependent on the processor and tools being used, so this page cannot provide 
specifics on the porting detail. There are however [plenty of other FreeRTOS ports already in existence](/Documentation/02-Kernel/03-Supported-devices/00-Supported-devices) 
and it is suggested that these are used as a reference.

Porting within the same processor family is a much more straight forward task - for example, from one ARM7 
based device to another. The documentation page 
detailing [how to modify an existing demo application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) 
would be a good point to start reading if this is your aim.

The [template port](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/main/portable/template) 
can be used as a starting point for developing a FreeRTOS port for a new architecture.


### Setting up the Directory Structure

The FreeRTOS kernel source code is generally contained within 3 source files (4 if co-routines are used) that are common 
to all ports, and one or two 'port' files that tailor the RTOS kernel to a particular architecture.

Suggested steps:

1. Download the latest version of the FreeRTOS source code.

2. Unzip the files into a convenient location, taking care to maintain the directory structure.

3. Familiarise yourself with the [source code organisation](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) and directory structure.

4. Create a directory that will contain the 'port' files for the [architecture] port. Following the convention outlined 
   in the link, the directory should be of the form: FreeRTOS/Source/portable/[compiler name]/[processor name]. For 
   example, if you are using the GCC compiler you can create a [architecture] directory off the existing 
   FreeRTOS/Source/portable/GCC directory.

5. Copy empty port.c and portmacro.h files into the directory you have just created. These files should just contain 
   the stubs of the functions and macro's that require implementing. See existing port.c and portmacro.h files for a 
   list of such functions and macros. You can create a stub file from one of these existing files by simply deleting 
   the function and macro bodies.

6. If the stack on the microcontroller being ported to grows downward from high memory to low memory then set 
   portSTACK\_GROWTH in portmacro.h to -1, otherwise set portSTACK\_GROWTH to 1.

7. Create a directory that will contain the [demo application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) files for the [architecture] port.
   Following the convention again this should be of the form FreeRTOS/Demo/[architecture\_compiler], or something similar.

8. Copy existing FreeRTOSConfig.h and main.c files into the directory just created. Again these should be edited to be just stub files.

9. Take a look at the FreeRTOSConfig.h file. It contains some macro's that will need setting for your chosen hardware.

10. Create a directory off the directory just created and call it ParTest (probably FreeRTOS/Demo/[architecture\_compiler]/ParTest).
    Copy into this directory a ParTest.c stub file.

11. ParTest.c contains three simple functions to:

	1. Setup some GPIO that can flash a few LEDs,
	2. Set or clear a specific LED, and
	3. Toggle the state of an LED.

    These three functions need implementing for your development board. Having LED outputs working will facilitate the rest 
	of the required work.
    Take a look at the many existing ParTest.c files included in the other demo projects for examples (the ParTest name is 
	a historical anomaly for PARallel port TEST), and the [page describing how to modify an existing demo application]
	(/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) for information on writing and testing the ParTest.c functions.


### Creating a Project


Now all the required files are in place you need to create a project (or makefile) that will successfully build them.
Obviously they just contain stubs so will not yet do anything, but once they are building the stubs can incrementally be 
replaced with working functions.

The project will need to contain the following files:

* Source/tasks.c
* Source/Queue.c
* Source/List.c
* Source/portable/[compiler name]/[processor name]/port.c
* Source/portable/MemMang/[heap\_1.c (or heap\_2.c or heap\_3.c or heap\_4.c)](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)
* Demo/[processor name]/main.c
* Demo/[Processor name]/ParTest/ParTest.c

The following directories need to be in the include path - please use relative paths from the Demo/[Process name] 
directory - NOT absolute paths:

* Demo/Common (i.e. ../Common)
* Demo/[Processor Name]
* Source/include
* Source/portable/[Compiler name]/[Processor name]


### Implementing the Stubs

Now the difficult bit. Once the project is compiling the portable layer stubs require implementation. It is suggested 
that pxPortInitialiseStack() is the first function to be implemented. To implement pxPortInitialiseStack() you must 
first decide upon your task context stack frame structure, which is very architecture dependent.
Some useful notes about the porting of FreeRTOS are provided on [FreeRTOS Porting Notes](/Documentation/02-Kernel/03-Supported-devices/05-feertos-porting-notes) page.

### Getting Help

Don't forget that [WITTENSTEIN high integrity systems](https://www.highintegritysystems.com/openrtos/) offer a full porting and testing service!
