import bz2
import gzip

__author__ = 'Hillel'
'''
This file contains *simple* function that are needed in various modules
'''
# =====================imports=====================#
import argparse
import logging
import operator
import os
import shutil
import csv
from pprint import pformat

from consts import LOGICAL_OPERATORS, OR_OPERATOR, GROUPS_FILE_SAMPLE_NAME_HEADER, \
    GROUPS_FILE_SAMPLE_PATH_HEADER, GROUPS_FILE_GROUP_NAME_HEADER, GROUPS_FILE_PARENT_GROUP_HEADER
from ..GGPSResources.DataEntites.BaseClasses.Sample import Sample
from ..GGPSResources.DataEntites.KnownProperties.Group import Group

# =====================consts=====================#

DEL_FILE_WRN = "GGPSResources.general_functions.remove_files Filed To Remove %s"
SAMPLE_PATH_JOKER_WRN = "Sample %s's Path Didn't End With *! This may cause Problems!"

GROUPS_FILE_CORRUPT_ERR_MSG = "Groups And Samples File Doesn't Contain The Needed Data (%s, %s, %s and optional %s)" % \
                              (GROUPS_FILE_SAMPLE_NAME_HEADER, GROUPS_FILE_SAMPLE_PATH_HEADER,
                               GROUPS_FILE_GROUP_NAME_HEADER, GROUPS_FILE_PARENT_GROUP_HEADER)


# ====================classes====================#

# ====================functions====================#

def get_index_dict(data_list, values):
    # type: (list, list) -> dict
    """
    This function returns an index dict of where in a line the values appear (useful for headers)
    :param list[str] data_list: The list to search in (e.g. headers line of a csv file)
    :param values: The values to look for.
    :return: a dict[index, value]
    """
    i_dict = dict()
    for val in values:
        try:
            i_dict[data_list.index(val)] = val
        except ValueError:
            continue

    return i_dict


def convert_params_to_bool_dict(param):
    # type: (list) -> dict
    """
    creates and "index" over a param (list)
    :param param: the param(s) to "index"
    :return: a boolean dict with all content of param as keys to True
    """
    bool_d = {}
    if not isinstance(param, (list, tuple)):
        param = [param, ]
    for p in param:
        bool_d[p] = True
    return bool_d


