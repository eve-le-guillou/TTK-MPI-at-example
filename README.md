# TTK-MPI-at-example
This github repository contains the exact code used to reproduce the AT example in the reference below.

## Reference

If you plan to use this code to generate results for a scientific document, thanks for referencing the following publication:

"TTK is Getting MPI-Ready"
Eve Le Guillou, Michael Will, Pierre Guillou, Jonas Lukasczyk, Pierre Fortin, Chistoph Garth, Julien Tierny

## Installation Notes

Tested on Ubuntu 22.04.2 LTS.

### Install the dependencies

To install the dependencies, run the following commands:

    sudo apt update
    sudo apt install g++ git cmake-qt-gui libboost-system-dev libopengl-dev qttools5-dev libqt5x11extras5-dev libqt5svg5-dev qtxmlpatterns5-dev-tools python3-dev libopenmpi-dev

### Install Paraview

In the following command, replace the `4` in `make -j4 install` by the number of cores available.

    cd ~
    git clone https://github.com/topology-tool-kit/ttk-paraview.git
    cd ttk-paraview
    git checkout 5.11.0
    mkdir build && cd build
    cmake -DCMAKE_BUILD_TYPE=Release -DPARAVIEW_USE_PYTHON=ON -DPARAVIEW_USE_MPI=ON -DPARAVIEW_INSTALL_DEVELOPMENT_FILES=ON -DCMAKE_INSTALL_PREFIX=../install ..
    make -j4 install

 ### Install TTK using this repository

We will now install TTK using the repository on Github. Again, replace the `4` in `make -j4 install` by the number of cores available.

    cd ~
    git clone https://github.com/topology-tool-kit/ttk.git
    cd ttk
    git checkout 1.2.0
    mkdir build && cd build
    PARAVIEW_PATH=~/ttk-paraview/install/lib/cmake/paraview-5.11
    cmake -DParaView_DIR=$PARAVIEW_PATH -DTTK_ENABLE_MPI=ON -DTTK_ENABLE_MPI_TIME=ON 
    -DTTK_ENABLE_64BITS_IDS=ON -DCMAKE_INSTALL_PREFIX=../install .. 
    make -j4 install

### Update environment variables

TTK is now installed, but needs an update of the environment variables to be called easily in the command line.

    export PATH=$PATH:~/ttk-paraview/install/bin/
    TTK_PREFIX=~/TTK-MPI-at-example/ttk-1.2.0/install
    export PV_PLUGIN_PATH=$TTK_PREFIX/bin/plugins/TopologyToolKit
    export LD_LIBRARY_PATH=$TTK_PREFIX/lib:$LD_LIBRARY_PATH
    export PYTHONPATH=$TTK_PREFIX/lib/python3.10/site-packages

### Run the example

By default, the example is resampled to $256^3$. To execute it using 2 threads and 4 processes, use the following command:

    OMP_NUM_THREADS=2 mpirun -n 4 pvbatch pipeline.py

We advise, for better performance, to have at most as many processes $p$ as there are physical cores on the system. For the thread number $t$, we advise to choose $t$ such that $t \times p$ is at most equal to the number of logical cores on the system.

Furthermore, the default placing of processes and threads on the computing cores and nodes may not be the best and may result in poor performance, particularly when the chosen number of threads is close to the total number of logical cores.

Here is the configuration used to produce the results in the reference paper:

    OMP_PLACES=cores OMP_PROC_BIND=close OMP_NUM_THREADS=2 mpirun --bind-to none --map-by node -n 4 pvbatch pipeline.py

Please note that this configuration may **not** be adapted to your CPU architecture, your OpenMP version or OpenMPI version. It is only a suggestion. To find the adapted configuration for you, please refer to the documentation of OpenMPI and OpenMP.


If you want to resample to a higher dimension, for example $2048^3$ as in the reference paper, it can simply be done by executing the following command:

    OMP_NUM_THREADS=2 mpirun -n 4 pvbatch pipeline.py 2048

Be aware that this will require a lot of memory to execute and will most likely not be possible on a regular laptop.

The command will create the following image and output the execution time of data loading and resampling, the pipeline and the creation of the output image. Depending on the dimension of the resample for the execution, the result may contain some resampling artifacts.

![output image](atExample.jpeg)