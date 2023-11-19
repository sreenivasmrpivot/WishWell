# Environment Setup on Ubuntu

## Nvidia GPU Driver and CUDA details

* Check the Nvidia driver version
    ``` zsh
    nvidia-smi
    ```
  To see something like this
    ``` zsh
    +-------------------------------------------------------------------------------+
    | NVIDIA-SMI 525.105.17    Driver Version: 525.105.17    CUDA Version: 12.0     |
    |-------------------------------+----------------------+------------------------+
    | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
    |                               |                      |               MIG M. |
    |===============================+======================+======================|
    |   0  GeForce RTX 3090    Off  | 00000000:01:00.0 Off |                  N/A |
    |  0%   46C    P8    32W / 350W |      0MiB / 24268MiB |      0%      Default |
    |                               |                      |                  N/A |
    +-------------------------------+----------------------+----------------------+
    |   1  GeForce RTX 3090    Off  | 00000000:02:00.0 Off |                  N/A |
    |  0%   46C    P8    32W / 350W |      0MiB / 24268MiB |      0%      Default |
    |                               |                      |                  N/A |
    +-------------------------------+----------------------+----------------------+
    |   2  GeForce RTX 3090    Off  | 00000000:03:00.0 Off |                  N/A |
    |  0%   46C    P8    32W / 350W |      0MiB / 24268MiB |      0%      Default |
    |                               |                      |                  N/A |
    +-------------------------------+----------------------+----------------------+
    |   3  GeForce RTX 3090    Off  | 00000000:04:00.0 Off |                  N/A |
    |  0%   46C    P8    32W / 350W |      0MiB / 24268MiB |      0%      Default |
    |                               |                      |                  N/A |
    +-------------------------------+----------------------+----------------------+
    |

## Install Nvidia Container Toolkit

* Add the package repositories
    ``` zsh
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
    ```
* Install the toolkit
    ``` zsh
    sudo apt-get update
    sudo apt-get install -y nvidia-docker2
    sudo systemctl restart docker
    ```
* Test the installation
    ``` zsh
    sudo docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
    ```
* If the above command fails with the following error:
    ``` zsh
    docker: Error response from daemon: could not select device driver "" with capabilities: [[gpu]].
    ERRO[0000] error waiting for container: context canceled 
    ```
    then try the following:
    ``` zsh
    sudo apt-get install nvidia-container-toolkit
    sudo systemctl restart docker
    ```
    and then test the installation again.
* Configure Docker to use NVIDIA Container Toolkit
    ``` zsh
    sudo vim /etc/docker/daemon.json
    ```
    and add the following lines:
    ``` zsh
    {
        "default-runtime": "nvidia",
        "runtimes": {
            "nvidia": {
                "path": "/usr/bin/nvidia-container-runtime",
                "runtimeArgs": []
            }
        }
    }

    or

    {
        "runtimes": {
            "nvidia": {
                "path": "nvidia-container-runtime",
                "runtimeArgs": []
            }
        },
        "default-runtime": "nvidia"
    }
    ```
    then restart docker
    ``` zsh
    sudo systemctl restart docker
    ```
* Test the installation
    ``` zsh
    sudo docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
    ```
## Install curl

* Install curl if not already installed
    ``` zsh
    sudo apt-get install curl
    ```

## Install docker

* Install docker if not already installed
    ``` zsh
    sudo apt-get update
    sudo apt-get install docker.io
    ```
* Login to docker using your credentials, if you don't have an account, create one at [Docker](https://hub.docker.com/).
    ``` zsh
    sudo docker login
    ```
    else you may get the following error:
    ``` zsh
    docker: Error response from daemon: toomanyrequests: You have reached your pull rate limit. You may increase the limit by authenticating and upgrading: https://www.docker.com/increase-rate-limit.
    See 'docker run --help'.
    ```

## Install docker-compose

* Install docker-compose if not already installed
    ``` zsh
    sudo apt-get install docker-compose
    ```
* If this method doesn't work, try the following:
    ``` zsh
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    ```
* Apply executable permissions to the binary:
    ``` zsh
    sudo chmod +x /usr/local/bin/docker-compose
    ```
* Test the installation.
    ``` zsh
    docker-compose --version
    ```

## Install Milvus

* Create a directory named `milvus` and enter it.
    ``` zsh
    mkdir milvus && cd milvus
    ```
* Download the `docker-compose.yml` file as per Milvus Standalone instructions from [Milvus](https://milvus.io/docs/install_standalone-gpu-docker.md).
    ``` zsh 
    wget https://github.com/milvus-io/milvus/releases/download/v2.3.3/milvus-standalone-docker-compose-gpu.yml -O docker-compose.yml
    ```
* Assign a single GPU device to Milvus as per the instructions from [Milvus](https://milvus.io/docs/install_standalone-gpu-docker.md).
    ``` zsh
    ``` yaml
      standalone:
    container_name: milvus-standalone
    image: milvusdb/milvus:v2.3.3-gpu
    command: ["milvus", "run", "standalone"]
    security_opt:
    - seccomp:unconfined
    environment:
      ETCD_ENDPOINTS: etcd:2379
      MINIO_ADDRESS: minio:9000
      KNOWHERE_GPU_MEM_POOL_SIZE: 2048;4096
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/milvus:/var/lib/milvus
    ports:
      - "19530:19530"
      - "9091:9091"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              capabilities: [gpu]
              device_ids: ['0']
    ```
* Start Milvus
    ``` zsh
    sudo docker-compose up -d
    ```
* Check the status of Milvus
    ``` zsh
    sudo docker-compose ps
    ```
  To see something like this:
    ``` zsh
    NAME                IMAGE                                      COMMAND                  SERVICE      CREATED        STATUS                  PORTS
    -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    milvus-etcd         quay.io/coreos/etcd:v3.5.5                 "etcd -advertise-cli…"   etcd         22 hours ago   Up 10 hours (healthy)   2379-2380/tcp
    milvus-minio        minio/minio:RELEASE.2022-03-17T06-34-49Z   "/usr/bin/docker-ent…"   minio        22 hours ago   Up 10 hours (healthy)   0.0.0.0:9000-9001->9000-9001/tcp, :::9000-9001->9000-9001/tcp
    milvus-standalone   milvusdb/milvus:v2.3.3-gpu                 "/tini -- milvus run…"   standalone   22 hours ago   Up 10 hours             0.0.0.0:9091->9091/tcp, :::9091->9091/tcp, 0.0.0.0:19530->19530/tcp, :::19530->19530/tcp
    ```
* Make GPU device 0 visible to Milvus:

    ``` zsh
    sudo docker update --device-add=0 milvus-standalone
    ```