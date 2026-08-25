---
title: AWS IoT Fleet Provisioning 演示
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 库
description: AWS IoT fleet provisioning 库简介
relatedLinks:
  - title: Fleet provisioning Github 存储库
    link: https://github.com/aws/Fleet-Provisioning-for-AWS-IoT-embedded-sdk
  - title: Fleet provisioning 简介
    link: /Documentation/03-Libraries/04-AWS-libraries/06-AWS-IoT-Fleet-Provisioning/01-AWS-IoT-fleet-provisioning/#introduction
---

## 引言

AWS IoT Fleet Provisioning 演示展示了为一批 IoT 设备预置唯一证书，
并使用 Fleet Provisioning（队列预置）功能将其注册到 AWS IoT 核心的方法。该演示
展示了能在板上生成公私密钥对的设备是如何利用
通用声明证书（遍及整批设备），为其生成的密钥对
向 AWS IoT 核心请求唯一证书，并在 AWS IoT 核心中将自身注册为
[AWS IoT 事物资源](https://docs.aws.amazon.com/iot/latest/developerguide/iot-thing-management.html)的过程。

有关AWS IoT Fleet Provisioning 功能的更多信息，请参阅
[使用 Fleet Provisioning 预置无证书设备](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html)
（位于 *AWS IoT 开发者指南*中）。Fleet Provisioning 有两种预置工作流程：
 [通过声明预置](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html#claim-based)
和[通过受信任的用户预置](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html#trusted-user)。
此演示展示了如何使用*声明预置*工作流程，
通过向 AWS IoT 核心注册通用*声明*，使用唯一证书预置设备的过程。此演示项目使用
[Visual Studio 免费社区版](https://visualstudio.microsoft.com/vs/community/)。

在启动 Fleet Provisioning 演示之前，我们建议您使用
[corePKCS11相互身份验证演示 (MQTT)](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/03-corePKCS11-demos/01-Mutual-authentication-demo) 来连接 AWS IoT。
这将确保 AWS IoT 连接正常运行以及 corePKCS11 凭证管理
功能正常执行。


## 源代码组织

演示项目名为 `fleet_provisioning_demo.sln`，可在
GitHub 上的 [FreeRTOS](https://github.com/FreeRTOS/FreeRTOS) 存储库中的以下目录中找到：

```c
FreeRTOS-Plus/Demo/AWS/Fleet_Provisioning_Windows_Simulator/Fleet_Provisioning_With_CSR_Demo
```


## 在运行演示前设置 AWS 资源

要使用 AWS IoT 核心的 Fleet Provisioning 功能，您必须在您的 AWS 账户中设置 *IAM 角色*和 *Provisioning
 模板*。这些 AWS 资源可通过 AWS 控制台
设置，也可通过 AWS CLI 以编程方式进行设置。下列说明将指导您
使用 AWS CLI 设置这些资源。（在下列示例命令中，将 `<aws-region>`
和 `<aws-account-id>` 替换为与您的 AWS 账户相关的 AWS 区域和 ID。）有关
设置 AWS CLI 的信息，
 请参阅 [AWSCLI 入门指南](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)。

1. 导航至
   [FreeRTOS-Plus/Demo/AWS/Fleet_Provisioning_Windows_Simulator/CSR_Demo](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/AWS/Fleet_Provisioning_Windows_Simulator/CSR_Demo) 中的演示子文件夹。

2. 创建队列预置模板所需的 IAM 角色。

   ```
   aws iam create-role \
    --role-name "FleetProvisioningDemoRole" \
    --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Action":"sts:AssumeRole","Effect":"Allow","Principal":{"Service":"iot.amazonaws.com"}}]}'
   ```
3. 将 “AWSIoTThingsRegistration” 策略附加至上一步骤创建的角色上。这
   使得该角色可以注册新的 AWS IoT 事物。

   ```
   aws iam attach-role-policy \
    --role-name "FleetProvisioningDemoRole" \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSIoTThingsRegistration
   ```

4. 创建 AWS IoT 策略， Fleet Provisioning 声明将把其附加至新创建的事物上。您可以修改
   IoT 事物策略示例，使其可同演示一起使用，
   该示例可在 "[example_iot_thing_policy.json](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Fleet_Provisioning_Windows_Simulator/CSR_Demo/DemoSetup/example_iot_thing_policy.json)" 文件中找到
   。在运行以下命令之前，请修改 `example_iot_thing_policy.json` 文件，
   将所有出现在尖括号中的下列项目都替换掉：

   * 将 `<aws-region>` 替换成您所选择的 AWS 区域（例如 us-west-2）
   * 将 `<aws-account-id>` 替换成您的 AWS 账户 ID

   ```
   aws iot create-policy \
   --policy-name FleetProvisioningDemoThingPolicy \
   --policy-document file://example_iot_thing_policy.json
   ```

5. 创建 IoT 事物类型。此事物类型将被附加至 Fleet Provisioning 演示创建的所有事物上，
   以方便清理。

   ```
   aws iot create-thing-type --thing-type-name "fp_demo_things"
   ```

6. 创建将用于预置演示应用程序的模板资源。这只需
   进行一次。有关队列预置模板的更多信息，请参阅
   [本指南](https://docs.aws.amazon.com/iot/latest/developerguide/provision-template.html#fleet-provision-template)。
   与演示一起使用的示例队列预置模板可在
   [example_fleet_provisioning_template.json](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Fleet_Provisioning_Windows_Simulator/CSR_Demo/DemoSetup/example_fleet_provisioning_template.json) 文件中找到
   。

   ```
   aws iot create-provisioning-template
    --template-name FleetProvisioningDemoTemplate
    --provisioning-role-arn arn:aws:iam::<aws-account>:role/FleetProvisioningDemoRole
    --template-body file://example_fleet_provisioning_template.json
    --enabled
   ```

7. 完成队列预置模板后，
   您可使用下列 CLI 命令验证其是否创建成功。

   ```
   aws iot describe-provisioning-template --template-name FleetProvisioningDemoTemplate
   ```

8. 创建声明证书和私钥，用于演示中的声明预置工作流程。
   在命令的输出中，要注意步骤 10 中的 "`certificateId`"。

   ```
   aws iot create-keys-and-certificate
    --certificate-pem-outfile "ClaimCertificate.pem"
    --public-key-outfile "ClaimPubKey.pem"
    --private-key-outfile "ClaimPrivateKey.pem"
    --set-as-active
   ```

9. 为声明证书创建 IoT 策略。下列 AWS CLI 命令就是
   用于创造 IoT 政策的命令。声明证书策略示例可在
   "[example_claim_policy.json](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Fleet_Provisioning_Windows_Simulator/CSR_Demo/DemoSetup/example_claim_policy.json)" 文件中找到
   。运行 `create-policy command` 前，请修改 "example_claim_policy.json"，
   将所有出现在尖括号中的下列项目都替换掉：

   * 将 `<aws-region>` 替换成您所选择的 AWS 区域（例如 us-west-2）
   * 将 `<aws-account-id>` 替换成您的 AWS 账户 ID

   ```
   aws iot create-policy \
    --policy-name FleetProvisioningDemoClaimPolicy \
    --policy-document file://example_claim_policy.json
   ```

10. 将策略附加至声明证书上。将 `<Claim-Cert-ID>` 替换为
   您在步骤 8 中创建的声明证书的 ID。

   ```
   aws iot attach-policy \
    --target "arn:aws:iot:<aws-region>:<aws-account-id>:cert/<Claim-Cert-ID>" \
    --policy-name "FleetProvisioningDemoClaimPolicy"
   ```


## 配置演示项目

11. 此演示使用 [FreeRTOS-Plus-TCP TCP/IP 堆栈](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)，
   因此，请按照
   [TCP/IP 入门项目](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)的说明操作：

   1. [安装了必要组件](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites)
      （如 WinPCap）。

   2. [设置了静态或动态 IP 地址、网关地址和网络掩码](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic)（可选）。

   3. [设置了 MAC 地址](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr)（可选）。

   4. 在您的主机上[选择以太网接口](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface)
      。

   上述设置应在
   文件 [FreeRTOSConfig.h](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/AWS/Fleet_Provisioning_Windows_Simulator/CSR_Demo) 中更改
   （该文件位于 Fleet Provisioning 演示项目中）。

12. 配置 `demo_config.h`。用户必须定义下列宏，才能让演示运行：

   ```c
   democonfigMQTT_BROKER_ENDPOINT
   democonfigROOT_CA_PEM
   democonfigPROVISIONING_TEMPLATE_NAME
   ```

13. 将您在步骤 6 中创建的声明证书和私钥文件转换为 DER 格式。这一步
   可手动完成，也可使用所包含的 Python 脚本 `fleet_provisioning_demo_setup.py` 来完成。

   方案 1 - 使用所包含的 Python 脚本：

   1. 此脚本需使用 Python 3。如果您未安装“加密” Python 模块，
      请运行命令 `pip3 install cryptography`

   2. 导航至文件夹 `...FreeRTOS-Plus\Demo\AWS\Fleet_Provisioning_Windows_Simulator\Fleet_Provisioning_With_CSR_Demo`

   3. 将密钥和证书 PEM 文件的绝对路径传递至 `fleet_provisioning_demo_setup.py`，
      这将在运行脚本的相同位置输出等效的 .dat 文件。

   4. 将 `*.dat` 文件移至 `...\FreeRTOS-Plus\Demo\AWS\Fleet_Provisioning_Windows_Simulator\Fleet_Provisioning_With_CSR_Demo`

   5. 运行脚本：

      ```
      python3 fleet_provisioning_demo_setup.py -c ClaimCertificate.pem -k ClaimPrivateKey.pem
      ```

   方案 2 - 手动转换 PEM 文件：

   1. 采用您所喜欢的方法将 PEM 文件转换为 PKCS #11兼容的 DER 格式。

   以下是使用 [OpenSSL](https://www.openssl.org/) 转换此文件格式的示例：

   1. `openssl x509 -outform der -in "ClaimCertificate.pem" -out corePKCS11_Claim_Certificate.dat`
   2. `openssl pkcs8 -topk8 -inform PEM -outform der -in "ClaimPrivateKey.pem" -out corePKCS11_Claim_Key.dat`
   3. 将 `*.dat` 文件移至 `...\FreeRTOS-Plus\Demo\AWS\Fleet_Provisioning_Windows_Simulator\Fleet_Provisioning_With_CSR_Demo`


## 构建演示项目

演示项目使用[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/)。
要构建演示，请执行如下操作：


14. 从 Visual Studio IDE 中打开 Visual Studio 解决方案
   文件 `FreeRTOS-Plus/Demo/AWS/Fleet_Provisioning_Windows_Simulator/Fleet_Provisioning_With_CSR_Demo/fleet_provisioning_demo.sln`
   。

15. 在 IDE 的 **“Build”** 菜单中选择 **“Build Solution”**。


## 功能

演示展示了 Fleet Provisioning 功能的 *声明预置* 工作流程，该功能为 AWS IoT
核心所有，该核心使用 corePKCS11 进行凭据管理。


1. 演示使用步骤 13 中准备的声明凭证连接到 AWS IoT MQTT 代理。

2. 演示使用 corePKCS11创建和存储新的密钥对和证书文件。这些凭据
   之后将用于预置新的 AWS IoT 事物。

3. 调用 [CreateCertificateWithCsr MQTT API](https://docs.aws.amazon.com/iot/latest/developerguide/fleet-provision-api.html#create-cert-csr)
   提出证书签名请求 (CSR)，以便 AWS IoT 确认并签署
   证书。

4. 调用 [RegisterThing MQTT API](https://docs.aws.amazon.com/iot/latest/developerguide/fleet-provision-api.html#register-thing)
   创建新的，且使用密钥对和新签名证书的 AWS IoT 事物。

5. 预置新事物后，演示将断开与 AWS IoT MQTT 代理的连接。

6. 演示使用新创建的事物凭据连接到 AWS IoT MQTT 代理，以验证
   该事物是否已成功注册。


`prvFleetProvisioningTask()` 函数的源代码可在
GitHub 上的 [FleetProvisioningDemoExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Fleet_Provisioning_Windows_Simulator/CSR_Demo/FleetProvisioningDemoExample.c)
文件中找到。

下列屏幕截图显示了演示正确执行时的预期输出：

[![演示成功](/media/2021/fleet_provisioning.png)](/media/2021/fleet_provisioning.png)
