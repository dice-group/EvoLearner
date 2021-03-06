from .abstracts import BaseConcept


class Concept(BaseConcept):
    """
    Concept Class representing Concepts in Description Logic, Classes in OWL.
    """

    def __init__(self, concept, kwargs, world=None):
        super().__init__(concept, kwargs, world)
        self.__parse(kwargs)

    def __parse(self, kwargs):
        """

        :param kwargs:
        :return:
        """
        if not self.is_atomic:
            if self.form in ['ObjectSomeValuesFrom', 'ObjectAllValuesFrom']:
                self.role = kwargs['Role']  # property
                self.filler = kwargs['Filler']  # Concept
            elif self.form in ['ObjectUnionOf', 'ObjectIntersectionOf']:
                self.concept_a = kwargs['ConceptA']
                self.concept_b = kwargs['ConceptB']
            elif self.form in ['ObjectComplementOf']:
                self.concept_a = kwargs['root']
            elif self.form in ['DataHasValue']:
                self.role = kwargs['Role']
                self.value = kwargs['Value']
            elif self.form in ['DataSomeValuesFrom']:
                self.role = kwargs['Role']
                self.facet = kwargs['Facet']
                self.value = kwargs['Value']
            elif self.form in ['ObjectCardinalityRestriction']:
                self.value = kwargs['Value']
                self.facet = kwargs['Facet']
                self.role = kwargs['Role']
                self.filler = kwargs['Filler']
            else:
                print('Wrong type')
                print(self)
                raise ValueError
