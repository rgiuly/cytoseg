#!/bin/bash

Num_of_processors=20

#mpirun -np $Num_of_processors python machine_learning_command.py /home/demo/data/machine_learning_tutorial/b /home/demo/data/machine_learning_tutorial/a /home/demo/data/machine_learning_tutorial/a_membranes /home/demo/temp /home/demo/temp

mpirun -np $Num_of_processors python sbfsem_batch_mpi.py /home/demo/data/neuropil-read-only/input /home/demo/data/neuropil-read-only/data /home/demo/data/neuropil-read-only/seg /home/demo/temp /mnt/disk2/data/cytoseg_data