def init_logging_dict(log_file):
    if not os.path.isdir(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] %(processName)s %(module)s %(levelname)-8s %(message)s',
                        datefmt='%y-%m-%d %H:%M:%S',
                        filename=log_file,
                        filemode='w')
    # define a Handler which writes WARN messages or higher to the sys.stderr
    console_logger = logging.StreamHandler()
    console_logger.setLevel(logging.WARN)
    # set a format which is simpler for console_logger use
    formatter = logging.Formatter('[%(asctime)s] %(module)s %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console_logger.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console_logger)


def convert_args_to_dict(arg):
    """
    This function is used with argsparse when using passage of bash args of the format - <var>=\'<val>\'  <var>=\'<val>\'.
    It's supposed to be sent with the "type" param in the parser.add_option function.
    :param arg: a couple <var>=\'<val>\'
    :return: a dict of {var : val}
    """
    args = []
    for a in arg:
        args.extend(a.split(","))
    res_dict = {}
    i = 0
    while i < len(args):
        try:
            res_dict.update(eval("dict(" + args[i] + ")"))
        except SyntaxError, e:
            # if "EOL while scanning string literal" in e.message:
            curr_arg = ""
            while not (curr_arg.endswith("'") or curr_arg.endswith('"')) and i < len(args):
                print args[i]
                curr_arg += args[i] + " "
                i += 1
            res_dict.update(eval("dict(" + curr_arg + ")"))
        i += 1
    return res_dict


def remove_files(files):
    # type (list[str]) -> None
    """
    This is a simple method to delete files after a pipeline run for example.
    Note: It ignores non-existence of target files.
    :param list files: A lis tof files to delete.
    :return: None
    """
    for del_path in files:
        try:
            if os.path.isdir(del_path):
                shutil.rmtree(del_path)
            else:
                os.remove(del_path)
        except:
            logging.warn(DEL_FILE_WRN % del_path)


def get_path_depth(path):
    length = 0
    run = True
    prev = None
    while run:
        path = os.path.split(path)[0]
        if prev == path:
            run = False
        else:
            prev = path
            length += 1
    return length


def path_included(path_fragments, full_path, operator_used):
    # type: (list, str, operator) -> object
    """
    This function checks if all\any of fragments are present in a path.
    :param list[str] path_fragments: The fragments that should be in the path
    :param str full_path: The path to check.
    :param operator operator_used: What type of operator (and / or)
    :return bool: True if included else False
    """
    included = None
    for path_fragment in path_fragments:
        if path_fragment:
            if None is included:
                included = path_fragment in full_path
            else:
                included = operator_used(included, path_fragment in full_path)

    return included


def get_paths(root_path, must_include_paths=[], must_include_operator=operator.or_, exclude_paths=[],
              exclude_operator=operator.or_, follow_links=False, recursion_depth=100, predicates_dict={}):
    # type: (str, list, operator, list, operator, bool, int, dict) -> list
    """
    This get a list of paths according ot the given filtering params.
    :param root_path: The path to begin recursively looking from.
    :type root_path: C{str}
    :param must_include_paths: Paths "fragments" that have to be part of a path for it to be included.
    :type must_include_paths: C{list} of C{str}
    :param must_include_operator: The operator used when checking for must_include_paths
    :type must_include_operator: C{operator.or_} or C{operator.and_}
    :param exclude_paths: Paths "fragments" that cannot be part of a path for it to be included.
    :type exclude_paths: C{list} of C{str}
    :param exclude_operator: The operator used when checking for must_include_paths
    :type exclude_operator: C{operator.or_} or C{operator.and_}
    :param follow_links: a flag for os.walk. If set will follow links.
    :type follow_links: C{bool}
    :param recursion_depth: A limiting depth for the dir recursion. (default is 100)
    :type recursion_depth: C{int}
    :param predicates_dict: A dictionary of path groups (if needed for differnet processing) to predicate.
    :type predicates_dict: C{dict} of C{str} to C{boolean function}
    :return: a dictionary of group names to their corresponding paths.
    :rtype: C{dict} of C{str} to C{list} of C{str}
    """
    res_dict = {key: [] for key in predicates_dict}
    if isinstance(exclude_operator, str):
        exclude_operator = LOGICAL_OPERATORS[exclude_operator]
    if isinstance(must_include_operator, str):
        must_include_operator = LOGICAL_OPERATORS[must_include_operator]
    root_path_len = get_path_depth(root_path)
    for root, dirs, files in os.walk(root_path, followlinks=follow_links):
        if exclude_paths and path_included(exclude_paths, root, exclude_operator):
            logging.debug("dir included the exclude 'fragments' (%s), skipping! (file: %s)" % (exclude_paths, root))
            del dirs[:]
            del files[:]
            continue
        split_root_len = get_path_depth(root)
        depth = split_root_len - root_path_len
        if depth >= recursion_depth:
            logging.debug("Got to recursion limit at %s" % root)
            del dirs[:]
        for sfile in files:
            full_path = os.path.join(root, sfile)

            if must_include_paths and not path_included(must_include_paths, full_path, must_include_operator):
                logging.debug("file didn't include the required 'fragments' (%s), skipping! (file: %s)" % (
                    must_include_paths, full_path))
                continue
            if exclude_paths and path_included(exclude_paths, full_path, exclude_operator):
                logging.debug(
                    "file included the exclude 'fragments'(%s), skipping! (file: %s)" % (exclude_paths, full_path))
                continue

            for paths_group, predicate in predicates_dict.iteritems():
                try:
                    if predicate(full_path):
                        res_dict[paths_group].append(full_path)
                except Exception as e:
                    logging.exception("file caused exception using the predicate, skipping! (file: %s)" % full_path)
                    continue
    logging.info("Paths Found: %s" % pformat(res_dict))
    return res_dict


def add_get_paths_function_to_argparser(parser):
    # type: (argparse.ArgumentParser) -> None
    """
    This function adds the common path filtering functions.
    Current options (option, description if needed, and var name):
        -d(root dir) root_dir
        -r(recursion depth) recursion_depth
        -x(exclude sub dirs fragments) exclude_prefixes
        -s(include sub dirs fragments) include_prefixes
        --follow_links follow_links
        --exclude_operator exclude_operator
        --include_operator include_operator
    :param parser: The argparse instance
    :type parser: argparse.ArgumentParser
    :return:None
    """
    operator_options = LOGICAL_OPERATORS.keys()
    parser.add_argument('-d', '--root_dir', metavar="root_dir", dest='root_dir', nargs='?', required=True,
                        help="The input directory.")
    parser.add_argument('-r', '--recursion_depth', metavar="recursion_depth", dest='recursion_depth', nargs='?',
                        required=False, default=100, help="The depth of recursion into the folders.")
    parser.add_argument('-x', '--exclude_prefixes', metavar="exclude_prefixes", dest='exclude_prefixes',
                        nargs='*', required=False, help="Fragments of paths that if present the file will be "
                                                        "*EXCLUDED* (OR operator is the default)", default=[])
    parser.add_argument('-s', '--subdirs_prefixes', metavar="subdirs_prefixes", dest='include_prefixes', nargs='*',
                        required=False, help="Fragments of paths that has to be present for the file to be included"
                                             " (OR operator is the default).",
                        default=[])
    parser.add_argument('--follow_links', dest='follow_links', required=False,
                        action='store_true',
                        help='If set will follow symlinks in the input directory. notice it\'s recursive.')
    parser.add_argument('--exclude_operator', metavar="exclude_operator", dest='exclude_operator',
                        nargs='?', required=False, help="The operator used with the excluded prefixes",
                        default=OR_OPERATOR,
                        choices=operator_options)
    parser.add_argument('--include_operator', metavar="include subdirs operator", dest='include_operator',
                        nargs='?', required=False, help="The operator used with the included subdirs prefixes )",
                        default=OR_OPERATOR,
                        choices=operator_options)


def add_groups_file_to_argparser(parser):
    # type: (argparse.ArgumentParser) -> None
    """
    This function adds the groups and samples file option: -g(groups and samples file) groups_file
    :param argparse.ArgumentParser parser: The parser instance
    :return: None
    """
    parser.add_argument('-g', '--groups_file', dest='groups_file', nargs='?', required=False, default=None,
                        help="The path to an groups and samples csv file containing their metadata (must contain the "
                             "columns 'Group','SampleName', and 'SamplePath'). Data will be automatically associated to"
                             " the group")


def load_groups_and_samples_from_file(groups_file, sep=","):
    """
    This function creates the groups of a path if groups file was given.
    :param sep: The separator fpr the csv.reader
    :param groups_file: The C{str} path to the groups file.
    :return: None.
    """
    with open(groups_file, 'rb') as gf:
        g_data = [line for line in csv.reader(gf, delimiter=sep)]

    headers_line = g_data[0]
    assert GROUPS_FILE_SAMPLE_NAME_HEADER in headers_line and GROUPS_FILE_SAMPLE_PATH_HEADER in headers_line \
           and GROUPS_FILE_GROUP_NAME_HEADER in headers_line, GROUPS_FILE_CORRUPT_ERR_MSG

    indexes_dict = get_index_dict(headers_line, headers_line)  # create index of each header to its location
    for line in g_data[1:]:
        if line:
            parent_group_name = ""
            sample_extra_data = {}
            for i, cell in enumerate(line):
                if indexes_dict[i] == GROUPS_FILE_SAMPLE_NAME_HEADER:
                    sample_name = cell
                elif indexes_dict[i] == GROUPS_FILE_SAMPLE_PATH_HEADER:
                    sample_path = cell
                    if not sample_path.endswith("*"):
                        logging.warn(SAMPLE_PATH_JOKER_WRN)
                elif indexes_dict[i] == GROUPS_FILE_GROUP_NAME_HEADER:
                    group_name = cell
                elif indexes_dict[i] == GROUPS_FILE_PARENT_GROUP_HEADER:
                    parent_group_name = cell
                else:
                    sample_extra_data[indexes_dict[i]] = cell

            sample = Sample(sample_name, sample_path)
            sample.extra_data.update(sample_extra_data)

            group = Group(group_name)
            sample.add_related_entity(group)
            group.add_related_entity(sample)

            if parent_group_name:
                parent_group = Group(parent_group_name)
                parent_group.add_related_entity(group)
                group.parent_group = parent_group


def _flatten_groups_dict(d):
    keys = d.keys()
    if not keys:
        return d
    key = keys[0]
    val = d[key]
    res = [key, ]
    res.extend(_flatten_groups_dict(val))
    return res


SORT_BY_GROUPS_DEC = "GroupsByParentsFirst"


def groups_decreasing(item):
    assert isinstance(item, Sample)
    groups_tree = Group.get_groups_tree(by_name=True, limit_to_samples=[item, ])
    return _flatten_groups_dict(groups_tree) + [item.sample_name, ]


SORT_BY_GROUPS_INC = "GroupsByChildrenFirst"


def groups_increasing(item):
    assert isinstance(item, Sample)
    rev_res = groups_decreasing(item)
    rev_res.reverse()
    return rev_res[1:] + [item.sample_name, ]


SORT_BY_SAMPLE_NAME = "SampleNames"


def sample_names(item):
    assert isinstance(item, Sample)

    return [item.sample_name, ]


SORT_SAMPLES_FUNCTIONS_DICT = {SORT_BY_SAMPLE_NAME: sample_names,
                               SORT_BY_GROUPS_DEC: groups_decreasing,
                               SORT_BY_GROUPS_INC: groups_increasing,
                               }


def get_sorted_samples(samples, sort_function):
    # type: (list, str) -> list
    """
    This function sort the samples according to one  of several implemented ways
    (general_functions.SORT_SAMPLES_FUNCTIONS_DICT)
    :param list[Sample] samples: A list of the samples to sort.
    :param str sort_function: on of the key of general_functions.SORT_SAMPLES_FUNCTIONS_DICT (a sorting function)
    :rtype list[Sample]
    """
    return sorted(samples, key=SORT_SAMPLES_FUNCTIONS_DICT.get(sort_function, None))


def get_groups_and_sample_names_dict(by_sample=False):
    # type: (bool) -> dict
    """
    This function returns a dictionary of group names to their sample names (and samples) to the group instances
    :param bool by_sample: If set the dict will be of dict[sample_name][(group_name, depth), Sample]
    :return: dict[group_name][sample_name, Sample]/[group_name, Group] if by_sample=False
    else dict[sample_name][(group_name, depth), Sample]
    """
    if by_sample:
        group_tree = Group.get_groups_tree(by_name=True)
    group_and_sample_names_dict = dict()
    for group in Group.get_all_records(of_types=(Group,)).values():
        group_and_sample_names_dict[group.group_name] = dict()
        group_and_sample_names_dict[group.group_name][group.group_name] = group
        for sample in group.samples:
            if not by_sample:
                group_and_sample_names_dict[group.group_name][sample.sample_name] = sample
            else:
                depth = get_depth_in_tree(group_tree, group.group_name)
                group_and_sample_names_dict.setdefault(sample.sample_name, {})[(group.group_name, depth)] = sample
    return group_and_sample_names_dict


def get_sample_paths_to_unique_name():
    """
    This function retrieves a unique top group + sample name for each sample mapped to sample path
    :return dict: A dict of sample path to unique name
    """
    top_groups = Group.top_groups()
    samples_paths_to_unique_names = dict()
    for group in top_groups:
        for sample in group.samples:
            samples_paths_to_unique_names[sample.sample_path] = group.group_name + "_" + sample.sample_name
    return samples_paths_to_unique_names


def get_depth_in_tree(tree_dict, lookup_key, depth=0):
    """
    This function find the depth of a value in a tree implemented using a dict.
    :param tree_dict: The current tree root.
    :param lookup_key: The value to look for.
    :param depth: a counter for the recursion
    :return:
    """
    if not isinstance(tree_dict, dict):
        if lookup_key != tree_dict:
            return 0
        else:
            return depth + 1
    curr_sum = 0
    for son in tree_dict:
        if son == lookup_key:
            return depth + 1
        curr_sum += get_depth_in_tree(tree_dict=tree_dict[son], lookup_key=lookup_key, depth=depth + 1)
    return curr_sum


def make_recursive_output_dir(outdir, root, extension, depth):
    out_p = []
    if depth <= 1:
        return os.path.join(outdir, extension)
    while depth > 1:
        tmp = os.path.split(root)
        out_p.append(tmp[1])
        root = tmp[0]
        depth -= 1
    out_p.reverse()

    return os.path.join(outdir, os.path.join(*out_p), extension)


def get_file_handle(file_path, mode='rb'):
    # type: (str, str) -> file
    """
    This function tries several available file opening method, providing the handle to the file.
    *POSSIBLE COMPRESSIONS* None, GZip, BZip2
    :param str file_path: The path to the file to open
    :param str mode: The mode to use when opening.
    """
    try:
        with gzip.open(file_path, mode) as fh:
            _ = fh.readline()
        return gzip.open(file_path, mode)
    except IOError:
        try:
            with bz2.BZ2File(file_path, mode) as fh:
                _ = fh.readline()
            # noinspection PyTypeChecker
            return bz2.BZ2File(file_path, mode)
        except IOError:
            # noinspection PyTypeChecker
            return open(file_path, mode)


def deep_copy_dict(orig_d):
    """
    Deep copies a dictionary
    :param orig_d: the original dictionary
    :return: a copy of orig_d
    """
    new_d = dict()
    for k, val in orig_d.iteritems():
        if isinstance(val, dict):
            new_d[k] = deep_copy_dict(val)
        else:
            new_d[k] = val
    return new_d

