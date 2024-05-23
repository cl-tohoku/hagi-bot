# Dialogue System Live Competition Setup

## Recommended Environment

### General Developers

- Windows 11
- CUDA 12.1

### SUNABA Developers

- Windows 11

## Directory Structure Requirements

Please ensure the downloaded software follows the structure below. `start.bat` will not work correctly if this structure is not maintained.

```
-- AmazonPollyServer/
|   |- config/
|   |- docs/
|   |- 00-launch-AmazonPollyServer.bat
|   |- ...
|- CGEricaSet/
|   |- 01-OculusLipSync/
|   |- 02-CGErica/
|   |- 03-MiracleErica/
|   |- 04-JointMapper/
|- dslc6/
|   |- dslclib/
|   |   |- ...
|   |- dockerfile
|   |- sample.py
|- FaceRecognitionServer/
|   |- face_recognition_server.pyz
|   |- ...
|- WebSocketBridge2/
|   |- Launcher2-TCPClient.bat
|   |- ...
|- installer.bat
|- README.md
|- start.bat

```

## Setup Procedure

### Enabling WSL2 (**Not Mandatory**)

Some may prefer development in UNIX-like environments.

In such cases, you can enable WSL2 and develop in an Ubuntu environment using `wsl -d Ubuntu`.

There are also articles suggesting that GPU operations via WSL may be faster than on Windows. Those who wish to train models might benefit from using the distributed Docker container on WSL.

