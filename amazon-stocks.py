'''
amazon-stocks.py
2025-04-28

Applies the piecewise funciton approximation algorithm to Amazon stock prices.
'''

import csv
from LinearApproximation import LinearApproximation
import matplotlib.pyplot as plt

# DATA SOURCE: https://www.kaggle.com/datasets/praxitelisk/financial-time-series-datasets?resource=download

labels = [] # Each item will be of the form [mm/dd/yyyy, c]
points = [] # Each item will be[i, adj_close]

with open('AMZN.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for i, row in enumerate(csv_reader):
        if i != 0: # Ignore the first row as it contains header information
            labels.append(row[0])
            points.append([i, float(row[1])])

print(labels)
fig, ax = plt.subplots()

START_INDEX = 0
END_INDEX = 100
data_subset = points[START_INDEX:END_INDEX] # Only take a subset of the data, otherwise approximation takes too long
obj = LinearApproximation(data_subset, 0, 4, labels) # alpha = 0 as there is no additional cost to store
approximated  = obj.approximate()
obj.plt_approximation(fig, ax, approximated, False, True)
plt.title('Adjusted Closing Price of Amazon Stocks Over Time')
plt.ylabel('Adjusted Closing Price ($)')
plt.xlabel('Date')
plt.show()