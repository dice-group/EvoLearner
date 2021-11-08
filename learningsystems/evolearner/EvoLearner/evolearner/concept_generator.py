from functools import lru_cache
from .concept import Concept
import concurrent.futures


class ConceptGenerator:

    cache_size = 4000

    def __init__(self, kb, concepts, T, Bottom, onto,
                 max_size_of_concept, min_size_of_concept):
        assert max_size_of_concept
        assert min_size_of_concept

        self.kb = kb
        self.min_size_of_concept = min_size_of_concept
        self.max_size_of_concept = max_size_of_concept
        self.namespace_base_iri = 'https://example.org/'

        self.concepts = concepts
        self.T = T
        self.Bottom = Bottom
        self.onto = onto

        # self.role_log = dict()
        # self.role_log_cardinality = dict()

        self.executor = concurrent.futures.ProcessPoolExecutor()

    @staticmethod
    def __concepts_sorter(A, B):
        if len(A) < len(B):
            return A, B
        if len(A) > len(B):
            return B, A

        args = [A, B]
        args.sort(key=lambda ce: ce.str)
        return args[0], args[1]

    @staticmethod
    def type_enrichment(instances, new_concept):
        for i in instances:
            i.is_a.append(new_concept)

    # TODO: Rewrite/optimize this
    def get_instances_for_restrictions(self, exist, role, filler):
        pairs_dict = self.kb.role_log[role]

        instances = filler.instances
        temp = set()
        if exist:
            for k in instances:
                if k in pairs_dict:
                    temp.update(pairs_dict[k])
            return temp
        else:
            for y in pairs_dict:
                if not (y in instances):
                    temp.update(pairs_dict[y])
            return self.T.instances - temp

    # TODO: Rewrite/optimize this
    def get_instances_value_restriction(self, role, value, facet):
        val_dict = self.kb.role_log[role]

        temp = set()
        if facet == 'eq':
            for k in val_dict.keys():
                if value == val_dict[k]:
                    temp.add(k)
        elif facet == 'geq':
            for k in val_dict.keys():
                if value <= val_dict[k]:
                    temp.add(k)
        elif facet == "leq":
            for k in val_dict.keys():
                if value >= val_dict[k]:
                    temp.add(k)

        return temp

    # TODO: Rewrite/optimize this
    def get_instances_card_restriction(self, role, value,
                                       concept, facet):
        pairs_dict = self.kb.role_log_cardinality[role]

        temp = set()
        instances = concept.instances
        if facet == 'geq':
            for x in pairs_dict.keys():
                tp = instances & pairs_dict[x]
                if len(tp) >= value:
                    temp.add(x)
        elif facet == 'leq':
            for x in pairs_dict.keys():
                tp = instances & pairs_dict[x]
                if len(tp) > value:
                    temp.add(x)
            temp = self.T.instances - temp
        return temp

    @lru_cache(maxsize=cache_size)
    def data_has_value(self, value, relation) -> Concept:
        # if (value, relation) in self.log_of_value_restriction:
        #    return self.log_of_value_restriction[(value, relation)]

        possible_instances_ = self.get_instances_value_restriction(relation,
                                                                   value,
                                                                   'eq')

        c = Concept(concept=None,
                    kwargs={'form': 'DataHasValue',
                            'Role': relation,
                            'Value': value})
        c.str = "({0} = {1})".format(relation.name, str(value))
        c.full_iri = self.namespace_base_iri + c.str
        c.length = c._calculate_length()

        c.instances = possible_instances_

        # self.log_of_value_restriction[(value, relation)] = c

        # return self.log_of_value_restriction[(value, relation)]
        return c

    @lru_cache(maxsize=cache_size)
    def data_some_values(self, value, relation, facet) -> Concept:
        # if (value, relation, facet) in self.log_of_some_value_restriction:
        # return self.log_of_some_value_restriction[(value, relation, facet)]

        possible_instances_ = self.get_instances_value_restriction(relation,
                                                                   value,
                                                                   facet)

        c = Concept(concept=None,
                    kwargs={'form': 'DataSomeValuesFrom',
                            'Role': relation,
                            'Facet': facet,
                            'Value': value})

        if facet == 'geq':
            c.str = "({0}.≥ {1})".format(relation.name, str(value))
        elif facet == 'leq':
            c.str = "({0}.≤ {1})".format(relation.name, str(value))

        c.full_iri = self.namespace_base_iri + c.str
        c.length = c._calculate_length()

        c.instances = possible_instances_

        # self.log_of_some_value_restriction[(value, relation, facet)] = c

        # return self.log_of_some_value_restriction[(value, relation, facet)]
        return c

    @lru_cache(maxsize=cache_size)
    def cardinality_restriction_object(self, value, relation,
                                       concept, facet) -> Concept:
        possible_instances_ = self.get_instances_card_restriction(relation,
                                                                  value,
                                                                  concept,
                                                                  facet)

        c = Concept(concept=None,
                    kwargs={'form': 'ObjectCardinalityRestriction',
                            'Value': value,
                            'Facet': facet,
                            'Role': relation,
                            'Filler': concept})
        if facet == 'geq':
            c.str = "(≥{0} {1}.{2})".format(str(value),
                                            relation.name,
                                            concept.str)
        elif facet == 'leq':
            c.str = "(≤{0} {1}.{2})".format(str(value),
                                            relation.name,
                                            concept.str)

        c.full_iri = self.namespace_base_iri + c.str
        c.length = c._calculate_length()

        c.instances = possible_instances_

        return c

    @lru_cache(maxsize=cache_size)
    def negation(self, concept: Concept) -> Concept:
        """
        ¬C = \\Delta^I \\ C.
        @param concept: an instance of Concept class
        @return: ¬C: an instance of Concept class
        """
        # if concept in self.log_of_negations:
        #    return self.log_of_negations[concept]
        if not (concept.str == 'Thing'):
            possible_instances_ = self.T.instances - concept.instances
            c = Concept(concept=None, kwargs={'form': 'ObjectComplementOf',
                                              'root': concept})
            c.str = "¬{0}".format(concept.str)
            c.full_iri = self.namespace_base_iri + c.str
            c.length = c._calculate_length()
            c.instances = possible_instances_

            return c
        elif concept.str == 'Thing':
            # self.log_of_negations[concept.full_iri] = self.Bottom
            # self.log_of_negations[self.Bottom.full_iri] = concept
            # return self.log_of_negations[concept.full_iri]
            return self.Bottom
        else:
            raise ValueError

    @lru_cache(maxsize=cache_size)
    def existential_restriction(self, concept: Concept,
                                relation, base=None) -> Concept:
        if not base:
            base = self.T.owl

        possible_instances_ = self.get_instances_for_restrictions(True,
                                                                  relation,
                                                                  concept)

        c = Concept(concept=None,
                    kwargs={'form': 'ObjectSomeValuesFrom',
                            'Role': relation,
                            'Filler': concept})
        c.str = "(∃{0}.{1})".format(relation.name, concept.str)
        c.full_iri = self.namespace_base_iri + c.str
        c.length = c._calculate_length()

        c.instances = possible_instances_

        return c

    @lru_cache(maxsize=cache_size)
    def universal_restriction(self, concept: Concept,
                              relation, base=None) -> Concept:
        if not base:
            base = self.T.owl

        possible_instances_ = self.get_instances_for_restrictions(False,
                                                                  relation,
                                                                  concept)

        if not (self.max_size_of_concept >=
                len(possible_instances_) >=
                self.min_size_of_concept):
            return self.Bottom

        c = Concept(concept=None,
                    kwargs={'form': 'ObjectAllValuesFrom',
                            'Role': relation,
                            'Filler': concept})
        c.str = "(∀{0}.{1})".format(relation.name, concept.str)
        c.full_iri = self.namespace_base_iri + c.str
        c.length = c._calculate_length()

        c.instances = possible_instances_

        return c

    @lru_cache(maxsize=cache_size)
    def union(self, A: Concept, B: Concept, base=None):

        A, B = self.__concepts_sorter(A, B)

        # Crude workaround
        if A.str == 'Nothing':
            return B

        if B.str == 'Nothing':
            return A

        if not base:
            base = self.T.owl

        if A.instances == B.instances:
            return A

        possible_instances_ = A.instances | B.instances

        if not (self.max_size_of_concept >=
                len(possible_instances_) >=
                self.min_size_of_concept):
            return self.Bottom
        c = Concept(concept=None,
                    kwargs={'form': 'ObjectUnionOf',
                            'ConceptA': A,
                            'ConceptB': B})
        c.str = "({0} ⊔ {1})".format(A.str, B.str)
        c.full_iri = self.namespace_base_iri + c.str
        c.length = c._calculate_length()

        c.instances = possible_instances_  # A.instances | B.instances

        return c

    @lru_cache(maxsize=cache_size)
    def intersection(self, A: Concept, B: Concept, base=None) -> Concept:
        A, B = self.__concepts_sorter(A, B)

        # Crude workaround
        if A.str == 'Nothing' or B.str == 'Nothing':
            return self.Bottom

        if not base:
            base = self.T.owl

        if A.instances == B.instances:
            return A

        possible_instances_ = A.instances & B.instances

        if not (self.max_size_of_concept >=
                len(possible_instances_) >=
                self.min_size_of_concept):
            return self.Bottom

        c = Concept(concept=None,
                    kwargs={'form': 'ObjectIntersectionOf',
                            'ConceptA': A,
                            'ConceptB': B})
        c.str = "({0} ⊓ {1})".format(A.str, B.str)
        c.full_iri = self.namespace_base_iri + c.str
        c.length = c._calculate_length()
        c.instances = possible_instances_  # A.instances & B.instances

        return c
