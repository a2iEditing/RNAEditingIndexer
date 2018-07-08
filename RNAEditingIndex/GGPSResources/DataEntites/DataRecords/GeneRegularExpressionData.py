__author__ = 'Hillel'
# =====================imports=====================#
# region Builtin Imports
from collections import namedtuple
import operator
# endregion

# region Internal Imports
from RNAEditingIndex.GGPSResources.consts import NA
from RNAEditingIndex.GGPSResources.data_structs import Site

from ..DataRecords.RegionsData import RegionsData


# endregion

# =====================constants===================#

# =====================classes=====================#
# noinspection PyClassHasNoInit
class GeneRegularExpression(namedtuple("GeneRegularExpression", "site average_rfpkms common_name")):
    """
    This holds the mismatch rate for a sample for a sites.
    :ivar Site site: the site of the gene.
    :ivar list[float] average_rfpkms: The average RFKPMs of the gene.
    :ivar str common_name: The gene common name (e.g. NR_075077.1).
    """
    __slots__ = ()


class GeneRegularExpressionData(RegionsData):
    """
    This class holds gene expression data .
    """

    GENE_EXPRESSION_NOT_FOUND = -1

    def add_site(self, region, start, end, strand, average_rfpkms=[], common_name=NA, connected_region_region_name=NA,
                 connected_region_start=0, connected_region_end=0, connected_region_strand=NA, ):
        # type: (str, int, int, str, list, str) -> None
        """
        This updates the genomic_function sites dictionary with new mismatch sites *overriding prev values*
        :param str region: The chromosome (or transcript name)
        :param int start: start position
        :param int end: end position
        :param str strand: the strand of the site
        :param list[float] average_rfpkms: The average RFKPMs of the gen
        :param str common_name: The gene common name (e.g. WASH7P).
        :param str connected_region_region_name: The chromosome (or transcript name) of the genomic region containing this position.
        :param int connected_region_start: The start position of the genomic region containing this position.
        :param int connected_region_end: The end position of the genomic region containing this position.
        :param str connected_region_strand: The end position of the genomic region containing this position.

        :return: None
        """
        start = int(start)
        end = int(end)
        site = Site(region, start, end, strand)
        gene_exp = GeneRegularExpression(site=site, average_rfpkms=average_rfpkms, common_name=common_name)

        reg_start = int(connected_region_start)
        reg_end = int(connected_region_end)
        reg_site = Site(connected_region_region_name, reg_start, reg_end,
                        connected_region_strand)

        super(GeneRegularExpressionData, self).add_site(region=region, start=start, end=end, strand=strand,
                                                        region_data=gene_exp, connected_region=reg_site)

    def get_gavg_rfkpm(self, region, start, end, strand, connected_region=None):
        # type: (str, int, int, str) -> float
        """
        Returns the geometrical average of the expression levels.
        :param str region: The chromosome (or transcript name)
        :param int start: start position
        :param int end: end position
        :param str strand: the strand of the site
        :param Site connected_region: A site connected to this record
        :return: float
        """
        if connected_region:
            data = self.get_connected_region_data(connected_region)
            if [] == data:
                return GeneRegularExpressionData.GENE_EXPRESSION_NOT_FOUND
            else:
                data = data[0]
        else:
            data = self.get_region_data(region=region, start=start, end=end, strand=strand)
            if not isinstance(data, GeneRegularExpression):
                return GeneRegularExpressionData.GENE_EXPRESSION_NOT_FOUND
        """:type data GeneRegularExpression"""
        return reduce(operator.mul, data.average_rfpkms) ** (1.0 / len(data.average_rfpkms))
