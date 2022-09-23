# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:12:48 2021

@author: Hao
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

with open('D:\\picture\\Result\\wyb_fan.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    rows1 = [row for row in reader]
    
rows1 = rows1[1:11]

with open('D:\\picture\\Result\\ym_fan.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    rows2 = [row for row in reader]
    
rows2 = rows2[1:11]

with open('D:\\picture\\Result\\yyqx_fan.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    rows3 = [row for row in reader]
    
rows3 = rows3[1:11]

with open('D:\\picture\\Result\\zyx_fan.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    rows4 = [row for row in reader]
    
rows4 = rows4[1:11]

rows = np.array(rows1+rows2+rows3+rows4).astype(np.float64)
mean = np.mean(rows, 0)
rows = rows-mean
Extraversion = rows[:, 0]
Agreeableness = rows[:, 1]
Conscientiousness = rows[:, 2]
Neuroticism = rows[:, 3]
Openness = rows[:, 4]

def plot(x):
    plt.subplot(221)
    plt.xlim(-0.11,0.11)
    n, bins1, patched = plt.hist(x[0:10], bins=10, color='r', alpha=0.5)
    mu1 = np.mean(x[0:10])
    sigma1 = np.std(x[0:10])
    y1 = norm.pdf(bins1, mu1, sigma1)
    plt.plot(bins1, y1, 'r--')
    plt.legend(['wyb'],fontsize=10, loc=1)
    plt.text(-0.11,5,r'mu='+('%.5f' % mu1),fontdict={'size':'10','color':'black'})
    
    plt.subplot(222)
    plt.xlim(-0.11,0.11)
    n, bins2, patched = plt.hist(x[10:20], bins=10, color='b', alpha=0.5)
    mu2 = np.mean(x[10:20])
    sigma2 = np.std(x[10:20])
    y2 = norm.pdf(bins2, mu2, sigma2)
    plt.plot(bins2, y2, 'b--')
    plt.legend(['ym'],fontsize=10, loc=1)
    plt.text(-0.11,5,r'mu='+('%.5f' % mu2),fontdict={'size':'10','color':'black'})
    
    plt.subplot(223)
    plt.xlim(-0.11,0.11)
    n, bins3, patched = plt.hist(x[20:30], bins=10, color='g', alpha=0.5)
    mu3 = np.mean(x[20:30])
    sigma3 = np.std(x[20:30])
    y3 = norm.pdf(bins3, mu3, sigma3)
    plt.plot(bins3, y3, 'g--')
    plt.legend(['yyqx'],fontsize=10, loc=1)
    plt.text(-0.11,5,r'mu='+('%.5f' % mu3),fontdict={'size':'10','color':'black'})
    
    plt.subplot(224)
    plt.xlim(-0.11,0.11)
    n, bins4, patched = plt.hist(x[30:40], bins=10, color='y', alpha=0.5)
    mu4 = np.mean(x[30:40])
    sigma4 = np.std(x[10:20])
    y4 = norm.pdf(bins4, mu4, sigma4)
    plt.plot(bins4, y4, 'y--')
    plt.legend(['zyx'],fontsize=10, loc=1)
    plt.text(-0.11,5,r'mu='+('%.5f' % mu4),fontdict={'size':'10','color':'black'})
    
    plt.suptitle('Agreeableness of fans')
    plt.show()
    
    return sigma1/mu1, sigma2/mu2, sigma3/mu3, sigma4/mu4 

wyb, ym, yyqx, zyx = plot(Agreeableness)
print(wyb, ym, yyqx, zyx)

# sig = np.array([sig_e,
#                 sig_a,
#                 sig_c,
#                 sig_n,
#                 sig_o])
# print(mean)

# eacno = [['Extraversion', 'Agreeableness', 'Conscientiousness', 'Neuroticism', 'Openness']]
# eacno = np.array(eacno)
# eacno = np.concatenate((eacno, rows))

# with open('C:\\Users\\hao\\Desktop\\fans.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerows(eacno)
