FROM waggle/plugin-base:1.1.1-ml

COPY . .

RUN rm /etc/apt/sources.list.d/cuda.list && apt-key del 7fa2af80 && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/cross-linux-sbsa/3bf863cc.pub
RUN apt-get update
RUN apt-get install stress-ng

ENTRYPOINT [ "python3", "controller.py" ]