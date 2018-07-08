# region Builtin Imports
import argparse
import os
import sys

from collections import OrderedDict
# endregion

# region Internal Imports
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from EditingIndexConsts import SUMMERY_G_STRANDED_INDEXED_EDITED_FORMAT, \
    SUMMERY_G_STRANDED_INDEXED_CANONICAL_FORMAT, SUMMERY_G_STRANDED_NUM_OF_INDEXED_MM_SITES_FORMAT, \
    SUMMERY_G_STRANDED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT, SUMMERY_G_STRANDED_NUM_OF_REGIONS, \
    SUMMERY_G_REGIONED_INDEXED_EDITED_FORMAT, SUMMERY_G_REGIONED_INDEXED_CANONICAL_FORMAT, \
    SUMMERY_G_REGIONED_NUM_OF_INDEXED_MM_SITES_FORMAT, SUMMERY_G_REGIONED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT, \
    SUMMERY_G_REGIONED_NUM_OF_REGIONS, STRAND_DECIDING_METHOD, EDITING_INDEX_FORMAT, REGIONED_INDEXED_EDITED_FORMAT, \
    REGIONED_INDEXED_CANONICAL_FORMAT, REGIONED_NUM_OF_INDEXED_MM_SITES_FORMAT, \
    REGIONED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT, REGIONED_NUM_OF_REGIONS, STRANDED_INDEXED_EDITED_FORMAT, \
    STRANDED_INDEXED_CANONICAL_FORMAT, STRANDED_NUM_OF_INDEXED_MM_SITES_FORMAT, \
    STRANDED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT, STRANDED_NUM_OF_REGIONS, SUMMERY_RANK_FORMAT
from GGPSResources.Outputers.CSVOutputer import CSVOutputer
from GGPSResources.consts import POSSIBLE_STRANDS, GROUP, SAMPLE, SAMPLE_PATH, MismatchesAndRefsEnum, \
    MISMATCH_TYPE
from GGPSResources.data_structs import RefSeqPosEnum
# endregion


