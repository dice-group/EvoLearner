import operator

from deap import base
from deap import creator
from deap import tools
from deap import gp
from owlready2 import AnnotationPropertyClass, DataPropertyClass, datetime

from evolearner import Concept
from .util import escape
from evolearner import ea_algorithms
from evolearner import fitness_functions
from evolearner import gen_trees
from evolearner.gen_trees import genHalfAndHalf, genFull, genGrow, cxOnePoint
from .value_splitter import EntropyValueSplitter, DefaultValueSplitter
from .gp_utils import PrimitiveGenerator


class EvoLearner:

    def __init__(self, kb, quality_func=None, heuristic_func=None,
                 algorithm='ea_simple',
                 init_method="random_walk",
                 expressivity="ALC(D)N",
                 dp_splitter=None,
                 terminate_on_goal=False,
                 random_walk_type=True,
                 random_walk_paths=True,
                 population_size=800,
                 ngen=200,
                 max_r=2,
                 max_nr_splits=10,
                 max_cardinality=5,
                 random_max_height=6,
                 height_limit=17):
        self.kb = kb
        self.concept_generator = kb._KnowledgeBase__concept_generator
        self.quality_func = quality_func
        self.heuristic_func = heuristic_func
        self.dp_splitter = dp_splitter
        self.expressivity = expressivity
        self.terminate_on_goal = terminate_on_goal
        self.random_walk_type = random_walk_type
        self.random_walk_paths = random_walk_paths
        self.height_limit = height_limit
        self.random_max_height = random_max_height
        self.ngen = ngen
        self.max_r = max_r
        self.init_method = init_method
        self.population_size = population_size
        self.max_nr_splits = max_nr_splits
        self.max_cardinality = max_cardinality
        self.algorithm = getattr(ea_algorithms, algorithm)
        self.use_data_props = False
        self.use_cardinalities = False

        self.result_population = None
        self.splits = {}
        self.types_prop = {}

        self.__setup()

    def __setup(self):
        if self.quality_func is None:
            self.quality_func = fitness_functions.accuracy

        if self.heuristic_func is None:
            self.heuristic_func = fitness_functions.lex_heuristic

        if self.dp_splitter is None:
            self.dp_splitter = EntropyValueSplitter(self.max_nr_splits)

        if "(D)" in self.expressivity:
            self.use_data_props = True

        if "N" in self.expressivity:
            self.use_cardinalities = True

        data_props = self.kb.property_hierarchy.data_properties
        anno_props = self.kb.property_hierarchy.annotation_properties
        self.data_properties = data_props + anno_props

        if not isinstance(self.dp_splitter, EntropyValueSplitter) and \
           self.use_data_props:
            self.splits = self.dp_splitter.compute_splits(data_props)

        self.prim_gen = PrimitiveGenerator(self.concept_generator)

        self.pset = self.__build_primitive_set()
        self.toolbox = self.__build_toolbox()
        self.__set_splitting_values()

    def __build_primitive_set(self):
        pset = gp.PrimitiveSetTyped("concept_tree", [], Concept)
        pset.addPrimitive(self.concept_generator.negation,
                          [Concept],
                          Concept,
                          name='negation')
        pset.addPrimitive(self.concept_generator.union,
                          [Concept, Concept],
                          Concept,
                          name="union")
        pset.addPrimitive(self.concept_generator.intersection,
                          [Concept, Concept],
                          Concept,
                          name="intersection")

        for property_ in self.kb.property_hierarchy.object_properties:

            pairs = list(property_.get_relations())
            pairs_dict = {}
            for x, y in pairs:
                if y.name in pairs_dict:
                    pairs_dict[y.name].append(x.name)
                else:
                    pairs_dict[y.name] = [x.name]
            self.kb.role_log[property_] = pairs_dict

            pairs_dict = {}
            for x, y in pairs:
                if x.name in pairs_dict:
                    pairs_dict[x.name].add(y.name)
                else:
                    pairs_dict[x.name] = {y.name}
            self.kb.role_log_cardinality[property_] = pairs_dict

            existential, universal = (
                self.prim_gen.create_qualifiers(property_))
            pset.addPrimitive(existential,
                              [Concept],
                              Concept,
                              name="exists" + escape(str(property_)))
            pset.addPrimitive(universal,
                              [Concept],
                              Concept,
                              name="forall" + escape(str(property_)))

            if self.use_cardinalities:
                geq, leq = self.prim_gen.create_cardinalities(property_)
                pset.addPrimitive(geq, [int, Concept],
                                  Concept,
                                  name="cargeq" + escape(str(property_)))
                pset.addPrimitive(leq, [int, Concept],
                                  Concept,
                                  name="carleq" + escape(str(property_)))

        if self.use_data_props:
            class Bool(object):
                pass
            for property_ in self.data_properties:
                prop_str = escape(str(property_))
                if isinstance(property_, AnnotationPropertyClass) \
                   or property_.range[0] == float or property_.range[0] == int:

                    pairs = list(property_.get_relations())
                    val_dict = {}
                    for x, y in pairs:
                        val_dict[x.name] = y
                    self.kb.role_log[property_] = val_dict

                    geq, leq = self.prim_gen.create_data_some_values(property_)
                    type_ = type(property_.name, (object,), {})
                    self.types_prop[property_] = type_

                    pset.addPrimitive(geq, [type_],
                                      Concept,
                                      name="someValuesG" + prop_str)
                    pset.addPrimitive(leq, [type_],
                                      Concept,
                                      name="someValuesL" + prop_str)
                elif property_.range[0] == bool:

                    pairs = list(property_.get_relations())
                    val_dict = {}
                    for x, y in pairs:
                        val_dict[x.name] = y
                    self.kb.role_log[property_] = val_dict

                    data_prim = self.prim_gen.create_data_has_value(property_)
                    pset.addPrimitive(data_prim, [Bool],
                                      Concept,
                                      name="hasValue" + prop_str)
                    self.types_prop[property_] = Bool

            pset.addTerminal(False, Bool)
            pset.addTerminal(True, Bool)

        if self.use_cardinalities:
            for i in range(1, self.max_cardinality + 1):
                pset.addTerminal(i, int)

        for c in self.kb.concepts.values():
            pset.addTerminal(c, Concept, name=escape(c.str))

        return pset

    def __set_splitting_values(self):
        for p in self.splits:
            del self.pset.terminals[self.types_prop[p]]
            if len(self.splits[p]) == 0:
                self.pset.addTerminal(0, self.types_prop[p])
            for split in self.splits[p]:
                self.pset.addTerminal(split, self.types_prop[p])

    def __build_toolbox(self):
        creator.create("Fitness", base.Fitness, weights=(1.0,))
        creator.create("quality", base.Fitness, weights=(1.0,))
        creator.create("Individual", gp.PrimitiveTree,
                       fitness=creator.Fitness,
                       quality=creator.quality)

        toolbox = base.Toolbox()
        toolbox.register("expr", genHalfAndHalf,
                         pset=self.pset,
                         min_=3,
                         max_=6)
        toolbox.register("individual", tools.initIterate,
                         creator.Individual,
                         toolbox.expr)
        toolbox.register("population", tools.initRepeat, list,
                         toolbox.individual)
        toolbox.register("compile", gp.compile, pset=self.pset)

        toolbox.register("evaluate", self._fitness_func)
        toolbox.register("select", tools.selTournament, tournsize=7)
        toolbox.register("mate", cxOnePoint)
        toolbox.register("expr_mut", genHalfAndHalf, min_=1, max_=3)
        toolbox.register("mutate", gp.mutUniform,
                         expr=toolbox.expr_mut,
                         pset=self.pset)

        toolbox.decorate("mate",
                         gp.staticLimit(key=operator.attrgetter("height"),
                                        max_value=self.height_limit))
        toolbox.decorate("mutate",
                         gp.staticLimit(key=operator.attrgetter("height"),
                                        max_value=self.height_limit))

        toolbox.register("print", self.print_top_n_individuals)
        toolbox.register("set_result", self.set_result_population)
        toolbox.register("terminate_on_goal", lambda: self.terminate_on_goal)
        toolbox.register("pset", lambda: self.pset)

        return toolbox

    def register_op(self, alias, function, *args, **kargs):
        self.toolbox.register(alias, function, *args, **kargs)
        self.toolbox.decorate(alias,
                              gp.staticLimit(key=operator.attrgetter("height"),
                                             max_value=self.height_limit))

    def fit(self, pos, neg, verbose=False, **params):
        pos_inds = self._retrieve_examples(pos)
        neg_inds = self._retrieve_examples(neg)
        if isinstance(self.dp_splitter, EntropyValueSplitter) \
           and self.use_data_props:
            self.splits = self.dp_splitter.compute_splits(self.data_properties,
                                                          pos_inds, neg_inds)

            for p in self.data_properties:
                if (isinstance(p, AnnotationPropertyClass) or
                        p.range[0] == float or p.range[0] == int) \
                        and p not in self.splits:

                    splitter = DefaultValueSplitter(self.max_nr_splits)
                    self.splits[p] = splitter.compute_split_property(p,
                                                                     self.kb)

            self.__set_splitting_values()

        self.pos = self._parse_examples(pos)
        self.neg = self._parse_examples(neg)

        if self.algorithm == ea_algorithms.ea_simple:
            if self.init_method == "random_full":
                population = self.init_random(genFull,
                                              size=self.population_size,
                                              max_=self.random_max_height)
            elif self.init_method == "random_grow":
                population = self.init_random(genGrow,
                                              size=self.population_size,
                                              max_=self.random_max_height)
            elif self.init_method == "random_rhh":
                population = self.init_random(genHalfAndHalf,
                                              size=self.population_size,
                                              max_=self.random_max_height)
            elif self.init_method == "random_walk":
                population = gen_trees.init_random_walk(self, pos, neg,
                                                        self.population_size,
                                                        ind_size=self.max_r,
                                                        use_type=self.random_walk_type,
                                                        use_paths=self.random_walk_paths)

        self.result_population = self.algorithm(self.toolbox,
                                                population,
                                                self.ngen,
                                                verbose,
                                                **params)
        return self

    def score(self, pos, neg, key='fitness', measure=None):
        assert self.result_population is not None
        assert len(self.result_population) > 0

        pos = self._parse_examples(pos)
        neg = self._parse_examples(neg)

        best = tools.selBest(self.result_population, k=1, fit_attr=key)
        if measure is None:
            return self.quality_func(gp.compile(best[0], self.pset),
                                     pos, neg)
        elif measure == "f1":
            return fitness_functions.f_1(gp.compile(best[0], self.pset),
                                         pos, neg)
        elif measure == "accuracy":
            return fitness_functions.accuracy(gp.compile(best[0], self.pset),
                                              pos, neg)

    def best_hypotheses(self, n=5, key='fitness'):
        assert self.result_population is not None
        assert len(self.result_population) > 0
        best_inds = tools.selBest(self.result_population, k=n, fit_attr=key)
        return [gp.compile(ind, self.pset) for ind in best_inds]

    def _fitness_func(self, individual):
        concept = gp.compile(individual, self.pset)
        quality = self.quality_func(concept, self.pos, self.neg)
        individual.quality.values = (quality,)
        fitness = self.heuristic_func(individual, concept, self.pos, self.neg)
        individual.fitness.values = (fitness,)

    def print_top_n_individuals(self, individuals, top_n=5, key='fitness'):
        best_inds = tools.selBest(individuals, k=top_n, fit_attr=key)
        best_concepts = [(gp.compile(ind, self.pset), ind.quality)
                         for ind in best_inds]
        for concept in best_concepts:
            print(concept[0].str, concept[1])

    def set_result_population(self, population):
        self.result_population = population

    def init_population(self, toolbox, min_=0, max_=6, size=100):
        def expr():
            while True:
                ind = genHalfAndHalf(self.pset, min_, max_, type_=None)
                con = gp.compile(creator.Individual(ind), self.pset)
                length = len(con.instances)
                if length != 0 and length != len(self.kb.thing.instances):
                    break

            return ind

        def gen_individual():
            return tools.initIterate(creator.Individual, expr)

        population = tools.initRepeat(container=list,
                                      func=gen_individual,
                                      n=size)
        return population

    def init_random(self, init_function, size=100, min_=0, max_=6):
        def expr():
            return init_function(self.pset, min_, max_, type_=None)

        def gen_individual():
            return tools.initIterate(creator.Individual, expr)

        population = tools.initRepeat(container=list,
                                      func=gen_individual,
                                      n=size)
        return population

    def _retrieve_examples(self, examples):
        inds_props = dict()
        for example in examples:
            ind = self.kb.onto.search(iri=example)[0]
            properties = list(ind.get_properties())
            properties = sorted(properties, key=lambda x: str(x))
            if not self.use_data_props:
                properties = [p for p in properties if not
                              (isinstance(p, DataPropertyClass) or
                               isinstance(p, AnnotationPropertyClass))]

            properties = [p for p in properties if not
                          (p.name == "label" or
                           (isinstance(p, DataPropertyClass) and
                            (p.range[0] == str or
                             p.range[0] == datetime.date)))]
            inds_props[example] = (ind, properties)
        return inds_props

    def _parse_examples(self, examples):
        new_examples = set()
        for example in examples:
            index = example.find("#")
            if index != -1:
                new_examples.add(example[index + 1:])
            else:
                new_examples.add(example[example.rfind("/") + 1:])
        return new_examples
