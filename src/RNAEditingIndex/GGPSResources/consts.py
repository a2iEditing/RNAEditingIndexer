from data_structs import Site, RefSeq

__author__ = 'Hillel'
'''
This file contains constants found across the project
'''
# =====================imports=====================#
import operator

# ====================="Enums"=====================#
# region Possible Mismatches
# list of mismatches option - please use these to create uniformity

class MismatchesAndRefsEnum(object):
    A2G = 'A2G'
    A2T = 'A2T'
    A2C = 'A2C'
    G2A = 'G2A'
    G2T = 'G2T'
    G2C = 'G2C'
    T2A = 'T2A'
    T2G = 'T2G'
    T2C = 'T2C'
    C2A = 'C2A'
    C2G = 'C2G'
    C2T = 'C2T'
    A = 'A'
    C = 'C'
    G = 'G'
    T = 'T'
    UNKNOWN = "Unknown"
    CANONICAL = "Canonical"
    MM_SEP = "2"

    ALL_MISMATCHES = [A2C, A2G, A2T, C2A, C2G, C2T, G2A, G2C, G2T, T2A, T2C, T2G]
    UNSTRANDED_MISMATCHES = [A2C, A2G, A2T, C2A, C2G, C2T]
    ALL_REFS = [A, C, G, T]

    COMPLEMENTARY_REF = {
        A: T,
        C: G,
        G: C,
        T: A
    }
    COMPLEMENTARY_MM = {
        A2C: T2G,
        A2G: T2C,
        A2T: T2A,
        C2A: G2T,
        C2G: G2C,
        C2T: G2A,
        G2A: C2T,
        G2C: C2G,
        G2T: C2A,
        T2A: A2T,
        T2C: A2G,
        T2G: A2C
    }

    REFS_TRANSLATE = {
        'a': A,
        'c': C,
        'g': G,
        't': T,
        'A': A,
        'C': C,
        'G': G,
        'T': T
    }

    MISMATCH_TYPE_TRANSLATE = {
        'AC': A2C,
        'A2C': A2C,
        'AG': A2G,
        'A2G': A2G,
        'AT': A2T,
        'AU': A2T,
        'A2T': A2T,
        'A2U': A2T,
        'CA': C2A,
        'C2A': C2A,
        'CG': C2G,
        'C2G': C2G,
        'CT': C2T,
        'CU': C2T,
        'C2T': C2T,
        'C2U': C2T,
        'GA': G2A,
        'G2A': G2A,
        'GC': G2C,
        'G2C': G2C,
        'GT': G2T,
        'GU': G2T,
        'G2T': G2T,
        'G2U': G2T,
        'TA': T2A,
        'UA': T2A,
        'T2A': T2A,
        'U2A': T2A,
        'TC': T2C,
        'UC': T2C,
        'T2C': T2C,
        'U2C': T2C,
        'TG': T2G,
        'U2G': T2G,
        'T2G': T2G,
        'UG': T2G,
    }

    HE_NOT_STRANDED_TRANSFORM_DICT = {
        A2C: A2C,
        A2G: A2G,
        A2T: A2T,
        C2A: C2A,
        G2A: G2A,
        G2C: G2C,
        G2T: C2A,
        T2A: A2T,
        T2G: A2C,
        T2C: A2G,
        C2G: G2C,
        C2T: G2A,
    }

    UNSTRANDED_TRANSFORM_DICT = {
        A2C: A2C,
        A2G: A2G,
        A2T: A2T,
        C2A: C2A,
        C2G: C2G,
        C2T: C2T,
        G2A: C2T,
        G2C: C2G,
        G2T: C2A,
        T2A: A2T,
        T2G: A2C,
        T2C: A2G,
    }


# endregion

# =====================consts=====================#
# used in general_functions.load_groups_and_samples_from_file (here for accessibility)
GROUPS_FILE_SAMPLE_NAME_HEADER = "Sample"
GROUPS_FILE_SAMPLE_PATH_HEADER = "SamplePath"
GROUPS_FILE_GROUP_NAME_HEADER = "Group"
GROUPS_FILE_PARENT_GROUP_HEADER = "ParentGroup"

# region Various Annotations
SENSE_STRAND = "+"
ANTISENSE_STRAND = "-"
UNKNOWN_STRAND = "Unknown"

POSSIBLE_STRANDS = [SENSE_STRAND, ANTISENSE_STRAND, UNKNOWN_STRAND]

# empty sequence for example when there's insertion or deletion
EMPTY_SEQ = "-"

UNKNOWN = "Unknown"
NA = "na"
ERROR_VAL = "ErrorValue"
ALL = "all"
MHC_CLASS_I = "MHC_Class_I"
MHC_CLASS_II = "MHC_Class_II"

# region Statistical Tests Related
# a common descriptor for "extra_data" atts.
STATISTICS_DATA = "StatisticalTestsResults"

GENERAL_TEST = "General_P_Value"
WILCOX = "Wilcox"
TTEST = "T-test"
FISHER = "Fisher"
BONFERRONI_P_TEST = "Bonferroni_Correction"
BH_P_TEST = "Benjamini-Hochberg_Correction"
OBJECTIVE_VALUE = "Objective"
# endregion

# region miRNA related
MIR_NAME = "miRNA_Name"
MATURE_MIR_POS = "Mature_miRNA_Pos"
PRE_MIR_POS = "Pre_miRNA_Pos"
# endregion

# region Outputer Headers and Names
# site
GENOMIC_REGION = "GenomicRegion"  # e.g. chr1, mir-22b
SITE_START = "Start"
SITE_END = "End"
SITE_STRAND = "Strand"
# mismatch and coverage data
MISMATCH_TYPE = "MismatchType"
MISMATCH_PREVALENCE = "MismatchPrevalence"
MISMATCH_RATE = "MismatchRate"
TOTAL_READS = "TotalFragments"
MISMATCHED_READS = "FragmentsWithMismatch"
CANONICAL_READS = "RefIdenticalFragments"
# sample data
GROUP = "Group"
SAMPLE = "Sample"
SAMPLE_PATH = "SamplePath"

# MHC data
MHC_ALLELE = "MHCAllele"
MHC_CLASS = "MHCClass"
MHC_LOCUS = "MHCLocus"
MHC_PREVALENCE = "MHCPrevalence"

DATA_SOURCE = "DataSource"

RECORD_HEADER_FORMAT = "%(record_name)s_%(data_type)s"
# endregion

# endregion

# region Logical Operators
NOT_OPERATOR = "Not"
OR_OPERATOR = "Or"
AND_OPERATOR = "And"
LOGICAL_OPERATORS = {
    NOT_OPERATOR: operator.not_,
    AND_OPERATOR: operator.and_,
    OR_OPERATOR: operator.or_
}
# endregion

# region Common Messages
IFILE_READ_ERR = "Could Not Open Input File %s!"
IFILE_CONVERT_ERR = "Could Not Convert Input File %s!"
IFILE_UNKNOWN_GROUP_WRN_MSG = "File has no matching group, skipping! (File: %s, Group Found: %s)"
IFILE_UNKNOWN_SAMPLE_WRN_MSG = "File has no matching sample, skipping! (File: %s, Sample Found: %s)"
NO_OUTPUT_DETECTED = "No Output Was Detected In %s For Conversion!"
# endregion

# region NA Data Structs
NA_SITE = Site(NA, NA, NA, NA)
NA_REFSEQ = RefSeq(NA_SITE, {}, NA, NA)
# endregion
