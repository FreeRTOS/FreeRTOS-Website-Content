---
title: Over the Air Updates (OTA)
created: 2018-09-20
categories:
  - libraries
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## Introduction

Over the Air Updates or OTA refers to the process of delivering new software/firmware to a device wirelessly. 
OTA updates provide a flexible, cost-effective, and efficient mechanism to keep IoT devices updated, secure, 
and performing optimally throughout their lifecycle.

The key benefits of **Over the Air (OTA) Updates** are:

1. **Security**  - The ability to quickly respond to security vulnerabilities and software bugs that are 
   discovered after the devices are deployed in the field.
2. **Innovation** - Products can be updated frequently as new features are developed, thus driving the 
   innovation cycle. The updates can take effect quickly, with minimum downtime compared to traditional 
   update methods.
3. **Cost** - OTA updates can reduce maintenance costs significantly compared to methods traditionally 
   used to update these devices.


## OTA workflow

The following diagram depicts the general flow of an OTA:
<br />
![](/media/2023/OTA-flow.png)

**Notify** - This is the first step of the OTA process. The device is notified of a pending Over The 
Air update. This notification starts the process of deciding how to handle the update. The device may 
choose to ignore the update or accept the update triggering the download. The device will notify the 
OTA update provider of its choice.

**Download** - The device begins downloading the OTA update over any one of its supported protocols. The 
device will download the update to a pre-selected storage region. This update may be an entirely new 
firmware image or a patch to the existing firmware.

**Verify** - The device performs various checks to ensure the authenticity of the downloaded firmware. 
A robust verification state prevents malicious actors from installing firmware, the device from being 
corrupted, and incorrectly signed updates from taking place.

**Install** - The device now updates itself (often through a bootloader) to the newest firmware. Checks 
may be performed after the install to verify functionality. The device will report the successful firmware 
update to the OTA update provider.

To remain robust against a failed or invalid update, a well-designed OTA flow runs a **self-test** on the 
new firmware before permanently committing to it. If the self-test fails, the device should **roll back** 
to the previous known-good image rather than risk being left in a non-functional ("bricked") state. Sharing 
a single network connection between the OTA process and the application can also save memory on 
resource-constrained devices.


## Modular OTA approach

Modular OTA consists of several small libraries and an orchestrator. Each library is responsible for a 
specific sub-task, like notifying for a pending OTA update or downloading the file over MQTT. The orchestrator 
synchronizes all of the small libraries along with a bootloader and memory pool to perform the OTA update.


#### Customizability

The Modular OTA approach allows you to swap out or change different parts of OTA as your requirements 
change. For example:

1. If you want to trigger OTA from AWS IoT, then you can use the IoT jobs library to check for new OTA 
   updates or to send notifications on the status of OTA jobs. Or, you can replace it with any other library 
   which can notify your device of pending OTA updates.
2. You can use the OTA job parser in the IoT jobs library to parse the received OTA job document. Or you 
   can use your own customized job document parser based on your OTA job document.
3. You can download the new software/firmware over MQTT or HTTP using MQTT streams or the CoreHTTP libraries, 
   respectively. If you want to use some other protocol or library, then you can use that as well.


#### Extensibility

The design allows for easy additions and improvements to your OTA without major overhauls. For example, 
you can add your own signature verification step or use your own bootloader.


#### Configurability

You can easily tweak settings to control different parameters, for example, to change the size of the 
data blocks, the number of blocks to be downloaded per request, or the encoding scheme to be used for 
data blocks.


#### Modular OTA data flow diagram
<br />
![](/media/2023/OTA-flowchart.drawio.png)


#### Orchestrator

The Orchestrator is the central component which specifies how an OTA update is to be coordinated. The 
Orchestrator is user provided, and contains as many custom components as desired to accomplish the desired 
OTA update method. A typical update will contain the 'Notify', 'Download', 'Verify', and 'Install' phases. 
The Orchestrator will provide these phases by stitching together component libraries and other external 
libraries. Descriptions of each component library can be found below and refer to the OTA using Simple 
Orchestrator demo to get a better understanding of what an Orchestrator looks like.


#### IoT Jobs library

The IoT Jobs handler is the first component used in the overall OTA flow. This library provides functions 
to start a pending IoT Job (shown as 'Notify' on the first diagram above) as well as update a job's status. 
When the Jobs handler learns of a new OTA update - coming through an IoT job - the handler will start the 
job and pass the job and its metadata on to a chain of parsers. If a parser is set up to handle the job, 
it will relay back to the job handler that the job was started successfully. This successful start notification 
is relayed back to the OTA update provider (which is IoT Jobs) to mark the update as started. If no parser 
is able to understand the job, this failure to start the OTA update is relayed to the provider.


#### OTA Job Parser

The parser will verify the IoT job is an OTA update and parse the fields into a usable format before 
calling on the downloader.


#### MQTT file streaming library

The file downloader provides functionality to download the OTA file. The file downloader handles downloading 
the update over an MQTT stream in either CBOR or JSON format. The download itself is performed on 'blocks' 
which is easier to think of as chunks of the overall OTA update file. This is done to increase the reliability 
of the download as well as to allow for larger firmware updates than possible in a single download 'block'.


#### Bootloader and Signature Verifier

The bootloader exists to verify and install the new firmware onto the device. Modular OTA deliberately 
avoids implementing a bootloader as several industry-wide bootloaders already exist for a large range 
of supported microcontrollers. Modular OTA leaves the choice of the bootloader and signature verification 
mechanism up to the user.

