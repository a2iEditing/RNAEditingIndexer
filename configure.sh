#!/usr/bin/env bash

DEV_ROOT="$(dirname $(readlink -f ${BASH_SOURCE}))"
JAVA_HOME="/usr"
BEDTOOLS_PATH="bedtools"
BAM_UTILS_PATH="bam"
SAMTOOLS_PATH="samtools"
RESOURCES_DIR="${DEV_ROOT}/Resources"


for i in "$@"
    do
case $i in
    -j=*|--java_home=*)
    JAVA_HOME="${i#*=}"
    shift # past argument=value
    ;;
esac

case $i in
    -b=*|--bedtools=*)
    BEDTOOLS_PATH="${i#*=}"
    shift # past argument=value
    ;;
esac

case $i in
    -s=*|--samtools=*)
    SAMTOOLS_PATH="${i#*=}"
    shift # past argument=value
    ;;
esac

case $i in
    -r=*|--resources_dir=*)
    SAMTOOLS_PATH="${i#*=}"
    shift # past argument=value
    ;;
esac

case $i in
    -bu=*|--bam_utils=*)
    BAM_UTILS_PATH="${i#*=}"
    shift # past argument=value
    ;;
esac

case $i in
    -h=*|--help*)
    echo "Optional Params:
    -h\--help   print this message
    -j=\--java_home=    set java home dir. (default is: /usr)
    -b=\--bedtools=     set bedtools invoke command. (default is: bedtools)
    -bu=\--bam_utils=   set bam utils invoke command. (default is: bam)
    -s=\--samtools=     set samtools invoke command. (default is: samtools)
    -r=\--resources_dir=   set the path of the resources dir to download to. (default is: ${RESOURCES_DIR})
"
esac

done



export DEV_ROOT=${DEV_ROOT}
export BEDTOOLS_PATH=${BEDTOOLS_PATH}
export SAMTOOLS_PATH=${SAMTOOLS_PATH}
export RESOURCES_DIR=${RESOURCES_DIR}
export JAVA_HOME=${JAVA_HOME}
export BAM_UTILS_PATH=${BAM_UTILS_PATH}
export IS_UNIX=true
