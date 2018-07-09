__author__ = 'Hillel'
# =====================imports=====================#
from ..BaseClasses.KnownProperty import KnownProperty
from ..BaseClasses.Sample import Sample
from ..BaseClasses.EntityRecord import EntityRecord

# =====================consts======================#
NO_PARENT_GROUP = None


# =====================classes=====================#


class Group(KnownProperty):
    """
    This class holds the data about a group (i.e. a cohort) of samples.
    :ivar group_name: The name of the group.
    :type group_name: C{str}
    :ivar extra_data: A dictionary holding any extra data about the sample in the format of <description> => <value>.
    :type extra_data: C{dict} of C{string} to C{object}
    """

    def dump_me(self):
        pass

    def __init__(self, group_name):
        # type: (str) -> None
        if hasattr(self, "group_name"):
            return
        self.group_name = group_name
        self.parent_group = NO_PARENT_GROUP

        self.extra_data = dict()

    @property
    def samples(self):
        return self.get_related_entities(of_types=(Sample,))[Sample]

    @property
    def group_size(self):
        return len(self.samples)

    @staticmethod
    def top_groups():
        """
        This function returns the topmost groups ("roots" of the groups graph)
        :return: A list of the topmost group(s)
        """
        res = []
        for group in EntityRecord.get_all_records(of_types=Group).values():
            if group.parent_group is NO_PARENT_GROUP:
                res.append(group)
        return res

    @staticmethod
    def get_groups_tree(by_name=False, limit_to_samples=None):
        return Group.__get_groups_tree(by_name=by_name, limit_to_samples=limit_to_samples)

    @staticmethod
    def __get_groups_tree(parent=NO_PARENT_GROUP, by_name=False, limit_to_samples=None):
        """
        This function returns a dict representation of the groups.
        :type limit_to_samples: list[Sample]
        :param parent: The parent group, used for the recursion.
        :param by_name: A flag. If set will return the dictionary with group names instead of ids.
        :type by_name: bool
        :return: A dictionary
        """
        res = {}
        child_groups = EntityRecord.get_all_records(of_types=Group).values()
        for group in child_groups:
            if group.parent_group is parent:
                if limit_to_samples:
                    samples = group.samples
                    if not all([sample in samples for sample in limit_to_samples]):
                        continue
                key = group.group_name if by_name else group.record_id
                res[key] = Group.__get_groups_tree(parent=group, by_name=by_name, limit_to_samples=limit_to_samples)

        return res
