import numpy as np
import math
import sys

def close(s, a):
    for v in a:
        if(abs(s - v) <= 1000):
            return True
    return False

array = []
names = []
with open(sys.argv[1], "r") as ins:
    for line in ins:
        if(not line.startswith(">")):
            array.append([float(x) for x in line.split(",")])
        else:
            names.append(line)

print("This is the final result!!")

for i in range(len(array)):
    a = np.array(array[i])
    inds = (-a).argsort()
    cinds = []
    print(names[i])
    for j in inds:
        if(a[j] > 0.5 and not close(j, cinds)):
            cinds.append(j)
            print("Position " + str(j+1))