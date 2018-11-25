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

tata = [[-1.02,-1.68,0,-0.28], [-3.05,0,-2.74,-2.06], [0,-2.28,-4.28,-5.22], [-4.61,0,-4.61,-3.49], [0,-2.34,-3.77,-5.17], [0,-0.52,-4.73,-4.63], [0,-3.65,-2.65,-4.12], [0,-0.37,-1.5,-3.74], [-0.01,-1.4,0,-1.13], [-0.94,-0.97,0,-0.05], [-0.54,-1.4,-0.09,0], [-0.48,-0.82,0,-0.05], [-0.48,-0.66,0,-0.11], [-0.74,-0.54,0,-0.28], [-0.62,-0.61,0,-0.4]]
score = 0
for i in range(len(tata)):
    for j in range(4):
        score = score + tata[i][j]*os[i][j]

print("TATA score is: " + str(score))