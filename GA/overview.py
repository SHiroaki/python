from deap import base, creator
from deap import tools
import random

#Types
creator.create("FitnessMin", base.Fitness, weights=(-1.0,)) # do not forget ","
creator.create("Individual", list, fitness=creator.FitnessMin)

#Initialization
IND_SIZE = 10
toolbox = base.Toolbox()
toolbox.register("attribute", random.random)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                    toolbox.attribute, n=IND_SIZE)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#Operators
def evaluate(individual):
    return sum(individual), # do not forget ","

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)

#Algorithms
#complete generational algorithm

def main():
    pop = toolbox.population(n=50)
    CXPB, MUTPB, NGEN = 0.5, 0.2, 40

    #Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)
    """
    >>> map((lambda x,y: x*y),[1,2,3,4],[2,3,4,5])
    [2, 6, 12, 20]
    """
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    #Select the next generation individuals
    for g in xrange(NGEN):
        offspring = toolbox.select(pop, len(pop))
        #Clone the selected individuals
        offspring = map(toolbox.clone, offspring)

    #Apply crossover and mutation on the offspring
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < CXPB:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    for mutant in offspring:
        if random.random() < MUTPB:
            toolbox.mutate(mutant)
            del mutant.fitness.values

    #Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = map(toolbox.evaluate, invalid_ind)

    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    #The population is entirely replaced by the offspring
    pop[:] = offspring

    return pop

if __name__ == "__main__":
    main()
