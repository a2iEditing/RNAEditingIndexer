__author__ = 'Hillel'
"""
This module runs editing index.
"""
# =====================imports=====================#
# region Builtin Import
import argparse
import logging
import multiprocessing
import operator
import os
import random
import sys
import threading

from collections import OrderedDict
from datetime import datetime
from pprint import pformat

# endregion

# region Internal Imports
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from EditingIndexConsts import *
from GGPSResources.general_functions import init_logging_dict, convert_args_to_dict, \
    add_get_paths_function_to_argparser, \
    get_paths, add_groups_file_to_argparser, load_groups_and_samples_from_file, get_groups_and_sample_names_dict, \
    remove_files
from GGPSResources.consts import ALL, UNKNOWN_STRAND, SENSE_STRAND, ANTISENSE_STRAND, SAMPLE, SAMPLE_PATH, GROUP, NA, \
    POSSIBLE_STRANDS, MismatchesAndRefsEnum, GENOMIC_REGION, SITE_START, SITE_END
from GGPSResources.data_structs import Site, RefSeqPosEnum

from GGPSResources.DataEntites.BaseClasses.Sample import Sample
from RNAEditingIndex.GGPSResources.DataEntites.DataRecords.GeneRegularExpressionData import GeneRegularExpressionData

from DataConverters.RefSeqGenesCoverter import load_refseq_bed
from DataConverters.GeneRegularExpressionCoverter import load_gene_expression_bed
from DataConverters.SNPsDBCoverter import load_snps_file
from DataConverters.CountPileupCoverter import parse_count_pileup, get_empty_region_counts

from EIPipeline.EIPipelineManger import run_pipeline

from GGPSResources.Outputers.CSVOutputer import CSVOutputer

# endregion

# =====================constants===================#

EDITING_INDEX_SOURCE = "EditingIndexScript"

COUNTS_KEY = "MismatchesAndCoverageCounts"
STRANDS_KEY = "Strands"

# region Logging Messages
PATH_UNAVAILABLE_ERR = "Could Not Access %s at %s!"
FASTQ_DIR_SUFF_ERR = "Fastqs Dir and Fastq Suffix Must Both Be Absent Or Provided!"
SPECIAL_COUNT_FAIL_ERR = "Failed At Generating Special Count %s for Sample %s"
# endregion

# region Operational and Output Options
STRAND_DECIDING_BY_REFSEQ_AND_UNFILTERED_MM_SITES = "RefSeqThenMMSites"
STRAND_DECIDING_BY_RANDOM = "Randomly"


def strand_deciding_by_refseq_first(counts, refseq_strand, mm_type):
    if refseq_strand != UNKNOWN_STRAND:
        return refseq_strand

    sense_count = counts[NUM_OF_MM_SITES_FORMAT % mm_type]
    antisense_count = counts[NUM_OF_MM_SITES_FORMAT % MismatchesAndRefsEnum.COMPLEMENTARY_MM[mm_type]]
    has_mm = sense_count + antisense_count > 0

    if has_mm:
        strand = SENSE_STRAND if sense_count >= antisense_count else ANTISENSE_STRAND
    else:
        strand = refseq_strand

    return strand


def strand_deciding_by_random(counts, refseq_strand, mm_type):
    random_strand_dict = {0: SENSE_STRAND, 1: ANTISENSE_STRAND, 2: UNKNOWN_STRAND}

    return random_strand_dict[random.randint(0, 2)]


STRAND_DECIDING_OPTIONS = {
    STRAND_DECIDING_BY_RANDOM: strand_deciding_by_random,
    STRAND_DECIDING_BY_REFSEQ_AND_UNFILTERED_MM_SITES: strand_deciding_by_refseq_first,
}

STRAND_DERIVING_OUTPUT_FILE_FORMAT = "StrandDerivingCountsPerRegion_%s.csv"
EDITING_INDEX_OUTPUT_FILE_FORMAT = "EditingIndex.csv"

SENSE_POSITION = "SenseGenomicPosition"
ANTISENSE_POSITION = "AntisenseGenomicPosition"
SENSE_NAME = "SenseGeneCommonName"
SENSE_REFSEQ_ID = "SenseGeneRefSeqID"
ANTISENSE_NAME = "AntisenseGeneCommonName"
ANTISENSE_REFSEQ_ID = "AntisenseGeneRefSeqID"


# endregion


