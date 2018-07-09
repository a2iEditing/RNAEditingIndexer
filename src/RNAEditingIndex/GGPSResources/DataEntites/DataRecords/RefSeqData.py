__author__ = 'Hillel'
# =====================imports=====================#
# region Builtin Imports
# endregion

# region Internal Imports
from RNAEditingIndex.GGPSResources.consts import NA
from RNAEditingIndex.GGPSResources.data_structs import Site, RefSeqPosEnum, RefSeq

from RegionsData import RegionsData


# endregion

# =====================constants===================#

# =====================classes=====================#


class RefSeqData(RegionsData):
    """
    This class holds RefSeq data.
    C{dict} of C{str} to C{dict} of C{int} to C{dict} of C{int} to  C{list} of L{SampleMMRate}
    :ivar source_name: The source of the data.
    :type source_name: C{str}
    """

    def __init__(self, source_name, refseq_source, genome):
        """
        :param str source_name: The (data-wise) origin of the data.
        :param str refseq_source: The origin of the SNPsData data.
        :param str genome: The genome.
        """
        if hasattr(self, "source_name"):
            return

        super(RefSeqData, self).__init__(source_name=source_name)

        self.refseq_source = refseq_source
        self.genome = genome

    def add_site(self, region, start, end, strand, connected_region_region_name=NA, connected_region_start=0,
                 connected_region_end=0,
                 connected_region_strand=NA, exons_starts=[], exons_ends=[], refseq_name=NA, common_name=NA, ):
        # type: (str, int, int, str, list, list, str, str) -> None
        """
        This genomic_function updates the sites dictionary with new mismatch sites *overriding prev values*
        :param str region: The chromosome (or transcript name)
        :param int start: start position
        :param int end: end position
        :param str strand: the strand of the site
        :param list[int] exons_starts: the *sorted* positions of exons starts
        :param list[int] exons_ends: the *sorted* positions of exons ends
        :param str refseq_name: The gene RefSeq name (e.g. NR_075077.1).
        :param str common_name: The gene common name (e.g. NR_075077.1).
        :param str connected_region_region_name: The chromosome (or transcript name) of the genomic region containing this position.
        :param int connected_region_start: The start position of the genomic region containing this position.
        :param int connected_region_end: The end position of the genomic region containing this position.
        :param str connected_region_strand: The end position of the genomic region containing this position.
        :return: None
        """
        start = int(start)
        end = int(end)
        site = Site(region, start, end, strand)
        exons = {int(e_start): int(e_end) for e_start, e_end in zip(exons_starts, exons_ends) if e_start}

        reg_start = int(connected_region_start)
        reg_end = int(connected_region_end)
        reg_site = Site(connected_region_region_name, reg_start, reg_end,
                        connected_region_strand)
        refseq = RefSeq(site=site, exons=exons, refseq_name=refseq_name, common_name=common_name)
        old_refseq_data = super(RefSeqData, self).get_region_data(region=region, start=start, end=end, strand=strand)
        refseq_data = dict() if old_refseq_data is None else old_refseq_data
        refseq_data[refseq_name] = refseq

        super(RefSeqData, self).add_site(region=region, start=start, end=end, strand=strand, region_data=refseq_data,
                                         connected_region=reg_site)

    def get_site_genomic_annotation(self, region, start, end, strand, connected_region=NA):
        # type: (str, int, int, str) -> list
        """
        This function retrieves the annotation of a site
        :param str region: The chromosome (or transcript name)
        :param int start: start position
        :param int end: end position
        :param str strand: the strand of the site
        :return list[RefSeq, RefSeqPosEnum]: The annotation if found, else NA
        """
        na_refseq = RefSeq(Site(NA, NA, NA, NA), {}, NA, NA)
        if connected_region:
            self_sites = dict()
            exons_data = self.get_connected_region_data(connected_region=connected_region)
            for exon in exons_data:
                """:type exon RefSeq"""
                self_sites.setdefault(exon.site.region, {}).setdefault(exon.site.start, {}).setdefault(exon.site.end,
                                                                                                       {})[
                    exon.site.strand] = exon
        else:
            self_sites = self.get_sites(dont_filter=True)
        exon_data = None
        if region not in self_sites:
            return [NA, na_refseq]
        region_d = self_sites[region]
        if start in region_d:
            start_d = region_d[start]
            if end in start_d:
                if strand in start_d[end]:
                    return [RefSeqPosEnum.GENE, self_sites[region][start][end][strand]]
                else:
                    return [RefSeqPosEnum.INTERGENIC, na_refseq]
            else:
                for e in sorted(start_d):
                    if e > end:
                        if strand in start_d[e]:
                            exon_data = super(RefSeqData, self).get_region_data(region, start, end, strand)
                        else:
                            return [RefSeqPosEnum.INTERGENIC, na_refseq]
        else:
            for s in sorted(region_d, reverse=True):
                if s < start:
                    start_d = region_d[s]
                    if end in start_d:
                        if strand in start_d[end]:
                            exon_data = super(RefSeqData, self).get_region_data(region, s, end, strand)
                        else:
                            return [RefSeqPosEnum.INTERGENIC, na_refseq]
                    else:
                        for e in sorted(start_d):
                            if e > end:
                                if strand in start_d[e]:
                                    exon_data = super(RefSeqData, self).get_region_data(region, s, e, strand)
                                else:
                                    return [RefSeqPosEnum.INTERGENIC, na_refseq]
        if exon_data:
            """:type exon_data RefSeq"""
            for e_start in sorted(exon_data.exons, reverse=True):  # this means we have position inside a gene
                if e_start <= start:
                    if exon_data.exons[e_start] >= end:
                        return [RefSeqPosEnum.EXONIC, exon_data]
                    else:
                        return [RefSeqPosEnum.INTRONIC, exon_data]

            return [RefSeqPosEnum.INTRONIC, exon_data]

        return [NA, na_refseq]

    def get_connected_region_genomic_annotation(self, strand, connected_region, allow_partial_overlaps=False):
        # type: (str, Site) -> list
        """
        This function retrieves the annotation of a site
        :param Site connected_region:
        :param str strand: the strand of the site
        :return list[RefSeq, RefSeqPosEnum]: The annotation if found, else NA
        """
        na_refseq = RefSeq(Site(NA, NA, NA, NA), {}, NA, NA)

        exons_data_c = self.get_connected_region_data(connected_region=connected_region)
        exons_data = None

        for refseq_d in exons_data_c:
            for refseq in refseq_d.values():
                """:type refseq RefSeq"""
                if refseq.site.strand == strand:
                    exons_data = refseq_d
                    break
            if exons_data:
                break

        annotation = RefSeqPosEnum.INTERGENIC
        if exons_data:
            """:type exon_data dict"""
            for exon_data in exons_data.values():
                annotation = RefSeqPosEnum.INTRONIC
                exons_sorted = sorted(exon_data.exons, reverse=True)
                num_of_exons = len(exon_data)
                for i, e_start in enumerate(exon_data):  # this means we have position inside a gene
                    if annotation == RefSeqPosEnum.EXONIC:
                        break
                    if e_start <= connected_region.start:
                        if exon_data.exons[e_start] >= connected_region.end:
                            annotation = RefSeqPosEnum.EXONIC
                            break
                        else:
                            if allow_partial_overlaps and exon_data.exons[e_start] >= connected_region.start:
                                for e_i in xrange(i + 1, num_of_exons - 1):
                                    if exons_sorted[e_i] >= connected_region.start:
                                        annotation = RefSeqPosEnum.EXONIC
                                        break
                        break
                if annotation == RefSeqPosEnum.EXONIC:
                    break

        else:
            exon_data = na_refseq

        return [annotation, exon_data]
