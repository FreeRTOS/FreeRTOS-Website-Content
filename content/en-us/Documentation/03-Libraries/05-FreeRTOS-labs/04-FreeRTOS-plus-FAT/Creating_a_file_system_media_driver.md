---
title: Creating a FreeRTOS-Plus-FAT Media Driver
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

![](/media/2018/Media_Driver.png)

## The Structure of a Media Driver

The *media* is the physical device on which files are stored. Examples of
media suitable for use in an embedded file system include SD cards,
solid state disks, NOR flash memory chips, NAND flash chips, and RAM
chips. The media driver is the software responsible for writing to the
media, and reading from the media.

FreeRTOS-Plus-FAT stores information that is common to all media types in a
structure of type FF\_Disk\_t. The FF\_Disk\_t structure can be extended by the
developer of the media driver so it includes additional information that
is specific to the media in use.

The FF\_Disk\_t structure references an object called an input/output manager
(IO Manager, or simply IOMAN). The IO manager is responsible for,
amongst other things, buffering and caching both file and directory information.

The mechanism for actually reading data from and writing data to the media
is dependent on the media type. Therefore the developer of the media
driver must provide suitable read and write functions.

Many media drivers will themselves make use of a peripheral driver in
order to perform the actual read and write operations. For example,
if the media is an SD card then it might
be necessary to access the card through an SPI peripheral.
A peripheral driver is not necessary when implementing a RAM disk, as
RAM can be read from and written to using the standard C library memcpy()
function.

Some media types also require higher level management logic to perform actions
such as [bad block management](https://en.wikipedia.org/wiki/Bad_sector),
or [wear levelling](http://en.wikipedia.org/wiki/Wear_leveling).


### Creating a New Media Driver

A media driver requires [at least] three functions.

1. [A function that reads sectors from the media](File_System_Media_Driver/Read_From_Disk)
2. [A function that writes sectors to the media](File_System_Media_Driver/Write_To_Disk)
3. [An initialisation function](File_System_Media_Driver/Media_Driver_Initialisation)

Click each item above for more information, and to see a worked example.


### Preparing Media For First Use

Just like a disk in a desktop computer, before the media can be used in
an embedded system it must first be [partitioned](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_Partition),
then a partition must be [formatted](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_Format)
and [mounted](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_Mount).

FreeRTOS-Plus-FAT implements a virtual file system in
which the mounted partition must be [registered](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_FS_Add),
after which it will
appear as a directory in the embedded file system's root directory.

### Driver API and Structures

* [FF\_CreateIOManager()](File_System_Media_Driver/FF_CreateIOManager)
* [FF\_Disk\_t](File_System_Media_Driver/FF_Disk_t)