__author__ = 'Hillel'
# =====================imports=====================#
# region Builtin Imports
# endregion

# region Internal Imports
from ....GGPSResources.consts import NA
from ....GGPSResources.general_functions import convert_params_to_bool_dict, deep_copy_dict

from ..BaseClasses.DataRecord import DataRecord


# endregion

# =====================constants===================#

# =====================classes=====================#

class RegionsData(DataRecord):
    """
    This class holds the mismatches from a data source.
    :ivar __regions_data_by_sites: (get - mismatch_sites, to add sites or remove use - add/remove_sites) the sites dict.
        <mismatch type> ><Chr/Transcript name>:<start>:<end>:<strand>:[SampleMMRate(s)]
    :type __regions_data_by_sites: C{dict} of C{str} to
    C{dict} of C{int} to C{dict} of C{int} to C{dict} of C{str} to C{dict} of C{str} to C{list} of L{SampleMMRate}
    :ivar source_name: The source of the data.
    :type source_name: C{str}
    """

    def dump_me(self):
        pass

    def __init__(self, source_name):
        """
        :param source_name: The (data-wise) origin of the data.
        :type source_name: C{str}
        """
        if hasattr(self, "source_name"):
            return
        self.source_name = source_name
        self.__regions_data_by_sites = dict()
        self.__region_data_by_connected_region = dict()

    def add_site(self, region, start, end, strand, region_data=NA, connected_region=NA, *args):
        # type: (str, int, int, str, object) -> None
        """
        This function updates the sites dictionary with new mismatch sites *overriding prev values*
        :param str region: The chromosome (or transcript name)
        :param int start: start position
        :param int end: end position
        :param str strand: the strand of the site
        :param Site connected_region: A region connected to this record
        :param object region_data: The data about the region.
        :return: None
        """

        start = int(start)
        end = int(end)
        self.__regions_data_by_sites.setdefault(region, {}).setdefault(start, {}).setdefault(end, {})[
            strand] = region_data
        if region_data not in self.__region_data_by_connected_region.get(connected_region, []):
            self.__region_data_by_connected_region.setdefault(connected_region, []).append(region_data)

    @property
    def connected_regions(self):
        return list(self.__region_data_by_connected_region.keys())

    def get_sites(self, dont_filter=True, chromosomes=None, starts=None, ends=None, strands=None, *args):
        """
        Retrieves the sites.
        :param dont_filter: A flag. if set will retrieving a simple copy without filtration. Use to save run-time.
        :param chromosomes: if given will return only mismatches that are inside this chromosomes.
        :param starts: if given will return only mismatches that match starts.
        :param ends: if given will return only mismatches that match ends.
        :param strands: if given will return only mismatches that match strands.
        :return: the sites relevant in the same structure as the calls dict.
        """
        chromosomes_d = convert_params_to_bool_dict(chromosomes)
        starts_d = convert_params_to_bool_dict(starts)
        ends_d = convert_params_to_bool_dict(ends)
        strands_d = convert_params_to_bool_dict(strands)
        filtered_copy = deep_copy_dict(self.__regions_data_by_sites)
        if dont_filter:
            return filtered_copy

        for chrom, chrom_d in self.__regions_data_by_sites.iteritems():
            if chromosomes and not chromosomes_d.get(chrom, False):
                _ = filtered_copy.pop(chrom)
                continue
            for st, st_d in chrom_d.iteritems():
                if starts and not starts_d.get(st, False):
                    _ = chrom_d.pop(st)
                    continue
                for e, e_d in st_d.iteritems():
                    if ends and not ends_d.get(e, False):
                        _ = st_d.pop(e)
                        continue
                    for strand, mm_dict in st_d.iteritems():
                        if strands and not strands_d.get(strand, False):
                            _ = st_d.pop(e)
                            continue

        return filtered_copy

    def get_region_data(self, region, start, end, strand):
        # type: (str, int, int, str) -> object
        """
        This function retrieves data of a specific region.
        :param str region: The chromosome (or transcript name)
        :param int start: start position
        :param int end: end position
        :param str strand: the strand of the site
        :return object: The region data if found, else - None
        """
        data = None

        try:
            data = self.__regions_data_by_sites[region][start][end][strand]
        except KeyError:
            pass

        return data

    def get_connected_region_data(self, connected_region):
        # type: (str, int, int, str) -> object
        """
        This function retrieves data of a specific region.
        :param Site connected_region: A region connected to this record
        :return list: The region data if found, else - []
        """
        data = []

        try:
            data = self.__region_data_by_connected_region[connected_region]
        except KeyError:
            pass

        return data
