# RNAEditingIndexer
A tool for the calculation of RNA-editing index from RNA seq data

## Requirements
### Dependencies
- _[SAMtools](http://samtools.sourceforge.net/)_ - version 1.8 or higher
- _[bedtools](https://bedtools.readthedocs.io/en/latest)_ - version 2.26 or higher
- [bamUtils](https://genome.sph.umich.edu/wiki/BamUtil)

- _Java_ - any recent version
- _Python 2.7_ (even a clean installation is sufficient)
### OS Requirements
**The program supports right now only GNU/Linux operating systems** (and probably any POSIX OS)
##### CPU and Memory
The default resources usage of SAMtools and bedtools. The tool's resources usage is very low, however **deafult threads number used is high** (easily controled by run params)



## Installation
The configuration bash include testing for the various programs required. **If the any of the tests fails (except for bamUtils) the configuration is _aborted_**

For the availabe option please run *./configure.sh -h*
**NOTE: The installation will defaultly download the builtin genomes (_unzipped_) and tables (_gzipped_). This requires about 10G of Disk space**
#change working dir to the installtion dir first
cd ./RNAEditingIndexer

#configure installtion environmental variables

. ./configure.sh

make
