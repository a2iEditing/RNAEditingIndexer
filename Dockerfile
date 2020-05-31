FROM biocontainers/biocontainers:latest

RUN conda install samtools=1.9 && \
        conda install bedtools=2.27.1 && \
        conda install bamutil=1.0.14 && \
        conda install -c cyclus java-jdk=8.0.92 && \
        conda install python=2.7.16 && \
        conda install -c anaconda git

USER root

RUN mkdir -p /bin/AEI &&\
    cd /bin/AEI &&\
    git clone https://github.com/shalomhillelroth/RNAEditingIndexer

ENV DEV_ROOT /bin/AEI/RNAEditingIndexer
ENV BEDTOOLS_PATH bedtools
ENV SAMTOOLS_PATH samtools
ENV RESOURCES_DIR=/bin/AEI/RNAEditingIndexer/Resources
ENV JAVA_HOME /opt/conda
ENV BAM_UTILS_PATH bam
ENV PYTHON27_PATH python
ENV DONT_DOWNLOAD false
ENV DONT_WRITE false
ENV IS_UNIX true

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/conda/bin:/home/biodocker/bin:/bin/AEI/RNAEditingIndexer

RUN cd /bin/AEI/RNAEditingIndexer && make

CMD /bin/AEI/RNAEditingIndexer/RNAEditingIndex