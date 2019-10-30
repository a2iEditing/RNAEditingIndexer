#!/bin/bash
'
This work is licensed under the Creative Commons Attribution-Non-Commercial-ShareAlike 4.0 International License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
For use of the software by commercial entities, please inquire with Tel Aviv University at ramot@ramot.org.
(c) 2019 Tel Aviv University (Erez Y. Levanon, Erez.Levanon@biu.ac.il;
Eli Eisenberg, elieis@post.tau.ac.il;
Shalom Hillel Roth, shalomhillel.roth@live.biu.ac.il).
'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
DEV_ROOT="$(dirname $(readlink -f ${BASH_SOURCE}))"
if [ -z "$DEV_ROOT" ]
then
DEV_ROOT="$(dirname $0)"
fi
JAVA_HOME="/usr"
BEDTOOLS_PATH="bedtools"
BAM_UTILS_PATH="bam"
SAMTOOLS_PATH="samtools"
PYTHON27_PATH="python"
RESOURCES_DIR="${DEV_ROOT}/Resources"
PRINT_HELP=false
DONT_DOWNLOAD=false
DONT_WRITE=false
CONF_OUT="${DEV_ROOT}/conf.vars"



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
    echo "Optional Params:
    -h\--help               print this message
    --dont_download         do not download resources, only create Resources.ini file and directories
    --no_resources_file     do not write resources file (Resources.ini file), to avoid overriding your changes
    -j=\--java_home=        set java home dir. (default is: /usr)
    -b=\--bedtools=         set bedtools invoke command. (default is: bedtools)
    -bu=\--bam_utils=       set bam utils invoke command. (default is: bam)
    -s=\--samtools=         set samtools invoke command. (default is: samtools)
    -p=\--python=           set python 2.7 invoke command. (default is: python)
    -r=\--resources_dir=    set the path of the resources dir to download to. (default is: ${RESOURCES_DIR})
"
    #shift # past argument=value
    ;;
    --dont_download)
    DONT_DOWNLOAD=true
    #shift # past argument=value
    ;;
    --no_resources_file)
    DONT_WRITE=true
    #shift # past argument=value
    ;;
esac
done

