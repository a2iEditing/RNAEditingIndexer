# RNAEditingIndexer
A tool for the calculation of RNA editing indexes from RNA seq data

## Requirements
### Dependencies
- _[SAMtools](http://samtools.sourceforge.net/)_ - version 1.8 or higher (tested on 1.8)
- _[bedtools](https://bedtools.readthedocs.io/en/latest)_ - version 2.26 or higher (tested on 2.26)
- [bamUtils](https://genome.sph.umich.edu/wiki/BamUtil)

- _[Java](https://www.oracle.com/technetwork/java/javase/downloads/index.html)_ - any recent version (with javac, i.e. a SDK)
- _Python 2.7_ (a clean installation is sufficient)
### OS Requirements
**Right now the program supports only GNU/Linux operating systems** (and probably any other POSIX OS)

##### CPU and Memory
The has low demand of system resources (CPU and memory) - only the default resource requirements of SAMtools and bedtools are needed (thay are ran with default CPU and memory parameters to generate the CMPileups). For the rest of the processing (after the creation of theCMPileups), the program demands very little. However **the deafult thread number is high** (and can be easily changed using command line parameters)

##### Disk Space
The installation requires a bit more than 12G of free disk space, almost all (~11.7G) of which is for the built-in resources (built-in genomes and tables which are not mandatory for running, see further details bellow for installation without downloading and running)

## Installation
(Installtion time for desktop computers should not exceed 15 minutes or so, downloading the data tables may take longer, depnding on internet connection)  
Prior to installation, you need to ran a configuration bash script (configure.sh, see below).It includes tests for the various programs required, and initialization of variables for the installation. **If the any of the tests fail (except for bamUtils) the configuration is _aborted_**
Any of the used paths (to resources directory and the programs) can be set at this stage, please run _*configure.sh -h*_ to see all options.

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

### Typical runtime
Typical runtime, parallelization taken into account, is around the 20-30 min. per sample on servers, could be up to four times as much on desktop computers, depending on samples sizes.

### Logging and flags
Under the logging directory a _flags_ directory is created. This contains a flags file for each **sample name** processed. In order to re-run samples **the flags belonging to the samples must be deleted or they will be ignored**. This feature enables parallel running with several instances of the program and re-runing with the same parameters only on a subset of the samples (e.g. failed to run ones). The logging directory also conatins a main log including timestamps per command and sample processing, progress should be checked there.

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
## Test Run
To run the test please use the following command - _InstallPath_/RNAEditingIndex -d _InstallPath_/TestResources/BAMs -f _sampled_with_0.1.Aligned.sortedByCoord.out.bam.AluChr1Only.bam -l _your wanted logs dir_ -o _wanted cmpileup output dir_ -os _wanted summery dir_ --genome hg38 -rb _InstallPath_/TestResources/AnnotationAndRegions/ucscHg38Alu.OnlyChr1.bed.gz --refseq _InstallPath_/TestResources/AnnotationAndRegions/ucscHg38RefSeqCurated.OnlyChr1.bed.gz --snps  _InstallPath_/TestResources/AnnotationAndRegions/ucscHg38CommonGenomicSNPs150.OnlyChr1.bed.gz --genes_expression  _InstallPath_/TestResources/AnnotationAndRegions/ucscHg38GTExGeneExpression.OnlyChr1.bed.gz --verbose --stranded --paired _
  Typical runtime should be within the 10 min, refernce results are in _InstallPath_/TestResources/CompareTo.
