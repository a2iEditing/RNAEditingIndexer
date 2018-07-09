__author__ = 'Hillel'
"""
This module contains the singleton base class for all entities.
"""
# =====================imports=====================#
import abc
import logging
from pprint import pformat

# =====================consts======================#
RELATED_ENTITY_TYPE_ERR_MSG = "Trying To Add A Non EntityRecord As Related Entity! (type: %s)"


# =====================classes=====================#


class EntityRecord(object):
    """
    This class is the base type for all nucleotides extracted information (e.g. Sequence, RNA expression of gene,
     Alignment etc.), and is abstract (i.e. one cannot create instances of of the class but can inherit from it)

    :cvar __records: A dictionary (i.e. a hash table) storing all of the EntityRecord instances by their IDs.
    It implements the flyweight pattern, where instances are indexed by the id calculated by the params used to
     create them.
    :type __records: C{dict} of C{int} to L{EntityRecord}.
    note:: Because IDs are calculated based on the values of the field in the instance, different instances
        sharing the same info will have the same ID. Using the locally overridden __new__,
         only instances with new IDS will be created, instances with IDs already "known" will not.

    :ivar __record_id: An injective key to the instance.
    :type __record_id: C{long}
    :ivar __related_entities: An dict of the entities related to the instance by their type.
    :type __related_entities: C{dict} of C{Type} to C{set} of C{EntityRecord}
    """
    __metaclass__ = abc.ABCMeta

    __records = {}

    @staticmethod
    def get_all_records(of_types=(object,)):
        # type: (tuple) -> dict
        """
        :param of_types: The types of entities to return. defaults to object (i.e. all)
        :type of_types: C{list} of C{Type}
        :return: All L{EntityRecord} instances of types P{of_types}.
        :rtype C{dict} of C{str} to L{EntityRecord}
        """
        return {entity_id: entity for entity_id, entity in EntityRecord.__records.iteritems() if
                isinstance(entity, of_types)}

    @staticmethod
    def entity_record_by_id(e_id):
        """
        Get an instance of L{EntityRecord} by its ID.
        :param e_id: The instance's ID.
        :return: The instance, None if not found.
        :rtype: L{EntityRecord}
        """
        return EntityRecord.__records.get(e_id, None)

    @staticmethod
    def entity_records_by_ids(ids):
        """
        Get a list of L{EntityRecord} instances by their ID.
        :param ids: A list of the IDs.
        :return: The instances, None if not found per ID.
        :rtype: C{list} of L{EntityRecord}
        """
        return [EntityRecord.__records.get(e_id, None) for e_id in ids]

    @staticmethod
    def exists(e_id):
        """
        Checks if an ID is known (and therefor the instance exists).
        note:: Use this function to avoid the reallocating of the dict for simple tests.
        :param e_id: The ID to check.
        :type e_id: C{long}
        :rtype : C{bool}
        """
        return e_id in EntityRecord.__records

    @abc.abstractmethod
    def dump_me(self, *args, **kwargs):
        """
        This function should return a dictionary holding all the data of the instance with att names as keys to enable
        pickling and unpickling.
        :return: A dictionary of the instance.
        """
        pass

    def __new__(cls, *args, **kwargs):
        """
        This function implement the flyweight pattern described above (in the class __doc__).
        :return: The new or already existing instance.
        """
        all_args = list(args)
        all_args.extend([kwargs[k] for k in sorted(kwargs.keys())])
        record_id = generate_id_from_args(cls, all_args)
        if record_id in EntityRecord.__records:
            return EntityRecord.__records[record_id]
        else:
            logging.info("Creating new entity of type %s, args %s and kwargs %s" % (str(cls),
                                                                                    pformat(args),
                                                                                    pformat(kwargs)))
            instance = object.__new__(cls, *args, **kwargs)
            instance.__record_id = record_id
            instance.__related_entities = dict()
            EntityRecord.__records[record_id] = instance
            return instance

    @property
    def record_id(self):
        return self.__record_id

    def get_related_entities(self, of_types=(object,)):
        """
        returns a dictionary of the requested types to instances found of them
        :param list[type] of_types: The types looked after
        :return dict[type, list[EntityRecord]]: a dict of the found instances
        """
        # type: (list) -> dict
        related_e_d = dict()
        for entity in self.__related_entities.values():
            if isinstance(entity, of_types):
                related_e_d.setdefault(type(entity), []).append(entity)

        return related_e_d

    def add_related_entity(self, entity):
        """
        This function adds a connection to an entity
        :param EntityRecord entity: The entity to add.
        :return: None
        """
        assert isinstance(entity, EntityRecord), RELATED_ENTITY_TYPE_ERR_MSG % type(entity)
        self.__related_entities[entity.record_id] = entity

    def add_related_entity_by_ids(self, e_ids):
        """
        This function adds a connection to an entity
        :param e_ids: The ID(s) of the entities to add.
        :return: None
        """
        entities = EntityRecord.entity_records_by_ids(e_ids)
        for e in entities:
            self.__related_entities[e.record_id] = e

    def remove_related_entity(self, e_id):
        """
        This function removes a connection to an entity
        :param e_id: The entity to remove the connection to.
        :return: None
        """
        entity = EntityRecord.entity_record_by_id(e_id)
        try:
            _ = self.__related_entities.pop(entity.record_id)
        except KeyError:
            pass

    @staticmethod
    def remove_entity(e_id):
        """
        This function removes an entity from the collection
        :param e_id: The entity's ID
        :return: None
        """
        for entity in EntityRecord.get_all_records().values():
            entity.remove_related_entity(e_id)
        EntityRecord.__records.pop(e_id)


# =====================functions=====================#


def generate_id_from_args(cls_type, args):
    """
    This function return an injective ID to an instance.
    :param cls_type: The type of the instance to get ID for
    :param args: The arguments sent to create it.
    :return: The ID generated
    :rtype C{long}
    """
    return "_".join([str(x) for x in list(args) + [str(cls_type), ]])
