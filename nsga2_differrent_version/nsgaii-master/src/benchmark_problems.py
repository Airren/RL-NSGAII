from problem import Problem
import random, math

class Benchmark_1(Problem):
    """
    ZTL 1
    """
    def __init__(self, size_of_genotype):
        super(Benchmark_1, self).__init__([self.objective_1, self.objective_2], size_of_genotype)

    def set_random_genotype(self):
        genotype = []
        for i in range(0, self.size_of_genotype):
            genotype.append(random.random())
        return genotype

    def objective_1(self, member):
        return member.genotype[0]

    def objective_2(self, member):
        gx = self.g(member)
        r = gx * (1.0 - math.sqrt(member.genotype[0] / gx))
        return r

    def g(self,member):
        sx = 0.0;
        for i in range(1, len(member.genotype)): # n genes numerated from 0
            sx += member.genotype[i]
        r = 1.0 + ((9.0 / (len(member.genotype) - 1.0))*sx)
        return r

    def mutation(self, member):
        for mutation_point in range(0, len(member.genotype)):
            if random.random() < 0.1:
                member.genotype[mutation_point] += random.uniform(-0.1, 0.1)
                if member.genotype[mutation_point] < 0:
                    member.genotype[mutation_point] = 0.0
                elif member.genotype[mutation_point] > 1:
                    member.genotype[mutation_point] = 1.0

    def crossover(self, parent_1, parent_2):
        crossover_point = int(len(parent_1.genotype) * random.random())
        crossover_size = int((len(parent_1.genotype) - crossover_point) * random.random())
        child_1 = parent_2.copy()
        child_2 = parent_1.copy()
        for i in range(0, crossover_size):
            child_1.genotype[i + crossover_point] = parent_1.genotype[i + crossover_point]
            child_2.genotype[i + crossover_point] = parent_2.genotype[i + crossover_point]
        return [parent_1, parent_2]
