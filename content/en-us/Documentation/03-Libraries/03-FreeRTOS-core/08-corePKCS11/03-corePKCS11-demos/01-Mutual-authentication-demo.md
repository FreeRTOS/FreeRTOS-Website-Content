---
title: corePKCS11 Mutual Authentication Demo (MQTT)
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


**Note: We recommend that you always use strong mutual authentication in any Internet of Things (IoT)
application. This example uses the recommended mutual authentication and is suitable for production IoT.**

* On this Page
    + [Source Code Organization](#source-code-organization)
    + [Configuring the Demo Project](#configuring-the-demo-project)
    + [Building the Demo Project](#building-the-demo-project)
    + [Functionality](#functionality)


## Introduction

This demo builds upon the MQTT mutual authentication demo. It assumes you are already familiar with the
MQTT demo series. Please see the [MQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) section if you haven't already.

The PKCS #11 demo projects use
the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW),
so they can be built and evaluated with
the [free Community version of Visual Studio](https://visualstudio.microsoft.com/vs/community/) on Windows
without the need for any particular MCU hardware.

This demo establishes a connection to AWS (Amazon Web Services) IoT in a way similar to MQTT mutual
authentication, but it uses PKCS #11 to manage the credentials necessary to establish a connection to
AWS IoT. For demonstration purposes, this PKCS #11 implementation uses the Windows file system for
credential management.

PKCS #11 works by assigning a human readable label to each crypto object. In this demo, we map the
label "Device Priv TLS Key" to our private key and "Device Cert" to our certificate. These labels can
be managed in `core_pkcs11_config.h`. In `core_pkcs11_pal.c`, we have mapped these labels to `FreeRTOS_P11_Key.dat`
and `FreeRTOS_P11_Certificate.dat` respectively.


### Source Code Organization

The Visual Studio solution for the PKCS #11 based mutual authentication demo is called `pkcs11\_mqtt\_mutual\_auth\_demo.sln.sln`
and is located in the `\FreeRTOS-Plus\Demo\corePKCS11\_MQTT\_Mutual\_Auth\_Windows\_Simulator\pkcs11\_mqtt\_mutual\_auth\_demo.sln`
directory of the main FreeRTOS download.

[![](/media/2020/PKCS11-Source-Code-Organization.png)](/media/2020/PKCS11-Source-Code-Organization.png)
*Click to enlarge*


## Configuring the Demo Project

Configure the demo project by following the instructions
under [MQTT mutual auth](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication), you can ignore the steps that
involve migrating your certificate and private key to the `democonfig.h` file, but make sure the Thing
name and AWS IoT endpoint are included in `democonfig.h`. These steps can be ignored since you will be
importing your credentials via the PKCS #11 interface instead through this demo.

Once this is complete follow the below steps:

1. In `democonfig.h`

   1. Set `democonfigCLIENT_CERTIFICATE_PEM` to an empty string.

      `#define democonfigprofileCLIENT_CERTIFICATE_PEM ""`

   2. Set `democonfigprofileCLIENT_PRIVATE_KEY_PEM` to an empty string.

      `#define democonfigprofileCLIENT_PRIVATE_KEY_PEM ""`

   3. This is to prevent `\FreeRTOS-Plus\Demo\corePKCS11_MQTT_Mutual_Auth_Windows_Simulator\demo_config.h;`
      from generating compiler errors, and will serve as further proof that the credentials in this header file
      are not used anywhere in the demo.

2. Convert the key and certificate PEM files that were authenticated with AWS IoT Core to DER format.

   1. You should already have acquired PEM formatted credentials in the MQTT demos. If not, please revisit
      the MQTT mutual auth series for guidance on retrieving these credentials.

   2. Option 1: Use the provided python script:

      1. Navigate to `\FreeRTOS-Plus\Demo\corePKCS11_MQTT_Mutual_Auth_Windows_Simulator`, and pass
         the absolute path for the key and certificate PEM files to `pkcs11_demo_setup.py`.

         `python3 pkcs11_demo_setup.py -c thing_cert_pem_file.pem -k thing_private_key_pem_file.pem`

      2. This will output equivalent .dat files in the same location as where the script was run.

   3. Option 2: Manually convert PEM files.

      1. If you choose not to use the above script, manually convert the PEM files to a PKCS #11 compatible DER format.

      2. An example using [OpenSSL](https://www.openssl.org/):

         `openssl x509 -outform der -in "CERTIFICATE_PEM_FILE" -out FreeRTOS_P11_Certificate.dat`

         `openssl pkcs8 -topk8 -inform PEM -outfrom -DER -in "KEY_PEM_FILE" -out FreeRTOS_P11_Key.dat`

3. Move the newly created .dat files to the same folder as the project solution. In this
   case `FreeRTOS-Plus\Demo\corePKCS11_MQTT_Mutual_Auth_Windows_Simulator\pkcs11_mqtt_mutual_auth_demo.sln;`.


## Building the Demo Project

The demo project uses
the  [free community edition of Visual Studio](https://visualstudio.microsoft.com/vs/community/)[.](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/01-coreMQTT-demo#source_code)

1. Open the `\FreeRTOS-Plus\Demo\corePKCS11_MQTT_Mutual_Auth_Windows_Simulator\pkcs11_mqtt_tls_mutual_auth\pkcs11_mqtt_tls_mutual_auth_demo.sln`
   Visual Studio solution file from within the Visual Studio IDE.

2. Select ‘build solution’ from the IDE’s ‘build’ menu.


## Functionality

The demo provides the same functionality as the mutual authentication MQTT demo with the addition of
using PKCS #11 for managing credentials. For details on MQTT functionality, please view
the [MQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication) demo series.

The major difference between this demo and the MQTT series, is
that `FreeRTOS-Plus/Source/Application-Protocols/platform/freertos/transport/src/tls_freertos_pkcs11.c`
was modified to use PKCS #11.
See `FreeRTOS-Plus/Source/Application-Protocols/platform/freertos/transport/src/tls_freertos_pkcs11.c`
and `FreeRTOS-Plus/Source/Application-Protocols/platform/freertos/transport/include/tls_freertos_pkcs11.h`
for how PKCS#11 was used to establish a TLS connection.

Code changes also exist at the application layer that emphasize the usage of PKCS #11 for credential
management. For example, in `FreeRTOS-Plus/Demo/corePKCS11_MQTT_Mutual_Auth_Windows_Simulator/DemoTasks/MutualAuthMQTTExample.c`,
the `xNetworkSecurityCredentials` struct does not contain the client certificate and key,
unlike `FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth/DemoTasks/MutualAuthMQTTExample.c`.

As an extra step, try moving your .dat files into a different directory mid demo. This will result in
an inability to establish a new connection to AWS IoT Core, so the subsequent iteration of the demo will
fail. For the example output of a successful demo, please see the MQTT demo series.
