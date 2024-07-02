import random
import stress_cpu
import stress_gpu
import os
import sys
import argparse

"""
Represents the resources used in a given program

Here we generate the resources randomly in order to simulate the black box
nature of a random program
"""
class RandomResource:
    def __init__(self, num_cores, max_stress, min_gpu_timeout, max_gpu_timeout):
        self.cpu_cores = random.randrange(num_cores)
        self.cpu_stress = random.randrange(max_stress)
        self.gpu_stress_timeout = random.random() * (max_gpu_timeout - min_gpu_timeout) + min_gpu_timeout

    def __str__(self):
        "CPU Cores: {}; CPU Stress: {}; GPU Timeout: {}".format(self.cpu_cores, self.cpu_stress, self.gpu_stress_timeout)

"""
Represents the resources used in a given program

Here we generate the resources deterministically to purposely generate 
testable data
"""
class DeterministicResource:
    def __init__(self, num_cores, max_stress, min_gpu_timeout, max_gpu_timeout, num_programs, i):
        self.cpu_cores = num_cores
        self.cpu_stress = max_stress / num_programs * i
        self.gpu_stress_timeout = (max_gpu_timeout - min_gpu_timeout) / num_programs * i + min_gpu_timeout

    def __str__(self):
        "CPU Cores: {}; CPU Stress: {}; GPU Timeout: {}".format(self.cpu_cores, self.cpu_stress, self.gpu_stress_timeout)

"""
Represents a program simulation that stresses resources at random amounts
over a period of time
"""
class ProgramSim:
    def __init__(self, max_num_programs, max_seconds, num_cores, max_stress, max_gpu_timeout, min_gpu_timeout, random, enable_gpu):
        self.enable_gpu = enable_gpu

        if random:
            random.seed()
            self.number = random.randrange(1, max_num_programs)
            max_time = max_seconds / self.number
            self.times = [random.random() * max_time + 1 for _ in range(self.number)]
            self.resources = [RandomResource(num_cores, 
                                             max_stress, 
                                             max_gpu_timeout, 
                                             min_gpu_timeout) for _ in range(self.number)]
        else:
            self.number = max_num_programs
            time = max_seconds / self.number
            self.times = [time] * self.number
            self.resources = [DeterministicResource(num_cores, 
                                                    max_stress, 
                                                    max_gpu_timeout, 
                                                    min_gpu_timeout, 
                                                    self.number, 
                                                    i) for i in range(self.number)]

        print("Running {} programs with the following resources: \n\t Times: {} \n\t Resources: {}".format(self.number, self.times, self.resources))

    def simulate(self):
        """
        Simulates the program by running each step at the given stress levels
        for a given amount of time
        """
        for i in range(self.number):
            print("Simulating program {}".format(i))

            r = self.resources[i]
            t = self.times[i]
            
            # start stressing
            pids = [
                stress_cpu.StressCPU(r.cpu_cores, r.cpu_stress, t).stress(), 
            ]

            if self.enable_gpu:
                pids.append(stress_gpu.StressGPU(r.gpu_stress_timeout, t, 16 * 1024 ** 2).stress())

            # wait until processes end
            for pid in pids:
                os.waitid(os.P_PID, pid, os.WEXITED)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    # max num programs
    parser.add_argument(
        "-n",
        "--num-programs",
        default=10,
        type=int,
        help="Number of distinct stress programs"
    )
    
    # max time
    parser.add_argument(
        "-t",
        "--max-time",
        default=120,
        type=int,
        help="Maximum time for running"
    )

    # num cores
    parser.add_argument(
        "--cpu",
        default=2,
        type=int,
        help="Number of CPU cores to use"
    )

    # cpu stress
    parser.add_argument(
        "--cpu-stress",
        default=50,
        type=int,
        help="Maximum CPU stress level"
    )

    # min gpu timeout
    parser.add_argument(
        "--min-gpu-timeout",
        default=0.1,
        type=float,
        help="Minimum GPU timeout"
    )

    # max gpu timeout
    parser.add_argument(
        "--max-gpu-timeout",
        default=0.1,
        type=float,
        help="Maximum GPU timeout"
    )

    parser.add_argument(
        "--random",
        action = "store_true",
        help="Whether to enable randomness"
    )

    parser.add_argument(
        "--enable-gpu",
        action = "store_true",
        help="Whether to enable gpu"
    )
    
    args = parser.parse_args()
    if args.min_gpu_timeout > args.max_gpu_timeout:
        print("MIN GPU timeout must be smaller than MAX GPU timeout")
        sys.exit(os.EX_DATAERR)

    print("Running with args: \n\t-n: {} \n\t-t: {} \n\t--cpu: {} \n\t--cpu-stress: {} \n\t--min-gpu-timeout: {} \n\t--max-gpu-timeout: {}"
          .format(
            args.num_programs, 
            args.max_time, 
            args.cpu, 
            args.cpu_stress, 
            args.min_gpu_timeout, 
            args.max_gpu_timeout))
    
    print("Randomness enabled: {}".format(args.random))
    print("GPU Enabled: {}".format(args.enable_gpu))

    ProgramSim(args.num_programs, 
               args.max_time, 
               args.cpu, 
               args.cpu_stress, 
               args.min_gpu_timeout, 
               args.max_gpu_timeout,
               args.random,
               args.enable_gpu).simulate()