if [ "${PRINT_HELP}" = false ]
then
    TESTS_SUCCEEDED=true
    #test bedtools
    if test -x $(which ${BEDTOOLS_PATH}); then
        echo "BEDTools Path Executable Test - Succeeded"
    else
        echo "BEDTools Path Executable Test - Failed"
        echo -e "${RED}BEDTools Path is Not An Executable"
        echo -e "${NC}"
        TESTS_SUCCEEDED=false
    fi
    RET=$(${BEDTOOLS_PATH} --version|  egrep -o "([0-9]{1,}\.)+[0-9]{1,}"|awk -F "." '(($1 > 2)||($1 ==2 && $2 > 25))')
    if [[ ${RET} =~ ^[0-9]+(\.[0-9]+){2,3}$ ]]; then
        echo "BEDTools Version Test - Succeeded"
    else
        echo "BEDTools Version Test - Failed"
        echo -e "${RED}BEDTools Version Must Be Equal or Greater Than 2.26.0"
        echo -e "${NC}"
        TESTS_SUCCEEDED=false
    fi
    #test samtools
    if test -x $(which ${SAMTOOLS_PATH}); then
        echo "SAMTools Path Executable Test - Succeeded"
    else
        echo "SAMTools Path Executable Test - Failed"
        echo -e "${RED}SAMTools Path is Not An Executable"
        echo -e "${NC}"
        TESTS_SUCCEEDED=false
    fi
    RET=$(${SAMTOOLS_PATH} --version|  egrep -o -m 1 "([0-9]{1,}\.)+[0-9]{1,}"|awk -F "." '($1 >=1 && $2 > 7)')
    if [[ ${RET} =~ ^[0-9]+(\.[0-9]+){1,3}$ ]]; then
        echo "SAMTools Version Test - Succeeded"
    else
        echo "SAMTools Version Test - Failed"
        echo -e "${RED}SAMTools Version Must Be Equal or Greater Than 1.8"
        echo -e "${NC}"
        TESTS_SUCCEEDED=false
    fi
    #test bamutils
    if test -x $(which ${BAM_UTILS_PATH}); then
        echo "BAM Utils Path Executable Test - Succeeded"
    else
        echo "BAM Utils Path Executable Test - Failed"
        echo -e "${RED}BAM Utils Path is Not An Executable"
        echo -e "${NC}"
        TESTS_SUCCEEDED=false
    fi
    RET=$(${BAM_UTILS_PATH} help 2>&1|  egrep -o -m 1 "([0-9]{1,}\.)+[0-9]{1,}")
    VER=$(echo ${RET}|awk -F "." '(($1 ==1 && $3 > 13) || ($1 > 1))')
    if [[ ${RET} =~ ^[0-9]+(\.[0-9]+){1,3}$ ]]; then
        echo "BAM Utils Run Test - Succeeded"
        if [[ ${VER} =~ ^[0-9]+(\.[0-9]+){1,3}$ ]]; then
            echo "BAM Utils Version Test - Succeeded"
        else
            echo -e "${YELLOW}Warning: BAM Utils Version is Bellow Tested Version (1.8)"
            echo -e "${NC}"
        fi
    else
        echo "BAM Utils Run Test - Failed"
        echo -e "${RED}Could Not Run BAM Utils help"
        echo -e "${NC}"
        TESTS_SUCCEEDED=false
    fi
    #test Java
    JAVA_FULL="${JAVA_HOME}/bin/java"
    if test -x $(which ${JAVA_FULL}); then
        echo "Java Path Executable Test - Succeeded"
    else
        echo "Java Path Executable Test - Failed"
        echo -e "${RED}BAM Utils Path is Not An Executable"
        echo -e "${NC}"
        TESTS_SUCCEEDED=false
    fi
    RET=$(${JAVA_FULL}  -XshowSettings:properties -version 2>&1| egrep -o -m 1 "java.version = ([0-9]{1,}\.)+[0-9]{1,}")
    if [[ ${RET} =~ ^java.version.* ]]; then
        echo "Java Run Test - Succeeded (${RET})"
    else
        echo "Java Run Test - Failed"
        echo -e "${RED}Could Not Run Java"
        echo -e "${NC}"
        TESTS_SUCCEEDED=false
    fi
    #test Python
    if test -x $(which ${PYTHON27_PATH}); then
        echo "Python 2.7 Path Executable Test - Succeeded"
    else
        echo "Python 2.7 Path Executable Test - Failed"
        echo -e "${RED}SAMTools Path is Not An Executable"
        echo -e "${NC}"
        TESTS_SUCCEEDED=false
    fi
    RET=$(${PYTHON27_PATH} --version 2>&1| egrep -o -m 1 "([0-9]{1,}\.)+[0-9]{1,}"|awk -F "." '($1 ==2 && $2 == 7)')
    if [[ ${RET} =~ ^[0-9]+(\.[0-9]+){1,3}$ ]]; then
        echo "Python 2.7 Version Test - Succeeded"
    else
        echo "Python 2.7 Version Test - Failed"
        echo -e "${RED}Python Version Must Be 2.27.x"
        echo -e "${NC}"
        TESTS_SUCCEEDED=false
    fi
    if [ "${TESTS_SUCCEEDED}" = false ]; then
        echo "Failed On Tests, Exiting..."
    else
        export DEV_ROOT=${DEV_ROOT}
        export BEDTOOLS_PATH=${BEDTOOLS_PATH}
        export SAMTOOLS_PATH=${SAMTOOLS_PATH}
        export RESOURCES_DIR=${RESOURCES_DIR}
        export JAVA_HOME=${JAVA_HOME}
        export BAM_UTILS_PATH=${BAM_UTILS_PATH}
        export PYTHON27_PATH=${PYTHON27_PATH}
        export DONT_DOWNLOAD=${DONT_DOWNLOAD}
        export DONT_WRITE=${DONT_WRITE}
        export IS_UNIX=true
    fi
fi
