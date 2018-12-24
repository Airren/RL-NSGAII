from problem import Problem
from individual import Member
from fpconst import *
import math, copy, random
import pylab as plt

class NSGAII:
    mutation_rate = 1.0
    crossover_rate = 0.0
    generations = 200

    def __init__(self,problem, pop_size = 100):
        self.problem = problem
        self.population = []
        self.pop_size = pop_size
        self.seeding_pop_size = pop_size
        self.initialise_population()

    def initialise_population(self):
        for i in range(0,self.seeding_pop_size):
            p = Member(self.problem.num_objectives)
            p.set_random_genotype(self.problem)
            self.population.append(p)
        self.evaluate_population()

    def evaluate_population(self, population=[]):
        if population == []:
            population = self.population
        for member in population:
            member.evaluate(self.problem)

    def fast_nondominated_sort(self, population=[]):
        S = dict() # dictionary, S, containing the solutions that an individual dominates
        if population == []:
            population = self.population
        fronts_list = [[] for m in population]
        # init population
        for member in population:
            member.n = 0 # num solutions dominated by
            S[hash(member)] = [] # individuals dominated
        # calculate #dominations
        for member in population:
            for other_member in population:
                # create entry for member in S, S_member
                if member.dominates(other_member):
                    S[hash(member)].append(other_member)
                    other_member.n += 1
        # create non-dominated front
        for member in population:
            # member is nondominated
            if member.n == 0:
                member.domination_index = 0
                fronts_list.append([])
                # add to first front
                fronts_list[0].append(member)
        i = 0
        while len(fronts_list[i]) != 0:
            front = []
            for member in fronts_list[i]:
                for dominated_member in S[hash(member)]:
                    dominated_member.n -= 1
                    if dominated_member.n == 0:
                        dominated_member.domination_index = i + 1
                        front.append(dominated_member)
            i += 1
            fronts_list.append([])
            fronts_list[i] = front
        return fronts_list

    def crowding_distance_assignment(self, front, to_print = False):
        len_front = len(front)
        if len_front > 0:
            # Initialize distance for each individual
            for x in front:
                x.crowded_distance = 0
            # iterate through each objective and add to CD for each individual
            for objective in range(0, self.problem.num_objectives):
                # Sort using objective
                front = sorted(front,key=lambda member: member.fitness[objective])
                normalised_front = []
                for member in front:
                    normalised_front.append(member.fitness[objective])
                try:
                    normalised_front = norm_list(normalised_front)
                except:
                    # stops ZeroDivision errors
                    for i in range(0,len(normalised_front)):
                        normalised_front[i] = 0.0
                for i,member in enumerate(front):
                    member.normalised_fitness[objective] = normalised_front[i]
                # Boundary points are always selected
                front[0].crowded_distance = PosInf
                front[len_front - 1].crowded_distance = PosInf
                for i in range(1, len_front - 1):
                    front[i].crowded_distance += (front[i + 1].normalised_fitness[objective] -
                                                  front[i - 1].normalised_fitness[objective])

    def binary_tournament(self, population):
        parent_a = random.choice(population)
        parent_b = random.choice(population)
        return self.crowded_comparison(parent_a, parent_b)

    def crowded_comparison(self,parent_a,parent_b):
        if parent_a.domination_index < parent_b.domination_index:
            return parent_a
        elif parent_b.domination_index < parent_a.domination_index:
                return parent_b
        elif parent_a.crowded_distance > parent_b.crowded_distance:
            return parent_a
        else:
            return parent_b

    def run(self, plot=False, plot_freq=50):
        # step 1: an initial population has been created already
        population = self.population
        # step 2: non dominated sort
        fronts = self.fast_nondominated_sort(population)
        if plot:
            self.plot_fronts(fronts)
        for f in fronts:
            self.crowding_distance_assignment(f)
        print('#############initial population###########')
        self.print_population(population)
        # step 3: main loop
        gen = 0
        while gen < self.generations:
            print('gen:', str(gen))
            if plot:
                if gen % plot_freq == 0:
                    self.plot_fronts(fronts, True, gen)
            # step 4: create child population
            child_population = []
            while len(child_population) < self.pop_size:
                parent_a = self.binary_tournament(population)
                child = parent_a.copy()
                if random.random() < self.crossover_rate:
                    parent_b = self.binary_tournament(population)
                    children = child.crossover(parent_b, self.problem) # children will be copies
                else:
                    children = [child]
                for child_to_mutate in children:
                    if random.random() < self.mutation_rate:
                        child_to_mutate.mutation(self.problem)
                while len(child_population) < self.pop_size and len(children) > 0:
                    child_population.append(children.pop())

            # step 5: evaluate child population
            self.evaluate_population(child_population)

            # step 6: merge with original
            population_R = population + child_population

            # step 7: determine fronts and crowding distance
            fronts = self.fast_nondominated_sort(population_R)
            for f in fronts:
                self.crowding_distance_assignment(f,to_print=False)
            new_population = []

            # step 8: merge fronts into new population
            for f in fronts:
                if (len(new_population) > self.pop_size):
                    break
                elif (len(new_population) + len(f)) < self.pop_size:
                    new_population += f
                else:
                    f = sorted(f, key=lambda member: -member.crowded_distance)
                    while len(new_population) < self.pop_size and len(f) > 0:
                        new_population.append(f.pop())
            fronts = self.fast_nondominated_sort(new_population)
            population = new_population
            gen += 1

        # present final population
        print('#############final population###########')
        self.print_population(population)
        if plot:
            self.plot_fronts(fronts, True, gen)
            plt.close()

    def print_population(self,population=[]):
        if population == []:
            population = self.population
        print("-"*10)
        population = sorted(population, key=lambda member: member.domination_index)
        for i,p in enumerate(population):
            print("["+str(i)+"] " + str(p) + "   di = " + str(p.domination_index) + "   cd = "+str(p.crowded_distance) +
                  "   fitness = " + str(p.fitness))

    def plot_fronts(self, fronts, print_to_file=False, gens=0):
        plt.ion()
        for i,f in enumerate(fronts):
            if len(f) > 0:
                if i % 3 == 0:
                    colour = 'b'
                elif i % 3 == 1:
                    colour = 'r'
                else:
                    colour = 'g'
                front_x = [m.fitness[0] for m in f]
                front_y = [m.fitness[1] for m in f]
                plt.plot(front_x, front_y, colour+"x")
        plt.pause(0.05)

def norm_list(L, normalizeTo=1):
    '''normalize values of a list to make its max = normalizeTo'''
    vMax = max(L)
    return [x / (vMax * 1.0) * normalizeTo for x in L]