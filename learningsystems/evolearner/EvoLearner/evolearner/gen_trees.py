import random
import itertools
import sys
from inspect import isclass
from collections import defaultdict
from itertools import chain
from functools import partial
from operator import eq, lt

from owlready2 import ObjectPropertyClass, DataPropertyClass
from owlready2 import AnnotationPropertyClass, Restriction, datetime
from deap import creator

from evolearner import Concept
from evolearner import util

__type__ = object

# next 4 functions modified from
# https://github.com/DEAP/deap/blob/master/deap/gp.py


def genGrow(pset, min_, max_, type_=None):
    def condition(height, depth):
        return depth == height or \
               (depth >= min_ and random.random() < pset.terminalRatio)
    return generate_r(pset, min_, max_, condition, type_)


def genHalfAndHalf(pset, min_, max_, type_=None):
    method = random.choice((genGrow, genFull))
    return method(pset, min_, max_, type_)


def genFull(pset, min_, max_, type_=None):
    def condition(height, depth):
        return depth == height

    return generate_r(pset, min_, max_, condition, type_)


def generate_r(pset, min_, max_, condition, type_=None):
    if type_ is None:
        type_ = pset.ret
    expr = []
    height = random.randint(min_, max_)
    stack = [(0, type_)]
    while len(stack) != 0:
        depth, type_ = stack.pop()
        if condition(height, depth):
            try:
                term = random.choice(pset.terminals[type_])
            except IndexError:
                _, _, traceback = sys.exc_info()
                raise IndexError("The gp.generate function tried to add "
                                 "a terminal of type '%s', but there is "
                                 "none available."
                                 % (type_,)).with_traceback(traceback)
            if isclass(term):
                term = term()
            expr.append(term)
        else:
            try:
                prim = random.choice(pset.primitives[type_])
            except IndexError:
                try:
                    term = random.choice(pset.terminals[type_])
                except IndexError:
                    _, _, traceback = sys.exc_info()
                    raise IndexError

                if isclass(term):
                    term = term()
                expr.append(term)
                continue

            expr.append(prim)
            for arg in reversed(prim.args):
                stack.append((depth + 1, arg))

    return expr


def init_random_walk(evo_learner, pos, neg, population_size,
                     pos_con_else_neg=True, ind_size=6,
                     use_type=True, use_paths=True):
    types = {}
    if pos_con_else_neg:
        examples = pos
    else:
        examples = neg

    types = dict()
    inds = []
    for example in examples:
        ind = evo_learner.kb.onto.search(iri=example)[0]
        inds.append(ind)
        for t in ind.is_a:
            types[t] = 0

    for ind in inds:
        ind_types = set(ind.is_a) | set(chain.from_iterable([t.ancestors()
                                        for t in ind.is_a]))
        common_types = types.keys() & ind_types
        for t in common_types:
            types[t] += 1

    count = 0
    trees = []
    for ind in itertools.cycle(inds):
        count += 1
        tree = build_tree(ind, evo_learner, ind_size, types=types,
                          use_type=use_type, use_paths=use_paths)
        if not pos_con_else_neg:
            pass
        trees.append(creator.Individual(tree))
        if count == population_size:
            return trees  #


def build_tree(ind, evo_learner, ind_size, types=None,
               use_type=True, use_paths=True):
    pset = evo_learner.pset

    if len(pset.primitives[Concept]) <= 3:
        return build_only_types(ind, evo_learner, ind_size, types)

    properties = list(ind.get_properties())
    properties = sorted(properties, key=lambda x: str(x))

    if not evo_learner.use_data_props:
        properties = [p for p in properties
                      if not (isinstance(p, DataPropertyClass) or
                              isinstance(p, AnnotationPropertyClass))]

    properties = [p for p in properties
                  if not (p.name == "label" or
                          (isinstance(p, DataPropertyClass) and
                           (p.range[0] == str or
                            p.range[0] == datetime.date)))]
    prop_objs = []

    if len(properties) <= ind_size:
        for p in properties:
            prop_objs.append((p, random.choice(p[ind])))
    else:
        temp_props = random.sample(properties, k=ind_size)
        for p in temp_props:
            prop_objs.append((p, random.choice(p[ind])))

    if len(prop_objs) < ind_size:
        temp = []
        for p in properties:
            for o in p[ind]:
                if (p, o) not in prop_objs:
                    temp.append((p, o))
        if len(temp) > (ind_size - len(prop_objs)):
            prop_objs += random.sample(temp, k=ind_size - len(prop_objs))
        else:
            prop_objs += temp

    properties = prop_objs
    expr = []

    if use_type and use_paths:
        add_intersection_or_union(expr, pset)

    if use_type:
        types_ind, weights = filter_types(ind, types)
        type_ = random.choices(types_ind, weights=weights)[0]
        add_object_terminal(expr, pset, type_)

    if use_paths:
        for i in range(len(properties)):
            if i != len(properties) - 1:
                add_intersection_or_union(expr, pset)

            if isinstance(properties[i][0], ObjectPropertyClass):
                build_object_property(expr, ind, properties[i], pset, evo_learner)
            elif isinstance(properties[i][0], AnnotationPropertyClass):
                build_float_property(expr, ind, properties[i], pset, evo_learner)
            elif properties[i][0].range[0] == bool:
                build_bool_property(expr, ind, properties[i], pset, evo_learner)
            elif properties[i][0].range[0] == float or \
                 properties[i][0].range[0] == int:
                build_float_property(expr, ind, properties[i], pset, evo_learner)

    return expr


