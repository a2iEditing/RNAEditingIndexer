FROM biocontainers/biocontainers:latest

#USER root

#RUN mkdir -p /bin/AEI &&\
#    cd /bin/AEI &&\
#    git clone --single_branch --branch autoconf https://github.com/shalomhillelroth/RNAEditingIndexer

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/conda/bin:/home/biodocker/bin:/bin/AEI/RNAEditingIndexer

WORKDIR /tmp
ADD docker_installations.sh .
RUN ./docker_installations.sh
WORKDIR /


#RUN cd /bin/AEI/RNAEditingIndexer && make

CMD /bin/AEI/RNAEditingIndexer/RNAEditingIndex