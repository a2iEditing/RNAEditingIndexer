__author__ = 'Shalom Hillel Roth'
"""
This module contains simple DS commonly used across various classes.
recommended usages are found in each class' docs.
"""
# =====================imports=====================#
from collections import namedtuple


# =====================classes=====================#

# noinspection PyClassHasNoInit
class Site(namedtuple("Site", "region start end strand")):
    """
    This hold the coordinates for a mismatch site.
    :ivar str mismatch_type: The type of the mismatch. *only from from MismatchesTypesEnum!*
    :ivar str chromosome: The chromosome (or transcript name)
    :ivar int start: start position
    :ivar int end: end position
    :ivar str strand: the strand of the site
    """
    __slots__ = ()

    def __str__(self):
        return "Coordinate: %s:%s-%s; Strand: %s" % (self.region, self.start, self.end, self.strand)


# noinspection PyClassHasNoInit
class RefSeqPosEnum(str):
    """
    Enum for position in genome.
    """
    __slots__ = ()

    EXONIC = "Exonic"
    INTERGENIC = "Intergenic"
    INTRONIC = "Intronic"

    ALL_ANNOTATIONS = [EXONIC, INTRONIC, INTERGENIC]

    __HIERARCHY_D = {EXONIC: 3, INTRONIC: 2, INTERGENIC: 1}
    __HIERARCHY_D_REVERSE = {3: EXONIC, 2: INTRONIC, 1: INTERGENIC}

    @staticmethod
    def stronger_annotation(this, other):
        return RefSeqPosEnum.__HIERARCHY_D_REVERSE[
            max(RefSeqPosEnum.__HIERARCHY_D[this], RefSeqPosEnum.__HIERARCHY_D[other])]


# noinspection PyClassHasNoInit
class RefSeq(namedtuple("RefSeq", "site exons refseq_name common_name")):
    """
    This holds the mismatch rate for a sample for a sites.
    :ivar Site site: the site of the SNP.
    :ivar dict[int, int] exons: The exons indexes (start=>end, relative to '+' strand).
    :ivar str refseq_name: The gene RefSeq name (e.g. NR_075077.1).
    :ivar str common_name: The gene common name (e.g. C1orf141).
    """
    __slots__ = ()


# noinspection PyClassHasNoInit
class SNP(namedtuple("SNP", "site prevalence function reference_seq snp_seq")):
    """
    This holds the mismatch rate for a sample for a sites.
    :ivar Site site: the site of the SNP.
    :ivar float prevalence: The prevalence of the reference.
    :ivar str function: the function of this region (e.g. intergenic)
    :ivar str reference_seq: the reference sequence
    :ivar str snp_seq: the SNP sequence
    """
    __slots__ = ()
