##########################
# quality functions
##########################

def accuracy(concept, pos, neg):
    instances = concept.instances

    if len(instances) == 0:
        return 0

    tp = len(pos.intersection(instances))
    tn = len(neg.difference(instances))

    # FP corresponds to CN in Learning OWL Class Expressions
    # OCEL paper, i.e., cn = |R(C) \AND E^-| covered negatives
    fp = len(neg.intersection(instances))
    # FN corresponds to UP in Learning OWL Class Expressions
    # OCEL paper, i.e., up = |E^+ \ R(C)| uncovered positives
    fn = len(pos.difference(instances))

    acc = (tp + tn) / (tp + tn + fp + fn)
    # acc = 1 - ((fp + fn) / len(self.pos) + len(self.neg))
    # from Learning OWL Class Expressions.
    return round(acc, 5)


def f_1(concept, pos, neg):
    instances = concept.instances

    if len(instances) == 0:
        return 0

    tp = len(pos.intersection(instances))
    fp = len(neg.intersection(instances))
    fn = len(pos.difference(instances))
    try:
        recall = tp / (tp + fn)
        precision = tp / (tp + fp)
        f_1 = 2 * ((precision * recall) / (precision + recall))
    except ZeroDivisionError:
        f_1 = 0

    return round(f_1, 5)


##########################
# heuristic functions
##########################

def celoe_heuristic(individual, concept, pos, neg, x=0,
                    lengthPenalty=0.0001,
                    gainBonusFactor=0.3,
                    startBonus=0.1):
    parent_f1 = individual.parent_quality.values
    fitness = individual.quality.values[0]

    if(len(parent_f1) > 0):
        fitness += (fitness-parent_f1[0])*gainBonusFactor
    else:
        fitness += startBonus

    fitness -= len(concept)*lengthPenalty
    return round(fitness, 5)


def lex_heuristic(individual, concept, pos, neg, x=2048):
    fitness = individual.quality.values[0]
    # if len(individual) <= 5:
    #    fitness = fitness*x
    # else:
    fitness = fitness*x - len(individual)
    return round(fitness, 5)


def f1_heuristic(individual, concept, pos, neg):
    return individual.quality.values[0]
