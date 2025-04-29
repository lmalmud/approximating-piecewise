'''
example.py
2025-04-28

Runs a nontrivial example by generatinf fifty points and
then running the approximation algorithm.
'''

from LinearApproximation import LinearApproximation
import matplotlib.pyplot as plt
import random

p = [[random.randint(0, 50), random.randint(0, 50)] for i in range(25)]
obj = LinearApproximation(p, 1, 1)

# Run the approximation algorithm and graph the results
fig, ax = plt.subplots()
approximated  = obj.approximate()
obj.plt_approximation(fig, ax, approximated, True, True)
plt.show()