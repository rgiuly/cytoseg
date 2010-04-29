#!/bin/bash

Num_of_processors=2

#mpirun -np $Num_of_processors python machine_learning_command.py /home/demo/data/machine_learning_tutorial/b /home/demo/data/machine_learning_tutorial/a /home/demo/data/machine_learning_tutorial/a_membranes /home/demo/temp /home/demo/temp

mpirun -np $Num_of_processors python sbfsem_batch_mpi.py /home/demo/data/neuropil-read-only/input/40x40 /home/demo/data/neuropil-read-only/data/40x40 /home/demo/data/neuropil-read-only/seg/40x40 /home/demo/temp /home/demo/temp