[Reference Article](https://www.kagoya.jp/howto/cloud/container/wsl2_docker/)

[Potential Pitfalls](https://zenn.dev/ohno/articles/1cb49d190af1f4)

**Be sure to perform the following in Windows Powershell with administrator rights!!**

```bash
$ wsl --set-default-version 2
$ wsl --install

```

If using the Ubuntu distribution, you can start it as follows:

```bash
$ wsl -d Ubuntu

```

### Installation

For simplified setup, a batch file `installer.bat` has been created.

To use `installer.bat`, enter the following command in the **Command Prompt** (do not include the `$`):

```
$ installer.bat

```

The following setup steps will be performed in sequence. Note that this is not a fully automated process, and you may need to perform some steps manually.
Also, be aware that the software to be installed may conflict with existing installations.

`installer.bat` will check if the target software is already installed before proceeding. If found, the installation process for that software will be skipped.

Software to be installed:

1. Java
2. Voicemeeter Banana
3. Python3.10.11
4. Docker for Windows

If you choose not to use `installer.bat`, please follow the setup steps outlined in the Dialogue System Live Competition 5 website.

## How to Start (Running Sample Code)

Running `start.bat` will sequentially launch all required applications.

After `start.bat` completes execution, start Docker and then launch the echo dialogue system.

The sequence for running the sample program is as follows.

### Command Prompt 1

```
$ start.bat

AmazonPollyServer will be launched.
AmazonPollyServer has been launched.
Press any key to continue . . .
CGErica will be launched.
    OculusLipSync will be launched.
Press any key to continue . . .
    CGErica will be launched.
Press any key to continue . . .
    MiracleErica will be launched.
Press any key to continue . . .
    JointMapper will be launched.
CGErica has been launched.
Press any key to continue . . .
FaceRecognitionServer will be launched.
FaceRecognitionServer has been launched.
Press any key to continue . . .
TCPSocketBridge2 will be launched.
TCPSocketBridge2 has been launched.
Google Speech API will be launched. Press connect to start socket communication.
Press any key to continue . . .

$

```

Follow the instructions to launch each application in sequence. **Launching them in order is crucial** (especially CGErica).

Since each application is launched individually, make sure to confirm each launch before pressing a key to start the next application.

**This should only be done once.**

### Command Prompt 2

```
$ docker build dslc6 -t dslc6

```

First, build the Docker image.
By specifying `-t dslc6`, the created image is named `dslc6`, making it easier to find the image you want to launch.

```
$ docker run --add-host="host.docker.internal:host-gateway" --rm -it dslc6

```

By running `docker run dslc6`, the image created as `dslc6` is used to start the Docker container.

- -`rm` is an option that automatically deletes the Docker container when you exit. Without this option, unnecessary containers will accumulate with each run.
- `it` allows you to enter the container. The sample program is set to launch a Python program simultaneously with the container startup.
While the program will run without `it`, it is recommended to enter the container to see how the program operates through standard output, etc.
- `add-host="host.docker.internal:host-gateway"` is **mandatory**. This is necessary for socket communication between the Docker container and the host port.
Handling this can be very cumbersome, so a Python library `dslclib` for the dialogue competition has been created. This library automatically detects whether it is inside a Docker container or on the host OS and sets the IP address accordingly.

Therefore, be sure to include `--add-host="host.docker.internal:host-gateway"`.

## How to Start (During Development)

The flow is almost the same as for running the sample code, but during development, you will want to interactively modify the code.
Therefore, the procedure is slightly adjusted to allow for more interactive development.

Running `start.bat` will sequentially launch all required applications.

After `start.bat` completes execution of all batch files, start Docker and then launch the echo dialogue system.

The overall flow remains unchanged. The Docker startup process is slightly modified.

The sequence for running the sample program is as follows.

### Command Prompt 1

```
$ start.bat

AmazonPollyServer will be launched.
AmazonPollyServer has been launched.
Press any key to continue . . .
CGErica will be launched.
    OculusLipSync will be launched.
Press any key to continue . . .
    CGErica will be launched.
Press any key to continue . . .
    MiracleErica will be launched.
Press any key to continue . . .
    JointMapper will be launched.
CGErica has been launched.
Press any key to continue . . .
FaceRecognitionServer will be launched.
FaceRecognitionServer has been launched.
Press any key to continue . . .
TCPSocketBridge2 will be launched.
TCPSocketBridge2 has been launched.
Google Speech API will be launched. Press connect to start socket communication.
Press any key to continue . . .

$

```

Follow the instructions to launch each application in sequence. **Launching them in order is crucial** (especially CGErica).

Since each application is launched individually, make sure to confirm each launch before pressing a key to start the next application.

**This should only be done once.**

### Command Prompt 2

```
$ docker build dslc6 -t dslc6

```

First, build the Docker image.
By specifying `-t dslc6`, the created image is named `dslc6`, making it easier to find the image you want to launch.

```
$ docker run --add-host="host.docker.internal:host-gateway" -v <absolute path of the development directory>:/home/ubuntu/<any directory name> --rm -it dslc6 /bin/bash

```

By running `docker run dslc6`, the image created as `dslc6` is used to start the Docker container.

- `--rm` is an option that automatically deletes the Docker container when you exit. Without this option, unnecessary containers will accumulate with each run.
- `-it` allows you to enter the container. The sample program is set to launch a Python program simultaneously with the container startup.
While the program will run without `it`, it is recommended to enter the container to see how the program operates through standard output, etc.
- `--add-host="host.docker.internal:host-gateway"` is **mandatory**. This is necessary for socket communication between the Docker container and the host port.
Handling this can be very cumbersome, so a Python library `dslclib` for the dialogue competition has been created. This library automatically detects whether it is inside a Docker container or on the host OS and sets the IP address accordingly.

Therefore, be sure to include `--add-host="host.docker.internal:host-gateway"`.

- **--- Differences from the previous instructions. -----**
- The `-v <absolute path of the development directory>:/home/ubuntu/<any directory name>` option mounts the development directory to the Docker container.
This allows changes made both on Docker and the host to be applied.
Eventually, you will need to copy this directory to Docker for submission, but during development, mounting the directory will allow for more comfortable development.

Specifying `/bin/bash` is to override the sample dialogue system call that starts upon container startup with `/bin/bash` to initiate shell operations.
You can modify the last line of the Dockerfile from `CMD [ "python3", "sample.py" ]` to `CMD [ "/bin/bash"]`, but those not confident with Docker operations can start development using the `docker run ...`