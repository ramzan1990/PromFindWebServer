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

def randomSeq(s):
    r = zeros((s, 4))
    for i in range(s):
        #r[i][randint(0, 3)] = 0
        r[i][0] = 1
    return r

def close(s, a):
    fmd = float('inf')
    for v in a:
        if(abs(s - v) < fmd):
            fmd = abs(s - v)
    return fmd

def tatascore(a, tss):
    tata = [[-1.02,-1.68,0,-0.28], [-3.05,0,-2.74,-2.06], [0,-2.28,-4.28,-5.22], [-4.61,0,-4.61,-3.49], [0,-2.34,-3.77,-5.17], [0,-0.52,-4.73,-4.63], [0,-3.65,-2.65,-4.12], [0,-0.37,-1.5,-3.74], [-0.01,-1.4,0,-1.13], [-0.94,-0.97,0,-0.05], [-0.54,-1.4,-0.09,0], [-0.48,-0.82,0,-0.05], [-0.48,-0.66,0,-0.11], [-0.74,-0.54,0,-0.28], [-0.62,-0.61,0,-0.4]]
    maxScore = -1000
    maxI = -1000
    for p in range(14):
        seq = a[tss-39 + p:tss-39+15 + p]
        score = 0
        for i in range(len(tata)):
            for j in range(4):
                score = score + tata[i][j]*seq[i][j]
        if(score>maxScore):
            maxScore = score
            maxI = 39 - p
    return maxScore, maxI

def ccaatscore(a, tss):
    ccat = [[-0.02,0,-1.46,-0.01],[-0.49,-0.01,-0.24,0],[-1.19,0,-1.26,-0.57],[0,-3.16,-0.4,-3.46],[-0.61,-1.44,0,-2.45],[-4.39,-3.99,-4.03,0],[-4.4,-4,-4.4,0],[0,-4.37,-4.37,-4.37],[0,-1.33,-1.69,-2.45],[-2.12,0,-2.26,-4.27],[-1.32,-2.84,-0.47,0],[0,-3.57,-0.81,-2.64]]
    maxScore = -1000
    maxI = -1000
    for p in range(142):
        seq = a[tss-200 + p:tss-200+12 + p]
        score = 0
        for i in range(len(ccat)):
            for j in range(4):
                score = score + ccat[i][j]*seq[i][j]
        if(score>maxScore):
            maxScore = score
            maxI = 200 - p
    return maxScore, maxI

def inrscore(a):
    inr = [[-1.14,0,-0.75,-1.16], [-5.26,-5.26,-5.26,0], [0,-2.74,-5.21,-5.21], [-1.51,-0.29,0,-0.41], [-0.65,0,-4.56,-0.45], [-0.55,-0.36,-0.86,0], [-0.91,0,-0.38,-0.29], [-0.82,0,-0.65,-0.18]]
    score = 0
    for i in range(len(inr)):
        for j in range(4):
            score = score + inr[i][j]*a[i][j]
    return score

def tctscore(a):
    tct = [[0.08,0.35,0.30,0.27],[0.08,0.32,0.17,0.43],[0.00,0.00,0.00,11.00],[0.07,0.62,0.08,0.24],[0.09,0.32,0.16,0.43],[0.11,0.43,0.15,0.30],[0.09,0.33,0.22,0.36],[0.10,0.28,0.24,0.38]]
    score = 0
    for i in range(len(tct)):
        for j in range(4):
            score = score + tct[i][j]*a[i][j]
    return score

def pick(sequences, scores, inds, all_chosen, dt, mod):
    for k, e in reversed(list(enumerate(scores))):
        if(e>=dt):
            fmd = close(inds[k], all_chosen[i])
            scaling = 1.0
            if(fmd < minDist):
                scaling = fmd / minDist
            if(e*scaling >= dt):
                all_chosen[i].append(inds[k])
                print("Position " + str(inds[k] + 1)  + " Score " + str(round(sorted((0, e, 1))[1], 2)))
                tss = head + inds[k] 
                cscore, cbp  = ccaatscore(sequences[i], tss)
                tscore, tbp  = tatascore(sequences[i], tss)
                seqp = ""
                if(cscore >= -4.54):
                    seqp = seqp + fastarev(sequences[i][tss-200:tss-cbp])
                    seqp = seqp + "<span style='background-color:#b3ffff;'>"
                    seqp = seqp + fastarev(sequences[i][tss-cbp:tss-cbp + 12])
                    seqp = seqp + "</span>"
                    seqp = seqp + fastarev(sequences[i][tss-cbp+12:tss-45])  
                else:
                    seqp = seqp + fastarev(sequences[i][tss-200:tss-45])
            
                if(tscore >= -8.16):
                    seqp = seqp + fastarev(sequences[i][tss-45:tss-tbp])
                    seqp = seqp + "<span style='background-color:#ffb3b3;'>"
                    seqp = seqp + fastarev(sequences[i][tss-tbp:tss-tbp + 15])
                    seqp = seqp + "</span>"
                    seqp = seqp + fastarev(sequences[i][tss-tbp+15:tss-2])  
                else:
                    seqp = seqp + fastarev(sequences[i][tss-45:tss-2])
                
                ns = ""                  
                if(inrscore(sequences[i][tss-2:tss+6]) >= -3.75):
                    seqp = seqp + "<span style='background-color:#ffe0b3;'>"
                    ns = "</span>"
                elif(tctscore(sequences[i][tss-2:tss+6]) >= 12.84):
                    seqp = seqp + "<span style='background-color:#c2efc2;'>"
                    ns = "</span>"
                seqp = seqp + fastarev(sequences[i][tss-2:tss])  
                seqp = seqp + "<b><span style='background-color:#b3ccff;'>"
                seqp = seqp + fastarev(sequences[i][tss:tss+1])  
                seqp = seqp + "</span></b>"
                seqp = seqp + fastarev(sequences[i][tss+1:tss+6])
                seqp = seqp + ns
                seqp = seqp + fastarev(sequences[i][tss+6:tss+400])
                print(seqp)
        else:
            break
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

