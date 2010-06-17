#!/bin/bash

Num_of_processors=10

#mpirun -np $Num_of_processors python machine_learning_command.py /home/rsingh/data/machine_learning_tutorial/b /home/rsingh/data/machine_learning_tutorial/a /home/rsingh/data/machine_learning_tutorial/a_membranes /home/rsingh/temp /home/rsingh/temp

#mpirun -np $Num_of_processors python sbfsem_batch_mpi.py 

mpirun -np $Num_of_processors python ../sbfsem_batch_mpi.py /home/demo/data/neuropil-read-only/data /home/demo/data/neuropil-read-only/data /home/demo/data/neuropil-read-only/seg /home/demo/temp /mnt/disk2/data/cytoseg_data sbfsem_settings1.py
