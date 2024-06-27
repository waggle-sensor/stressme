FROM http://nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3

COPY . .

RUN apt-get update
RUN apt-get install stress-ng

ENTRYPOINT [ "python3", "controller.py" ]