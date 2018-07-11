#!/usr/bin/env bash

echo $0
echo $2
echo $3

DEV_ROOT="$(dirname $(readlink -f ${0}))"
JAVA_HOME="/usr"
BEDTOOLS_PATH="bedtools"
JAVA_HOME="samtools"

HELP_MSG="Optional Params:
    -h\--help   print this message
    -j=\--java_home=   set java home dir. (default is: /usr)
    -b=\--bedtools=   set bedtools invoke command. (default is: bedtools)
    -s=\--samtools=   set samtools invoke command. (default is: samtools)
    -r=\--resources_dir=   set the path of the resources dir to download to. (default is: ${DEV_ROOT}/Resources)
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
    -h=*|--help*)
    echo
    exit
esac

done



export DEV_ROOT=${DEV_ROOT}
export JAVA_HOME=${JAVA_HOME}
export IS_UNIX=true
