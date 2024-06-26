# Stress Me

# Developer notes
## Jetpack 5.0 support
In JetPack 5.x we need to change the base container image to [l4t Pytorch](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-pytorch/tags) because the JetPack expects containers to hold libraries. [The reference](https://forums.developer.nvidia.com/t/missing-cuda-csv-cudnn-csv-tensorrt-csv-in-etc-nvidia-container-runtime-host-files-for-container-d/240831/2)
