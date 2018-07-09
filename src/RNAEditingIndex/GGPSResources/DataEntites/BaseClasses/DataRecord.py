__author__ = 'Hillel'
"""
This module contains the three base classes for the "raw" genomic data - DataRecord, Sequence and Alignment.
In addition, it contains the GenomicRecordProperty base class.
"""
# =====================imports=====================#
# region Builtin Imports
import abc
# endregion

from EntityRecord import EntityRecord


# endregion

# =====================classes=====================#


# Genomic Records
class DataRecord(EntityRecord):
    """
    This class is the base type for all extracted information (e.g. Sequence, RNA expression of gene, Alignment etc.)
    that doesn't relate to a specific sample.
    """
    __metaclass__ = abc.ABCMeta
