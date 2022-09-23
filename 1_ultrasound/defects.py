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


x, y, f, absY, absY1, mi, ma = read(path, start, end, zrs=5000, main_freq=3.6e6)
plot(x, y, f, absY, absY1, n, fft=True)

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