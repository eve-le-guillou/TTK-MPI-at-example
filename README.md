# TTK-MPI-at-example
This github repository contains the exact code used to reproduce the AT example.

## Prerequisites

Hardware?

## Installation Notes

Tested on Ubuntu 22.04.2 LTS.

### Install the dependencies

    sudo apt update
    sudo apt install g++ git
    sudo apt-get install cmake-qt-gui libboost-system-dev libopengl-dev qttools5-dev libqt5x11extras5-dev libqt5svg5-dev qtxmlpatterns5-dev-tools 
    sudo apt install python3-dev libopenmpi-dev

### Install Paraview

    git clone https://github.com/topology-tool-kit/ttk-paraview.git
    cd ttk-paraview
    git checkout 5.11.0
    mkdir build && cd build
    cmake -DCMAKE_BUILD_TYPE=Release -DPARAVIEW_USE_PYTHON=ON -DPARAVIEW_USE_MPI=ON -DPARAVIEW_INSTALL_DEVELOPMENT_FILES=ON -DCMAKE_INSTALL_PREFIX=../install ..
    make -j4 install

 ### Install TTK

    cd ttk-1.2.0
    mkdir build && cd build
    PARAVIEW_PATH=~/ttk-paraview/install/lib/cmake/paraview-5.11
    cmake -DParaView_DIR=$PARAVIEW_PATH -DTTK_ENABLE_MPI=ON -DTTK_ENABLE_MPI_TIME=ON -DCMAKE_INSTALL_PREFIX=../install .. 
    make -j4 install

### Run the example

By default, the example is resampled to 512.

    OMP_NUM_THREADS=4 mpirun -n 4 pvbatch pipeline.py

