import random
from deap import tools

######################################
# EA Simple from the DEAP library
######################################


def ea_simple(toolbox, population, ngen, verbose, cxpb=0.9,
              mutpb=0.1, elitism=False, elite_size=0.01):
    for p in population:
        toolbox.evaluate(p)

    goal = False
    for g in range(ngen):
        if elitism:
            num_elite = len(population) * elite_size
            elite = tools.selBest(population,
                                  k=round(num_elite),
                                  fit_attr="quality")
            offspring = toolbox.select(population,
                                       k=(len(population)-round(num_elite)))
        else:
            offspring = toolbox.select(population, k=len(population))
        offspring = [toolbox.clone(ind) for ind in offspring]

        for i in range(1, len(offspring), 2):
            if random.random() < cxpb:
                offspring[i - 1], offspring[i] = (
                        toolbox.mate(offspring[i - 1], offspring[i]))
                del offspring[i - 1].fitness.values
                del offspring[i].fitness.values

        for i in range(len(offspring)):
            if random.random() < mutpb:
                offspring[i], = toolbox.mutate(offspring[i])
                del offspring[i].fitness.values

        invalids = [ind for ind in offspring if not ind.fitness.valid]
        for ind in invalids:
            toolbox.evaluate(ind)
            if ind.quality.values == (1.0,):
                goal = True

        if elitism:
            population[:] = offspring + elite
        else:
            population[:] = offspring

        toolbox.set_result(population)
        if verbose:
            print("\nGeneration: ", g+1, "-----------------------------")
            toolbox.print(population)

        if toolbox.terminate_on_goal() and goal:
            return population

    return population
