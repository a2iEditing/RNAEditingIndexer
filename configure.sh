#!/usr/bin/env bash



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



export DEV_ROOT=$PWD
export JAVA_HOME=$JAVA_HOME
export IS_UNIX=true
