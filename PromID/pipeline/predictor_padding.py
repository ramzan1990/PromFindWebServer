#!/usr/bin/env python
import tensorflow as tf
import numpy as np
from math import sqrt
import numpy as np
from numpy import zeros
import sys
import re
import math
import os
from random import randint
from tensorflow.python.saved_model import builder as saved_model_builder


def brun(sess, y, a):
    preds = []
    batch_size = 100
    number_of_full_batch = int(math.ceil(float(len(a))/batch_size))
    for i in range(number_of_full_batch):
        preds += list(sess.run(y,
                               feed_dict={input_x: a[i*batch_size:(i+1)*batch_size], kr1: 1.0, kr2: 1.0}))
    return preds

def fastarev(a):
    sb = []
    for i in range(len(a)):
        if (a[i][0] == 1):
            sb.append("A")
        elif (a[i][1] == 1):
            sb.append("T")
        elif (a[i][2] == 1):
            sb.append("G")
        elif (a[i][3] == 1):
            sb.append("C")
        else:
            sb.append("N")            
    return ''.join(sb)

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

def encodeComp(s):
    ns = s.upper()
    pattern = re.compile(r'\s+')
    ns = re.sub(pattern, '', ns)
    ns = ns[::-1]
    ns = ns.replace("A", "1,")
    ns = ns.replace("T", "0,")
    ns = ns.replace("G", "3,")
    ns = ns.replace("C", "2,")
    if re.search('[a-zA-Z]', ns):
        #print(s)
        #print('Non-standard symbol in sequence - changed to A.')
        ns = re.sub("[a-zA-Z]", "4,", ns)
    return ns[:-1]

def randomSeq(s):
    r = zeros((s, 8))
    for i in range(s):
        #r[i][randint(0, 3)] = 0
        r[i][0] = 1
        r[i][4 + 1] = 1
    return r

def close(s, a):
    for v in a:
        if(abs(s - v) <= 1000):
            return True
    return False

def tatascore(a):
    tata = [[-1.02,-1.68,0,-0.28], [-3.05,0,-2.74,-2.06], [0,-2.28,-4.28,-5.22], [-4.61,0,-4.61,-3.49], [0,-2.34,-3.77,-5.17], [0,-0.52,-4.73,-4.63], [0,-3.65,-2.65,-4.12], [0,-0.37,-1.5,-3.74], [-0.01,-1.4,0,-1.13], [-0.94,-0.97,0,-0.05], [-0.54,-1.4,-0.09,0], [-0.48,-0.82,0,-0.05], [-0.48,-0.66,0,-0.11], [-0.74,-0.54,0,-0.28], [-0.62,-0.61,0,-0.4]]
    score = 0
    for i in range(len(tata)):
        for j in range(4):
            score = score + tata[i][j]*a[i][j]
    return score

def inrscore(a):
    inr = [[-1.14,0,-0.75,-1.16], [-5.26,-5.26,-5.26,0], [0,-2.74,-5.21,-5.21], [-1.51,-0.29,0,-0.41], [-0.65,0,-4.56,-0.45], [-0.55,-0.36,-0.86,0], [-0.91,0,-0.38,-0.29], [-0.82,0,-0.65,-0.18]]
    score = 0
    for i in range(len(inr)):
        for j in range(4):
            v111 = inr[i][j]
            v222 = a[i][j]
            score = score + v111*v222
            #score = score + inr[i][j]*a[i][j]
    return score

np.random.seed(2504)

#total = len(sys.argv)
# if total<3:
#    print('USAGE: <model> <input file>')
#    exit(0)

#print('\nClassification of promoter and non-promoter sequences\n')

sLen = int(sys.argv[3])
step = int(sys.argv[4])
output = str(sys.argv[5])
inp = str(sys.argv[2])
sequences1 = []
sequences2 = []
names = []
seq = ""
with open(inp) as f:
    for line in f:
        if(line.startswith(">")):
            names.append(line.strip())
            if(len(seq) != 0):
                sequences1.append(np.fromstring(encode(seq), dtype=int, sep=","))
                sequences2.append(np.fromstring(encodeComp(seq), dtype=int, sep=","))
                seq = ""
            continue
        else:
            seq += line