dt = 0.4
try:
    dt = float(sys.argv[6]) 
except:
    pass
dt = sorted((0.1, dt, 0.9))[1]

minDist = 5000
try:
    minDist = int(sys.argv[7])
except:
    pass

if(minDist < 600):
    minDist = 600

fixw = 1.01

sequences1 = []
names = []
seq = ""
with open(inp) as f:
    for line in f:
        if(line.startswith(">")):
            names.append(line.strip())
            if(len(seq) != 0):
                sequences1.append(np.fromstring(encode(seq), dtype=int, sep=","))
                seq = ""
            continue
        else:
            seq += line

if(len(seq) != 0):
    sequences1.append(np.fromstring(encode(seq), dtype=int, sep=","))

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
    os = zeros((len(sequences1[i]), 4))
    for j in range(len(sequences1[i])):
        if(sequences1[i][j]<4):
            os[j][sequences1[i][j]] = 1
    temp = []
    temp.extend(randomSeq(head))
    temp.extend(os)
    temp.extend(randomSeq(tail))
    sequences.append(temp)

print("This is the final result!!")
all_scores_tata = []
all_scores_ntata = []
all_chosen = []
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
        topred = np.zeros(shape=(total, sLen, 4))
        for j in range(total):
            topred[j] = sequences[i][j * step: j * step + sLen]
        predict = brun(sess, y, topred)
        prefix = ""
        scores = []
        for j in range(total):
            score = (predict[j][0] - predict[j][1] + 1.0)/2.0  
            tss = head + j
            if(score > 0.1):  
                #if tata+ model says no, this should as well
                #if(tatascore(sequences[i], tss)[0] >= -8.16):
                #    score = score - 0.4
                if(inrscore(sequences[i][tss-2:tss+6]) >= -3.75):
                    score = score + 0.02
                elif(tctscore(sequences[i][tss-2:tss+6]) >= 12.84):
                    score = score + 0.005
                elif(sequences[i][tss][2] == 1):
                    score = score + 0.01
                elif(sequences[i][tss][0] == 1):
                    score = score + 0.01
                elif(sequences[i][tss][3] == 1):
                    score = score - 0.3
                elif(sequences[i][tss][1] == 1):
                    score = score - 0.3
            scores.append(score)
            prefix = ", "
        scores= np.array(scores)        
        all_scores_ntata.append(scores)

new_graph = tf.Graph()
with tf.Session(graph=new_graph) as sess:
    # Import the previously export meta graph.
    tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING], "PromID/model_2")
    # Restore the variables
    saver = tf.train.Saver()
    saver.restore(sess, "PromID/model_2"+"/variables/variables")
    input_x = tf.get_default_graph().get_tensor_by_name("input_prom:0")
    y = tf.get_default_graph().get_tensor_by_name("output_prom:0")
    kr1 = tf.get_default_graph().get_tensor_by_name("kr1:0")
    kr2 = tf.get_default_graph().get_tensor_by_name("kr2:0")
    for i in range(len(sequences)):
        total = int(math.ceil((len(sequences[i]) - sLen) / step) + 1)
        topred = np.zeros(shape=(total, sLen, 4))
        for j in range(total):
            topred[j] = sequences[i][j * step: j * step + sLen]
        predict = brun(sess, y, topred)
        scores = []
        for j in range(total):
            score = (predict[j][0] - predict[j][1] + 1.0)/2.0 
            tss = head + j
            
            if(score > 0.1):    
                if(tatascore(sequences[i], tss)[0] >= -8.16):
                    score = score + 0.02
                else:
                    score = score - 0.3
                if(inrscore(sequences[i][tss-2:tss+6]) >= -3.75):
                    score = score + 0.02
                elif(tctscore(sequences[i][tss-2:tss+6]) >= 12.84):
                    score = score + 0.005
                elif(sequences[i][tss][2] == 1):
                    score = score + 0.01
                elif(sequences[i][tss][0] == 1):
                    score = score + 0.01
                elif(sequences[i][tss][3] == 1):
                    score = score - 0.3
                elif(sequences[i][tss][1] == 1):
                    score = score - 0.3
            scores.append(score)
        scores= np.array(scores)        
        all_scores_tata.append(scores)

for i in range(len(sequences)):   
    print("<b>" + names[i] + "</b>")

    all_chosen.append([])

    inds = np.argsort(all_scores_tata[i])
    scores = all_scores_tata[i][inds]
    pick(sequences, scores, inds, all_chosen, 0.7, "+")

    inds = np.argsort(all_scores_ntata[i])
    scores = all_scores_ntata[i][inds]
    pick(sequences, scores, inds, all_chosen, dt, "-")

    inds = np.argsort(all_scores_tata[i])
    scores = all_scores_tata[i][inds]
    pick(sequences, scores, inds, all_chosen, dt, "+")