# =====================functions===================#
def init_empty_index_dict(stranded=False):
    """
        This function inits an empty index dict.
        :return dict: an initialized index dict.
        """
    empty_index_counts = dict()
    for ref_pos in MismatchesAndRefsEnum.ALL_REFS:
        empty_index_counts[COVERAGE_AT_N_POSITIONS_FORMAT % ref_pos] = 0
        empty_index_counts[NUM_OF_N_SITES_COVERED_FORMAT % ref_pos] = 0

    for mm_type in MismatchesAndRefsEnum.ALL_MISMATCHES:
        empty_index_counts[NUM_OF_MM_FORMAT % mm_type] = 0
        empty_index_counts[NUM_OF_MM_SITES_FORMAT % mm_type] = 0
        empty_index_counts[SNPS_NUM_OF_MM_FORMAT % mm_type] = 0
        empty_index_counts[SNPS_NUM_OF_MM_SITES_FORMAT % mm_type] = 0

    for mm_type in MismatchesAndRefsEnum.UNSTRANDED_MISMATCHES:
        empty_index_counts[INDEXED_EDITED_FORMAT % mm_type] = 0
        empty_index_counts[INDEXED_CANONICAL_FORMAT % mm_type] = 0
        empty_index_counts[NUM_OF_INDEXED_MM_SITES_FORMAT % mm_type] = 0
        empty_index_counts[NUM_OF_INDEXED_OVERALL_SITES_FORMAT % mm_type] = 0
        empty_index_counts[NUM_OF_REGIONS % mm_type] = 0
        for strand in POSSIBLE_STRANDS:
            empty_index_counts[STRANDED_INDEXED_EDITED_FORMAT % (mm_type, strand)] = 0
            empty_index_counts[STRANDED_INDEXED_CANONICAL_FORMAT % (mm_type, strand)] = 0
            empty_index_counts[STRANDED_NUM_OF_INDEXED_MM_SITES_FORMAT % (mm_type, strand)] = 0
            empty_index_counts[STRANDED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT % (mm_type, strand)] = 0
            empty_index_counts[STRANDED_NUM_OF_REGIONS % (mm_type, strand)] = 0
        for region in RefSeqPosEnum.ALL_ANNOTATIONS:
            empty_index_counts[REGIONED_INDEXED_EDITED_FORMAT % (mm_type, region)] = 0
            empty_index_counts[REGIONED_INDEXED_CANONICAL_FORMAT % (mm_type, region)] = 0
            empty_index_counts[REGIONED_NUM_OF_INDEXED_MM_SITES_FORMAT % (mm_type, region)] = 0
            empty_index_counts[REGIONED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT % (mm_type, region)] = 0
            empty_index_counts[REGIONED_NUM_OF_REGIONS % (mm_type, region)] = 0

    for base in MismatchesAndRefsEnum.ALL_REFS:
        empty_index_counts[NUM_OF_CANONICAL_FORMAT % base] = 0

    return empty_index_counts


def derive_strand_from_refseq(genes_exp, refseqs, region):
    sense_genomic_pos, genomic_region_sense = refseqs[region][SENSE_STRAND]
    antisense_genomic_pos, genomic_region_antisense = refseqs[region][ANTISENSE_STRAND]
    if sense_genomic_pos == antisense_genomic_pos:
        if sense_genomic_pos == RefSeqPosEnum.INTERGENIC:
            derived_strand = UNKNOWN_STRAND
        else:
            sense_rfpkms = genes_exp.get_gavg_rfkpm(region=genomic_region_sense.site.region,
                                                    start=genomic_region_sense.site.start,
                                                    end=genomic_region_sense.site.end,
                                                    strand=genomic_region_sense.site.strand,
                                                    connected_region=genomic_region_sense.site)
            antisense_rfpkms = genes_exp.get_gavg_rfkpm(region=genomic_region_antisense.site.region,
                                                        start=genomic_region_antisense.site.start,
                                                        end=genomic_region_antisense.site.end,
                                                        strand=genomic_region_antisense.site.strand,
                                                        connected_region=genomic_region_antisense.site)
            if sense_rfpkms >= antisense_rfpkms:
                derived_strand = SENSE_STRAND
            else:
                derived_strand = ANTISENSE_STRAND
    else:
        stronger_annotation = RefSeqPosEnum.stronger_annotation(sense_genomic_pos, antisense_genomic_pos)
        if stronger_annotation == sense_genomic_pos:
            derived_strand = SENSE_STRAND
        else:
            derived_strand = ANTISENSE_STRAND
    return derived_strand


def get_index(refseq_strands, refseq_annotations, samples_configs, summery_dir, pipeline_output_dir, snps,
              get_regions_data, per_sample_output, delete_cmpileups, verbose, max_processes_sample,
              max_processes_strand_decision):
    # type: (dict, dict, dict, str, str, dict, bool, bool, bool, bool, int, int) -> None
    """
    This is the main functional method, that calculates the index.
    :param dict[Site, str] refseq_annotations: The annotations for each region according to the refseq.
    :param dict[Site, str] refseq_strands: The most likely strand of the regions according to the annotations (by
    region).
    :param dict[str, str] samples_configs: A dictionary containing each pof the samples config instances.
    :param str summery_dir: The path of summery output dir (will be created)
    :param str pipeline_output_dir: The path of pipeline (where pileup etc are created) output dir (will be created)
    :param dict snps: A dictionary with the SNPs per mismatch type per position.
    :param bool get_regions_data: A flag. If set will also output the counts per region (huge output, use
    carefully)
    :param bool per_sample_output: A flag. If set will output the counts per region also per sample.
    :param bool delete_cmpileups: A flag. If set will delete the cmpileup after processing it.
    :param bool verbose: A flag. If set, will output a verbose output for the index, including all the counts
    :param int max_processes_sample: The maximal number of samples to process in parallel.
    :param int max_processes_strand_decision:  The maximal strand decisions per sample to process in parallel.
    :return: None
    """

    empty_index_dict = init_empty_index_dict()
    empty_counter = get_empty_region_counts()
    confs = list()
    samples_groups_dict = get_groups_and_sample_names_dict(by_sample=True)
    samples = Sample.get_all_records(of_types=(Sample,))
    sema_sample = threading.Semaphore(max_processes_sample)
    samples_p_l = list()
    num_of_samples = len(samples)
    if get_regions_data:
        get_regions_data_dict = dict()
        for region, annotations in refseq_annotations.iteritems():
            antisense_position, antisense_refseq = annotations[ANTISENSE_STRAND]
            sense_position, sense_refseq = annotations[SENSE_STRAND]
            get_regions_data_dict[region] = OrderedDict({
                ANTISENSE_POSITION: antisense_position,
                ANTISENSE_NAME: antisense_refseq.common_name,
                ANTISENSE_REFSEQ_ID: antisense_refseq.refseq_name,
                SENSE_POSITION: sense_position,
                SENSE_NAME: sense_refseq.common_name,
                SENSE_REFSEQ_ID: sense_refseq.refseq_name,
            })
            get_regions_data_dict[region].update(empty_counter)
    else:
        get_regions_data_dict = None

    for rec_id, sample in samples.iteritems():
        """type sample Sample"""
        sample_name = sample.sample_name
        # get the config dict to retrieve the cmpileup
        try:
            config_defaults = samples_configs[rec_id].defaults(formatted=True)  # get the sample's specific paths
            confs.append(config_defaults)
        except KeyError:
            logging.info("No Config Was Available For %s, Cannot Retrieve cmpileup!" % sample_name)
            continue  # No data for this sample or this is a group

        all_methods_sample_index_dict = {method: empty_index_dict.copy() for method in STRAND_DECIDING_OPTIONS}
        tr = multiprocessing.Process(target=load_and_process_sample,
                                     args=(
                                         all_methods_sample_index_dict, config_defaults, get_regions_data_dict,
                                         refseq_annotations, refseq_strands, samples_groups_dict, snps,
                                         per_sample_output, max_processes_strand_decision, num_of_samples,
                                         pipeline_output_dir, summery_dir, sema_sample, sample, verbose),
                                     name="EditingIndexProcessingSubprocess%s" % sample_name)
        tr.daemon = True
        samples_p_l.append(tr)

    for thr in samples_p_l:
        sema_sample.acquire()
        thr.run()
    for thr in multiprocessing.active_children():
        thr.join(36000)  # if processed sample for more than 10 hours something is wrong with the thread...

    if get_regions_data:
        logging.info("Creating Region Counts Output For All Samples")
        recs = [OrderedDict([(key, str(val)) for key, val in get_regions_data_dict[region].iteritems()]) for region in
                get_regions_data_dict]
        out_format = os.path.join(summery_dir, STRAND_DERIVING_OUTPUT_FILE_FORMAT % "OverallAverage")
        csv_outputer = CSVOutputer()
        csv_outputer.output([out_format], recs[0].keys(), recs)

    if delete_cmpileups:
        logging.info("Trying to Delete cmpileups")
        for conf in confs:
            remove_files([conf[REGIONS_PILEUP_COUNT], ])

        os.system("find %s -type d -empty -delete" % pipeline_output_dir)


