# Use NVIDIA base image
FROM nvidia/cuda:12.1.0-devel-ubuntu20.04

# Install dependencies
ARG DEBIAN_FRONTEND=noninteractive 


RUN apt -q update && apt -yq upgrade && apt install -yq systemd curl git sudo gcc build-essential locales\
        libbz2-dev libcurl4-gnutls-dev vim dos2unix apt-file tree git zip unzip cmake wget ca-certificates locales fonts-liberation run-one \
        libglib2.0-0 libxext6 libsm6 libxrender1 mercurial subversion zlib1g-dev gridsite-clients \
        libbz2-dev libncursesw5-dev liblzma-dev libssl-dev build-essential \
        sendemail libnet-smtp-ssl-perl file shc ssh texlive-xetex texlive-fonts-recommended texlive-plain-generic \
        autoconf automake make gcc perl zlib1g-dev libbz2-dev liblzma-dev libssl-dev libncurses5-dev \
        tzdata net-tools psmisc iproute2 cron bind9-dnsutils \
        libssl-dev libxml2-dev libmariadbclient-dev libpq-dev unixodbc unixodbc-dev libcairo2-dev libgtk2.0-dev \
        openjdk-11-jdk rsync imagemagick libhdf5-dev git htop zsh htop dumb-init

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen

ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

RUN sed -i "s/# en_US.UTF-8/en_US.UTF-8/" /etc/locale.gen \
  && locale-gen
# ENV LANG=en_US.UTF-8

RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash

RUN apt install git-lfs -y

RUN mkdir -p /etc/sudoers.d

ENV CONDA_DIR=/opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH
RUN apt -q update \
    && apt -q -y upgrade \
    && apt -q -y install curl bzip2 \
    && curl -sSL https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -f -b -p $CONDA_DIR \
    && rm -rf /tmp/miniconda.sh \
    && conda install -y python=3 \
    && conda update conda 

RUN apt -q -y autoremove \
    && apt autoclean \
    && rm -rf /var/lib/apt/lists/* /var/log/dpkg.log \
    && conda clean --all --yes

RUN conda init bash
#COPY etc/conda_env.sh /opt/jupyterhub/
#RUN bash /opt/jupyterhub/conda_env.sh \
#  && cat /opt/jupyterhub/conda_env.sh >> /etc/bash.bashrc \
RUN  conda install -y -c conda-forge jupyterhub jupyterlab \
  && conda config --add channels defaults \
  && conda config --add channels bioconda \
  && conda config --add channels conda-forge \
  && conda install -y ipykernel seaborn scikit-learn statsmodels numba pytables 

# Port just for Jupyter 
EXPOSE 8888
EXPOSE 8443

RUN curl -fsSL https://code-server.dev/install.sh | sh

RUN ARCH="$(dpkg --print-architecture)" \
  && curl -fsSL "https://github.com/boxboat/fixuid/releases/download/v0.5/fixuid-0.5-linux-$ARCH.tar.gz" | tar -C /usr/local/bin -xzf - \
  && chown root:root /usr/local/bin/fixuid \
  && chmod 4755 /usr/local/bin/fixuid \
  && mkdir -p /etc/fixuid \
  && printf "user: coder\ngroup: coder\n" > /etc/fixuid/config.yml

RUN mkdir -p /opt/jupyterhub
# COPY etc/jupyterhub_config.py /opt/jupyterhub/

RUN ls etc

COPY etc/jupyterhub.service /etc/systemd/system/
COPY etc/code-server.service /etc/systemd/system/

# add local files

RUN mkdir /data
VOLUME /data

# USER 1000351

HEALTHCHECK NONE

RUN systemctl enable jupyterhub

RUN systemctl enable code-server

RUN systemctl set-default multi-user.target

STOPSIGNAL SIGRTMIN+3

RUN systemctl set-default multi-user.target

STOPSIGNAL SIGRTMIN+3

# RUN chmod +x /usr/bin/get-bin
CMD ["/bin/bash", "-c", "exec /sbin/init --log-target=journal 3>&1"]
# CMD ['jupyter', "lab", "--ip=0.0.0.0"]
# Start Jupyter by default