#!/usr/bin/env bash

set -e

echo "\n\tBy default, install openCV4.6.0 with CUDA, please make sure you have enlarged memory swap before running this script\n"
#sleep(2)
sudo apt update

echo "\n\tSet CUDA location\n"
sudo sh -c "echo '/usr/local/cuda/lib64' >> /etc/ld.so.conf.d/nvidia-tegra.conf"
sudo ldconfig

echo "\n\tInstall dependencies\n"

echo "Are you using default Jetpack Python version ? "
read -p "y/n " ans
case ${ans} in
    [Nn]* ) 
        sudo -H python3.8 -m pip install numpy --upgrade numpy
        sudo apt-get install -y build-essential cmake git unzip pkg-config zlib1g-dev && \
        sudo apt-get install -y libjpeg-dev libjpeg8-dev libjpeg-turbo8-dev libpng-dev libtiff-dev && \
        sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libglew-dev && \
        sudo apt-get install -y libgtk2.0-dev libgtk-3-dev libcanberra-gtk* && \
        sudo apt-get install -y python-dev python-numpy python-pip && \
        sudo apt-get install -y python3-dev python3-numpy python3-pip && \
        sudo apt-get install -y libxvidcore-dev libx264-dev libgtk-3-dev && \
        sudo apt-get install -y libtbb2 libtbb-dev libdc1394-22-dev libxine2-dev && \
        sudo apt-get install -y gstreamer1.0-tools libv4l-dev v4l-utils v4l2ucp  qv4l2 && \
        sudo apt-get install -y libgstreamer-plugins-base1.0-dev libgstreamer-plugins-good1.0-dev && \
        sudo apt-get install -y libavresample-dev libvorbis-dev libxine2-dev libtesseract-dev && \
        sudo apt-get install -y libfaac-dev libmp3lame-dev libtheora-dev libpostproc-dev && \
        sudo apt-get install -y libopencore-amrnb-dev libopencore-amrwb-dev && \
        sudo apt-get install -y libopenblas-dev libatlas-base-dev libblas-dev && \
        sudo apt-get install -y liblapack-dev liblapacke-dev libeigen3-dev gfortran && \
        sudo apt-get install -y libhdf5-dev protobuf-compiler nano && \
        sudo apt-get install -y libprotobuf-dev libgoogle-glog-dev libgflags-dev
        ;;
    * ) echo "Please answer yes or no." ;;
esac

free -m
cd $HOME

echo -e "\n\tDownloading openCV4.6.0\n"
cd ~
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.6.0.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.6.0.zip
unzip opencv.zip
unzip opencv_contrib.zip
mv opencv-4.6.0 opencv
mv opencv_contrib-4.6.0 opencv_contrib

echo -e "\n\tBuild\n"
cd ~/opencv
mkdir build
cd build

echo -e "\n\tCmake, you may have to change flags\n"
cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
-D EIGEN_INCLUDE_PATH=/usr/include/eigen3 \
-D WITH_OPENCL=OFF \
-D WITH_CUDA=ON \
-D CUDA_ARCH_BIN=5.3 \
-D CUDA_ARCH_PTX="" \
-D WITH_CUDNN=ON \
-D WITH_CUBLAS=ON \
-D ENABLE_FAST_MATH=ON \
-D CUDA_FAST_MATH=ON \
-D OPENCV_DNN_CUDA=ON \
-D ENABLE_NEON=ON \
-D WITH_QT=OFF \
-D WITH_OPENMP=ON \
-D BUILD_TIFF=ON \
-D WITH_FFMPEG=ON \
-D WITH_GSTREAMER=ON \
-D WITH_TBB=ON \
-D BUILD_TBB=ON \
-D BUILD_TESTS=OFF \
-D WITH_EIGEN=ON \
-D WITH_V4L=ON \
-D WITH_LIBV4L=ON \
-D OPENCV_ENABLE_NONFREE=ON \
-D INSTALL_C_EXAMPLES=OFF \
-D INSTALL_PYTHON_EXAMPLES=OFF \
-D BUILD_opencv_python3=ON \
-D BUILD_opencv_python2=OFF \
-D PYTHON3_EXECUTABLE=/usr/local/bin/python3.8 \
-D PYTHON3_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
-D OPENCV_GENERATE_PKGCONFIG=ON \
-D BUILD_EXAMPLES=OFF ..

