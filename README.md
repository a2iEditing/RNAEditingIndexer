# RNAEditingIndexer
A tool for the calculation of RNA editing indexes from RNA seq data

## Requirements
### Dependencies
- _[SAMtools](http://samtools.sourceforge.net/)_ - version 1.8 or higher (tested on 1.8)
- _[bedtools](https://bedtools.readthedocs.io/en/latest)_ - version 2.26 or higher (tested on 2.26)
- [bamUtils](https://genome.sph.umich.edu/wiki/BamUtil)

- _Java_ - any recent version
- _Python 2.7_ (a clean installation is sufficient)
### OS Requirements
**Right now the program supports only GNU/Linux operating systems** (and probably any other POSIX OS)

##### CPU and Memory
Only the default resource requirements of SAMtools and bedtools (default running parameters are used) are needed. The program's other resources usage is very low, however **deafult threads number used is high** (easily controled by run parameters)

##### Disk Space
Installation requires a bit more than 12G of free disk space, almost all (~11.7G) of which is for the resources (built-in genomes and tables which are not mandatory for running, see further details bellow for installation without downloading and running)

## Installation
(Installtion time for desktop computers should not exceed 15 minutes or so, downloading the data tables may take longer, depnding on internet connection)  
The configuration bash includes testing for the various programs required. **If the any of the tests fail (except for bamUtils) the configuration is _aborted_**

To see all availabe options, please run *./configure.sh -h*
**NOTE: The installation will by default download the built-in genomes (_unzipped_) and tables (_gzipped_). This requires about 12G of Disk space**

```
#change working dir to the installtion dir

cd ./RNAEditingIndexer

#configure installtion environmental variables

. ./configure.sh

make
```

### Resources File
The installation creates a file named ResourcesPaths.ini at <install dir>/src/RNAEditingIndex/Configs (set with *configure.sh*) which specifies the default path to the required programs and data files (such as genomes and tables). **Modify this file after installtion to change defaults (such as in the case of not downloading the data files)**

## Running
Simply run _RNAEditingIndex -h_  to see full help.

### Logging and flags
Under the logging directory a _flags_ directory is created. This contains a flags file for each **sample name** processed. In order to re-run samples **the flags belonging to the samples must be deleted or they will be ignored**. This feature enables parallel running with several instances of the program and re-runing with the same parameters only on a subset of the samples (e.g. failed to run ones).

### Inputs
The input directory can be any directory containing BAM files (however nested, the program looks for them recursively)  
**Note: BAMs should be created with unique alignemt** (non-unique alignemt may alter the results in an algorithm dependant way)

### Outputs
#### CMPileup and genome index files
CMPileups, pileup files converted into a numerical format (for more details see the full documentaion), are created in the directory specified under _-o_ flag and unless stated otherwise (with the _keep_cmpileup_ flag) will be deleted after processing due to their, usually, very large size. A genome index (with the suffix _.jsd_ by default) is also created there (and deleted).

### Summary file
The summary file is created under the root specified by _-os_. **The output is _appended_**, so that several instances of the program may be run with the same output file (creating a single joined output).
Full explanation of the output can be seen in the documentaion, but in a nutshell:
  - use lines where _StrandDecidingMethod_ is "_RefSeqThenMMSites_" (in verbose mode)
  - A2GEditingIndex is the signal (i.e. value) of the editing
  - C2TEditingIndex is the highest noise (in most cases)
