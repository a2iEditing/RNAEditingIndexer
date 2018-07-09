"""
config file for the running of the Pipeline procedure
Michal Barak
13-12-2011
Shalom Hillel Roth
17-10-2017
"""

import ConfigParser
import logging
import time
from tempfile import mkstemp

from RNAEditingIndex.GGPSResources.consts import LOGICAL_OPERATORS
from ConfigConsts import *


class EIConfig(ConfigParser.SafeConfigParser):
    def __init__(self, file_name=r"Pipeline.conf"):
        ConfigParser.SafeConfigParser.__init__(self)
        self.__file_name = file_name

    def set_config_file_name(self, file_name):
        self.__file_name = file_name

    @property
    def file_name(self):
        return self.__file_name

    def load_config(self, update_time=True):
        self.read(self.__file_name)
        if update_time:
            timeadd = time.strftime("%d-%m-%Y-%H", time.gmtime())
            self.set_config_file_name(timeadd + ".cnf")

    def defaults(self, formatted=False):
        defaults_dict = ConfigParser.SafeConfigParser.defaults(self)
        if not formatted:
            return defaults_dict
        formatted_defaults = dict()
        for opt in defaults_dict:
            formatted_defaults[opt] = self.get("DEFAULT", opt)

        return formatted_defaults

    def create_view(self, dropped_sections=[], added_sections={}, conf_file_dir=None):
        """
        This function creates a "view" copy of the config with the given changes, first dropped then added, overriding.
        :param dropped_sections: A list of section to drop from the copy.
        :type dropped_sections: C{list} of C{str}
        :param added_sections: A dictionary of the the wanted values to add in the format of section=>option=>value.
        :type added_sections: C{dict} of C{str} to C{dict} of C{str} to C{str}
        :param conf_file_dir: If given, where to save the temp conf.
        :type conf_file_dir: C{str}
        :return: The view copy created.
        :rtype: L{EIConfig}
        """
        copy = self.deepcopy(conf_file_dir)
        for dropped_section in dropped_sections:
            copy.remove_section(dropped_section)

        for section in added_sections:
            for option in added_sections[section]:
                copy.set(section=section, option=option, value=added_sections[section][option])

        copy.WriteConfig()
        copy.load_config(False)
        return copy

    def deepcopy(self, dir=None):
        s_fname = self.__file_name
        handle, path = mkstemp(dir=dir, prefix=self.__file_name + "copy" + time.strftime("%d-%m-%Y-%H", time.gmtime()))
        self.set_config_file_name(path)
        self.WriteConfig()
        self.set_config_file_name(s_fname)

        copy = EIConfig(file_name=path)
        copy.load_config(False)

        return copy

    def WriteConfig(self):
        with open(self.__file_name, 'w') as configfile:
            self.write(configfile)

    def WriteDefaultConfig(self):
        self.add_section('Run')
        self.set('Run', 'working_dir', '.')
        self.set('Run', 'date', '')
        self.set('Run', 'version', '1')

    def enabled(self, step_name):
        if not self.getboolean(step_name, ENABLE_SECTION_OPTION):
            logging.info("Step %s Was Not Enabled, Skipping." % step_name)
            return False
        if self.has_option(step_name, RECOVER_SECTION) and self.getboolean(step_name, RECOVER_SECTION):
            return False
        if self.has_option(step_name, CONSTRAIN_COND_OPTION) and condition(self.get(step_name, CONSTRAIN_COND_OPTION)):
            logging.info("Step %s's Constraint Was Met, Skipping." % step_name)
            return False
        return True

    def get_error_step(self, curr_step):
        """
        This function retrieves the error step for a step.
        :param curr_step: The step to retrieve for.
        :return: The name of the error step
        """
        try:
            error_step = self.get(curr_step, ERROR_STEP_OPTION)
        except ConfigParser.NoOptionError:
            # if error step wasn't specified "inject" the default value (even if the step
            # doesn't exist, this still have logging importance).
            error_step = ERROR_STEP

        return error_step

    def get_next_step(self, curr_step):
        """
        This function retrieves the next step for a given step.
        :param curr_step: The current step.
        :return: The next step according to the condition(s)
        """
        error_step = self.get_error_step(curr_step)

        # get the ordered pairs of next steps and conditions.
        next_s_pairs = [s.strip() for s in self.get(curr_step, NEXT_STEP_OPTION).split(NEXT_STEPS_SEPARATOR)]

        for step_condition_pair in next_s_pairs:
            split_res = [s.strip() for s in step_condition_pair.split(STEP_CONDITION_SEPARATOR)]
            if len(split_res) == 1:
                return split_res[0]
            step = split_res[0]
            con = self.get(curr_step, split_res[1])
            if condition(con):
                return step

        return error_step

    def get_all_next_steps(self, curr_step):
        """
        This function return all possible following steps for a given step (and their matching conditions).
        :param curr_step: The step to get the next steps for.
        :return: A list of matched pairs of a next step and its corresponding condition.
        """
        error_step = self.get_error_step(curr_step)

        # get the ordered pairs of next steps and conditions.
        next_s_pairs = [s.strip() for s in self.get(curr_step, NEXT_STEP_OPTION).split(NEXT_STEPS_SEPARATOR)]

        next_steps = []
        conditions = []
        for step_condition_pair in next_s_pairs:
            split_res = [s.strip() for s in step_condition_pair.split(STEP_CONDITION_SEPARATOR)]
            next_steps.append(split_res[0])
            if len(split_res) > 1:
                conditions.append(self.get(curr_step, split_res[1]))
            else:
                conditions.append(STEP_SEMI_CONDITION)

            if error_step != curr_step:
                next_steps.append(error_step)
                conditions.append(STEP_SEMI_CONDITION)

        return zip(next_steps, conditions)

    def get_all_steps(self, root_step=FIRST_STEP):
        """
        This recursive function retrieves all the steps (unlike just sections) in a config.
        :param root_step: The step to start the recursion with.
        :return: A list of all the possible steps.
        """
        if self.has_section(root_step):
            steps = [root_step]
            next_steps = self.get_all_next_steps(root_step)
            for step, con in next_steps:
                if self.has_section(step):
                    steps.append(step)
                    steps.extend(self.get_all_steps(step))

            return set(steps)


def condition(cond):
    parts = cond.split(IN_CONDITION_SEPARATOR)
    i = 0
    res = None
    while i < len(parts):
        if parts[i] == IN_CONDITION_SEPARATOR:
            continue  # it's a typo
        if parts[i] in LOGICAL_OPERATORS:
            op = LOGICAL_OPERATORS[parts[i]]
            if parts[i + 1] in LOGICAL_OPERATORS:
                op2 = LOGICAL_OPERATORS[parts[i + 1]]
                con = CONDITIONS[parts[i + 2]]
                param = parts[i + 3]
                i += 4
                if res is None:
                    res = op(op2(con(param)))
                else:
                    res = op(res, op2(con(param)))
            else:
                con = CONDITIONS[parts[i + 1]]
                param = parts[i + 2]
                i += 3
                if res is None:
                    res = op(con(param))
                else:
                    res = op(res, con(param))
        else:
            con = CONDITIONS[parts[i]]
            param = parts[i + 1]
            res = con(param)
            i += 2

    return res