def add_intersection_or_union(expr, pset):
    if random.random() <= 0.5:
        expr.append(pset.primitives[Concept][2])
    else:
        expr.append(pset.primitives[Concept][1])


def add_object_terminal(expr, pset, type_):
    for t in pset.terminals[Concept]:
        if t.name == util.escape(str(type_)):
            expr.append(t)
            return


def add_data_terminal(expr, evo, property_, value):
    for t in evo.pset.terminals[evo.types_prop[property_[0]]]:
        if t.name == str(value):
            expr.append(t)
            return


def add_primitive(expr, pset, property_):
    for p in pset.primitives[Concept]:
        if p.name == property_:
            expr.append(p)
            return


def filter_types(ind, types):
    types_ind = set()
    for t in ind.is_a:
        if isinstance(t, Restriction):
            continue
        types_ind.add(t)
        for anc in t.ancestors():
            if anc in types:
                types_ind.add(anc)

    types_ind = sorted(list(types_ind), key=lambda x: str(x))
    weights = []
    for t in types_ind:
        weights.append(types[t])

    return types_ind, weights


def build_only_types(ind, evo_learner, ind_size, types):
    types_ind, weights = filter_types(ind, types)
    if len(types_ind) > ind_size:
        types_ind = random.choices(types_ind, weights, k=ind_size)

    expr = []
    for idx, type_ in enumerate(types_ind):
        if idx != len(types_ind) - 1:
            add_intersection_or_union(expr, evo_learner.pset)
        add_object_terminal(expr, evo_learner.pset, type_)

    return expr


def build_bool_property(expr, ind, property_, pset, evo):
    prop = "hasValue" + util.escape(str(property_[0]))
    add_primitive(expr, pset, prop)

    value = property_[1]
    add_data_terminal(expr, evo, property_, value)


def build_float_property(expr, ind, property_, pset, evo):
    value = property_[1]
    splits = evo.splits[property_[0]]
    if len(splits) != 0:
        nearest_value = min(splits, key=lambda k: abs(k - value))
    else:
        nearest_value = 0

    if nearest_value <= value:
        prop = "someValuesG" + util.escape(str(property_[0]))
    else:
        prop = "someValuesL" + util.escape(str(property_[0]))

    add_primitive(expr, pset, prop)
    add_data_terminal(expr, evo, property_, nearest_value)


