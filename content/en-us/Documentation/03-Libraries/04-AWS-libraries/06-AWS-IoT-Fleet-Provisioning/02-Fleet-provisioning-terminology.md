---
title: Fleet Provisioning Terminology
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

*Fleet Provisioning*   
Workflow which creates resources so your devices and AWS IoT can communicate securely. Fleet Provisioning 
can create AWS IoT Things For more information, consult 
the [AWS IoT docs](https://docs.aws.amazon.com/iot/latest/developerguide/iot-provision.html) on Device 
Provisioning.


*Device Certificate*   
A device certificate is a credential associated with a specific device. Many devices are manufactured 
with device certificates already on them. When a device has a certificate already, it can be registered 
with AWS IoT. Otherwise, a device certificate can be obtained from AWS IoT. For more information on 
device certificates, consult 
the [AWS IoT docs](https://docs.aws.amazon.com/iot/latest/developerguide/iot-provision.html) on Device 
Provisioning.


*Provisioning Template*   
Provisioning templates describe the resources AWS IoT requires to provision your device. Templates contain 
variables that enable you to use one template to provision multiple devices. When you provision a device, 
you specify values for the variables specific to the device using a dictionary or map. To provision another 
device, specify new values in the dictionary. 


*Provisioning by Claim*   
A way to set up a device with AWS IoT using a claim certificate and private key. Devices can be manufactured 
with special-purpose credentials (a provisioning claim certificate and private key) embedded in them. 
If these certificates are registered with AWS IoT, the service can exchange them for unique device certificates 
that the device can use for regular operations. For more information on provisioning by claim, consult 
the [AWS IoT docs](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html).


*Provisioning by Trusted User*   
A way to set up a device with AWS IoT using a trusted user’s access and permissions. For more information 
on provisioning by trusted user, consult 
the [AWS IoT docs](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html).
