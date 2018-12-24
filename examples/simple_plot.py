from platypus import NSGAII, ZDT1

# define the problem definition
problem = ZDT1()

# instantiate the optimization algorithm
# algorithm = NSGAII(problem)
algorithm = NSGAII(problem)

# optimize the problem using 10,000 function evaluations
algorithm.run(10000)





# plot the results using matplotlib
import matplotlib.pyplot as plt
plt.figure(figsize=(8,8))


plt.scatter([s.objectives[0] for s in algorithm.result],
            [s.objectives[1] for s in algorithm.result],c = 'r',marker='.')
plt.xlim([0, 1.1])
plt.ylim([0, 1.1])
plt.xlabel("$f_1(x)$")
plt.ylabel("$f_2(x)$")
plt.show()