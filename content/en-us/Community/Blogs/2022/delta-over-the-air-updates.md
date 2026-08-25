---
title: Delta Over-the-Air Updates
date: 12 Jan 2022
feature: blog
categories:
  - Long term support
authors: 
  - pvyawaha
---
<p className="tips">
  <span className="display-6">⚠️ Deprecated</span>
  <span className="content">
    The AWS IoT OTA library used in this post is now deprecated. For new designs we recommend using [Modular Over-the-Air Updates](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates), which replace the monolithic OTA Agent with smaller, composable libraries. The cloud-side OTA process (AWS IoT console and the OTA Update Manager service) is unchanged — only the on-device library has changed.
  </span>
</p>

The ability to update device software Over-the-Air (OTA) is becoming increasingly important 
as more embedded devices get connected to the cloud. OTA updates enable operators to apply 
security fixes and add new features to already deployed devices, at scale, quickly and 
reliably, and without requiring an expensive or impractical technician visit.

While OTA benefits all connected devices, those on low bandwidth networks such as LoRaWAN 
and NB-IoT face some additional challenges. These networks are severely constrained in 
bandwidth, making OTA updates costly if they require sending large firmware (or other) images 
to these devices. Sending large images over the air is also problematic for battery-powered 
devices connected to more power-hungry Wi-Fi and cellular networks - the sooner the radio is 
turned off the longer the battery will last. So it can be seen that introducing a mechanism 
that reduces the transmitted image size will benefit both these use cases. This blog 
describes one such mechanism- Delta Over-the-Air Updates. Instead of sending an entire new 
firmware image to a device, Delta Over-the-Air Updates only send the portions of the image 
that have actually changed.


## Delta Over-the-Air Updates Using Binary Difference

Delta Over-the-Air Updates reduce the size of the OTA update by sending only the binary 
difference (binary diff) between the firmware currently running on the device and the new 
firmware, instead of sending the complete firmware image. The binary difference is sent 
to the device as a patch file. A patching library running on the device then reconstructs 
the new firmware image from the patch file and the firmware already on the device. The 
following two components are major parts of the binary diff mechanism:


* **Diff Utility** – The developer runs this utility on their PC to 
  compute the binary difference between the current firmware and the new firmware. 
  This difference is sent over the air to the device as a patch file.
* **Patching Library** – The patching library runs on the device and 
  reconstructs the new firmware from the patch file and the current firmware on the 
  device.

The following diagram shows the process of updating the firmware on a device or a fleet of 
devices using a Delta Over-the-Air Update:

![](/media/2021/firmware-update-process.png)

Available binary diff algorithms include [bsdiff](https://www.daemonology.net/bsdiff/), [xdelta](http://xdelta.org/), [jojodiff](http://jojodiff.sourceforge.net/), 
and [courgette](https://www.chromium.org/developers/design-documents/software-updates-courgette). The 
application writer is free to choose the algorithm best suited for their application. Some of the things 
to keep in mind when choosing a binary diff algorithm are memory requirements, performance, and the size of 
the delta image.


## Using the AWS IoT OTA Library for Delta Over-the-Air Updates

The [AWS IoT OTA library](https://github.com/aws/ota-for-aws-iot-embedded-sdk) runs on devices and manages 
receiving notifications of newly available updates, downloading the update, and performing cryptographic 
verification of the update received. The same library can be used for Delta Over-the-Air Updates. The AWS 
IoT OTA library requires the application to supply implementations of the following interfaces:

* MQTT Interface
* HTTP Interface
* OS Interface (Operating System interface)
* PAL Interface (Platform Abstraction Layer interface)

![](/media/2021/delta-update-library.png)

The only component that requires an update to support Delta Over-the-Air Updates is the OTA PAL. More 
specifically, the `OtaPalCloseFile_t` function of the OTA PAL must invoke the patching library to reconstruct 
the new firmware image from the patch file and the current firmware.

The following pseudo code shows an example implementation of the `OtaPalCloseFile_t` function that supports 
Delta Over-the-Air Updates:

![](/media/2021/otapalclosefile.png)


## Getting Started

Start with [this example](https://github.com/FreeRTOS/Labs-Project-Espressif-Demos) which uses 
the [jojodiff](http://jojodiff.sourceforge.net/) utility and the [janpatch](https://github.com/janjongboom/janpatch) 
library to demonstrate Delta Over-the-Air Updates on Espressif's ESP32 system-on-chip (SoC.) The step 
by step instructions for running the example are [here](https://github.com/FreeRTOS/Labs-Project-Espressif-Demos/blob/main/README#getting-started).


## Conclusion

Delta Over-the-Air (OTA) Updates reduce the time, cost, and power consumption of OTA updates 
on bandwidth-constrained or battery-powered networked devices. If you are using the AWS IoT 
OTA library, then you can achieve these benefits by adding a patching stage to the function 
that writes a received image to non-volatile storage on your device. There are several 
patching algorithms available, each with its own trade-offs between resource requirements, 
processing speed, and achieved image size reduction.


## About the author

![](https://secure.gravatar.com/avatar/4ae57ecc6122ef1c1844135bab3e9310?s=200&d=mm&r=g)   
Prasad is a Software Development Engineer at Amazon Web Services where he focuses on developing libraries 
to enable IoT connectivity for edge devices. Prior to AWS, he worked in developing low power network 
stacks and embedded software for in-vehicle infotainment systems, cellular modem and industrial analytical 
instruments.   
[View articles by this author](../author/pvyawaha) 


FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
