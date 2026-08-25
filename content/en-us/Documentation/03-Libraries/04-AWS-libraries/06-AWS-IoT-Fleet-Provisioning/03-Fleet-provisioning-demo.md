---
title: AWS IoT Fleet Provisioning Demo
created: 2018-09-20
categories:
  - libraries
description: An introduction to the AWS IoT fleet provisioning library
relatedLinks:
  - title: Fleet provisioning Github repository
    link: https://github.com/aws/Fleet-Provisioning-for-AWS-IoT-embedded-sdk
  - title: Fleet provisioning introduction
    link: /Documentation/03-Libraries/04-AWS-libraries/06-AWS-IoT-Fleet-Provisioning/01-AWS-IoT-fleet-provisioning/#introduction
---

## Introduction

The AWS IoT Fleet Provisioning Demo showcases a way to provision a fleet of IoT devices with unique
certificates and register them with AWS IoT Core using the Fleet Provisioning feature. This demo
shows how devices with the ability to generate a public-private key-pair on board can utilize a
common claim certificate (across the entire fleet of devices) to request unique certificates from
AWS IoT Core for their generated key-pairs, and register themselves with AWS IoT Core
as [AWS IoT thing resources](https://docs.aws.amazon.com/iot/latest/developerguide/iot-thing-management.html).

For more information on the Fleet Provisioning feature of AWS IoT, refer
to [Provisioning devices that don't have device certificates using fleet provisioning](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html)
in the *AWS IoT Developer's Guide*. There are two provisioning workflows with Fleet
 Provisioning, [Provisioning by Claim](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html#claim-based)
and [Provisioning by Trusted User](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html#trusted-user).
This demo shows how to use the *Provisioning by Claim* workflow to provision devices with unique certificates
using a common *Claim* certificate registered with AWS IoT Core. This demo project uses
the [free community edition of Visual Studio](https://visualstudio.microsoft.com/vs/community/).

Prior to starting the Fleet Provisioning demo, we recommend that you use
the [corePKCS11 Mutual Authentication Demo (MQTT)](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/03-corePKCS11-demos/01-Mutual-authentication-demo) to connect to AWS IoT.
That will ensure that connectivity to AWS IoT is working correctly and that corePKCS11 credential management
is functioning properly.


## Source Code Organization

The demo project is called `fleet_provisioning_demo.sln` and can be found in
the [FreeRTOS](https://github.com/FreeRTOS/FreeRTOS) repository on GitHub in the following directory:

```c
FreeRTOS-Plus/Demo/AWS/Fleet_Provisioning_Windows_Simulator/Fleet_Provisioning_With_CSR_Demo
```


## Setting up AWS resources before running the demo

To use the Fleet Provisioning feature of AWS IoT Core, you must set up an *IAM role* and a *Provisioning
Template* in your AWS account. These AWS resources can be set up either through the AWS console or
programmatically through the AWS CLI. The following instructions guide you through the set up of these
resources using the AWS CLI. (In the following example commands, replace the `<aws-region>`
and `<aws-account-id>` with the AWS Region and ID relevant to your AWS account.) For information on
setting up the AWS CLI,
see [Getting started with the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html).

1. Navigate to the demo subfolder
   at [FreeRTOS-Plus/Demo/AWS/Fleet_Provisioning_Windows_Simulator/CSR_Demo](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/AWS/Fleet_Provisioning_Windows_Simulator/CSR_Demo).

2. Create an IAM role that will be needed by a fleet provisioning template.

   ```
   aws iam create-role \
    --role-name "FleetProvisioningDemoRole" \
    --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Action":"sts:AssumeRole","Effect":"Allow","Principal":{"Service":"iot.amazonaws.com"}}]}'
   ```
3. Attach the "AWSIoTThingsRegistration" policy to the role created in the above step. This allows the
   role to register new AWS IoT Things.

   ```
   aws iam attach-role-policy \
    --role-name "FleetProvisioningDemoRole" \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSIoTThingsRegistration
   ```

4. Create an AWS IoT Policy which the Fleet Provisioning Claim will attach to newly-created things. An
   example IoT thing policy which you can modify to work with the demo can be found in
   the "[example_iot_thing_policy.json](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Fleet_Provisioning_Windows_Simulator/CSR_Demo/DemoSetup/example_iot_thing_policy.json)"
   file. Before you run the following command, modify the `example_iot_thing_policy.json` file by replacing
   all occurrences of the following items in angle brackets:

   * `<aws-region>` with the AWS region of your choice (e.g. us-west-2)
   * `<aws-account-id>` with your AWS account ID

   ```
   aws iot create-policy \
   --policy-name FleetProvisioningDemoThingPolicy \
   --policy-document file://example_iot_thing_policy.json
   ```

5. Create an IoT Thing Type. This Thing Type will be attached to all things created by the Fleet Provisioning
   demo, which allows for easy cleanup.

   ```
   aws iot create-thing-type --thing-type-name "fp_demo_things"
   ```

6. Create the template resource which will be used for provisioning the demo application. This needs
   to be done only once. For more information on fleet provisioning templates, refer
   to [this guide](https://docs.aws.amazon.com/iot/latest/developerguide/provision-template.html#fleet-provision-template).
   An example fleet provisioning template which works with the demo can be found in
   the [example_fleet_provisioning_template.json](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Fleet_Provisioning_Windows_Simulator/CSR_Demo/DemoSetup/example_fleet_provisioning_template.json)
   file.

   ```
   aws iot create-provisioning-template
    --template-name FleetProvisioningDemoTemplate
    --provisioning-role-arn arn:aws:iam::<aws-account>:role/FleetProvisioningDemoRole
    --template-body file://example_fleet_provisioning_template.json
    --enabled
   ```

7. After you've made your fleet provisioning template, you can verify it was successfully created using
   the following CLI command.

   ```
   aws iot describe-provisioning-template --template-name FleetProvisioningDemoTemplate
   ```

8. Create a claim certificate and private key to use for the Provisioning by Claim workflow in the demo.
   In the command's output, note the "`certificateId`" for step 10.

   ```
   aws iot create-keys-and-certificate
    --certificate-pem-outfile "ClaimCertificate.pem"
    --public-key-outfile "ClaimPubKey.pem"
    --private-key-outfile "ClaimPrivateKey.pem"
    --set-as-active
   ```

9. Create an IoT policy for the Claim certificate. The following is the AWS CLI command for creating
   an IoT Policy. An example Claim certificate policy can be found in
   the "[example\_claim\_policy.json](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Fleet_Provisioning_Windows_Simulator/CSR_Demo/DemoSetup/example_claim_policy.json)"
   file. Before you run the `create-policy command`, modify "example_claim_policy.json" by replacing
   all occurrences of the following items in angle brackets:

   * `<aws-region>` with the AWS region of your choice (e.g. us-west-2)
   * `<aws-account-id>` with your AWS account ID

   ```
   aws iot create-policy \
    --policy-name FleetProvisioningDemoClaimPolicy \
    --policy-document file://example_claim_policy.json
   ```

10. Attach the policy to the claim certificate. Replace `<Claim-Cert-ID>` with the certificate ID of
   the Claim Certificate that you created in Step 8.

   ```
   aws iot attach-policy \
    --target "arn:aws:iot:<aws-region>:<aws-account-id>:cert/<Claim-Cert-ID>" \
    --policy-name "FleetProvisioningDemoClaimPolicy"
   ```


## Configure the Demo Project

11. The demo uses the [FreeRTOS-Plus-TCP TCP/IP stack](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP),
   so follow the instructions provided for
   the [TCP/IP starter project](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator) to:

   1. [Install the pre-requisite components](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites)
      (such as WinPCap).

   2. Optionally [set a static or dynamic IP address, gateway address and netmask](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic).

   3. Optionally [set a MAC address](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr).

   4. [Select an Ethernet network interface](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface)
      on your host machine.

   The above settings should be changed in the
   file [FreeRTOSConfig.h](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/AWS/Fleet_Provisioning_Windows_Simulator/CSR_Demo)
   in the Fleet Provisioning demo project.

12. Configure `demo_config.h`. The following macros must be defined by the user for the demo to work:

   ```c
   democonfigMQTT_BROKER_ENDPOINT
   democonfigROOT_CA_PEM
   democonfigPROVISIONING_TEMPLATE_NAME
   ```

13. Convert the Claim certificate and private key files you created in Step 6 above to DER format. This
   can be done manually or by using the included Python script `fleet_provisioning_demo_setup.py`.

   Option 1 - Using the included Python script:

   1. The script requires Python 3. If you do not have the 'cryptography' Python module installed, run
      the command `pip3 install cryptography`

   2. Navigate to the folder `...FreeRTOS-Plus\Demo\AWS\Fleet_Provisioning_Windows_Simulator\Fleet_Provisioning_With_CSR_Demo`

   3. Pass the absolute path for the key and certificate PEM files to `fleet_provisioning_demo_setup.py`,
      which will output the equivalent .dat files in the same location where the script is run.

   4. Move the `*.dat` files into `...\FreeRTOS-Plus\Demo\AWS\Fleet_Provisioning_Windows_Simulator\Fleet_Provisioning_With_CSR_Demo`

   5. Run the script:

      ```
      python3 fleet_provisioning_demo_setup.py -c ClaimCertificate.pem -k ClaimPrivateKey.pem
      ```

   Option 2 - Manually convert the PEM files:

   1. Use your preferred method of converting PEM files to a PKCS #11 compatible DER format.

   Here is an example using [OpenSSL](https://www.openssl.org/):

   1. `openssl x509 -outform der -in "ClaimCertificate.pem" -out corePKCS11_Claim_Certificate.dat`
   2. `openssl pkcs8 -topk8 -inform PEM -outform der -in "ClaimPrivateKey.pem" -out corePKCS11_Claim_Key.dat`
   3. Move the `*.dat` files into `...\FreeRTOS-Plus\Demo\AWS\Fleet_Provisioning_Windows_Simulator\Fleet_Provisioning_With_CSR_Demo`


## Build the Demo Project

The demo project uses the [free community edition of Visual Studio](https://visualstudio.microsoft.com/vs/community/).
To build the demo:


14. Open the Visual Studio solution
   file `FreeRTOS-Plus/Demo/AWS/Fleet_Provisioning_Windows_Simulator/Fleet_Provisioning_With_CSR_Demo/fleet_provisioning_demo.sln`
   from within the Visual Studio IDE.

15. Select **build solution** from the IDE's **build** menu.


## Functionality

The demo showcases the *Provisioning by Claim* workflow of the Fleet Provisioning feature of AWS IoT
Core using corePKCS11 for credential management.


1. The demo connects to the AWS IoT MQTT broker using the Claim credentials prepared in step 13.

2. The demo creates and stores new key-pair and certificate files using corePKCS11. These credentials
   will be later used to provision a new AWS IoT thing.

3. The [CreateCertificateWithCsr MQTT API](https://docs.aws.amazon.com/iot/latest/developerguide/fleet-provision-api.html#create-cert-csr)
   is called to make a Certificate Signing Request (CSR), so that AWS IoT will acknowledge and sign the
   certificate.

4. The [RegisterThing MQTT API](https://docs.aws.amazon.com/iot/latest/developerguide/fleet-provision-api.html#register-thing)
   is called to create a new AWS IoT thing which uses the key-pair and newly-signed certificate.

5. After the new thing is provisioned, the demo disconnects from the AWS IoT MQTT broker.

6. The demo connects to the AWS IoT MQTT broker using the newly-created thing credentials to verify that
   the thing was successfully registered.


The source code for the `prvFleetProvisioningTask()` function can be found in
the [FleetProvisioningDemoExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Fleet_Provisioning_Windows_Simulator/CSR_Demo/FleetProvisioningDemoExample.c)
file on GitHub.

The screenshot below shows the expected output when the demo executes correctly:

[![demo success](/media/2021/fleet_provisioning.png)](/media/2021/fleet_provisioning.png)
