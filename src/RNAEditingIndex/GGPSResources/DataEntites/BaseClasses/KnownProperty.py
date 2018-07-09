__author__ = 'Hillel'
# =====================imports=====================#
import abc

from EntityRecord import EntityRecord


# =====================constants===================#

# =====================classes=====================#


class KnownProperty(EntityRecord):
    """
    This class represent some information known about a certain data or sample (e.g. variants).
    Its is the base class for all types of known information (e.g. editing percentage at locus, SNPsData etc.)
    """
    __metaclass__ = abc.ABCMeta
