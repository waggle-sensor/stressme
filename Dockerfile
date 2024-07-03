FROM nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3

COPY . .

RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/cross-linux-sbsa/3bf863cc.pub
RUN apt-get update
RUN apt-get install stress-ng --yes

ENTRYPOINT [ "python3", "controller.py" ]