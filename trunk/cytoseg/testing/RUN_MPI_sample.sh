#!/bin/bash

Num_of_processors=2

#mpirun -np $Num_of_processors python machine_learning_command.py /home/rsingh/data/machine_learning_tutorial/b /home/rsingh/data/machine_learning_tutorial/a /home/rsingh/data/machine_learning_tutorial/a_membranes /home/rsingh/temp /home/rsingh/temp

mpirun -np $Num_of_processors python sbfsem_batch_mpi.py 
