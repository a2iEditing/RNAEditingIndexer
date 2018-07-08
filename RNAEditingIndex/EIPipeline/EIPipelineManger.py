__author__ = 'Hillel'
"""
This module is based on Michal Barak's script - Pipeline.
"""
# =====================imports=====================#
# region Builtin Import
import logging.config
import multiprocessing
import subprocess
import sys
from ConfigParser import NoOptionError
from re import compile

# endregion

# region Internal Imports
from EIConfig import *
from ConfigConsts import MAX_STEP_PROCESSES_OPTION, OVERALL_MAX_PS_OPTION, STEP_TYPE_OPTION, \
    STEP_NAME_OPTION, PROGRAM_NAME_OPTION, PROGRAM_PARAMS_OPTION, RECOVER_SECTION, FIRST_STEP
from RNAEditingIndex.GGPSResources.general_functions import get_path_depth, remove_files, get_groups_and_sample_names_dict, \
    make_recursive_output_dir
from RNAEditingIndex.GGPSResources.DataEntites.BaseClasses.Sample import Sample
from RNAEditingIndex.GGPSResources.DataEntites.KnownProperties.Group import Group

# endregion

# =====================constants===================#
# A string format for the subprocesses names.
PIPELINE_SUB_PS_NAME = "Editing_Index_Pipline_%s"

# ---defaults---
# The default value of the maximal number of processes running simultaneously.
MAX_PROCESSES_NUM = 10
# Default values for kill flag
KILL_FLAG = os.path.join(".", "end")
# log file's default path
LOG_DIR = os.path.join(".", "PipelineLogs", "pipeline %s.log")

# ---logging string formats---
START_STEP = "Process: %(ps_name)s; Started Step: %(step)s - %(name)s"
RUNNING_STEP = "Process: %(ps_name)s; Running Step: %(step)s"
ERROR_STEP_MSG = "Process: %(ps_name)s; Going To Error Step: %(step)s"
END_STEP = "Process: %(ps_name)s; Finished Step: %(step)s"
STARTED_RUNNING = "Started Running Editing Index Pipeline"
FINISHED_RUNNING = "Finished Running Editing Index Pipeline"
FILE_FLOW_START = "Started Processing File %(file)s"
PS_END = "Process: %(ps_name)s; Exited With Code: %(ret_code)s"
RAN_ON_MSG = "Ran (Or Running) On %s Files So Far"

KW_ARGS_RE = compile("(?:^ *\w*=.*$)|(?:^$)")


# =====================functions===================#


def RunSteps(config, sema_dict, first_step_name=FIRST_STEP):
    """
    This function is a single linear subprocesses following the pipeline
    :param config: The configuration obejct.
    :type config: L{EIConfig.EIConfig}
    :param sema_dict: The semaphore to step dict.
    :param first_step_name: The name of the first step.
    :return: None
    """
    step_name = first_step_name
    while True:
        try:
            if not config.has_section(step_name):
                logging.info("Next Step %s Doesn't Exist - Assuming Exit Step!" % step_name)
                break

            logging.debug(multiprocessing.current_process().name)
            sema_dict[step_name].acquire()
            logging.debug(START_STEP % {'ps_name': multiprocessing.current_process().name, 'step': step_name,
                                        'name': config.get(step_name, STEP_NAME_OPTION)})
            retcode = RunStep(config, step_name)
            sema_dict[step_name].release()

            if retcode == 0:
                config.set(step_name, RECOVER_SECTION, "True")
                logging.debug(END_STEP % {'ps_name': multiprocessing.current_process().name, 'step': step_name})
                step_name = config.get_next_step(step_name)
                logging.debug("going to " + step_name + "\n")
            else:
                step_name = config.get(step_name, ERROR_STEP_OPTION)
                logging.error(ERROR_STEP_MSG % {'ps_name': multiprocessing.current_process().name, 'step': step_name})
        except Exception, e:
            err_step = config.get(step_name, ERROR_STEP_OPTION)
            logging.exception(
                "Pipeline Encountered An Exception On %s! Going To Error Step %s" % (step_name, err_step))
            logging.error(ERROR_STEP_MSG % {'ps_name': multiprocessing.current_process().name, 'step': err_step})
            step_name = err_step
    sema_dict[OVERALL_MAX_PS_OPTION].release()
    logging.debug(PS_END % {"ret_code": str(retcode), "ps_name": multiprocessing.current_process().name})


