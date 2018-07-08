__author__ = 'Hillel'
"""
This module contains the consts for the editing index.
"""
# region Builtin Imports
import os

# endregion

# region Internal Imports
# endregion

# region Mismatches & Coverage Keys and Headers
COVERAGE_AT_N_POSITIONS_FORMAT = "TotalCoverageAt%sPositions"

NUM_OF_N_SITES_COVERED_FORMAT = "NumOf%sPositionsCovered"

NUM_OF_MM_FORMAT = "NumOf%sMismatches"
SNPS_NUM_OF_MM_FORMAT = "NumOf%sMismatchesAtSNPs"

NUM_OF_MM_SITES_FORMAT = "NumOf%sMismatchesSites"
SNPS_NUM_OF_MM_SITES_FORMAT = "NumOf%sMismatchesSitesAtSNPs"

NUM_OF_CANONICAL_FORMAT = "NumOf%s"

EDITING_INDEX_FORMAT = "%sEditingIndex"

INDEXED_EDITED_FORMAT = "IndexedMismatchesOf%s"
STRANDED_INDEXED_EDITED_FORMAT = "IndexedMismatchesOf%sOn%sStrand"
REGIONED_INDEXED_EDITED_FORMAT = "IndexedMismatchesOf%sFrom%sRegions"
SUMMERY_G_REGIONED_INDEXED_EDITED_FORMAT = "IndexedMismatchesFrom%sRegions"
SUMMERY_G_STRANDED_INDEXED_EDITED_FORMAT = "IndexedMismatchesOn%sStrand"

INDEXED_CANONICAL_FORMAT = "IndexedCoverageOf%s"
STRANDED_INDEXED_CANONICAL_FORMAT = "IndexedCoverageOf%sOn%sStrand"
REGIONED_INDEXED_CANONICAL_FORMAT = "IndexedCoverageOf%sFrom%sRegions"
SUMMERY_G_STRANDED_INDEXED_CANONICAL_FORMAT = "IndexedCoverageOn%sStrand"
SUMMERY_G_REGIONED_INDEXED_CANONICAL_FORMAT = "IndexedCoverageFrom%sRegions"

NUM_OF_INDEXED_MM_SITES_FORMAT = "NumOfIndexedMismatchesSitesOf%s"
STRANDED_NUM_OF_INDEXED_MM_SITES_FORMAT = "NumOfIndexedMismatchesSitesOf%sOn%sStrand"
REGIONED_NUM_OF_INDEXED_MM_SITES_FORMAT = "NumOfIndexedMismatchesSitesOf%sFrom%sRegions"
SUMMERY_G_REGIONED_NUM_OF_INDEXED_MM_SITES_FORMAT = "NumOfIndexedMismatchesSitesFrom%sRegions"
SUMMERY_G_STRANDED_NUM_OF_INDEXED_MM_SITES_FORMAT = "NumOfIndexedMismatchesSitesOn%sStrand"

NUM_OF_INDEXED_OVERALL_SITES_FORMAT = "NumOfIndexedOverallSitesOf%s"
STRANDED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT = "NumOfIndexedOverallSitesOf%sOn%sStrand"
REGIONED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT = "NumOfIndexedOverallSitesOf%sFrom%sRegions"
SUMMERY_G_STRANDED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT = "NumOfIndexedOverallSitesOn%sStrand"
SUMMERY_G_REGIONED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT = "NumOfIndexedOverallSitesFrom%sRegions"

NUM_OF_REGIONS = "NumOfRegionsWithCoverageFor%s"
STRANDED_NUM_OF_REGIONS = "NumOfRegionsWithCoverageFor%sOn%sStrand"
REGIONED_NUM_OF_REGIONS = "NumOfRegionsWithCoverageFor%sFrom%sRegions"
SUMMERY_G_STRANDED_NUM_OF_REGIONS = "NumOfRegionsWithCoverageOn%sStrand"
SUMMERY_G_REGIONED_NUM_OF_REGIONS = "NumOfRegionsWithCoverageFrom%sRegions"

STRAND_DECIDING_METHOD = "StrandDecidingMethod"

SUMMERY_RANK_FORMAT = "RankFor%sEditingIndex"
# endregion

