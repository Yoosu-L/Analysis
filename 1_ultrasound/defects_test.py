# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 16:23:26 2021

@author: Hao
"""

import os
import sys
import numpy as np
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import matplotlib.pyplot as plt
from cumulative_peak_finding import gradient, read, find_peak, calculate, plot
from scipy.signal import argrelextrema

n = 13
n1 = 12

p1 = 'C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\data\\T000'
p2 = 'C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\data\\T00'
if n < 10:
    path = p1 + str(n) + 'CH1.CSV'
else:
    path = p2 + str(n) + 'CH1.CSV'

if n < 12:
    start = 1734
    end = 1756
elif 12 <= n < 15:
    start = 1563
    end = 1595
elif 15 <= n < 21:
    start = 1325
    end = 1357
else:
    start = 1325
    end = 1357

p12 = 'C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\data\\T0012CH1.CSV'

x, y, f, absY, absY1, mi, ma = read(path, 1563, end, zrs=0, main_freq=3.6e6)
x12, y12, f12, absY12, absY112, mi12, ma12 = read(p12, 1563, 1595, zrs=0, main_freq=3.6e6)

yNew = []
y12New = []
ys = []

for i in y:
    if abs(i) > 0.02:
        yNew.append(abs(i))
    else:
        yNew.append(0)
        
for i in y12:
    if abs(i) > 0.02:
        y12New.append(abs(i))
    else:
        y12New.append(0)

for i in range(len(x)):
    if y12New[i] >= yNew[i]:
        ys.append(y12New[i]-yNew[i])
    else:
        ys.append(0)
        

# y = (y**2)**0.5
# y12 = (y12**2)**0.5
# y12 = y12/max(y12)
# y = y/max(y)

plot(x, yNew, f, absY, absY1, n, fft=False)
plot(x12, y12New, f12, absY12, absY112, 12, fft=False)

# ys = y - y12

plt.figure()
plt.plot(x, ys)
plt.xlabel('time')
# plt.title("Whole waveform FFT subtracted by envelope")
plt.grid()
plt.show()

import sys
sys.exit()

try:
    # first parameter is minimum number of point to be found
    f_diff, diff, mini_f, mini_amp = find_peak(6, f, absY, absY1, mi, ma)
except TypeError:
    # mi -= 70
    # ma += 80
    f_diff = f[mi:ma]
    diff = absY1[mi:ma] - absY[mi:ma]
    
    min_pos = argrelextrema(np.array(diff), np.less)
    mini_f = [f_diff[i] for i in min_pos[0]]
    mini_amp = [diff[i] for i in min_pos[0]]
    # mini_f, mini_amp = cumulative_peak(mini_f, mini_amp)
    
    min_pos = argrelextrema(np.array(mini_amp), np.less)
    mini_f = [mini_f[i] for i in min_pos[0]]
    mini_amp = [mini_amp[i] for i in min_pos[0]]
    
    plt.figure()
    plt.plot(f_diff, diff)
    plt.plot(mini_f, mini_amp, 'rx')
    plt.xlabel('freq(Hz)')
    plt.title("Whole waveform FFT subtracted by envelope")
    plt.grid()
    plt.show()
    
    print(mini_f, mini_amp)
    p = -1
    while True:
        p = int(input("Delete point.\n"))
        if p != 0:
            mini_f.pop(p-1)
            mini_amp.pop(p-1)
            plt.figure()
            plt.plot(f_diff, diff)
            plt.plot(mini_f, mini_amp, 'rx')
            plt.xlabel('freq(Hz)')
            plt.title("Whole waveform FFT subtracted by envelope")
            plt.grid()
            plt.show()
        else:
            break
        
peak_number, tmini_f, coeff, uncertainty = gradient(mini_f)
g, u = calculate(coeff, uncertainty, 6350)
print('%.2f' % (1000*g), '±', '%.2f' % (1000*u))

plt.figure()
plt.plot(peak_number, mini_f, 'rx')
plt.plot(peak_number, tmini_f, 'k-')
plt.legend(labels=['data points',"gradient="+str(int(coeff))+"±"+str(int(uncertainty))], loc = 'upper left')
plt.title("Frequency at each peak")
plt.xlabel('Peak #')
plt.ylabel('Frequency')
plt.grid()
plt.show()

plt.figure()
plt.plot(f_diff, diff)
plt.plot(mini_f, mini_amp, 'rx')
plt.xlabel('freq(Hz)')
plt.title("Whole waveform FFT subtracted by envelope")
plt.grid()
plt.show()