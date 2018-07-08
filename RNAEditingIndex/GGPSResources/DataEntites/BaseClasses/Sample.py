__author__ = 'Hillel'
# =====================imports=====================#
from EntityRecord import EntityRecord
from DataRecord import DataRecord

# =====================constants===================#
# error messages
RECORD_ERR = "Sample Got EntityRecord Instance ID That Doesn't Exits! (got %s)"
NON_EXISTING_SAMPLE_IDS_ERROR = "Some Of the Sample IDs Sent Do Not Exist!"


# =====================classes=====================#

class Sample(DataRecord):
    """
    This class represents a single sample of genomic data (e.g. DNA/RNA sequencing from a single patient).

    :ivar sample_path: The path of the sample's file
    :type sample_path: C{string}
    :ivar sample_name: The name of the sample
    :type sample_path: C{string}
    :ivar extra_data: A dictionary holding any extra data about the sample in the format of <description> => <value>.
    :type extra_data: C{dict} of C{string} to C{object}
    """

    @staticmethod
    def get_sample_id(sample_name, sample_path):
        all_samples = EntityRecord.get_all_records(of_types=(Sample,))
        for sample in all_samples:
            if sample.sample_name == sample_name and sample.sample_path == sample_path:
                return sample.record_id

    @staticmethod
    def bind_samples(samples_ids):
        """
        bind the given samples one to the other.
        :param samples_ids: The ids of the samples to bind.
        :type samples_ids: C{list} of C{str}
        :rtype : None
        """
        assert all([EntityRecord.exists(s_id) for s_id in samples_ids]), NON_EXISTING_SAMPLE_IDS_ERROR
        samples = EntityRecord.entity_records_by_ids(samples_ids)
        for i, sample in enumerate(samples):
            tmp = list(samples)
            tmp.remove(sample)
            sample.add_related_entity(tmp)

    @staticmethod
    def sample_names_unique():
        # type: () -> bool
        """
        This function checks if the sample names are unique
        :return: True if they are unique, False if not.
        :rtype bool
        """
        sample_names = [sample.sample_name for sample in EntityRecord.get_all_records(of_types=(Sample,)).values()]
        return len(sample_names) == len(set(sample_names))

    def __init__(self, sample_name, sample_path):
        """
        :type sample_name: C{str}
        :type sample_path: C{str}
        """
        if hasattr(self, "sample_name"):
            return
        self.extra_data = {}
        self.sample_name = sample_name
        self.sample_path = sample_path

    def dump_me(self):
        pass

    @property
    def bound_samples(self):
        """
        :return: The samples bound to this instance
        """
        return self.get_related_entities(of_types=(Sample,))[Sample]
