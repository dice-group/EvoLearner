class PrimitiveGenerator:

    def __init__(self, generator, min_key='geq', max_key='leq'):
        self.generator = generator
        self.min_key = min_key
        self.max_key = max_key

    def create_qualifiers(self, property_):
        def existential_restriction(concept):
            return self.generator.existential_restriction(concept, property_)

        def universal_restriction(concept):
            return self.generator.universal_restriction(concept, property_)
        return existential_restriction, universal_restriction

    def create_cardinalities(self, property_,):
        def cardinality_min_inclusive(value, concept):
            return self.generator.cardinality_restriction_object(value,
                                                                 property_,
                                                                 concept,
                                                                 self.min_key)

        def cardinality_max_inclusive(value, concept):
            return self.generator.cardinality_restriction_object(value,
                                                                 property_,
                                                                 concept,
                                                                 self.max_key)
        return cardinality_min_inclusive, cardinality_max_inclusive

    def create_data_has_value(self, property_):
        def data_has_value(value):
            return self.generator.data_has_value(value, property_)
        return data_has_value

    def create_data_some_values(self, property_):
        def data_some_min_inclusive(value):
            return self.generator.data_some_values(value,
                                                   property_,
                                                   self.min_key)

        def data_some_max_inclusive(value):
            return self.generator.data_some_values(value,
                                                   property_,
                                                   self.max_key)
        return data_some_min_inclusive, data_some_max_inclusive
