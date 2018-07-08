__author__ = 'Hillel'
# =====================imports=====================#
# region Builtin Imports
# endregion

# region Internal Imports
from RNAEditingIndex.GGPSResources.consts import NA
from RNAEditingIndex.GGPSResources.data_structs import Site, SNP

from RegionsData import RegionsData
# endregion

# =====================constants===================#
# =====================classes=====================#


class SNPsData(RegionsData):
    """
    This class holds SNPsData data .
    C{dict} of C{str} to C{dict} of C{int} to C{dict} of C{int} to  C{list} of L{SampleMMRate}
    :ivar source_name: The source of the data.
    :type source_name: C{str}
    """

    def __init__(self, source_name, snps_source, genome):
        """
        :param str source_name: The (data-wise) origin of the data.
        :param str snps_source: The origin of the SNPsData data.
        :param str genome: The genome.
        """
        if hasattr(self, "source_name"):
            return

        super(SNPsData, self).__init__(source_name=source_name)

        self.snps_source = snps_source
        self.genome = genome

    def add_site(self, region, start, end, strand, snp_seq="", reference_seq="", ref_prevalence=NA, genomic_function=NA,
                 connected_region_region_name=NA, connected_region_start=0, connected_region_end=0,
                 connected_region_strand=NA):
        """
        This genomic_function updates the sites dictionary with new mismatch sites *overriding prev values*
        :param str region: The chromosome (or transcript name)
        :param int start: start position
        :param int end: end position
        :param str strand: the strand of the site
        :param str snp_seq: the SNP sequence
        :param str reference_seq: the reference sequence
        :param float ref_prevalence: The prevalence of the reference sequence.
        :param str genomic_function: the genomic_function of this region (e.g. intergenic)
        :param str connected_region_region_name: The chromosome (or transcript name) of the genomic region containing this position.
        :param int connected_region_start: The start position of the genomic region containing this position.
        :param int connected_region_end: The end position of the genomic region containing this position.
        :param str connected_region_strand: The end position of the genomic region containing this position.
        :return: None
        """
        start = int(start)
        end = int(end)
        site = Site(region, start, end, strand)
        ref_prevalence = float(ref_prevalence)
        snp = SNP(site=site, prevalence=ref_prevalence, function=genomic_function,
                  reference_seq=reference_seq, snp_seq=snp_seq)

        old_snps_data = super(SNPsData, self).get_region_data(region=region, start=start, end=end, strand=strand)
        snps_data = dict() if old_snps_data is None else old_snps_data
        snps_data[snp_seq] = snp
        reg_start = int(connected_region_start)
        reg_end = int(connected_region_end)
        reg_site = Site(connected_region_region_name, reg_start, reg_end,
                        connected_region_strand)
        super(SNPsData, self).add_site(region=region, start=start, end=end, strand=strand, region_data=snps_data,
                                       connected_region=reg_site)
