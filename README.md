# RNAEditingIndexer
A tool for the calculation of RNA editing indexes from RNA seq data

## Requirements
### Dependencies
- _[SAMtools](http://samtools.sourceforge.net/)_ - version 1.8 or higher (tested on 1.8)
- _[bedtools](https://bedtools.readthedocs.io/en/latest)_ - version 2.26 or higher (tested on 2.26)
- [bamUtils](https://genome.sph.umich.edu/wiki/BamUtil)

- _[Java](https://www.oracle.com/technetwork/java/javase/downloads/index.html)_ - any recent version (with javac, i.e. a SDK)
- _[Python 2.7](https://www.python.org/download/releases/2.7/)_ (a clean installation is sufficient)
### OS Requirements
**Right now the program supports only GNU/Linux operating systems** (and probably any other POSIX OS)

##### CPU and Memory
The program has low demand of system resources (CPU and memory) - only the default resource requirements of SAMtools and bedtools are needed (thay are ran with default CPU and memory parameters to generate the CMPileups). For the rest of the processing (after the creation of theCMPileups), the program demands very little. However **the deafult thread number is high** (and can be easily changed using command line parameters)

##### Disk Space
The installation requires a bit more than 12G of free disk space, almost all (~11.7G) of which is for the built-in resources (built-in genomes and tables which are not mandatory for running, see further details bellow for installation without downloading and running)

## Installation
(Installtion time for desktop computers should not exceed 15 minutes or so, downloading the data tables may take longer, depnding on internet connection)  
Prior to installation, you need to ran a configuration bash script (configure.sh, see below).It includes tests for the various programs required, and initialization of variables for the installation. **If the any of the tests fail (except for bamUtils) the configuration is _aborted_**
Any of the used paths (to resources directory and the programs) can be set at this stage, please run __configure.sh -h__ to see all options.

**NOTE: The installation will by default download the built-in genomes (_unzipped_) and tables (_gzipped_). This requires about 12G of Disk space**

```
#change working dir to the installtion dir

cd ./RNAEditingIndexer

#configure installtion environmental variables

. ./configure.sh

make
```

### Resources File
The installation creates a file named ResourcesPaths.ini at \<_InstallPath_\>/src/RNAEditingIndex/Configs (set with *configure.sh*) which specifies the default path to the required programs and data files (such as genomes and tables). **Modify this file after installtion to change defaults (such as in the case of not downloading the data files)**

## Running
Simply run _RNAEditingIndex -h_  to see full help.

### An example for a simple run:
```
_InstallPath_/RNAEditingIndex -d _BAMs diretory_ -f Aligned.sortedByCoord.out.bam. -l _logs directory_ -o _cmpileup output directory_ -os _summery files directory_ --genome hg38 
```

### Typical runtime
Typical runtime, parallelization taken into account, is around the 20-30 min. per sample on servers, could be up to four times as much on desktop computers, depending on BAMs sizes (i.e. coverage).

### Logging and flags
Under the chosen logging directory a _flags_ directory is created. This contains a flag file for each **sample name** processed (of the format _\<sample name\>.flg_. In order to re-run samples **the flags belonging to the samples must be deleted or they will be ignored**. This feature enables parallel running with several instances of the program and re-runing with the same parameters only on a subset of the samples (e.g. failed to run ones). The logging directory also conatins a main log (the name is EditingIndex.\<_timestamp_\>.log) including timestamps per (internal) command and sample processing (this is the place to check for progress and errors).

### Inputs

#### Alignments
The input directory containing alignemnt (BAM) files. The directory can be nested (i.e. folders within folders), the program looks for the BAM files recursively.  
**Note: alignment should be unique** (non-unique alignemt may create unpredicted, algorithm dependant, biases)

#### Genome and Annotations
You can use any of the built-in genomes (and thier corresponding annotations) without providing any additional paramters (using the _--genome_ option). However any used resource (regions indexed BED, SNPs, gene annotations and expression levels, and genome) can be provided by the user instead. See help and documentations for details.

## Outputs and Output Directories

### Temporary Outputs - CMPileup and genome index files
CMPileups, pileup files converted into a numerical format (for more details see the full documentaion), are created in the directory specified under _-o_ flag and unless specified otherwise (with the _keep_cmpileup_ flag) will be deleted after processing due to their, usually, very large size. A genome index (with the suffix _.jsd_ by default) is also created there (and deleted).

### Summary file
A summary file is created in the directory specified by _-os_. **The output is _appended_ for each run**, so that several instances of the program may be run with the same output file (creating a single joined output).
For a full explanation of the output see the documentaion, but in a nutshell:
  - A2GEditingIndex is the signal (i.e. value) of the editing
  - C2TEditingIndex is the highest noise (in most cases)
  - (in verbose mode) use lines where _StrandDecidingMethod_ is "_RefSeqThenMMSites_"
 
## Test Run
To run the test please use the following command: \<_InstallPath_\>/RNAEditingIndex -d \<_InstallPath_\>/TestResources/BAMs -f _sampled_with_0.1.Aligned.sortedByCoord.out.bam.AluChr1Only.bam -l \<_your wanted logs dir_\> -o \<_wanted cmpileup output dir_\> -os \<_wanted summery dir_\> --genome hg38 -rb \<_InstallPath_\>/TestResources/AnnotationAndRegions/ucscHg38Alu.OnlyChr1.bed.gz --refseq \<_InstallPath_\>/TestResources/AnnotationAndRegions/ucscHg38RefSeqCurated.OnlyChr1.bed.gz --snps  \<_InstallPath_\>/TestResources/AnnotationAndRegions/ucscHg38CommonGenomicSNPs150.OnlyChr1.bed.gz --genes_expression  \<_InstallPath_\>/TestResources/AnnotationAndRegions/ucscHg38GTExGeneExpression.OnlyChr1.bed.gz --verbose --stranded --paired

Typical runtime should be within the 10 min, refernce results are in \<_InstallPath_\>/TestResources/CompareTo.