def output_sample(summery_dir, get_regions_data_dict, num_of_samples, per_sample_output, per_sample_output_dir, sample,
                  refseq_annotations, regions_d, by_groups_dict, all_methods_sample_index_dict, verbose):
    # type: (str, dict, int, bool, str, Sample, dict, dict, dict, dict, bool) -> None

    tmp_dict = dict()
    get_regions_data = get_regions_data_dict is not None
    overall_index_recs = list()
    per_sample_regions_dict = OrderedDict()
    per_sample_regions_recs = list()
    csv_outputer = CSVOutputer(append=True, override=False)

    """:type sample Sample"""
    assert isinstance(sample, Sample)
    group = NA
    for group_p in by_groups_dict.get(sample.sample_name).keys():
        if group_p[1] <= 1:
            group = group_p[0]
            break

    sample_name = sample.sample_name
    per_sample_regions_dict[GROUP] = group
    per_sample_regions_dict[SAMPLE] = sample_name
    per_sample_regions_dict[SAMPLE_PATH] = sample.sample_path

    logging.info("Summing Data for %s" % sample.sample_name)
    for region, region_data_d in regions_d.iteritems():
        if per_sample_output:
            tmp_dict = per_sample_regions_dict.copy()
            tmp_dict[GENOMIC_REGION] = region.region
            tmp_dict[SITE_START] = region.start
            tmp_dict[SITE_END] = region.end
            tmp_dict[ANTISENSE_POSITION] = get_regions_data_dict[region][ANTISENSE_POSITION]
            tmp_dict[ANTISENSE_NAME] = get_regions_data_dict[region][ANTISENSE_NAME]
            tmp_dict[ANTISENSE_REFSEQ_ID] = get_regions_data_dict[region][ANTISENSE_REFSEQ_ID]
            tmp_dict[SENSE_POSITION] = get_regions_data_dict[region][SENSE_POSITION]
            tmp_dict[SENSE_NAME] = get_regions_data_dict[region][SENSE_NAME]
            tmp_dict[SENSE_REFSEQ_ID] = get_regions_data_dict[region][SENSE_REFSEQ_ID]

        if get_regions_data:
            for count_type, count in region_data_d[COUNTS_KEY]:
                get_regions_data_dict[region][count_type] += count / float(num_of_samples)
                if per_sample_output:
                    tmp_dict[count_type] = str(count_type)

        for strand_deciding_method, strands_dict in region_data_d[STRANDS_KEY].iteritems():
            sample_index_dict = all_methods_sample_index_dict[strand_deciding_method]
            if per_sample_output:
                tmp_dict[STRAND_DECIDING_METHOD] = strand_deciding_method
                tmp_dict.update(strands_dict)
                per_sample_regions_recs.append(tmp_dict.copy())

            for count_type, count_val in region_data_d[COUNTS_KEY].iteritems():
                sample_index_dict[count_type] += count_val

            annotations = refseq_annotations[region]
            antisense_position, _ = annotations[ANTISENSE_STRAND]
            sense_position, _ = annotations[SENSE_STRAND]

            for mm_type, strand in strands_dict.iteritems():
                if strand == SENSE_STRAND:
                    genomic_position = sense_position
                    ref_base = mm_type.split(MismatchesAndRefsEnum.MM_SEP)[0]

                    stranded_edited = region_data_d[COUNTS_KEY][NUM_OF_MM_FORMAT % mm_type]
                    stranded_edited_sites = region_data_d[COUNTS_KEY][NUM_OF_MM_SITES_FORMAT % mm_type]
                    stranded_overall_sites = region_data_d[COUNTS_KEY][NUM_OF_N_SITES_COVERED_FORMAT % ref_base]
                    stranded_canonical = region_data_d[COUNTS_KEY][NUM_OF_CANONICAL_FORMAT % ref_base]
                elif strand == ANTISENSE_STRAND:
                    genomic_position = antisense_position
                    stranded_mm_type = MismatchesAndRefsEnum.COMPLEMENTARY_MM[mm_type]
                    ref_base = stranded_mm_type.split(MismatchesAndRefsEnum.MM_SEP)[0]

                    stranded_edited = region_data_d[COUNTS_KEY][NUM_OF_MM_FORMAT % stranded_mm_type]
                    stranded_edited_sites = region_data_d[COUNTS_KEY][NUM_OF_MM_SITES_FORMAT % stranded_mm_type]
                    stranded_overall_sites = region_data_d[COUNTS_KEY][
                        NUM_OF_N_SITES_COVERED_FORMAT % ref_base]
                    stranded_canonical = region_data_d[COUNTS_KEY][NUM_OF_CANONICAL_FORMAT % ref_base]
                else:
                    genomic_position = RefSeqPosEnum.INTERGENIC
                    ref_base = mm_type.split(MismatchesAndRefsEnum.MM_SEP)[0]

                    stranded_edited = region_data_d[COUNTS_KEY][NUM_OF_MM_FORMAT % mm_type] * 0.5
                    stranded_edited_sites = region_data_d[COUNTS_KEY][NUM_OF_MM_SITES_FORMAT % mm_type] * 0.5
                    stranded_overall_sites = region_data_d[COUNTS_KEY][
                                                 NUM_OF_N_SITES_COVERED_FORMAT % ref_base] * 0.5
                    stranded_canonical = region_data_d[COUNTS_KEY][NUM_OF_CANONICAL_FORMAT % ref_base] * 0.5

                    stranded_mm_type = MismatchesAndRefsEnum.COMPLEMENTARY_MM[mm_type]
                    ref_base = stranded_mm_type.split(MismatchesAndRefsEnum.MM_SEP)[0]

                    stranded_edited += region_data_d[COUNTS_KEY][NUM_OF_MM_FORMAT % stranded_mm_type] * 0.5
                    stranded_edited_sites += region_data_d[COUNTS_KEY][
                                                 NUM_OF_MM_SITES_FORMAT % stranded_mm_type] * 0.5
                    stranded_overall_sites += region_data_d[COUNTS_KEY][
                                                  NUM_OF_N_SITES_COVERED_FORMAT % ref_base] * 0.5
                    stranded_canonical += region_data_d[COUNTS_KEY][NUM_OF_CANONICAL_FORMAT % ref_base] * 0.5

                sample_index_dict[INDEXED_EDITED_FORMAT % mm_type] += stranded_edited
                sample_index_dict[STRANDED_INDEXED_EDITED_FORMAT % (mm_type, strand)] += stranded_edited
                sample_index_dict[REGIONED_INDEXED_EDITED_FORMAT % (mm_type, genomic_position)] += stranded_edited

                sample_index_dict[INDEXED_CANONICAL_FORMAT % mm_type] += stranded_canonical
                sample_index_dict[STRANDED_INDEXED_CANONICAL_FORMAT % (mm_type, strand)] += stranded_canonical
                sample_index_dict[
                    REGIONED_INDEXED_CANONICAL_FORMAT % (mm_type, genomic_position)] += stranded_canonical

                sample_index_dict[NUM_OF_INDEXED_MM_SITES_FORMAT % mm_type] += stranded_edited_sites
                sample_index_dict[
                    STRANDED_NUM_OF_INDEXED_MM_SITES_FORMAT % (mm_type, strand)] += stranded_edited_sites
                sample_index_dict[
                    REGIONED_NUM_OF_INDEXED_MM_SITES_FORMAT % (mm_type, genomic_position)] += stranded_edited_sites

                sample_index_dict[NUM_OF_INDEXED_OVERALL_SITES_FORMAT % mm_type] += stranded_overall_sites
                sample_index_dict[
                    STRANDED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT % (mm_type, strand)] += stranded_overall_sites
                sample_index_dict[
                    REGIONED_NUM_OF_INDEXED_OVERALL_SITES_FORMAT % (
                        mm_type, genomic_position)] += stranded_overall_sites

                sample_index_dict[NUM_OF_REGIONS % mm_type] += 1
                sample_index_dict[STRANDED_NUM_OF_REGIONS % (mm_type, strand)] += 1
                sample_index_dict[REGIONED_NUM_OF_REGIONS % (mm_type, genomic_position)] += 1

    logging.info("Done Summing Data for %s" % sample.sample_name)

    if get_regions_data and per_sample_output:
        logging.info("Creating Per Sample Region Counts Output For %s" % sample.sample_name)
        out_format = os.path.join(per_sample_output_dir, STRAND_DERIVING_OUTPUT_FILE_FORMAT)
        csv_outputer.output([out_format % sample.sample_name], per_sample_regions_recs[0].keys(),
                            per_sample_regions_recs)

    for strand_deciding_method in STRAND_DECIDING_OPTIONS:
        sample_index_dict = all_methods_sample_index_dict[strand_deciding_method]

        sample_rec = OrderedDict()
        sample_rec[GROUP] = group
        sample_rec[SAMPLE] = sample.sample_name
        sample_rec[SAMPLE_PATH] = sample.sample_path
        sample_rec[STRAND_DECIDING_METHOD] = strand_deciding_method

        for mm_type in MismatchesAndRefsEnum.UNSTRANDED_MISMATCHES:
            sample_rec[EDITING_INDEX_FORMAT % mm_type] = 100 * sample_index_dict[
                INDEXED_EDITED_FORMAT % mm_type] / (sample_index_dict[INDEXED_EDITED_FORMAT % mm_type] +
                                                    sample_index_dict[INDEXED_CANONICAL_FORMAT % mm_type])

        if verbose:
            # cast to str all of the values
            for key in sorted(sample_index_dict):
                sample_rec[key] = str(sample_index_dict[key])

        overall_index_recs.append(sample_rec)

    logging.info("Writing Into Index Output For All Samples, For %s" % sample_name)
    overall_index_headers = overall_index_recs[0].keys()
    csv_outputer.output([os.path.join(summery_dir, EDITING_INDEX_OUTPUT_FILE_FORMAT), ], overall_index_headers,
                        overall_index_recs)