if(len(seq) != 0):
    sequences1.append(np.fromstring(encode(seq), dtype=int, sep=","))
    sequences2.append(np.fromstring(encodeComp(seq), dtype=int, sep=","))

sequences = []
head = 0
tail = 0
if(sLen == 251):
    head = 200
    tail = 50
elif(sLen == 750):
    head = 300
    tail = 449
elif(sLen == 1500):
    head = 1000
    tail = 499
elif(sLen == 600):
    head = 200
    tail = 399

for i in range(len(sequences1)):
    os = zeros((len(sequences1[i]), 8))
    for j in range(len(sequences1[i])):
        if(sequences1[i][j]<4):
            os[j][sequences1[i][j]] = 1
        if(sequences2[i][j]<4):
            os[j][4 + sequences2[i][j]] = 1
    temp = []
    temp.extend(randomSeq(head))
    temp.extend(os)
    temp.extend(randomSeq(tail))
    sequences.append(temp)

print("This is the final result!!")
new_graph = tf.Graph()
with tf.Session(graph=new_graph) as sess:
    # Import the previously export meta graph.
    tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING], sys.argv[1])
    # Restore the variables
    saver = tf.train.Saver()
    saver.restore(sess, sys.argv[1]+"/variables/variables")
    input_x = tf.get_default_graph().get_tensor_by_name("input_prom:0")
    y = tf.get_default_graph().get_tensor_by_name("output_prom:0")
    kr1 = tf.get_default_graph().get_tensor_by_name("kr1:0")
    kr2 = tf.get_default_graph().get_tensor_by_name("kr2:0")
    for i in range(len(sequences)):
        total = int(math.ceil((len(sequences[i]) - sLen) / step) + 1)
        topred = np.zeros(shape=(total, sLen, 8))
        for j in range(total):
            topred[j] = sequences[i][j * step: j * step + sLen]
        predict = brun(sess, y, topred)
        prefix = ""
        scores = []
        for j in range(total):
            score = (predict[j][0] - predict[j][1] + 1.0)/2.0
            if(sequences[i][head + j][0] == 1):
                score = score * 1.1
            elif(sequences[i][head + j][2] == 1):
                score = score * 1.05

            if(sequences[i][head + j-1][3] == 1):
                score = score * 1.1
            elif(sequences[i][head + j-1][1] == 1):
                score = score * 1.05    
            scores.append(score)
            prefix = ", "
        scores= np.array(scores)
        chosen = []
        inds = np.argsort(scores)
        scores = scores[inds]
        print("<b>" + names[i] + "</b>")
        for k, e in reversed(list(enumerate(scores))):
            if(e>0.5):
                if(not close(inds[k], chosen)):
                    chosen.append(inds[k])
                    print("Position " + str(inds[k] + 1))       
                    tss = head + inds[k]         
                    seqp = fastarev(sequences[i][tss-200:tss-39])
                    ns = ""
                    if(tatascore(sequences[i][tss-39:tss-39 + 15]) > -19):
                        seqp = seqp + "<span style='background-color:red;'>"
                        ns = "</span>"
                    seqp = seqp + fastarev(sequences[i][tss-39:tss-39 + 15])
                    seqp = seqp + ns
                    seqp = seqp + fastarev(sequences[i][tss-39+15:tss-2])  
                    ns = ""                  
                    if(inrscore(sequences[i][tss-2:tss+6])>-88):
                        seqp = seqp + "<span style='background-color:#ffd714;'>"
                        ns = "</span>"
                    seqp = seqp + fastarev(sequences[i][tss-2:tss])  
                    seqp = seqp + "<b><span style='background-color:#80bfff;'>"
                    seqp = seqp + fastarev(sequences[i][tss:tss+1])  
                    seqp = seqp + "</span></b>"
                    seqp = seqp + fastarev(sequences[i][tss+1:tss+6])
                    seqp = seqp + ns
                    seqp = seqp + fastarev(sequences[i][tss+6:tss+400])
                    print(seqp)
            else:
                break