def get_index_summery_statistics(index_summery_path, summery_out_path, groups_summery_path):
    # type: (str, str, str, str) -> None
    """
    This function generates a short statistical summery out of the summery output.
    :param str index_summery_path: The path to the summery output.
    :param str summery_out_path: Output path for the summery.
    :param str groups_summery_path: Output path for per group summery.
    :return: None
    """

    csv_outputer = CSVOutputer(append=True, override=False)
    all_recs = dict()
    group_recs = list()
    group_counter = dict()
    group_rank = dict()
    counter_dict = dict()
    for strand in POSSIBLE_STRANDS:
        counter_dict[SUMMERY_G_STRANDED_INDEXED_EDITED_FORMAT % strand] = list()
        counter_dict[SUMMERY_G_STRANDED_INDEXED_CANONICAL_FORMAT % strand] = list()
        counter_dict[SUMMERY_G_STRANDED_NUM_OF_INDEXED_MM_SITES_FORMAT % strand] = list()
        counter_dict[SUMMERY_G_STRANDED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT % strand] = list()
        counter_dict[SUMMERY_G_STRANDED_NUM_OF_REGIONS % strand] = list()
    for region in RefSeqPosEnum.ALL_ANNOTATIONS:
        counter_dict[SUMMERY_G_REGIONED_INDEXED_EDITED_FORMAT % region] = list()
        counter_dict[SUMMERY_G_REGIONED_INDEXED_CANONICAL_FORMAT % region] = list()
        counter_dict[SUMMERY_G_REGIONED_NUM_OF_INDEXED_MM_SITES_FORMAT % region] = list()
        counter_dict[SUMMERY_G_REGIONED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT % region] = list()
        counter_dict[SUMMERY_G_REGIONED_NUM_OF_REGIONS % region] = list()

    with open(index_summery_path) as isp:
        indexes = {header: i for i, header in enumerate(isp.readline().strip().split(","))}
        for line in isp:
            sample_rec = OrderedDict()
            recs = line.strip().split(",")
            group = recs[indexes[GROUP]]
            sample_rec[GROUP] = group
            sample_rec[SAMPLE] = recs[indexes[SAMPLE]]
            sample_rec[SAMPLE_PATH] = recs[indexes[SAMPLE_PATH]]
            strand_d_method = recs[indexes[STRAND_DECIDING_METHOD]]
            group_rank.setdefault(strand_d_method, dict()).setdefault(group, dict())
            sample_rec[STRAND_DECIDING_METHOD] = strand_d_method
            group_counter.setdefault(strand_d_method, dict()).setdefault(group, dict())
            for mm_type in MismatchesAndRefsEnum.UNSTRANDED_MISMATCHES:
                g_count_d = group_counter[strand_d_method][group].setdefault(mm_type, dict())
                group_rank[strand_d_method][group].setdefault(mm_type, dict())
                group_rank[strand_d_method][group][mm_type][float(recs[indexes[EDITING_INDEX_FORMAT % mm_type]])] = \
                    sample_rec[
                        SAMPLE_PATH]

                edited_index_sum = 0
                indexed_canonical_sum = 0
                indexed_mm_sites_sum = 0
                total_indexed_sites_sum = 0
                indexed_regions_sum = 0
                for region in RefSeqPosEnum.ALL_ANNOTATIONS:
                    edited_index_sum += float(recs[indexes[REGIONED_INDEXED_EDITED_FORMAT % (mm_type, region)]])

                    indexed_canonical_sum += float(recs[indexes[REGIONED_INDEXED_CANONICAL_FORMAT % (mm_type, region)]])

                    indexed_mm_sites_sum += float(
                        recs[indexes[REGIONED_NUM_OF_INDEXED_MM_SITES_FORMAT % (mm_type, region)]])

                    total_indexed_sites_sum += float(
                        recs[indexes[REGIONED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT % (mm_type, region)]])

                    indexed_regions_sum += float(recs[indexes[REGIONED_NUM_OF_REGIONS % (mm_type, region)]])

                for region in RefSeqPosEnum.ALL_ANNOTATIONS:
                    fraction = 100 * float(
                        recs[indexes[REGIONED_INDEXED_EDITED_FORMAT % (mm_type, region)]]) / edited_index_sum
                    sample_rec[REGIONED_INDEXED_EDITED_FORMAT % (mm_type, region)] = str(fraction)
                    g_count_d.setdefault(SUMMERY_G_REGIONED_INDEXED_EDITED_FORMAT % region, list()).append(fraction)

                for region in RefSeqPosEnum.ALL_ANNOTATIONS:
                    fraction = 100 * float(
                        recs[indexes[REGIONED_INDEXED_CANONICAL_FORMAT % (mm_type, region)]]) / indexed_canonical_sum
                    sample_rec[REGIONED_INDEXED_CANONICAL_FORMAT % (mm_type, region)] = str(fraction)
                    g_count_d.setdefault(SUMMERY_G_REGIONED_INDEXED_CANONICAL_FORMAT % region, list()).append(fraction)

                for region in RefSeqPosEnum.ALL_ANNOTATIONS:
                    fraction = 100 * float(recs[indexes[
                        REGIONED_NUM_OF_INDEXED_MM_SITES_FORMAT % (mm_type, region)]]) / indexed_mm_sites_sum
                    sample_rec[REGIONED_NUM_OF_INDEXED_MM_SITES_FORMAT % (mm_type, region)] = str(fraction)
                    g_count_d.setdefault(SUMMERY_G_REGIONED_NUM_OF_INDEXED_MM_SITES_FORMAT % region, list()).append(
                        fraction)

                for region in RefSeqPosEnum.ALL_ANNOTATIONS:
                    fraction = 100 * float(recs[indexes[
                        REGIONED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT % (mm_type, region)]]) / total_indexed_sites_sum
                    sample_rec[REGIONED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT % (mm_type, region)] = str(fraction)
                    g_count_d.setdefault(SUMMERY_G_REGIONED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT % region,
                                         list()).append(fraction)

                for region in RefSeqPosEnum.ALL_ANNOTATIONS:
                    fraction = 100 * float(
                        recs[indexes[REGIONED_NUM_OF_REGIONS % (mm_type, region)]]) / indexed_regions_sum
                    sample_rec[REGIONED_NUM_OF_REGIONS % (mm_type, region)] = str(fraction)
                    g_count_d.setdefault(SUMMERY_G_REGIONED_NUM_OF_REGIONS % region, list()).append(fraction)

                edited_index_sum = 0
                indexed_canonical_sum = 0
                indexed_mm_sites_sum = 0
                total_indexed_sites_sum = 0
                indexed_regions_sum = 0
                for strand in POSSIBLE_STRANDS:
                    edited_index_sum += float(recs[indexes[STRANDED_INDEXED_EDITED_FORMAT % (mm_type, strand)]])

                    indexed_canonical_sum += float(recs[indexes[STRANDED_INDEXED_CANONICAL_FORMAT % (mm_type, strand)]])

                    indexed_mm_sites_sum += float(
                        recs[indexes[STRANDED_NUM_OF_INDEXED_MM_SITES_FORMAT % (mm_type, strand)]])

                    total_indexed_sites_sum += float(
                        recs[indexes[STRANDED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT % (mm_type, strand)]])

                    indexed_regions_sum += float(recs[indexes[STRANDED_NUM_OF_REGIONS % (mm_type, strand)]])

                for strand in POSSIBLE_STRANDS:
                    fraction = 100 * float(
                        recs[indexes[STRANDED_INDEXED_EDITED_FORMAT % (mm_type, strand)]]) / edited_index_sum
                    sample_rec[STRANDED_INDEXED_EDITED_FORMAT % (mm_type, strand)] = str(fraction)
                    g_count_d.setdefault(SUMMERY_G_STRANDED_INDEXED_EDITED_FORMAT % strand, list()).append(fraction)

                for strand in POSSIBLE_STRANDS:
                    fraction = 100 * float(recs[indexes[STRANDED_INDEXED_CANONICAL_FORMAT % (mm_type, strand)]]) / \
                               indexed_canonical_sum
                    sample_rec[STRANDED_INDEXED_CANONICAL_FORMAT % (mm_type, strand)] = str(fraction)
                    g_count_d.setdefault(SUMMERY_G_STRANDED_INDEXED_CANONICAL_FORMAT % strand, list()).append(fraction)

                for strand in POSSIBLE_STRANDS:
                    fraction = 100 * float(recs[indexes[
                        STRANDED_NUM_OF_INDEXED_MM_SITES_FORMAT % (mm_type, strand)]]) / indexed_mm_sites_sum
                    sample_rec[STRANDED_NUM_OF_INDEXED_MM_SITES_FORMAT % (mm_type, strand)] = str(fraction)
                    g_count_d.setdefault(SUMMERY_G_STRANDED_NUM_OF_INDEXED_MM_SITES_FORMAT % strand, list()).append(
                        fraction)

                for strand in POSSIBLE_STRANDS:
                    fraction = 100 * float(recs[indexes[
                        STRANDED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT % (mm_type, strand)]]) / total_indexed_sites_sum
                    sample_rec[STRANDED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT % (mm_type, strand)] = str(fraction)
                    g_count_d.setdefault(SUMMERY_G_STRANDED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT % strand,
                                         list()).append(fraction)

                for strand in POSSIBLE_STRANDS:
                    fraction = 100 * float(
                        recs[indexes[STRANDED_NUM_OF_REGIONS % (mm_type, strand)]]) / indexed_regions_sum
                    sample_rec[STRANDED_NUM_OF_REGIONS % (mm_type, strand)] = str(fraction)
                    g_count_d.setdefault(SUMMERY_G_STRANDED_NUM_OF_REGIONS % strand, list()).append(fraction)

            all_recs[strand_d_method + group + sample_rec[SAMPLE_PATH]] = sample_rec

    for strand_d_method, group_d in group_rank.iteritems():
        for group, mm_type_d in group_d.iteritems():
            for mm_type, samples_d in mm_type_d.iteritems():
                for rank, index in enumerate(sorted(samples_d, reverse=True)):
                    sample_path = samples_d[index]
                    all_recs[strand_d_method + group + sample_path][SUMMERY_RANK_FORMAT % mm_type] = str(rank)

    all_recs = all_recs.values()

    csv_outputer.output([summery_out_path, ], all_recs[0].keys(), all_recs)
    for method in group_counter:
        for group in group_counter[method]:
            for mm_type, counts_d in group_counter[method][group].iteritems():
                record = OrderedDict()
                record[GROUP] = group
                record[STRAND_DECIDING_METHOD] = method
                record[MISMATCH_TYPE] = mm_type
                for count in sorted(counts_d):
                    record[count] = str(sum(counts_d[count]) / len(counts_d[count]))
                group_recs.append(record)

    csv_outputer.output([groups_summery_path, ], group_recs[0].keys(), group_recs)


if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    desc = """Create a summed percentile output from the index full counts output"""


    class MyFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
        pass


    parser = argparse.ArgumentParser(prog='Editing Index Summery', description=desc, formatter_class=MyFormatter)

    parser.add_argument('-i', '--indexFile', metavar="A2IEditingIndex with counts output", dest='index_file', nargs='?',
                        required=True, help="The path of the A2IEditingIndex full output (with the counts) to sum")

    parser.add_argument('-o', '--output_dir', metavar="output_dir", dest='output_dir', nargs='?', required=False,
                        default=".", help="The root directory fr the output (where per sample and per group data "
                                          "will be written)")

    options = parser.parse_args()

    get_index_summery_statistics(index_summery_path=options.index_file,
                                 summery_out_path=os.path.join(options.output_dir,
                                                               "A2IEditingIndexPerSampleSummery.csv"),
                                 groups_summery_path=os.path.join(options.output_dir,
                                                                  "A2IEditingIndexPerGroupSummery.csv"))