# region Paths Formats
BUILTIN_GENOMES = {
    "hg19": os.path.join("%(script_dir)s", "Resources", "Genomes", "HomoSapiens", "hg19.fa"),
    "hg38": os.path.join("%(script_dir)s", "Resources", "Genomes", "HomoSapiens", "hg38.fa"),
    "mm9": os.path.join("%(script_dir)s", "Resources", "Genomes", "MusMusculus", "mm9.fa"),
    "mm10": os.path.join("%(script_dir)s", "Resources", "Genomes", "MusMusculus", "mm10.fa"),
}
BUILTIN_REGIONS = {
    "hg19_Alu": os.path.join("%(script_dir)s", "Resources", "Regions", "HomoSapiens", "ucscHg19Alu.bed.gz"),
    "hg38_Alu": os.path.join("%(script_dir)s", "Resources", "Regions", "HomoSapiens", "ucscHg38Alu.bed.gz"),
    "mm9_SINE_B1_B2": os.path.join("%(script_dir)s", "Resources", "Regions", "MusMusculus", "mm9_SINE_A_B.bed"),
    "mm10_SINE_B1_B2": os.path.join("%(script_dir)s", "Resources", "Regions", "MusMusculus", "mm10_SINE_A_B.bed"),
}
BUILTIN_REFSEQS = {
    "hg19": os.path.join("%(script_dir)s", "Resources", "Annotations", "HomoSapiens",
                         "ucsucHg19RefSeqRefGene.bed.gz"),
    "hg38": os.path.join("%(script_dir)s", "Resources", "Annotations", "HomoSapiens",
                         "ucscHg38RefSeqCurated.bed.gz"),
    "mm9": os.path.join("%(script_dir)s", "Resources", "Annotations", "MusMusculus", "mm9_SINE_A_B.bed"),
    "mm10": os.path.join("%(script_dir)s", "Resources", "Annotations", "MusMusculus", "mm10_SINE_A_B.bed"),
}
BUILTIN_SNPsDB = {
    "hg19": os.path.join("%(script_dir)s", "Resources", "Annotations", "HomoSapiens",
                         "ucscHg19CommonGenomicSNPs150.bed.gz"),
    "hg38": os.path.join("%(script_dir)s", "Resources", "Annotations", "HomoSapiens",
                         "ucscHg38CommonGenomicSNPs150.bed.gz"),
    "mm9": os.path.join("%(script_dir)s", "Resources", "Annotations", "MusMusculus", "mm9_SINE_A_B.bed"),
    "mm10": os.path.join("%(script_dir)s", "Resources", "Annotations", "MusMusculus", "mm10_SINE_A_B.bed"),
}
BUILTIN_GENE_EXP = {
    "hg19": os.path.join("%(script_dir)s", "Resources", "Annotations", "HomoSapiens",
                         "ucscHg19GTExGeneExpression.bed.gz"),
    "hg38": os.path.join("%(script_dir)s", "Resources", "Annotations", "HomoSapiens",
                         "ucscHg38GTExGeneExpression.bed.gz"),
    "mm9": os.path.join("%(script_dir)s", "Resources", "Annotations", "MusMusculus", "mm9_SINE_A_B.bed"),
    "mm10": os.path.join("%(script_dir)s", "Resources", "Annotations", "MusMusculus", "mm10_SINE_A_B.bed"),
}
DEFAULTS_CONFIG_PATH_FORMAT = os.path.join("%(script_dir)s", "Resources", "Configs", "DefaultsConfig.ini")
FULL_CONFIG_PATH_FORMAT = os.path.join("%(script_dir)s", "Resources", "Configs", "FullConfig.ini")
# endregion


# region EIConfig Consts
GENOME_FASTA_OPTION = "genome_fasta"
REGIONS_BED_OPTION = "regions_coordinates_bed"
BAM_FILE_SUFFIX_OPTION = "bam_file_suffix"
IN_BAM_FILE_OPTION = "input_bam_file"
ALIGNER_OUT_FORMAT = "aligner_output_format"
SAMTOOLS_PATH_OPTION = "samtools_path"
BEDTOOLS_PATH_OPTION = "bedtools_path"
OVERALL_MAX_PROCESSES_NUM_OPTION = "overall_max_processes_num"
REGIONS_PILEUP_COUNT = "regions_pileup_with_count"
GENOME_INDEX_PATH = "genome_index_path"
# endregion

# region EditingIndexJavaUtils Consts
ORIG_REG_SEP = "#"
# endregion
