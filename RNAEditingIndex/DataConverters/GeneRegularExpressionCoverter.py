__author__ = 'Hillel'
"""
This module loads a gzipped DB RefSeqData file of the tab format (the format is as found in the UCSC Genome Browser,
 a header is assumed to be present):
1.	Chromosome
2.	Start (0-based)
3.	End
4.	Gene Common name (e.g. C1orf141)
5.	Average RFKPMs (each average refers to a single tissue) separated by ","
6.	Strand
"""
# =====================imports=====================#
# region Builtin Import
import os
# endregion

# region InternalImports
from RNAEditingIndex.GGPSResources.DataEntites.DataRecords import GeneRegularExpressionData

# endregion

# =====================constants===================#
UCSC_TABLE_SEP = "\t"
UCSC_SEP = ","

INTERSECT_FORMAT = "%(bedtools)s intersect -a '%(gene_expression_file)s' -b '%(intersect_file)s' -wo -s"


# =====================functions===================#

def load_gene_expression_bed(gene_expression_file, source_name, intersect_first_with=None, bedtools_path="bedtools"):
    # type: (str, str, str, str, str) -> None
    """
    This function loads a RefSeqData DB file
    :param str gene_expression_file: The file in the described format.
    :param str source_name: The source_name to give the instance.
    :param str intersect_first_with: If provided will first intersect SNPs file with it.
    :param str bedtools_path: The run-path of bedtools.
    :return None
    """
    gene_exp_fh = os.popen(INTERSECT_FORMAT % dict(bedtools=bedtools_path, gene_expression_file=gene_expression_file,
                                                   intersect_file=intersect_first_with))

    gene_exp = GeneRegularExpressionData(source_name=source_name)
    for line in gene_exp_fh:
        chrom, start, end, common_name, rfpkms, strand, reg_chrom, reg_start, reg_end, refseq_name, common_name, reg_strand, e_starts, e_ends, count = line.strip(
            "\n").split(UCSC_TABLE_SEP)
        rfpkms = [float(rfpkm) for rfpkm in rfpkms.strip().split(UCSC_SEP) if rfpkm]
        gene_exp.add_site(region=chrom,
                          start=start,
                          end=end,
                          strand=strand,
                          average_rfpkms=rfpkms,
                          common_name=common_name,
                          connected_region_region_name=reg_chrom,
                          connected_region_start=reg_start,
                          connected_region_end=reg_end,
                          connected_region_strand=reg_strand
                          )
