import os
#PATH=\home\demo\bin:\usr\local\cglX\bin\:\home\demo\epd-6.1-1-rh5-x86_64\bin:$PATH
#LD_LIBRARY_PATH=$SAGE_DIRECTORY\lib:\usr\local\cglX\lib\:\usr\local\lib64:\usr\local\lib:\home\demo\epd-6.1-1-rh5-x86_64\lib\python2.6\site-packages\orange:\home\demo\epd-6.1-1-rh5-x86_64\lib\:$LD_LIBRARY_PATH
#.\RUN_MPI_sample.sh
os.system(r"python ..\sbfsem_batch_mpi.py o:\images\neuropil\data o:\images\neuropil\data o:\images\neuropil\seg o:\temp o:\temp sbfsem_settings1.py")
