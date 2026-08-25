---
title: "Building FreeRTOS with Eclipse Using relative paths to reference the RTOS source code"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

### Introduction

The [FreeRTOS download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) contains many different pre-configured demo application
projects, but for maintenance and
sanity reasons it contains only one copy of the RTOS source code. Ideally each demo project
would reference and build the single RTOS source code copy, and this is exactly what
most of the pre-configured [RTOS demo projects](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos) do. However, historically this has not
been easy (although not impossible) to do in Eclipse, and older Eclipse based
RTOS demo projects use a batch file to copy all the necessary source files
from their default locations in the [FreeRTOS directory tree](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) into the
Eclipse project directory.

The latest versions of Eclipse have gone some way to alleviate
these problems by allowing the definition of variables that can resolve paths both
up and down the directory tree from the directory that contains the Eclipse .project
file. Newer RTOS demo applications that are built with an Eclipse based IDEs
are pre-configured to use this improved (although still comparatively awkward)
method, instead of the batch file method used previously. This page describes
how these projects are created.

**Note:** This page is provided for information only. The RTOS demo projects
in the official FreeRTOS download are already pre-configured, and should build
'out of the box', provided the [build instructions](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)
specific to the demo project in use are followed, and that the Eclipse version in use
is up to date.

### Creating Eclipse Projects that Build Files Outside of the Project Directory

By way of example the following instructions show how to reference the FreeRTOS
source files, which reside in the /FreeRTOS/Source directory, from an Eclipse
project file, which resides in the /FreeRTOS/Demo/[project\_name] directory.

1. **Open the Project's Properties Window** 

 Right click on the project's name in the Eclipse Project Explorer window,
 then select 'Properties' from the pop up menu. The Properties window
 will open.
2. **Define a New Eclipse Variable** 

 In the Properties window, select 'Resources->Linked Resources' to view
 the path variables. Click the 'New' button to create a new variable that
 will be used to point to the FreeRTOS source files directory
 tree.

![Defining a new Eclipse variable that will be used to reference the RTOS source files](/media/2018/Define_a_New_Eclipse_Variable.jpg)

**Define a new Eclipse variable** 

 Name the new variable FREERTOS\_ROOT, and use the pre-defined PROJECT\_LOC
 variable to enter a path that resolves to the /FreeRTOS/Source
 directory.

![Use a relative path to set the Eclipse variable to the RTOS source directory](/media/2018/Extend_PROJECT_LOC_Variable.jpg)

**Extending the PROJECT\_LOC variable so it resolves to the /FreeRTOS/Source directory** 

 Close the Properties window.
3. **Creating a Virtual Folder** 

 Eclipse managed make projects build all the source files
 that appear in the Project Explorer window. The RTOS source files
 are outside of the Eclipse project directory, so don't automatically appear in the
 Project Explorer window, and must be added manually using a virtual
 folder.

 Right click on the folder name in the Project Explorer under which you
 would like the RTOS source files to appear. Select 'New -> Folder'. The
 New Folder window will open.

 In the New Folder window, enter FreeRTOS as the folder name, and select
 the 'Folder is not located in the file system (Virtual Folder)' radio
 button.

![Create a virtual folder in Eclipse Project Explorer](/media/2018/Create_A_Virtual_Folder.jpg)

**Creating a virtual folder in the Eclipse Project Explorer**
4. **Linking the RTOS Source Code Directory Into The Virtual Folder** 

 Right click on the newly created virtual folder and select 'New -> Folder'
 from the pop up menu to bring up the New Folder window again.

![Creating a linked resource in Eclipse](/media/2018/Create_New_Folder_In_The_Eclipse_Project_Explorer.jpg)

**Right click the virtual folder in order to view the pop up menu** 

 In the new folder window, enter Source as the directory name, and this
 time select the 'Link to alternative location (Linked Folder)' radio
 button. Enter the newly created FREERTOS\_ROOT variable as the folder's location.

![Using a relative path to add files into an Eclipse project](/media/2018/Link_To_Alternative_Location.jpg)

**Using a relative path to add a linked folder into an Eclipse project**
5. **Selecting the Files To Build** 

 The FreeRTOS/Source directory is now visible within the
 Eclipse Project explorer. The directory contains the source files for
 every RTOS port, so the next step is to use Eclipse resource filters to
 ensure only the files necessary to build the FreeRTOS port actually being
 used are visible.

 Right click on the Portable directory to view the pop up menu again, this
 time select 'Properties'. A pop up window that shows the proprieties of
 the Portable directory will be displayed.

![View the properties of the RTOS source code directory](/media/2018/Select_RTOS_Source_Portable_Directory.jpg)

**Viewing the properties of the RTOS Source code's Portable directory** 

 In the Properties window, select 'Resources->Resource Filters' to view
 the directory's resource filters. Create two 'Include Only' resource filters
 so the only directories that are shown match the text 'MemMang' and '[compiler]',
 where [compiler] is the compiler used to build the source files. By way of
 example, the next
 two images show the settings to use if the project is being built with the
 Renesas compiler.

![Adding Eclipse resource filters to down select the RTOS source files being built](/media/2018/Add_Eclipse_Resource_Filters.jpg)

**Defining 'Include Only' resource filters on the directories** 

![The Eclipse project resource filters](/media/2018/Resource_Filters_Defined.jpg)

**The Resource Filters window after the two filters have
 been defined.** 

 At the time of writing, the MemMang directory contains four .c files,
 each of which provides one of
 [four different options for heap memory management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management).
 Add a resource filter to the MemMang directory
 to ensure only one of the four .c files is visible.

![Ensure only one RTOS heap source file is built](/media/2018/Only_Include_One_Heap_File.jpg)

**Using a resource filter to ensure only one heap\_x.c file is built,
 heap\_4.c in the depicted case** 

 The [compiler] directory will contain a sub directory for each architecture
 FreeRTOS supports with that compiler. Add a resource filter to the
 [compiler] directory to ensure only the directory for the architecture
 actually being used is visible. For example, the resource filter being
 created in the image below is correct if the Renesas compiler is being
 used to build a project that targets a microcontroller form the RX600 family.

![Ensuring only the source files for the architecture the RTOS is being built for are shown](/media/2018/Repeat_For_Any_Subdirectories.jpg)

**Creating a resource filter to ensure only one sub directory
 under the [compiler] directory is visible**
6. **Adding Linked Directories Into the Compiler's Include Path** 

 Virtual and linked folders can be added to the compiler's include path
 in the normal way.

![Adding the RTOS's header source files to the project's include path](/media/2018/Linked_Folders_Can_Be_Added_In_Include_Path.jpg)

**Adding directories from the virtual and linked folders into
 the compiler's include path**

[Google](https://plus.google.com/106895663740671259833?  rel=author target=)
[Profile](https://profiles.google.com/106895663740671259833)
