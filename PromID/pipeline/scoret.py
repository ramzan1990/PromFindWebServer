import numpy as np
import sys
import re
from numpy import zeros

def encode(s):
    ns = s.upper()
    pattern = re.compile(r'\s+')
    ns = re.sub(pattern, '', ns)
    ns = ns.replace("A", "0,")
    ns = ns.replace("T", "1,")
    ns = ns.replace("G", "2,")
    ns = ns.replace("C", "3,")
    if re.search('[a-zA-Z]', ns):
        # print(s)
        # print('Non-standard symbol in sequence - changed to A.')
        ns = re.sub("[a-zA-Z]", "4,", ns)
    return ns[:-1]


a = np.fromstring(encode(sys.argv[1]), dtype=int, sep=",")
os = zeros((len(a), 4))
for j in range(len(os)):
    if(a[j]<4):
        os[j][a[j]] = 1

tct = [[0,1.0,0,0.5], [0,1.0,0,0.5], [0,0,0,10.0], [0,1.0,0,0], [0,1.0,0,0], [0,1.0,0,0], [0,1.0,0,0.5], [0,0.5,0,0.5]]
score = 0
for i in range(len(tct)):
    for j in range(4):
        score = score + tct[i][j]*os[i][j]

print("TCT score is: " + str(score))