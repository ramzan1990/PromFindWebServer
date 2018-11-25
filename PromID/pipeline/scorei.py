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

inr = [[-1.14,0,-0.75,-1.16], [-5.26,-5.26,-5.26,0], [0,-2.74,-5.21,-5.21], [-1.51,-0.29,0,-0.41], [-0.65,0,-4.56,-0.45], [-0.55,-0.36,-0.86,0], [-0.91,0,-0.38,-0.29], [-0.82,0,-0.65,-0.18]]
score = 0
for i in range(len(inr)):
    for j in range(4):
        score = score + inr[i][j]*os[i][j]

print("INR score is: " + str(score))