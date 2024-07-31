# Stress Me

This is a program for general purpose variable stress testing.
We used this to gather performance data in the design of a system model and edge computing dataset.

## Theoratical Viewpoint

### What is a program?

We can think about a program as a black box. Within the problem space of metrics gathering, we can think about this program as a time-series set of resources usages Ri where each set corresponds to a time ti. Now, to represent any program, we let this set of resources R vary within the space of available resources. Finally, to simulate all possible programs, we can vary the length of ti and the set Ri randomly.

### How is this tool built?
To simulate a program, we use existing stress tools to vary the load on the system. We take the tools

- stressng: a tool for stressing cpu
- gpu-stress-test: a Waggle tool for stressing gpu

and combine them into a variable stress program that we call stressme.

## How to use this tool?
To run this tool, we provide a docker image that is located [here](https://hub.docker.com/r/waggle/stressme).
We run this docker image using Kubernetes and the NVIDIA container runtime. 
For information about flags, see the table below

| Flag | Type | Description |
|-|-|-|
| -n, --num-programs | int | Number of distinct stress programs |
| -t, --max-time | int | Maximum time for running (seconds) |
| --cpu | int | Number of CPU cores to use |
| --cpu-stress | int | Maximum CPU stress level (percentage) |
| --min-gpu-timeout | float | Minimum GPU timeout (seconds) |
| --max-gpu-timeout | float | Maximum GPU timeout (seconds) |
| --random | boolean | Enables randomization in resource selection |
| --enable-gpu | boolean | Enables GPU stressing |
