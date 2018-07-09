__author__ = 'Hillel'
"""
This module loads a gzipped DB SNP file of the tab format (the format is as found in the UCSC Genome Browser,
 a header is assumed to be present):
1.	Chromosome
2.	Start (0-based)
3.	End
4.	Strand
5.  <Reference>
6.  <SNP sequences> ('-' means no bases, as in insertions and deletions)
7.	Genomic function (e.g. intergenic, intronic)
8.	Alleles frequencies <Reference>/<SNP>

Input file should either be intersected of gzipped
"""
# =====================imports=====================#
# region Builtin Import
import os
import logging
# endregion

# region InternalImports
from RNAEditingIndex.GGPSResources.consts import EMPTY_SEQ, ANTISENSE_STRAND, MismatchesAndRefsEnum, UNKNOWN_STRAND
from RNAEditingIndex.GGPSResources.data_structs import Site
from RNAEditingIndex.GGPSResources.general_functions import get_file_handle

# endregion

# =====================constants===================#
UCSC_TABLE_SEP = "\t"

FREQS_UCSC_SEP = ","
SEQUENCES_UCSC_SEP = "/"
UCSC_REF_I = 0
SEQUENCES_UCSC_EMPTY_SEQ = "-"

INTERSECT_FORMAT = "%(bedtools)s intersect -a '%(snps_file)s' -b '%(intersect_file)s' -wo "


# =====================functions===================#
def load_snps_file(snps_file, intersect_first_with='', bedtools_path="bedtools"):
    # type: (str, str, str) -> dict
    """
    This function parses a SNPsData DB file
    :param str snps_file: The file in the described format.
    :param str intersect_first_with: If provided will first intersect SNPs file with it.
    :param str bedtools_path: The run-path of bedtools.
    :return dict index (to boolean) of the SNPs compared to the sense strand of the ref genome.
    """
    sites = dict()
    logging_counter = dict()
    for mm_type in MismatchesAndRefsEnum.ALL_MISMATCHES:
        logging_counter[mm_type] = 0
    if intersect_first_with:
        snps_fh = os.popen(
            INTERSECT_FORMAT % dict(bedtools=bedtools_path, snps_file=snps_file, intersect_file=intersect_first_with))
    else:
        snps_fh = get_file_handle(snps_file)
    for line in snps_fh:
        if intersect_first_with:
            chrom, start, end, strand, ref_seq, seqs, func, freqs, reg_chrom, reg_start, reg_end, count = line.strip(
                "\n").split(UCSC_TABLE_SEP)
        else:
            chrom, start, end, strand, ref_seq, seqs, func, freqs = line.strip("\n").split(UCSC_TABLE_SEP)

        seqs = seqs.strip().replace(SEQUENCES_UCSC_EMPTY_SEQ, EMPTY_SEQ).split(SEQUENCES_UCSC_SEP)

        ref_seq = MismatchesAndRefsEnum.REFS_TRANSLATE.get(ref_seq, None)
        if None is ref_seq:
            continue

        seqs = [MismatchesAndRefsEnum.REFS_TRANSLATE.get(s, None) for s in seqs]

        start = int(start)
        end = int(end)
        site = Site(chrom, start, end, UNKNOWN_STRAND)

        for snp_seq in seqs:
            if None is snp_seq or snp_seq == ref_seq:
                continue
            if strand == ANTISENSE_STRAND:
                mismatch = MismatchesAndRefsEnum.MISMATCH_TYPE_TRANSLATE[
                    MismatchesAndRefsEnum.COMPLEMENTARY_REF[ref_seq] + MismatchesAndRefsEnum.COMPLEMENTARY_REF[snp_seq]]
            else:
                mismatch = MismatchesAndRefsEnum.MISMATCH_TYPE_TRANSLATE[ref_seq + snp_seq]

            sites.setdefault(mismatch, dict())[site] = True
            logging_counter[mismatch] += 1

    logging.info(
        "Loaded %s SNPs" % ", ".join([mm_type + ": %s" % count for mm_type, count in logging_counter.iteritems()]))

    return sites