def load_and_process_sample(all_methods_sample_index_dict, config_defaults, get_regions_data_dict, refseq_annotations,
                            refseq_strands, samples_groups_dict, snps, per_sample_output, max_processes, num_of_samples,
                            pipeline_output_dir, summery_dir, sema_sample, sample, verbose):
    # type: (dict, dict, dict, dict, dict, dict, dict, bool, int, int, str, str, multiprocessing.Semaphore, Sample, bool) -> None
    """
    This function parses each sample's cmpileup data and decide the strands for each mm type per region and creates the
        output.
    :param dict[str, dict[str, float]] all_methods_sample_index_dict: a counter dict, sent as param to save run time
    :param dict[str, str] config_defaults: The dict containing the defaults part of the sample's configuration.
    :param dict[str, float\str] get_regions_data_dict: The dict containing the overall regions data.
    :param dict[Site,dict[str, RefSeqPosEnum]] refseq_annotations: A dictionary of all possible refeseq annotations per region.
    :param dict[Site, str] refseq_strands: The most likely strand of the regions according to the annotations (by region).
    :param dict[str, dict] samples_groups_dict: A dictionary of all "known" samples and groups.
    :param dict[str, dict[Site, bool]] snps:  A dictionary with the SNPs per mismatch type per position.
    :param per_sample_output:
    :param int max_processes: The maximal number of threads for strands decision
    :param int num_of_samples: The overall number of samples, used in per region data.
    :param str pipeline_output_dir: The base output dir of the pipeline part.
    :param str summery_dir: The base dir for summery files.
    :param multiprocessing.Semaphore sema_sample: The semaphore to use.
    :param Sample sample: The sample instance the data is relevant to.
    :param bool verbose: A flag. If set, will output a verbose output for the index, including all the counts
    :return: None
    """

    if per_sample_output:
        per_sample_output_dir = config_defaults["output_dir"].replace(pipeline_output_dir, summery_dir)
    else:
        per_sample_output_dir = None
    # get cmpileup path
    count_pileup_file = config_defaults[REGIONS_PILEUP_COUNT]

    try:
        regions_strands = get_strands_and_counts(refseq_strands=refseq_strands,
                                                 sample=sample,
                                                 snps=snps,
                                                 max_processes=max_processes,
                                                 count_pileup_file=count_pileup_file)

        output_sample(summery_dir=summery_dir,
                      get_regions_data_dict=get_regions_data_dict,
                      num_of_samples=num_of_samples,
                      per_sample_output=per_sample_output,
                      per_sample_output_dir=per_sample_output_dir,
                      sample=sample,
                      refseq_annotations=refseq_annotations,
                      regions_d=regions_strands,
                      by_groups_dict=samples_groups_dict,
                      all_methods_sample_index_dict=all_methods_sample_index_dict,
                      verbose=verbose)
    except Exception, e:
        logging.exception("Failed Loading Processing Data of %s! (Won't Delete cmpileup)" % sample.sample_name)
    finally:
        sema_sample.release()


