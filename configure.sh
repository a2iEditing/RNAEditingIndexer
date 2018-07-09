#! /bin/sh



set JAVA_HOME = 'java'

for i in "$@"
    do
case $i in
    -j=*|--java_home=*)
    JAVA_HOME="${i#*=}"
    shift # past argument=value
    ;;
esac
done



set DEV_ROOT = $PWD
set JAVA_HOME = $JAVA_HOME
set IS_UNIX = true

export DEV_ROOT
export JAVA_HOME
export IS_UNIX