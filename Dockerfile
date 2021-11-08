FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive
ENV LANG=en_US.UTF-8

RUN  apt-get update && \
     apt-get upgrade -y && \
     apt-get install -y software-properties-common && \
     apt-add-repository ppa:swi-prolog/stable && \ 
     apt-get install -q -y openjdk-8-jdk python3-pip libsnappy-dev \
                           language-pack-en git maven vim swi-prolog wget

RUN pip3 install --upgrade pip 
RUN swipl -g "pack_install(aleph, [interactive(false)])." -g halt 

RUN ln -s /usr/bin/python3 /usr/bin/python && \
    ln -s /usr/bin/pip3 /usr/bin/pip

COPY . /sml-bench
WORKDIR /sml-bench
RUN ./setup.sh
CMD ["/bin/bash"]