def build_object_property(expr, ind, property_, pset, evo):
    prop = "exists" + util.escape(str(property_[0]))
    add_primitive(expr, pset, prop)

    ind2 = property_[1]
    if isclass(ind2):
        p_types = list(ind2.descendants())
        properties2 = list(ind2.get_properties(ind2))
    else:
        p_types = ind2.is_a
        properties2 = list(ind2.get_properties())

    p_types = sorted(p_types, key=lambda x: str(x))
    properties2 = sorted(properties2, key=lambda x: str(x))
    if not evo.use_data_props:
        properties2 = [p for p in properties2
                       if not (isinstance(p, DataPropertyClass) or
                               isinstance(p, AnnotationPropertyClass))]

    properties2 = [p for p in properties2
                   if not (p.name == "label" or
                           (isinstance(p, DataPropertyClass) and
                            (p.range[0] == str or
                             p.range[0] == datetime.date)))]
    proper = None
    if len(properties2) > 0:
        proper = random.choice(properties2)
        while (ind in proper[ind2] or (
               isinstance(proper, DataPropertyClass) and
               (isinstance(proper, AnnotationPropertyClass) or
                proper.range[0] == float or proper.range[0] == int)
                and proper not in evo.splits)) and len(properties2) > 1:
            properties2.remove(proper)
            proper = random.choice(properties2)

    if proper is not None and ind not in proper[ind2] \
       and random.random() < 0.5 and \
       not (isinstance(proper, DataPropertyClass) and
            (isinstance(proper, AnnotationPropertyClass) or
             proper.range[0] == float or proper.range[0] == int) and
       proper not in evo.splits):
        if isinstance(proper, DataPropertyClass):
            if proper.range[0] == bool:
                build_bool_property(expr, ind2, (proper, proper[ind2][0]),
                                    pset, evo)
            elif proper.range[0] == float or proper.range[0] == int:
                build_float_property(expr, ind2, (proper, proper[ind2][0]),
                                     pset, evo)
        elif isinstance(proper, AnnotationPropertyClass):
            build_float_property(expr, ind2, (proper, proper[ind2][0]),
                                 pset, evo)
        else:
            prop = "exists" + util.escape(str(proper))
            add_primitive(expr, pset, prop)

            p_types = proper[ind2][0].is_a
            p_types = sorted(p_types, key=lambda x: str(x))
            type_ = random.choice(p_types)
            add_object_terminal(expr, pset, type_)
    else:
        type_ = random.choice(p_types)
        add_object_terminal(expr, pset, type_)


# crossover functions modified from
# https://github.com/DEAP/deap/blob/master/deap/gp.py so they
# work with a seed
def cxOnePoint(ind1, ind2):
    if len(ind1) < 2 or len(ind2) < 2:
        # No crossover on single node tree
        return ind1, ind2

    # List all available primitive types in each individual
    types1 = defaultdict(list)
    types2 = defaultdict(list)
    if ind1.root.ret == __type__:
        # Not STGP optimization
        types1[__type__] = range(1, len(ind1))
        types2[__type__] = range(1, len(ind2))
        common_types = [__type__]
    else:
        for idx, node in enumerate(ind1[1:], 1):
            types1[node.ret].append(idx)
        for idx, node in enumerate(ind2[1:], 1):
            types2[node.ret].append(idx)
        common_types = set(types1.keys()).intersection(set(types2.keys()))

    if len(common_types) > 0:
        common_types = sorted(common_types, key=lambda x: x.__name__)
        type_ = random.choice(list(common_types))

        index1 = random.choice(types1[type_])
        index2 = random.choice(types2[type_])

        slice1 = ind1.searchSubtree(index1)
        slice2 = ind2.searchSubtree(index2)
        ind1[slice1], ind2[slice2] = ind2[slice2], ind1[slice1]

    return ind1, ind2


def cxOnePointLeafBiased(ind1, ind2, termpb):

    if len(ind1) < 2 or len(ind2) < 2:
        # No crossover on single node tree
        return ind1, ind2

    # Determine whether to keep terminals or primitives for each individual
    terminal_op = partial(eq, 0)
    primitive_op = partial(lt, 0)
    arity_op1 = terminal_op if random.random() < termpb else primitive_op
    arity_op2 = terminal_op if random.random() < termpb else primitive_op

    # List all available primitive or terminal types in each individual
    types1 = defaultdict(list)
    types2 = defaultdict(list)

    for idx, node in enumerate(ind1[1:], 1):
        if arity_op1(node.arity):
            types1[node.ret].append(idx)

    for idx, node in enumerate(ind2[1:], 1):
        if arity_op2(node.arity):
            types2[node.ret].append(idx)

    common_types = set(types1.keys()).intersection(set(types2.keys()))

    if len(common_types) > 0:
        common_types = sorted(common_types, key=lambda x: x.__name__)
        # Set does not support indexing
        type_ = random.sample(common_types, 1)[0]
        index1 = random.choice(types1[type_])
        index2 = random.choice(types2[type_])

        slice1 = ind1.searchSubtree(index1)
        slice2 = ind2.searchSubtree(index2)
        ind1[slice1], ind2[slice2] = ind2[slice2], ind1[slice1]

    return ind1, ind2