def get_strands_and_counts(refseq_strands, sample, snps, max_processes, count_pileup_file):
    # type: (dict, Sample, dict, int, str) -> dict
    """
    This function parallels (using threading) the processing of the sample's data (counting coverages and mismatches, deciding strands per region)
    :param dict[Site, str] refseq_strands: The most likely strand of the regions according to the annotations (by region).
    :param Sample sample: The sample we're processing now.
    :param dict snps: A dictionary with the SNPs per mismatch type per position.
    :param int max_processes: The maximal number of threads for strands decision
    :param str count_pileup_file: The path to the current sample cmpileup to process
    :return dict: The regions counts and strands
    """
    sample_name = sample.sample_name
    sema_decide = threading.Semaphore(max_processes)

    # process cmpileup
    logging.info("Started Processing The Data Of %s" % sample_name)
    logging.info("Loading Coverage File %s" % count_pileup_file)
    try:
        sample_coverages = parse_count_pileup(count_pileup_file=count_pileup_file, snps=snps)
        logging.info("Done Loading Coverage Data of %s" % sample_name)
    except Exception, e:
        logging.exception("Failed Loading Coverage Data of %s! (Won't Delete cmpileup)" % sample_name)
        return dict()
    # create the threads (run later) for deciding strands for all regions
    threads = list()
    covered_chroms = dict()
    regions_strands = dict()
    for region, region_coverage_counts in sample_coverages.iteritems():
        regions_strands[region] = dict()
        covered_chroms[region.region] = True
        tr = multiprocessing.Process(target=decide_strands,
                                     args=(
                                         region_coverage_counts, refseq_strands[region], sema_decide,
                                         regions_strands[region]),
                                     name="EditingIndexStrandDecideSubprocess%s" % sample_name)

        tr.daemon = True
        threads.append(tr)
    # decide all strands (paralleling)
    logging.info("Started Deciding Strands For %s" % sample_name)
    for thr in threads:
        sema_decide.acquire()
        thr.run()
    for thr in multiprocessing.active_children():
        thr.join(3600)  # if waited for more than an hour something is wrong....
    logging.info(
        "Done Deciding Regions Strands of %s, found regions in: %s" % (sample_name, pformat(covered_chroms.keys())))

    return regions_strands


