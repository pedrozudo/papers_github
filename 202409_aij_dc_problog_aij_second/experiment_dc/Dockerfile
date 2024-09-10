FROM ubuntu:14.04


RUN apt-get update \
    && \
    echo "------------------------------------------------------ essentials" \
    && \
    apt-get install -y --no-install-recommends -y \
    build-essential \
    apt-utils \
    && \
    echo "------------------------------------------------------ editors" \
    && \
    apt-get install -y --no-install-recommends -y \
    emacs \
    vim \
    nano \
    && \
    echo "------------------------------------------------------ software" \
    && \
    apt-get install -y --no-install-recommends -y \
    python3-pip \
    tmux \ 
    wget \
    git \
    unzip





RUN echo "------------------------------------------------------ YAP install" \
    && \
    apt-get install -y --no-install-recommends libreadline6 libreadline6-dev libncurses5-dev \
    && \
    wget https://bitbucket.org/problog/dc_problog/downloads/yap-6.2.2.zip \
    && \
    unzip yap-6.2.2.zip \
    && \
    cd yap-6.2.2 \
    && \
    mkdir arch \
    && \
    cd arch \
    && \
    ../configure --enable-tabling=yes --enable-dynamic-loading --disable-myddas \
    && \
    make \
    && \
    make install \
    && \
    make install_library


RUN echo "------------------------------------------------------ DC install" \
    && \
    apt-get install -y --no-install-recommends  libgsl0-dev libgsl0ldbl \
    && \
    apt-get install -y --no-install-recommends libboost-all-dev  \
    && \
    cd / \
    && \
    git clone https://github.com/davidenitti/DC.git \
    && \
    cd DC \
    && \
    sh make.sh


RUN echo "------------------------------------------------------ cleanup" \
    apt-get clean && rm -rf /var/lib/apt/lists/*