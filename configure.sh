#!/usr/bin/env bash

DEV_ROOT="$(dirname $(readlink -f ${BASH_SOURCE}))"
JAVA_HOME="/usr"
BEDTOOLS_PATH="bedtools"
SAMTOOLS_PATH="samtools"
RESOURCES_DIR="${DEV_ROOT}/Resources"

HELP_MSG="Optional Params:
    -h\--help   print this message
    -j=\--java_home=   set java home dir. (default is: /usr)
    -b=\--bedtools=   set bedtools invoke command. (default is: bedtools)
    -s=\--samtools=   set samtools invoke command. (default is: samtools)
    -r=\--resources_dir=   set the path of the resources dir to download to. (default is: ${RESOURCES_DIR})
"

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
    -h=*|--help*)
    echo
    exit
esac

done



export DEV_ROOT=${DEV_ROOT}
export BEDTOOLS_PATH=${BEDTOOLS_PATH}
export SAMTOOLS_PATH=${SAMTOOLS_PATH}
export RESOURCES_DIR=${RESOURCES_DIR}
export JAVA_HOME=${JAVA_HOME}
export IS_UNIX=true