def decide_strands(region_coverage_counts, refseq_strand, semaphore_decide, regions_strands_of_sample):
    # type: (dict, str, multiprocessing.Semaphore, dict) -> None
    """
    Decides, paralleling (using threading), the strand (for each type of mismatch) for the region.
    :param dict[str, int] region_coverage_counts: The counts of coverages and mismatches, as parsed from the cmpileup.
    :param str refseq_strand: The most likely strand of the region according to the annotations.
    :param multiprocessing.Semaphore semaphore_decide: The semaphore used for th4e threading.
    :param dict[str, dict] regions_strands_of_sample: The output variable, containing the decisions and count for all of the samples.
    :return: None
    """
    try:
        regions_strands_of_sample[COUNTS_KEY] = region_coverage_counts

        mm_to_strands_d = dict()

        for strand_deciding_method, operation in STRAND_DECIDING_OPTIONS.iteritems():
            mm_to_strands_d[strand_deciding_method] = dict()
            for mm_type in MismatchesAndRefsEnum.UNSTRANDED_MISMATCHES:
                mm_to_strands_d[strand_deciding_method][mm_type] = operation(region_coverage_counts, refseq_strand,
                                                                             mm_type)

        regions_strands_of_sample[STRANDS_KEY] = mm_to_strands_d
    except Exception, e:
        logging.exception("Failed On Strand Decisions")
    finally:
        semaphore_decide.release()


