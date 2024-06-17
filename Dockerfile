FROM waggle/plugin-base:1.1.1-ml

COPY . .

RUN sudo apt-key del 7fa2af80 && 
    \ wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/cross-linux-sbsa/cuda-keyring_1.0-1_all.deb && 
    \ sudo dpkg -i cuda-keyring_1.0-1_all.deb
RUN apt-get update
RUN apt-get install stress-ng

ENTRYPOINT [ "python3", "controller.py" ]