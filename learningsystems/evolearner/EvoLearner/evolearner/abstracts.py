from functools import total_ordering
from abc import ABCMeta, abstractmethod
from owlready2 import ThingClass
from .util import get_full_iri
from typing import Set


@total_ordering
class BaseConcept(metaclass=ABCMeta):
    """Base class for Concept."""
    __slots__ = ['owl', 'world', 'full_iri', 'str',
                 'is_atomic', '__instances',
                 '__idx_instances', 'embeddings',
                 'length', 'form', 'role', 'filler',
                 'concept_a', 'concept_b', 'value', 'facet']

    @abstractmethod
    def __init__(self, concept: ThingClass, kwargs, world=None):
        # assert isinstance(concept, ThingClass)
        assert kwargs['form'] in ['Class', 'ObjectIntersectionOf',
                                  'ObjectUnionOf', 'ObjectComplementOf',
                                  'ObjectSomeValuesFrom',
                                  'ObjectAllValuesFrom',
                                  'DataHasValue', 'DataSomeValuesFrom',
                                  'ObjectCardinalityRestriction']

        self.owl = concept
        self.world = world
        if concept is not None:
            self.full_iri = get_full_iri(concept)
            self.str = concept.name
            self.length = self._calculate_length()
        self.form = kwargs['form']

        self.is_atomic = True if self.form == 'Class' else False
        self.__idx_instances = None

        self.embeddings = None
        self.__instances = None

    @property
    def instances(self) -> Set:
        """ Returns all instances belonging to the concept."""
        if self.__instances is not None:
            return self.__instances
        self.__instances = {jjj.name
                            for jjj in self.owl.instances(world=self.world)}
        return self.__instances

    @instances.setter
    def instances(self, x: Set):
        """ Setter of instances."""
        self.__instances = x

    @property
    def idx_instances(self):
        """ Getter of integer indexes of instances."""
        return self.__idx_instances

    @idx_instances.setter
    def idx_instances(self, x):
        """ Setter of idx_instances."""
        self.__idx_instances = x

    def __str__(self):
        return '{self.__repr__}\t{self.full_iri}'.format(self=self)

    def __len__(self):
        return self.length

    def _calculate_length(self):
        """
        The length of a concept is defined as
        the sum of the numbers of
            concept names, role names, quantifiers,
            and connective symbols occurring in the concept

        The length |A| of a concept CAis defined inductively:
        |A| = |\top| = |\bot| = 1
        |¬D| = |D| + 1
        |D \\sqcap E| = |D \\sqcup E| = 1 + |D| + |E|
        |∃r.D| = |∀r.D| = 2 + |D|
        :return:
        """
        num_of_exists = self.str.count("∃")
        num_of_for_all = self.str.count("∀")
        num_of_negation = self.str.count("¬")
        is_dot_here = self.str.count('.')

        num_of_operand_and_operator = len(self.str.split())
        count = num_of_negation + num_of_operand_and_operator + (
                num_of_exists + is_dot_here + num_of_for_all)
        return count

    def __is_atomic(self):
        """
        @todo Atomic class definition must be explicitly defined.
        Currently we consider all concepts having length=1 as atomic.
        :return: True if self is atomic otherwise False.
        """
        if '∃' in self.str or '∀' in self.str:
            return False
        elif '⊔' in self.str or '⊓' in self.str or '¬' in self.str:
            return False
        return True

    def __lt__(self, other):
        return self.length < other.length

    def __gt__(self, other):
        return self.length > other.length
