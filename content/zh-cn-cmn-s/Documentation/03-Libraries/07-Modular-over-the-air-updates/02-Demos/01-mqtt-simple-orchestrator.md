---
title: "OTA（使用简单 OTA Orchestrator）"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## 序言

虽然本演示使用 AWS IoT OTA 更新服务，但 FreeRTOS 是通用的 MIT 许可开源软件， 
可用于任何适合您的 OTA 机制。**然而，我们强烈建议，无论选择哪种 OTA 方法，最好对
固件进行数字签名。**这样一来，收到新的可执行映像的设备可以 
验证该固件来自授权来源，并且未经修改。您可以使用 AWS 
IoT 代码签名对固件进行签名，也可以使用您自己的代码签名工具进行签名。


## 演示简介

**简单 OTA Orchestrator：**此演示 Orchestrator 执行 OTA 更新的最小功能，即 
在 IoT Core 中检查 OTA 作业、下载固件文件， 
并向 IoT Core 报告完成情况。该简单 OTA Orchestrator 会在命令行打印 OTA 文件内容。该演示 
使用 FreeRTOS、coreMQTT、MQTT 文件流和 IoT 作业库

简单 OTA Orchestrator 代码分为 ota_demo.h 和 ota_demo.c 两个文件。这些文件可在 
[此处](https://github.com/FreeRTOS/Labs-Project-ota-example-for-aws-iot-core/tree/main/demo/simple-Ota-Orchestrator)找到。

此演示中有两项任务：OTA 任务和 MQTT 任务。

**OTA 任务**

该任务执行以下操作：

1. 检查是否有挂起的 OTA 作业。
2. 如果有挂起的 OTA 作业，则下载作业文档。该任务还会更新 AWS IoT Core 上的作业状态。
3. 解析下载的作业文档并提取下载新固件所需的参数。
4. 将提取的参数传递给 MQTT 流下载器进行初始化。
5. MQTT 文件流下载器请求数据块后，即可开始下载新固件。
6. 成功下载新固件后，它会将 AWS IoT Core 上的作业状态更新为 "SUCCESS"。


**MQTT 任务**

此任务负责运行 MQTT 进程循环，处理所有传入的 MQTT 消息。


## 演示设置

### 设置 AWS IoT Core

要设置 AWS IoT Core，请遵循 
[AWS IoT Core 设置指南](https://github.com/FreeRTOS/Labs-Project-ota-example-for-aws-iot-core/blob/demo_refactor/docs/AWSSetup.md)。 
该指南介绍了如何注册 AWS 账户、创建用户以及向 AWS IoT 
Core 注册设备。按照 AWS IoT Core 设置指南中的说明生成以下实体：

1. 设备端点。
2. AWS IoT 事物（以及关联的 ThingName）。
3. PEM 编码的设备证书。
4. PEM 编码的私钥。
5. PEM 编码的根 CA 证书。

模拟器/设备需要实体才能与 AWS IoT Core 连接。


### 设置 OTA 云服务

+ S3 是一项 AWS 服务，您可以利用该服务将文件存储在云端， 
  您或其他服务均可访问存储的文件。在将固件映像发送到设备之前，OTA Update Manager Service 使用 S3 将固件映像 
  存入 S3 “存储桶”中 
  。[创建 Amazon S3 存储桶，以存储更新](https://docs.aws.amazon.com/freertos/latest/userguide/dg-ota-bucket.html)。

+ 默认情况下，OTA Update Manager 无权访问包含固件映像的 S3 存储桶 
  。要想为 OTA Update Manager Service 授予 S3 存储桶的读写权限，必须设置 OTA 
  服务角色 
  。[创建 OTA 更新服务角色](https://docs.aws.amazon.com/freertos/latest/userguide/create-service-role.html)。

+ 需要 OTA 用户策略，授予您的账户与 AWS 服务交互的权限， 
  用于创建 OTA 
  更新。[创建 OTA 用户策略](https://docs.aws.amazon.com/freertos/latest/userguide/create-ota-user-policy.html)。

+ [创建代码签名证书](https://docs.aws.amazon.com/freertos/latest/userguide/ota-code-sign-cert-win.html)。

+ [授予 AWS IoT](https://docs.aws.amazon.com/freertos/latest/userguide/code-sign-policy.html) 代码签名的权限。


### 简化 OTA 设置向导

我们创建了一个[辅助向导](https://github.com/aws/simplify-ota-script/tree/main)以改善 
AWS IoT 和 OTA 体验。此脚本能够简化 IoT 事物和 OTA 作业的创建， 
还提供事物组管理功能。使用该向导时需要遵循的设置步骤 
与其他并无不同，它只给出连接到 AWS IoT 和处理 
创建任何必要 OTA 相关工具所需的全部信息提示。**我们强烈建议使用设置向导**， 
因为它既能缩短连接到 AWS IoT 生态系统的时间，又比手动设置更易于使用。


## 准备创建 OTA 更新作业

要发送 OTA 作业，需要更新存储在 S3 存储桶中的固件映像。AWS IoT OTA 
Manager 服务将从该存储桶中读取映像并将其发送到设备。

生产工作流程示例：

1. 编写 MCU 固件，集成 OTA 客户端库源代码。
2. 使用初始固件对设备硬件 (MCU) 进行编程。
3. 在本地更改和测试固件。
4. 为新版本的固件生成二进制文件。
5. 将新版本上传到 S3，并使用 OTA 作业将其发送至 MCU。


## 运行演示

### 构建并运行 OTA 演示项目

OTA 演示项目可在此处下载。点击此处查看构建项目的说明。在继续之前， 
请验证是否能够构建并运行该项目。


### 创建 OTA 更新作业

此时，您应该已经：

+ 使用 AWS IoT Service 创建 AWS IoT 事物。
+ 设置 S3 存储桶并管理各种服务的权限。
+ 将“更新”的固件映像上传到 S3 存储桶。
+ 完成代码签名所需的设置。
+ 配置在设备上运行的 OTA 客户端。

OTA 客户端运行且云服务设置完成后，接下来 
应创建 OTA 作业，向设备发送新的固件映像。首先，请转到 
[AWS IoT 控制台](https://console.aws.amazon.com/iot/home)。

1. 在 AWS IoT 控制台的导航窗格中，依次选择 **Manage** 和 **Jobs**。然后， 
   点击 **Create Job**。
   <br />
   ![](/media/2023/create-job.png)

2. 选择 **Create FreeRTOS OTA update job**，然后点击 **Next**。
   <br />
   ![](/media/2023/create-ota-update-job.png)

3. 在 **OTA job properties** 页面上，为 FreeRTOS OTA 更新作业输入 **Job name** 
   （例如，"ota_sim_update"）。您可以选择输入 **Description** 并为作业添加 **Tags**。 
   然后点击 **Next** 以继续。
   <br />
   ![](/media/2023/ota-job-properties.png)

4. 您可在单个设备或一组设备上部署 OTA 更新。在 **OTA file configuration** 页面的 
   **Devices to update** 下，选择与要更新的设备相关的事物或事物组 
   。在 **Select the protocol for file transfer** 下，选中 **MQTT** 旁边的复选框。
   <br />
   ![](/media/2023/ota-file-configuration-devices.png)

5. 在 **Sign and choose your file** 下，选中默认选项 **Sign a new file for me**。 
   在 **Code signing profile** 下，点击 **Create new profile** 按钮，该按钮位于 **Existing 
   code signing profile** 旁边。
   <br />
   ![](/media/2023/ota-file-configuration-sign-file.png)

6. 在 **Create a code signing profile** 页面的 **Profile name** 下，输入 "ota_codesigning"。 
   在 **Device hardware platform** 下，选择 "Windows Simulator"。在 **Code signing certificate** 下， 
   更改默认选项并选中 **Select an existing certificate** 复选框。在 **Certificates** 下， 
   选择之前生成的证书和证书私钥。如果是按照建议操作， 
   这些文件将命名为 "ecdsasigner.crt" 和 "ecdsasigner.key"。然后点击 **Import** 
   按钮。在 **Path name of code signing certificate on device** 下，输入刚导入的 "ecdsasigner.crt" 
   证书的路径。但是，演示时，应该在此处输入 "/" 作为路径。

   最后，点击 **Create** 按钮，创建代码签名配置文件。
   <br />
   ![](/media/2023/create-code-signing-profile.png)

7. 返回 **OTA file configuration** 页面，在 **File** 下，更改默认选项并选中 
   **Select an existing file** 复选框，然后点击 **Browse S3** 按钮，选择 
   在之前步骤中上传至 S3 的可执行文件。在 **Path name of file on device** 下，输入 "/"。此路径 
   是在 OTA 更新期间用来保存下载文件的位置 。注意：**文件类型**功能 
   在 [OTA 库 v2.0.0](https://github.com/aws/ota-for-aws-iot-embedded-sdk/tree/v2.0.0) 或更高版本中可用。
   <br />
   ![](/media/2023/ota-file-configuration-s3-upload.png)

8. 在 **IAM role** 下，选择为 OTA 流程创建的 IAM 角色。然后点击 **Next** 以继续。
   <br />
   ![](/media/2023/ota-file-configuration-iam.png)

9. 在 **OTA job configuration** 下，保留为 **Job run type**（快照）、 
   **Job start rollout configuration**（恒定速率）以及 **Job run timeout configuration**（无超时）等选择的默认设置。 
   然后点击 **Create job** 按钮以完成 OTA 更新作业的创建。
   <br />
   ![](/media/2023/ota-job-configuration.png)

10. 要监控作业状态，请点击 "**View Job**"，系统随即弹出一个窗口， 
   或者在 AWS IoT 控制台中导航到 **Manage &gt; Jobs**。设备成功下载映像之前，作业将显示为 "**IN PROGRESS**" 
   。
   <br />
   ![](/media/2023/Jobs_in_progress.png)
     


## 接收更新

创建作业后，设备即可开始下载更新。您可以在终端上 
监控下载进度。以下是控制台消息的示例：

```
  MQTT streams handling incoming message
  Incoming data block 
```

收到下载的最后一个块后，下列消息将被打印到监视器上：

```
  OTA Completed successfully!

```

作业进程完成后，IoT 控制台中的作业状态将从 "IN PROGRESS" 改为 "COMPLETED"。

<br />
![](/media/2023/Jobs_success.png)

