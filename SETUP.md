# Setup details

The following need to be installed in order to replicate setup

- CMake
- WxWidgets

## On Linux

The following instructions were documentated based on Ubuntu 20.04

### Step 1: Clone the repo

### Step 2: Install wxWidgets

Run the following command:

`sudo apt install libwxgtk3.0-gtk3-dev`

This will install the wxWidgets package on your machine


You will need to build mathplot:
1. `cd  <root of repo>`
2. `cd mathplot`
3. `cmake .`
4. `make`

Then, run the following instructions:
1. `cd  <root of repo>`
2. `mkdir build`
3. `cd build`
4. `cmake ..`
5. `make`




## On Windows

Make sure you have cpp compiler 


### TODO
Add proper citations
    -to get CMAKE working I referenced this website: https://www.pragmaticlinux.com/2021/08/getting-started-with-wxwidgets-on-linux/#google_vignette
    https://github.com/pragmaticlinuxblog/cmake_wxwidgets (MIT License so I think we do need to cite them in CMakeLists.txt)




