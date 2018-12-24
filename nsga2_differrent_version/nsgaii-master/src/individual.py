'''
@author: Alex
'''
import copy
class Member:
    def __init__(self, num_objectives, genotype=[]):
        self.genotype = genotype
        self.fitness = []
        self.normalised_fitness = []
        self.num_objectives = num_objectives
        for objective in range(0, self.num_objectives):
            self.fitness.append([0])
            self.normalised_fitness.append([0])
        self.domination_index = 0 # front individual is in
        self.crowded_distance = 0 # measure of diversity in front
        self.n = 0 # number of individuals dominating

    def set_random_genotype(self, problem):
        self.genotype = problem.set_random_genotype()
        return self.genotype
                
    def dominates(self,other):
        dominated = False
        all_functions_equal_or_smaller_than_self = True
        at_least_one_function_better_than_other = False
        for i in range(0, self.num_objectives):
            if self.fitness[i] > other.fitness[i]:
                all_functions_equal_or_smaller_than_self = False
            if self.fitness[i] < other.fitness[i]:
                at_least_one_function_better_than_other = True
            
        if all_functions_equal_or_smaller_than_self == True and at_least_one_function_better_than_other == True:
            # if no objective is larger in the other
            dominated = True
        return dominated
    
    def evaluate(self, problem):
        for i in range(0, self.num_objectives):
            self.fitness[i] = problem.objectives[i](self)
            
    def mutation(self, problem):
        problem.mutation(self)
        
    def crossover(self, other_parent, problem):
        return problem.crossover(self, other_parent)
    
    def copy(self):
        new_member = Member(num_objectives=self.num_objectives, genotype=copy.deepcopy(self.genotype))
        new_member.fitness = copy.deepcopy(self.fitness)
        new_member.normalised_fitness = copy.deepcopy(self.normalised_fitness)
        new_member.domination_index = copy.deepcopy(self.domination_index)
        new_member.crowded_distance = copy.deepcopy(self.crowded_distance)
        return new_member
    
    def equals(self, other):
        for g_index in range(0, len(self.genotype)):
            if self.genotype != other.genotype:
                return False
        return True
        
    def __str__(self):
        return ",".join(str(g) for g in self.genotype)
        
if __name__ == "__main__":
    pass
    