def main(script_install_dir, root_dir, output_dir, output_dir_summery, genome_path, regions_bed, log_path,
         bam_files_suffix, groups_file, include_paths, include_paths_operator, exclude_paths, exclude_paths_operator,
         recursion_depth, follow_links, defaults_override_conf, defaults_override_args, snps_file,
         refseq_file, gene_expression_file, get_regions_metadata, just_get_configs, per_sample_output, delete_cmpileups,
         max_processes_sample, max_processes_strand_decision, verbose, get_stats):
    # type: (str, str, str, str, str, str, str, str, str, list,  operator, list, operator, int, bool, str, dict, str, str, str, bool, bool, bool, bool, int, int, bool, bool) -> None
    """
    :param str script_install_dir: The path to this script (for relative path usage)
    :param str root_dir: The directory in which the BAM files from the aligner are. Aligner logs should be there to if availabe.
    :param str output_dir: The output directory for the run outputs.
    :param str output_dir_summery: The output directory for the summary output.
    :param str genome_path: The path of the genome fasta or one of keys of BUILTIN_GENOMES
    :param str regions_bed: The path of the edited regions bed file or one of the keys of BUILTIN_REGIONS
    :param str groups_file: The path of the groups file if given, otherwise all sample are considered if the same group.
    :param str log_path: The path to the log directory.
    :param str bam_files_suffix: The suffixes of the BAM files to run on.
    :param list[str] include_paths: List of path fragments that must be in path for it to be included.
    :param operator include_paths_operator: The operator used to check for fragments (AND or OR)
    :param list[str] exclude_paths: List of path fragments that mustn't be in path for it to be included.
    :param operator exclude_paths_operator: The operator used to check for fragments (AND or OR)
    :param int recursion_depth: The recursion depth to look for files from root directory
    :param bool follow_links: If set will follow links (a dir command param)
    :param str defaults_override_conf: A path to a cofig file for overriding default setting conf.
    :param dict[str, str] defaults_override_args: A dictionary of options to override in the defaults,
     will also override defaults_override_conf.
    :param str snps_file: A path to a user given SNPs file.
    :param str refseq_file: A path to a user given RefSeq file.
    :param str gene_expression_file: A path to a user given gene expression file.
    :param bool get_regions_metadata: A flag. If set, will also print per region data (big output)
    :param bool just_get_configs: A flag. If set, will not run pipeline part (i.e. will not generate the cmpileups and assume they exist)
    :param bool per_sample_output: A flag. If set,  will also print per region *per sample* data (*very* big output)
    :param bool delete_cmpileups: A flag. If set, will delete the cmpileups after conversion, maintaining relatively low memory profile.
    :param int max_processes_sample: The maximal number of samples to process in parallel.
    :param int max_processes_strand_decision:  The maximal strand decisions per sample to process in parallel.
    :param bool verbose: A flag. If set, will output a verbose output for the index, including all the counts
    :param bool get_stats: A flag. If set, will output a verbose statistical summery output in which all columns of the verbose
        output in percentages, as well as alignment data, collected from the BAMs
    :return:None
    """
    assert genome_path in BUILTIN_GENOMES or os.path.exists(genome_path), PATH_UNAVAILABLE_ERR % (
        "Genome File", genome_path)
    assert regions_bed in BUILTIN_REGIONS or os.path.exists(regions_bed), PATH_UNAVAILABLE_ERR % (
        "Regions BED File", genome_path)
    assert refseq_file in BUILTIN_REFSEQS or os.path.exists(refseq_file), PATH_UNAVAILABLE_ERR % (
        "Refseq Annotations File", genome_path)

    snps_file_good = snps_file in BUILTIN_SNPsDB or os.path.exists(snps_file)
    if not snps_file_good and snps_file:
        logging.warn(PATH_UNAVAILABLE_ERR % ("SNPs File", genome_path))

    gene_expression_file_good = gene_expression_file in BUILTIN_GENE_EXP or os.path.exists(gene_expression_file)
    if not gene_expression_file and gene_expression_file:
        logging.warn(PATH_UNAVAILABLE_ERR % ("Genes Expression File", genome_path))

    timestamp = datetime.today().isoformat()
    init_logging_dict(os.path.join(log_path, ".".join(["EditingIndex", timestamp, "log"])))

    genome_full_path = BUILTIN_GENOMES[genome_path] % dict(script_dir=script_install_dir) \
        if genome_path in BUILTIN_GENOMES else genome_path
    regions_bed_full_path = BUILTIN_REGIONS[regions_bed] % dict(script_dir=script_install_dir) \
        if regions_bed in BUILTIN_REGIONS else regions_bed
    snps_full_path = BUILTIN_SNPsDB[snps_file] % dict(script_dir=script_install_dir) \
        if snps_file in BUILTIN_SNPsDB else snps_file
    refseq_full_path = BUILTIN_REFSEQS[refseq_file] % dict(script_dir=script_install_dir) \
        if refseq_file in BUILTIN_REFSEQS else refseq_file
    gene_expression_full_path = BUILTIN_GENE_EXP[gene_expression_file] % dict(script_dir=script_install_dir) \
        if gene_expression_file in BUILTIN_GENE_EXP else gene_expression_file

    genome_index_path = os.path.join(output_dir, os.path.basename(genome_full_path) + ".GenomeIndex.jsd")
    defaults_override_args.update({GENOME_FASTA_OPTION: genome_full_path,
                                   REGIONS_BED_OPTION: regions_bed_full_path,
                                   BAM_FILE_SUFFIX_OPTION: bam_files_suffix,
                                   GENOME_INDEX_PATH: genome_index_path})

    predicates_dict = {ALL: lambda path: path.endswith(bam_files_suffix)}
    bam_files = get_paths(root_path=root_dir,
                          must_include_paths=include_paths,
                          must_include_operator=include_paths_operator,
                          exclude_paths=exclude_paths,
                          exclude_operator=exclude_paths_operator,
                          follow_links=follow_links,
                          recursion_depth=recursion_depth,
                          predicates_dict=predicates_dict)[ALL]

    if groups_file:
        load_groups_and_samples_from_file(groups_file=groups_file)

    samples_confs = run_pipeline(root_path=root_dir,
                                 output_dir=output_dir,
                                 bam_files_suffix=bam_files_suffix,
                                 full_conf_path=FULL_CONFIG_PATH_FORMAT % dict(script_dir=script_install_dir),
                                 defaults_conf_path=DEFAULTS_CONFIG_PATH_FORMAT % dict(script_dir=script_install_dir),
                                 defaults_override_conf_path=defaults_override_conf,
                                 defaults_override_args=defaults_override_args,
                                 files=bam_files,
                                 log_dir=log_path,
                                 create_na_group=None is groups_file,
                                 just_get_configs=just_get_configs)

    if len(samples_confs) == 0:
        logging.warn("No Samples Were Found To Run On! Exiting...")
        return

    bedtools_path = samples_confs.values()[0].defaults(formatted=True)[BEDTOOLS_PATH_OPTION]

    logging.info("Loading RefSeq File")
    refseqs = load_refseq_bed(refseq_file=refseq_full_path,
                              regions_file=regions_bed_full_path,
                              bedtools_path=bedtools_path)

    logging.info("Loading SNPs File")
    if not snps_file_good:
        logging.warn("No SNPs File Was Loaded!")
        snps = dict()
    else:
        snps = load_snps_file(snps_file=snps_full_path,
                              intersect_first_with=regions_bed_full_path,
                              bedtools_path=bedtools_path)

    logging.info("Loading Gene Expression File")
    if not gene_expression_file_good:
        logging.warn("No Gene Expression File Was Loaded!")
        _ = GeneRegularExpressionData(source_name=EDITING_INDEX_SOURCE)
    else:
        load_gene_expression_bed(gene_expression_file=gene_expression_full_path,
                                 source_name=EDITING_INDEX_SOURCE,
                                 intersect_first_with=refseq_full_path,
                                 bedtools_path=bedtools_path)

    logging.info("Calculating Strands For Regions According to RefSeq")
    refseqs_strands = {
        region: derive_strand_from_refseq(GeneRegularExpressionData(source_name=EDITING_INDEX_SOURCE), refseqs, region)
        for
        region in refseqs}

    get_index(refseq_strands=refseqs_strands,
              refseq_annotations=refseqs,
              samples_configs=samples_confs,
              summery_dir=output_dir_summery,
              pipeline_output_dir=output_dir,
              snps=snps,
              get_regions_data=get_regions_metadata,
              per_sample_output=per_sample_output,
              delete_cmpileups=delete_cmpileups,
              verbose=verbose,
              max_processes_sample=max_processes_sample,
              max_processes_strand_decision=max_processes_strand_decision)
    logging.info("Done Writing Index Data")


