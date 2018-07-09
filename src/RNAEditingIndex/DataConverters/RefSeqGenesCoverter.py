__author__ = 'Hillel'
"""
This module loads a gzipped DB RefSeqData file of the tab format (the format is as found in the UCSC Genome Browser,
 a header is assumed to be present):
1.	Chromosome
2.	Start (0-based)
3.	End
4.	RefSeq Name (e.g. NR_075077.1)
5.	Gene Common name (e.g. C1orf141)
6.	Strand
7.	Exons Start Positions (0-based) separated by ","
8.	Exons End Positions separated by ","

Input file should either be intersected of gzipped
"""
# =====================imports=====================#
# region Builtin Import
import gzip
import logging
import os
from pprint import pformat
# endregion

# region InternalImports
from RNAEditingIndex.GGPSResources.consts import UNKNOWN_STRAND, SENSE_STRAND, ANTISENSE_STRAND, NA_REFSEQ
from RNAEditingIndex.GGPSResources.data_structs import Site, RefSeq, RefSeqPosEnum

# endregion

# =====================constants===================#
UCSC_TABLE_SEP = "\t"
UCSC_SEP = ","

INTERSECT_FORMAT = "%(bedtools)s intersect -a '%(refseq_file)s' -b '%(intersect_file)s' -wo "


# =====================functions===================#
def get_connected_region_genomic_annotation(region, region_refseqs):
    # type: (str, list) -> (str, RefSeq)
    """
    This function retrieves the annotation of a site.
    For regions falling inside several RefSeq records: for exonic match, the first match will be returned,
     and for intronic - the last.
    :param Site region: The region to check for
    :param list[RefSeq] region_refseqs: object
    :return list[RefSeq, RefSeqPosEnum]: The annotation if found, else NA_REFSEQ
    """
    #

    refseq_match = None

    annotation = RefSeqPosEnum.INTRONIC  # call this function means we have position inside a gene
    for refseq in region_refseqs:
        refseq_match = refseq
        exons_sorted = sorted(refseq.exons, reverse=True)
        num_of_exons = len(exons_sorted)
        # partial overlapping from the 5' of the gene
        if region.start <= exons_sorted[num_of_exons - 1] <= region.end:
            annotation = RefSeqPosEnum.EXONIC
            break

        if region.start <= refseq.exons[exons_sorted[0]] <= region.end:
            annotation = RefSeqPosEnum.EXONIC
            break

        for i, e_start in enumerate(exons_sorted):
            if region.start <= e_start <= region.end:
                annotation = RefSeqPosEnum.EXONIC
                break

            elif region.start <= refseq.exons[e_start] <= region.end:
                annotation = RefSeqPosEnum.EXONIC
                break

            elif refseq.exons[e_start] >= region.start >= e_start:
                annotation = RefSeqPosEnum.EXONIC
                break

        if annotation == RefSeqPosEnum.EXONIC:
            break

    return [annotation, refseq_match]


def load_refseq_bed(refseq_file, regions_file, bedtools_path="bedtools"):
    # type: (str, str, str, str, str) -> dict
    """
    This function loads a RefSeqData DB file
    :param str refseq_file: The file in the described format.
    :param str regions_file: If provided will first intersect SNPs file with it.
    :param str bedtools_path: The run-path of bedtools.
    :return dict
    """
    refseq_fh = os.popen(INTERSECT_FORMAT % dict(bedtools=bedtools_path, refseq_file=refseq_file,
                                                 intersect_file=regions_file))

    refseqs = dict()
    for line in refseq_fh:
        chrom, start, end, refseq_name, common_name, strand, e_starts, e_ends, reg_chrom, reg_start, reg_end, count = \
            line.strip("\n").split(UCSC_TABLE_SEP)

        start = int(start)
        end = int(end)
        site = Site(chrom, start, end, strand)

        exons_starts = e_starts.strip().split(UCSC_SEP)
        exons_ends = e_ends.strip().split(UCSC_SEP)
        exons = {int(e_start): int(e_end) for e_start, e_end in zip(exons_starts, exons_ends) if e_start}

        reg_site = Site(region=reg_chrom, start=int(reg_start), end=int(reg_end), strand=UNKNOWN_STRAND)

        refseq = RefSeq(site=site, exons=exons, refseq_name=refseq_name, common_name=common_name)

        refseqs.setdefault(reg_site, dict()).setdefault(strand, []).append(refseq)

    res = annotate_regions(refseqs, regions_file.strip('"'))

    return res


def annotate_regions(refseqs, regions_file):
    regions = []
    try:
        with gzip.open(regions_file) as reg_fh:
            for line in reg_fh:
                reg_chrom, reg_start, reg_end = line.strip("\n").split(UCSC_TABLE_SEP)
                regions.append(Site(region=reg_chrom, start=int(reg_start), end=int(reg_end), strand=UNKNOWN_STRAND))
    except IOError:
        with open(regions_file) as reg_fh:
            for line in reg_fh:
                reg_chrom, reg_start, reg_end = line.strip("\n").split(UCSC_TABLE_SEP)
                regions.append(Site(region=reg_chrom, start=int(reg_start), end=int(reg_end), strand=UNKNOWN_STRAND))
    res = {}
    logging_counter = {SENSE_STRAND: {RefSeqPosEnum.EXONIC: 0,
                                      RefSeqPosEnum.INTRONIC: 0,
                                      RefSeqPosEnum.INTERGENIC: 0, },
                       ANTISENSE_STRAND: {RefSeqPosEnum.EXONIC: 0,
                                          RefSeqPosEnum.INTRONIC: 0,
                                          RefSeqPosEnum.INTERGENIC: 0, }
                       }
    for reg in regions:
        res[reg] = dict()

        region_refseqs = refseqs.get(reg, {}).get(SENSE_STRAND, None)
        if region_refseqs:
            sense_annotation = get_connected_region_genomic_annotation(region=reg, region_refseqs=region_refseqs)
        else:
            sense_annotation = [RefSeqPosEnum.INTERGENIC, NA_REFSEQ]
        logging_counter[SENSE_STRAND][sense_annotation[0]] += 1
        res[reg][SENSE_STRAND] = sense_annotation

        region_refseqs = refseqs.get(reg, {}).get(ANTISENSE_STRAND, None)
        if region_refseqs:
            antisense_annotation = get_connected_region_genomic_annotation(region=reg, region_refseqs=region_refseqs)
        else:
            antisense_annotation = [RefSeqPosEnum.INTERGENIC, NA_REFSEQ]
        logging_counter[ANTISENSE_STRAND][antisense_annotation[0]] += 1
        res[reg][ANTISENSE_STRAND] = antisense_annotation
    logging.info("Loaded Refseq Annotations: %s" % pformat(logging_counter))
    return res
