__author__ = 'Hillel'
# =====================imports=====================#
import abc
import os

# =====================constants===================#
ALL_ACCESS = 511


# =====================classes=====================#


class Outputer(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def output(self, *args, **kwargs):
        """
        This function creates the output (virtual).
        :param args: optional arguments.
        :param kwargs: optional key word args.
        :return: None
        """
        pass

    def make_dir(self, path):
        if path and not os.path.isdir(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
            try:
                os.chmod(os.path.dirname(path), ALL_ACCESS)
            except:
                pass

    def chmod_to_all(self, path):
        try:
            os.chmod(path, ALL_ACCESS)
        except:
            pass