if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    desc = """Run on each file in a given directory a set of steps."""


    class MyFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
        pass


    parser = argparse.ArgumentParser(prog='Editing Index Runner', description=desc, formatter_class=MyFormatter)

    inputs_g = parser.add_argument_group(title="Input Files Detection Options:")
    add_get_paths_function_to_argparser(parser=inputs_g)
    inputs_g.add_argument('-f', '--bam_files_suffix', metavar="bam files suffix", dest='files_suffix', nargs='?',
                          required=False,
                          default="Aligned.sortedByCoord.out.bam",
                          help="A suffix of the BAM files to run on (e.g. Sorted.By.Coord.bam). Should be the *full* "
                               "suffix")

    outputs_g = parser.add_argument_group(title="Output Files Options:")
    outputs_g.add_argument('-o', '--output_dir', metavar="output_dir", dest='output_dir', nargs='?', required=False,
                           default=".", help="The root directory for the cmpileup creation outputs"
                                             " (will create sub-dirs per sample). If keep_cmpileup is not set, "
                                             "all content here will be deleted.")
    outputs_g.add_argument('--get_regions_metadata', dest='get_regions_metadata', action='store_true', required=False,
                           help="If set, will output regions metadata (raw counts, big output)")
    outputs_g.add_argument('--keep_cmpileup', dest='keep_cmpileup', action='store_true', required=False,
                           help="If set, will not delete the cmpileups")
    outputs_g.add_argument('-os', '--output_dir_summery', metavar="output_dir_summery", dest='output_dir_summery',
                           nargs='?', required=False, default=".", help="The directory for the summary output.")
    outputs_g.add_argument('--per_sample_output', dest='per_sample_output', action='store_true', required=False,
                           help="If set,  will output regions metadata per sample too (very big output)")
    outputs_g.add_argument('--verbose', dest='verbose', action='store_true', required=False,
                           help="If set, will give a verbose output including all counts, otherwise will output only indexes")

    resources_g = parser.add_argument_group(title="Resources Options:")
    resources_g.add_argument('-rb', '--regions', metavar="regions bed", dest='regions_bed', nargs='?', required=True,
                             help="The path of the edited regions bed file or one of the builtin names (%s)" %
                                  ", ".join(BUILTIN_REGIONS.keys()))
    resources_g.add_argument('--snps', metavar="SNPs file", dest='snps_file', nargs='?', required=False,
                             default="", help="A path to a SNPs file to use or one of the builtin names (%s)" %
                                              ", ".join(BUILTIN_SNPsDB.keys()))
    resources_g.add_argument('--refseq', metavar="refseq file", dest='refseq_file', nargs='?', required=True,
                             default="", help="A path to a refseq file to use or one of the builtin names (%s)" %
                                              ", ".join(BUILTIN_REFSEQS.keys()))
    resources_g.add_argument('--genes_expression', metavar="genes expression file", dest='genes_expression_file',
                             nargs='?',
                             required=False, default="",
                             help="A path to a genes_expression_file to use or one of the builtin names (%s)" %
                                  ", ".join(BUILTIN_GENE_EXP.keys()))
    resources_g.add_argument('-gf', '--genome', metavar="genome fasta", dest='genome_path', nargs='?', required=True,
                             help="The path of the genome fasta or one of the builtin names (%s)" %
                                  ", ".join(BUILTIN_GENOMES.keys()))
    add_groups_file_to_argparser(parser=resources_g)

    run_configs = parser.add_argument_group(title="Run Configuration Options:")
    run_configs.add_argument('-l', '--log_path', metavar="log_path", dest='log_path', nargs='?', required=False,
                             default=".",
                             help="The path where the logs (and flags) will be written.")
    run_configs.add_argument('-c', '--config_override_file', metavar="config_override_file",
                             dest='config_override_file',
                             nargs='?', required=False,
                             help="A path to a configuration file (in INI format) to override "
                                  "the values in the editing index config file found in %s." %
                                  os.path.join(script_dir, "Resources"))
    run_configs.add_argument('-a', '--args', metavar="override config extra args", dest='args', required=False,
                             default={}, nargs='*',
                             help='named args (in the format of <var>=\"<val>\",<var>=\"<val>\") to override in the defaults'
                                  ' config.')
    run_configs.add_argument('--recalc', dest='just_get_configs', action='store_true', required=False,
                             help="If set, will not the run pipeline part (i.e. will not generate the cmpileups, instead "
                                  "the script assumes they exist)")

    sys_opts = parser.add_argument_group(title="System Options:")
    sys_opts.add_argument('--ts', metavar="sample threads", dest='max_processes_sample', nargs='?', required=False,
                          default=10, type=int, help="The number of samples to process in parallel")
    sys_opts.add_argument('--tsd', metavar="sample strands threads", dest='max_processes_strand_decision', nargs='?',
                          required=False, default=50, type=int,
                          help="The maximal strand decisions per sample to process in parallel")

    options = parser.parse_args()

    args = convert_args_to_dict(options.args)

    main(script_install_dir=script_dir,
         root_dir=options.root_dir,
         output_dir=options.output_dir,
         output_dir_summery=options.output_dir_summery,
         genome_path=options.genome_path,
         regions_bed=options.regions_bed,
         groups_file=options.groups_file,
         include_paths=options.include_prefixes,
         include_paths_operator=options.include_operator,
         exclude_paths=options.exclude_prefixes,
         exclude_paths_operator=options.exclude_operator,
         recursion_depth=options.recursion_depth,
         follow_links=options.follow_links,
         log_path=options.log_path,
         bam_files_suffix=options.files_suffix,
         defaults_override_conf=options.config_override_file,
         defaults_override_args=args,
         snps_file=options.snps_file,
         refseq_file=options.refseq_file,
         gene_expression_file=options.genes_expression_file,
         get_regions_metadata=options.get_regions_metadata,
         just_get_configs=options.just_get_configs,
         per_sample_output=options.per_sample_output,
         delete_cmpileups=not options.keep_cmpileup,
         max_processes_sample=options.max_processes_sample,
         max_processes_strand_decision=options.max_processes_strand_decision,
         verbose=options.verbose,
         get_stats=options.stats
         )
