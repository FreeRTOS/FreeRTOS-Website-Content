---
title: OTA Terminology
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

*AWS Jobs*
AWS IoT Jobs is a service that notifies one or more connected devices of a pending “Job”. A Job can
be used to manage your fleet of devices, update firmware and security certificates on your devices,
or perform administrative tasks such as restarting devices and performing diagnostics. For more information,
see [Jobs](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/01-AWS-IoT-jobs).


*AWS Management Console*
The [AWS Management Console](https://aws.amazon.com/console/) is a website that is used to access various
AWS services.


*AWS IoT Console*
The [AWS IoT Console](https://aws.amazon.com/iot/) is a website that is used to interact with the IoT
related AWS services. This includes services for managing, monitoring, and updating devices.


*OTA Update Manager Service*
The over-the-air (OTA) Update Manager service provides a way to:

1. Create an OTA update and the resources it uses, including an AWS IoT job, an AWS IoT stream, and code signing.
2. Get information about an OTA update.
3. List all OTA updates associated with your AWS account.
4. Delete an OTA update.

[Learn More](https://docs.aws.amazon.com/freertos/latest/userguide/ota-manager.html)


*AWS Command Line Interface (AWS CLI)*
Run commands for AWS IoT on Windows, macOS, and Linux. These commands allow you to create and manage
things, certificates, rules, and policies. To get started, see
the [AWS Command Line Interface User Guide](https://docs.aws.amazon.com/cli/latest/userguide/). For
more information about the commands for AWS IoT,
see [iot](https://docs.aws.amazon.com/cli/latest/reference/iot/index.html) in the *AWS CLI Command
Reference*.


*S3 Bucket*
Amazon Simple Storage Service (S3) AWS Service that enables you to store files in the cloud that can
be accessed by you or other services. OTA update files are stored in Amazon S3 buckets.
[Learn More](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/what-is-s3.html)


*Registry*
Organizes the resources associated with each device in the AWS Cloud. You register your devices and
associate up to three custom attributes with each one. You can also associate certificates and MQTT
client IDs with each device to improve your ability to manage and troubleshoot them. For more information,
see [Managing Devices with AWS IoT](https://docs.aws.amazon.com/iot/latest/developerguide/iot-thing-management.html)


*"Things" in AWS IoT*
A thing is a representation of a device or logical entity in AWS IoT. It can be a physical device or
sensor (for example, a light bulb or a switch on a wall). It can also be a logical entity like an instance
of an application or physical entity that does not connect to AWS IoT, but is related to devices that
do (for example, a car that has engine sensors or a control panel). AWS IoT provides a thing registry
that helps you manage your things.

Things are identified by a name. Things can also have attributes, which are name-value pairs you can
use to store information about the thing, such as its serial number or manufacturer. Adding your things
to the thing registry allows you to manage and search for them more easily.

**Did you know?** Things don't always need to be connected to a device. You can connect a thing to
your computer, simulator, and more.


*AWS IoT Policy*
The [AWS IoT policy](https://docs.aws.amazon.com/iot/latest/developerguide/iot-policies.html) grants
your device permissions to access AWS IoT resources. It is stored on the AWS Cloud


*IAM Role*
Identity Access Management [(IAM)](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
helps you securely control access to AWS resources. You use IAM to control who is authenticated (signed
in) and authorized (has permissions) to use resources.
An [IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html) is an entity within
your AWS account that has specific permissions that you can assign to other users.


*MQTT*
The [MQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) (Message Queue Telemetry Transport) library provides a lightweight publish/subscribe
(or [PubSub](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern)) messaging protocol that
runs on top of TCP/IP and is often used in Machine to Machine (M2M) and Internet of Things (IoT) use cases.
[Learn More](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)


*MQTT Broker Endpoint*
Clients connect to their AWS account's device endpoints. Each account has several device endpoints that
are unique to the account and support specific IoT functions.
[Learn More](https://docs.aws.amazon.com/iot/latest/developerguide/iot-connect-devices.html#iot-connect-device-endpoints)


*Patch*
A patch is a set of changes between 2 firmware versions. Users can generate a patch by using any binary
diff mechanism. Some of the most popular ones include bsdiff, xdelta, jojodiff, and courgette.
