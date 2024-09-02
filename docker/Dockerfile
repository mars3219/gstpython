ARG UBUNTU_VERSION=ubuntu20.04
ARG CUDA_VERSION=11.8.0
FROM nvidia/cuda:${CUDA_VERSION}-cudnn8-devel-${UBUNTU_VERSION}

LABEL maintainer="H. S. Nam @ Gaonplatform Product2 <hsnam@gaonpf.com>"

ENV TRT_VERSION 8.6.1.6
ENV DEBIAN_FRONTEND=noninteractive
ENV TORCH_CUDA_ARCH_LIST="6.0 6.1 7.0 7.5 8.0 8.6+PTX" \
    TORCH_NVCC_FLAGS="-Xfatbin -compress-all" \
    CMAKE_PREFIX_PATH="$(dirname $(which conda))/../" \
    FORCE_CUDA="1"

ENV PATH=/opt/conda/bin:/usr/local/cuda:/usr/local/cuda-11.8/bin:$PATH
ENV LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH
ENV CUDA_HOME=/usr/local/cuda-11.8
ENV FORCE_CUDA="1"
ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libffi.so.7                            

COPY ./requirements.txt /

RUN apt-get update && \
    apt-get --no-install-recommends install -y gcc git wget curl zip htop tar vim openssl software-properties-common \
    python3 python3-pip python-is-python3 pip python3-distutils python3-typing-extensions build-essential python3-dev python3-wheel\
    libcurl4-openssl-dev libgl1 libglib2.0-0 libgl1-mesa-glx libpython3-dev gnupg libsm6 libxext6 libgtk2.0-dev pkg-config libssl-dev \
    pbzip2 pv bzip2 unzip devscripts lintian fakeroot dh-make && \
    cd /usr/local/bin && \
    ln -s /usr/bin/python3 python &&\
    ln -s /usr/bin/pip3 pip && \
    rm -rf /var/lib/apt/lists/*


RUN add-apt-repository ppa:ubuntu-toolchain-r/test

RUN apt-get update && \
    apt-get install -y \
        libcairo2-dev \
        libxt-dev \
        libgirepository1.0-dev && \
    pip install \
        pycairo && \
    apt-get install -y \
        libgstreamer1.0-dev \
        libgstrtspserver-1.0-dev \
        libgstreamer-plugins-base1.0-dev \
        libgstreamer-plugins-bad1.0-dev \
        gstreamer1.0-plugins-base \
        gstreamer1.0-plugins-good \
        gstreamer1.0-plugins-bad \
        gstreamer1.0-plugins-ugly \
        gstreamer1.0-libav \
        gstreamer1.0-tools \
        gstreamer1.0-x \
        gstreamer1.0-alsa \
        gstreamer1.0-gl \
        gstreamer1.0-gtk3 \
        gstreamer1.0-qt5 \
        gstreamer1.0-pulseaudio

# RUN wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
# RUN bash Anaconda3-2022.05-Linux-x86_64.sh -b -p /opt/conda
# RUN rm Anaconda3-2022.05-Linux-x86_64.sh
# ENV PATH /opt/conda/bin:$PATH
# RUN /opt/conda/bin/conda init && \
#     apt-get install -y python3.9
    # /opt/conda/bin/conda create -n gaonpf python=3.9


RUN pip3 install --upgrade pip
RUN pip3 install setuptools>=41.0.0

# SHELL [ "/bin/bash", "-c" ]
# RUN source /opt/conda/etc/profile.d/conda.sh && \
    # conda activate gaonpf && \
RUN pip install PyGObject && \
    pip install torch==2.0.0 torchvision==0.15.1 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cu118
    
    
RUN git clone https://github.com/mars3219/super-gradients.git && \
    cd ./super-gradients && \
    pip install --ignore-installed PyYAML && \
    pip install --no-cache-dir -e . && \
    cd ..
    # rm -rf ./super-gradients && \
    # pip install -qq super_gradients==3.5.0 && \
RUN pip install git+https://github.com/openai/CLIP.git --no-cache-dir && \
    pip install -r /requirements.txt && \
    git clone https://github.com/nvidia/TensorRT /TensorRT && \
    cd /TensorRT && git submodule update --init --recursive && \
    cd ./tools/pytorch-quantization && \
    pip install --no-cache-dir -e .

# install TensorRT
RUN if [ "${CUDA_VERSION}" = "10.2" ] ; then \
    v="${TRT_VERSION%.*}-1+cuda${CUDA_VERSION}" &&\
    apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub &&\
    apt-get update &&\
    apt-get install libnvinfer8=${v} libnvonnxparsers8=${v} libnvparsers8=${v} libnvinfer-plugin8=${v} \
        libnvinfer-dev=${v} libnvonnxparsers-dev=${v} libnvparsers-dev=${v} libnvinfer-plugin-dev=${v} \
        python3-libnvinfer=${v} libnvinfer-dispatch8=${v} libnvinfer-dispatch-dev=${v} libnvinfer-lean8=${v} \
        libnvinfer-lean-dev=${v} libnvinfer-vc-plugin8=${v} libnvinfer-vc-plugin-dev=${v} \
        libnvinfer-headers-dev=${v} libnvinfer-headers-plugin-dev=${v}; \
else \
    ver="${CUDA_VERSION%.*}" &&\
    if [ "${ver%.*}" = "12" ] ; then \
        ver="12.0"; \
    fi &&\
    v="${TRT_VERSION}-1+cuda${ver}" &&\
    apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub &&\
    apt-get update &&\
    apt-get -y install libnvinfer8=${v} libnvonnxparsers8=${v} libnvparsers8=${v} libnvinfer-plugin8=${v} \
        libnvinfer-dev=${v} libnvonnxparsers-dev=${v} libnvparsers-dev=${v} libnvinfer-plugin-dev=${v} \
        python3-libnvinfer=${v} libnvinfer-dispatch8=${v} libnvinfer-dispatch-dev=${v} libnvinfer-lean8=${v} \
        libnvinfer-lean-dev=${v} libnvinfer-vc-plugin8=${v} libnvinfer-vc-plugin-dev=${v} \
        libnvinfer-headers-dev=${v} libnvinfer-headers-plugin-dev=${v}; \
fi

# Install Cmake
RUN cd /tmp && \
    wget https://github.com/Kitware/CMake/releases/download/v3.14.4/cmake-3.14.4-Linux-x86_64.sh && \
    chmod +x cmake-3.14.4-Linux-x86_64.sh && \
    ./cmake-3.14.4-Linux-x86_64.sh --prefix=/usr/local --exclude-subdir --skip-license && \
    rm ./cmake-3.14.4-Linux-x86_64.sh

# Download NGC client
RUN cd /usr/local/bin && wget https://ngc.nvidia.com/downloads/ngccli_cat_linux.zip && unzip ngccli_cat_linux.zip && chmod u+x ngc-cli/ngc && rm ngccli_cat_linux.zip ngc-cli.md5 && echo "no-apikey\nascii\n" | ngc-cli/ngc config set

# Set environment and working directory
RUN mkdir -p /TensorRT/build
ENV TRT_LIBPATH /usr/lib/x86_64-linux-gnu
ENV TRT_OSSPATH /TensorRT
ENV PATH="${PATH}:/usr/local/bin/ngc-cli:${TRT_OSSPATH}/build/out"
ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${TRT_OSSPATH}/build/out:${TRT_LIBPATH}"

RUN cd ${TRT_OSSPATH}/build && \
    cmake .. -DTRT_LIB_DIR=$TRT_LIBPATH -DTRT_OUT_DIR=${TRT_OSSPATH}/build/out && \
    make -j$(nproc)
