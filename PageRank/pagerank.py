import numpy as np
from numpy.linalg import matrix_power
import array

#Importing the 'from node' 
with open('test2.txt') as f:
    col1 = [int(line.split()[0]) for line in f]
    colLen = len(col1)
    col1num = list(dict.fromkeys(col1))
    nl = len(col1num)

#Importing the 'to node'
with open('test2.txt') as f:
    col2 = [int(line.split()[1]) for line in f]
    col2num = list(dict.fromkeys(col2))
    n2 = len(col2num)

#Finds the maximum node
if max(col1num) > max(col2num):
    n = max(col1num) + 1
else:
    n = max(col2num) + 1

#Initialise m matrix to zeros
m = [ [ 0 for i in range(n) ] for j in range(n) ]

#Creating m matrix
for i in range(n):
    sum = 0
    for j in range(colLen):
        if col1[j] == i:
            sum += 1
            m[i][col2[j]] = 1

m = np.array(m)
original = m

#Finding the dead ends 
rm = np.where(np.sum(np.abs(m), axis=1)==0)[0]
store = []

while len(rm) != 0:
    for i in reversed(rm):
        store.append(rm)
        m = np.delete(m,i,0)
        m = np.delete(m,i,1)

    rm = np.where(np.sum(np.abs(m), axis=1)==0)[0]

#Finding the percentages 
m_size = len(m)
totals = [ 0 for i in range(m_size) ]
totals = np.array([totals]).T

for i in range(m_size):
    sum = 0
    for j in range(m_size):
        if m[i][j] == 1:
            sum += 1
    totals[i] = sum

#Deletes the sums of zeros from the total
rmZero = np.where(np.sum(np.abs(totals), axis=1)==0)[0]

for i in reversed(rmZero):
    totals = np.delete(totals,i,0)
    m_size -= 1

#Final transition matrix
m = m/totals
m = np.array(m).T

#Finding the pagerank
pgRank = [ 1/m_size for i in range(m_size) ]

#Removing spider-traps
beta = 0.8
e = [ 1 for i in range(m_size) ]
e = np.array(e).T
pgRank = np.array(pgRank).T

for i in range(100):
    pgRank = beta*np.dot(m,pgRank) + ((1-beta)/m_size)*e
print(pgRank)

# print(original)
extra = []