# TTK-MPI-at-example
This github repository contains the exact code used to reproduce the AT example.

## Prerequisites

Hardware?

## Installation Notes

Tested on Ubuntu 22.04.2 LTS.

### Install the dependencies

    sudo apt update
    sudo apt install g++ git cmake-qt-gui libboost-system-dev libopengl-dev qttools5-dev libqt5x11extras5-dev libqt5svg5-dev qtxmlpatterns5-dev-tools python3-dev libopenmpi-dev

### Install Paraview

    cd ~
    git clone https://github.com/topology-tool-kit/ttk-paraview.git
    cd ttk-paraview
    git checkout 5.11.0
    mkdir build && cd build
    cmake -DCMAKE_BUILD_TYPE=Release -DPARAVIEW_USE_PYTHON=ON -DPARAVIEW_USE_MPI=ON -DPARAVIEW_INSTALL_DEVELOPMENT_FILES=ON -DCMAKE_INSTALL_PREFIX=../install ..
    make -j4 install

 ### Install TTK using this repository

    cd ~
    git clone https://github.com/eve-le-guillou/TTK-MPI-at-example.git
    cd ~/TTK-MPI-at-example/ttk-1.2.0
    mkdir build && cd build
    PARAVIEW_PATH=~/ttk-paraview/install/lib/cmake/paraview-5.11
    cmake -DParaView_DIR=$PARAVIEW_PATH -DTTK_ENABLE_MPI=ON -DTTK_ENABLE_MPI_TIME=ON -DCMAKE_INSTALL_PREFIX=../install .. 
    make -j4 install

### Update environment variables

    TTK_PREFIX=~/TTK-MPI-at-example/ttk-1.2.0/install
    export PV_PLUGIN_PATH=$TTK_PREFIX/bin/plugins/TopologyToolKit
    export LD_LIBRARY_PATH=$TTK_PREFIX/lib:$LD_LIBRARY_PATH
    export PYTHONPATH=$TTK_PREFIX/lib/python3.10/site-packages

### Run the example

By default, the example is resampled to 256.

    OMP_NUM_THREADS=4 mpirun -n 4 pvbatch pipeline.py

The output image can be shown using the following command:

    eog atExample.jpeg