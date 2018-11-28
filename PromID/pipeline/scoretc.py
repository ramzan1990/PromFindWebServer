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

tct = [[0.08,0.35,0.30,0.27],[0.08,0.32,0.17,0.43],[0.00,0.00,0.00,11.00],[0.07,0.62,0.08,0.24],[0.09,0.32,0.16,0.43],[0.11,0.43,0.15,0.30],[0.09,0.33,0.22,0.36],[0.10,0.28,0.24,0.38]]
score = 0
for i in range(len(tct)):
    for j in range(4):
        score = score + tct[i][j]*os[i][j]

print("TCT score is: " + str(score)) 