def RunStep(config, step_name):
    """
    This function runs a signle step in the pipeline.
    :param config:The configuration obejct.
    :type config: L{EIConfig.EIConfig}
    :param step_name:
    :return:
    """
    retcode = 0
    if not config.enabled(step_name):
        return retcode
    logging.debug(RUNNING_STEP % {'ps_name': multiprocessing.current_process().name, 'step': step_name})
    if config.get(step_name, STEP_TYPE_OPTION) == "cmd":
        program_name = config.get(step_name, PROGRAM_NAME_OPTION)
        program_paras = config.get(step_name, PROGRAM_PARAMS_OPTION)
        logging.debug(program_name + " " + program_paras + '\n')
        retcode = subprocess.call(program_name + " " + program_paras, shell=True, )
        logging.debug("returned: " + str(retcode) + "\n")
    elif config.get(step_name, STEP_TYPE_OPTION) == "shell":
        program_name = config.get(step_name, PROGRAM_NAME_OPTION)
        program_paras = config.get(step_name, PROGRAM_PARAMS_OPTION)
        logging.debug(program_name + " " + program_paras + '\n')
        retcode = subprocess.call(program_name + " " + program_paras, shell=True)
        logging.debug("returned: " + str(retcode) + "\n")

    return retcode


def Pipeline_mt(config, sema_dict):
    outdir = config.get("DEFAULT", "output_dir")

    os.chdir(outdir)
    RunSteps(config=config, sema_dict=sema_dict)
    del config


def run_on_dir(root_path, output_dir, bam_files_suffix, config, files, log_dir, create_na_group=False,
               just_get_configs=False):
    semaphore_dict = create_semaphores(config, config.get_all_steps())
    temp_conf_files = []  # for cleanup
    created_dirs_and_files = []  # for revert
    exception = None  # for exception handling
    samples_confs = dict()

    file_counter = 0
    if not create_na_group:
        samples_dict = get_groups_and_sample_names_dict(by_sample=True)

    if not os.path.isdir(os.path.join(log_dir, "flags")):
        os.makedirs(os.path.join(log_dir, "flags"))
        created_dirs_and_files.append(os.path.join(log_dir, "flags"))
    try:
        for full_file_name in files:
            file_name = os.path.basename(full_file_name)
            logging.info(RAN_ON_MSG % file_counter)

            if not file_name.endswith(".flg"):
                short_file_name = file_name.replace(bam_files_suffix, "")
                root = os.path.dirname(full_file_name)
                new_o_dir = make_recursive_output_dir(outdir=output_dir,
                                                      root=root,
                                                      extension=short_file_name,
                                                      depth=get_path_depth(full_file_name) - get_path_depth(root_path))
                if create_na_group:
                    sample = Sample(short_file_name, full_file_name)
                    na_group = Group("Editing_Index_Unknown")
                    na_group.add_related_entity(sample)
                    sample.add_related_entity(na_group)
                else:
                    try:
                        sample = samples_dict[short_file_name].values()[0]
                    except KeyError as e:
                        logging.exception(
                            "Samples Names Don't Match, Probably There's Problem With Either Groups File or "
                            "the -t Option")
                        raise e
                if not just_get_configs:
                    # Check if the file is already processed in another run.
                    flag_name = flags_dir(log_dir, short_file_name)
                    if not os.path.exists(flag_name):  # for more than one run parallel
                        try:
                            open(flag_name, "w")
                        except:
                            logging.warn(
                                "Could Not Create Flag For %s, This May Cause Down-Stream Problems!" % file_name)
                    else:
                        continue  # The file is already processed in another run.

                    logging.debug(FILE_FLOW_START % {'file': file_name})

                    if not os.path.exists(new_o_dir):
                        os.makedirs(new_o_dir)
                        created_dirs_and_files.append(new_o_dir)

                updated_options = {"DEFAULT": {"input_dir": root,
                                               "file_name": short_file_name,
                                               "output_dir": new_o_dir,
                                               "input_file": full_file_name}
                                   }
                config_copy = config.create_view(added_sections=updated_options)
                samples_confs[sample.record_id] = config_copy
                temp_conf_files.append(config_copy.file_name)
                if just_get_configs:
                    continue
                semaphore_dict[OVERALL_MAX_PS_OPTION].acquire()

                tr = multiprocessing.Process(target=Pipeline_mt, args=(config_copy, semaphore_dict),
                                             name=PIPELINE_SUB_PS_NAME % short_file_name)
                tr.daemon = True
                tr.start()

                file_counter += 1

            active = multiprocessing.active_children()
            for tr in active:
                tr.join(timeout=1)

        active = multiprocessing.active_children()
        for tr in active:
            tr.join()

    except Exception as e:
        exception = sys.exc_info()
    finally:
        return temp_conf_files, created_dirs_and_files, exception, samples_confs


