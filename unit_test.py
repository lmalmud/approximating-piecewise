'''
unit_test.py
2025-04-28

Runs unit tests to ensure that helper functions involved in evaluating piecewise functions run correctly
and runs a very small example.
'''

from LinearApproximation import LinearApproximation
import matplotlib.pyplot as plt

test1 = [[0, 0], [1, 2], [3, -1], [4, 0], [6, 2]]
test1_obj = LinearApproximation(test1, 1, 1)

print('TEST: evaluate_segment')
print(f'evaluate segment between (0, 0), (1, 2) at 0 expects 0: {test1_obj.eval_segment(0, test1[0], test1[1])}')
print(f'evaluate segment between (0, 0), (1, 2) at .5 expects 1: {test1_obj.eval_segment(.5, test1[0], test1[1])}')
print(f'evaluate segment between (0, 0), (1, 2) at 1 expects 2: {test1_obj.eval_segment(1, test1[0], test1[1])}')

print('TEST: f_1')
print(f'evaluate f_1(.5) expects 1: {test1_obj.f_1(.5)}')
print(f'evaluate f_1(3.5) expects -.5: {test1_obj.f_1(3.5)}')
print(f'evaluate f_1(0) expects 0 (first point - edge case): {test1_obj.f_1(0)}')
print(f'evaluate f_1(6) expects 2 (last point - edge case): {test1_obj.f_1(6)}')

# Graph the underlying function
# test1_obj.plt()

# Run the approximation algorithm and graph the results
'''
fig, ax = plt.subplots()
approximated  = test1_obj.approximate()
test1_obj.plt_approximation(fig, ax, approximated)
plt.show()
'''

test1_obj.animate_dijkstra()