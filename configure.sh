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
    *)
      # unknown option
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
#else
#    unset  DEV_ROOT
#    unset  BEDTOOLS_PATH
#    unset  SAMTOOLS_PATH
#    unset  RESOURCES_DIR
#    unset  JAVA_HOME
#    unset  BAM_UTILS_PATH
#    unset  PYTHON27_PATH
#    unset  IS_UNIX
fi