def flags_dir(log_dir, short_file_name):
    return os.path.join(log_dir, "flags", short_file_name + ".flg")


def create_semaphores(config, steps):
    """
    This function creates semaphores for all the steps according to what was defined on each step's configuration.
    :param config: The L{EIConfig} instace used for this run.
    :param steps: A list of all the steps in the config.
    :return: A dictionary containing all the semaphores mapped to the step name.
    :rtype: C{dict} of C{str} to C{multiprocessing.Semaphore}
    """
    sema_dict = dict()

    for step in steps:
        try:
            max_ps_num = config.get(step, MAX_STEP_PROCESSES_OPTION)  # get max num. of processes for the step
        except NoOptionError:
            max_ps_num = MAX_PROCESSES_NUM
        sema_dict[step] = multiprocessing.Semaphore(int(max_ps_num))  # init a semaphore with that number.
    try:
        max_ps_num = config.get(step, OVERALL_MAX_PS_OPTION)  # get max num. of processes for the step
    except NoOptionError:
        max_ps_num = MAX_PROCESSES_NUM
    sema_dict[OVERALL_MAX_PS_OPTION] = multiprocessing.Semaphore(int(max_ps_num))  # init a semaphore with that number.

    return sema_dict


def run_pipeline(root_path, output_dir, bam_files_suffix, full_conf_path, defaults_conf_path,
                 defaults_override_conf_path,
                 defaults_override_args, files, log_dir, create_na_group=False, just_get_configs=False):
    # type: (str, str, str, str, str, str, dict, list, str, list, bool) -> dict

    del_files = []

    logging.info(STARTED_RUNNING)
    full_conf = EIConfig(full_conf_path)
    full_conf.load_config()
    del_files.append(full_conf.file_name)
    defaults_conf = EIConfig(defaults_conf_path)
    defaults_conf.load_config()
    del_files.append(defaults_conf.file_name)

    defaults_override = defaults_conf.defaults()

    if defaults_override_conf_path:
        defaults_override_conf = EIConfig(defaults_override_conf_path)
        defaults_override_conf.load_config(False)
        defaults_override.update(defaults_override_conf.defaults())

    defaults_override.update(defaults_override_args)

    config_copy = full_conf.create_view(added_sections=dict(DEFAULT=defaults_override))
    del_files.append(config_copy.file_name)

    to_del_files, created_dirs_and_files, exception, samples_confs = run_on_dir(root_path, output_dir, bam_files_suffix,
                                                                                config_copy, files, log_dir,
                                                                                create_na_group, just_get_configs)

    logging.info(FINISHED_RUNNING)

    if exception:
        logging.error("Fatal Exception Occurred While Running Pipeline!", exc_info=exception)
        remove_files(to_del_files)
        remove_files(del_files)
        remove_files(created_dirs_and_files)
        raise exception

    remove_files(to_del_files)
    remove_files(del_files)

    return samples_confs
