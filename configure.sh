#!/usr/bin/env bash

DEV_ROOT="$(dirname $(readlink -f ${BASH_SOURCE}))"
JAVA_HOME="/usr"
BEDTOOLS_PATH="bedtools"
BAM_UTILS_PATH="bam"
SAMTOOLS_PATH="samtools"
PYTHON27_PATH="python"
RESOURCES_DIR="${DEV_ROOT}/Resources"
PRINT_HELP=false


for i in "$@"
do

case ${i} in
    -j=*|--java_home=*)
    JAVA_HOME="${i#*=}"
    #shift # past argument=value
    ;;
    -b=*|--bedtools=*)
    BEDTOOLS_PATH="${i#*=}"
    #shift # past argument=value
    ;;
    -s=*|--samtools=*)
    SAMTOOLS_PATH="${i#*=}"
    ;;
    -r=*|--resources_dir=*)
    RESOURCES_DIR="${i#*=}"
    #shift # past argument=value
    ;;
    -bu=*|--bam_utils=*)
    BAM_UTILS_PATH="${i#*=}"
    #shift # past argument=value
    ;;
    -p=*|--python=*)
    PYTHON27_PATH="${i#*=}"
    #shift # past argument=value
    ;;
    -h|--help)
    PRINT_HELP=true
    #shift # past argument=value
    ;;
esac

done

if [ "${PRINT_HELP}" = true ] ; then
    echo "Optional Params:
    -h\--help   print this message
    -j=\--java_home=    set java home dir. (default is: /usr)
    -b=\--bedtools=     set bedtools invoke command. (default is: bedtools)
    -bu=\--bam_utils=   set bam utils invoke command. (default is: bam)
    -s=\--samtools=     set samtools invoke command. (default is: samtools)
    -p=\--python=       set python 2.7 invoke command. (default is: python)
    -r=\--resources_dir=   set the path of the resources dir to download to. (default is: ${RESOURCES_DIR})
"
else
    export DEV_ROOT=${DEV_ROOT}
    export BEDTOOLS_PATH=${BEDTOOLS_PATH}
    export SAMTOOLS_PATH=${SAMTOOLS_PATH}
    export RESOURCES_DIR=${RESOURCES_DIR}
    export JAVA_HOME=${JAVA_HOME}
    export BAM_UTILS_PATH=${BAM_UTILS_PATH}
    export PYTHON27_PATH=${PYTHON27_PATH}
    export IS_UNIX=true
fi

