---
title: "Import and build a demo project in Eclipse"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

This page provides general information on how to use Eclipse to import and build the many FreeRTOS demo applications
provided as Eclipse projects. The [Demo application specific documentation](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos) pages provide additional
information specific to a given demo, including the project's location within the FreeRTOS directory structure. The
demonstration below is based on the base Eclipse Embedded CDT version on a Windows environment.

**NOTE:** Vendor-specific Eclipse distributions may look different from the base Eclipse version used to create
the screen shots below.

## Prerequisites:

1. Install an Eclipse distribution

   The base Eclipse version, Eclipse Embedded CDT (C/C++ Development Tools), can be downloaded
   [here](https://projects.eclipse.org/projects/iot.embed-cdt/downloads).

   **NOTE:** Most of the vendor-specific Eclipse-based IDEs include the toolchain in the distribution, and
   handle setting up the path to it automatically and transparently for you. Please check with your specific demo page
   linked to on [Demo application specific documentation](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos). You may skip the following steps if
   your vendor-specific IDE provides the toolchain and build tools.

2. Install the GCC Toolchain

   Refer to the [Demo application specific documentation](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos) pages for information on the specific
   toolchain needed for your demo.

3. Install the build tool (Windows)

   POSIX platforms generally include `make` in the system distribution, or they might require you to install
   some developer packages (for example, on macOS you need to install the Xcode Command Line Tools). Follow the "Windows
   Build Tools" section in this [guide](https://gnu-mcu-eclipse.github.io/install/) to install the Make build
   tools.

   **NOTE:** If you have another environment installed, such as MinGW or Cygwin, and want to use the Make
   tool provided by that environment, make sure the `make` program is named "`make.exe`". In the same way, for
   MinGW, rename (or create a copy and rename) "`mingw32-make.exe`" to "`make.exe`".

4. Manage the PATH Environment variable

   The base Eclipse version relies on setting the environment variable `PATH` to reach the toolchain binaries.
   The `PATH` can be set from:

   - The system global `PATH` setting or a per user `PATH` setting.
   - The Eclipse workspace's common settings for all projects.
   - The project's build configuration. We highly recommend that you set the `PATH` from the project's build configuration to avoid any
     conflict when using multiple toolchains that may be installed on your computer. To set the project's `PATH`
     variable in Eclipse:

   1. Right click the demo project from the "Project Explorer" and select "Properties".

      ![](/media/2020/Screen-Shot-2020-08-26-at-6.22.25-PM.png)
      Open Project Properties

   2. On the left side of the pop-up window, select "C/C++ build --> Environment" and then click the "Add..."
      button on the right to add a new variable.

      ![](/media/2020/Screen-Shot-2020-08-26-at-5.52.10-PM.png)
      Project Properties

   3. Enter "PATH" as the variable name and set the value with the path to your toolchain and build tools binaries
      folder.

      ![](/media/2020/Screen-Shot-2020-08-26-at-5.53.03-PM.png)
      Add PATH Variable

## Import and Build a Demo Project:

**Important!** FreeRTOS Eclipse projects use relative paths to source files and therefore will not build
if your directory structure is different from the directory structure used in the official FreeRTOS zip-file releases. Ensure
the 'copy projects into workspace' check box is not checked when importing the project into
the Eclipse workspace.

1. Start Eclipse, then select an existing, or create a new workspace when prompted.

2. Select "Import..." from the Eclipse "File" menu. The Import dialog box will open.

3. In the Import dialog box, select "General -> Existing Project into Workspace". The Import Projects dialog box
   will open.

   ![](/media/2020/Screen-Shot-2020-08-19-at-10.06.25-AM.png)
   Importing an existing project into the workspace

4. In the Import Projects dialog box, navigate to and select the `FreeRTOS/Demo/<YOUR_PROJECT>`
   directory, and make sure the 'Copy projects into workspace' check box is not checked.

   ![](/media/2020/Screen-Shot-2020-08-19-at-10.07.29-AM.png)
   Selecting the directory and project in the Import Project dialog box.

5. In the "Projects" window of the Import Projects dialog box, select the RTOSDemo project, and choose "finish".

6. Select "Build all" from the Eclipse "Project" menu. Make sure the project builds without any errors or warnings.
