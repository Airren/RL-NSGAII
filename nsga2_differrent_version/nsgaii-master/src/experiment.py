from nsgaii import *
from benchmark_problems import *

problem = Benchmark_1(size_of_genotype=30)
algorithm = NSGAII(problem, 100)
algorithm.run(True, 50)