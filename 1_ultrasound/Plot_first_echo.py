"""
Created on Thu Feb 9 16:04:50 2022

@author: Hao
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.signal import argrelextrema
from numpy import polyfit
from cumulative_peak_finding import gradient, read, find_peak, calculate, plot

p_pre = 'C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\Ex2-data\\T00'
p_pree = 'C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\Ex2-data\\T0'
bp = 7213 # base point (12813 for previous data)
td = 0.4 # Threshold (0.15 for previous data) 0.23
n = 118
""" p = p_pree + str(n) + 'CH1.CSV' """ # same with shown later

""" x, y, f, absY, absY1, mi, ma = read(p, bp, 50000, zrs=0, main_freq=5e6, first=False)

y_abs = abs(y)
a = 0
for i in y_abs:
    if i <= 0.16:
        a+=1
    else:
        break

n_first = bp+a
print(n_first)

x, y, f, absY, absY1, mi, ma = read(p, n_first, 50000, zrs=0, main_freq=5e6, first=False)
plot(x, y, f, absY, absY1, n, w=True, fft=False) """

n_first_list = []

def find_n_first(n):
    if n < 100:
        p = p_pre + str(n) + 'CH1.CSV'
    else:
        p = p_pree + str(n) + 'CH1.CSV'
    x, y, f, absY, absY1, mi, ma = read(p, bp, 50000, zrs=0, main_freq=5e6, first=False)
    y_abs = abs(y)
    a = 0
    for i in y_abs:
        if i <= td:
            a+=1
        else:
            break

    n_first = bp+a
    n_first_list.append(n_first)

x_range = []

for i in range(118,152):
    find_n_first(i)
    x_range.append(i*2-218)
""" x_range.append(0.1*(i-55)+13) """

for i in range(176,204):
    find_n_first(i)
    x_range.append(i*2-266)

t_range = []
for i in n_first_list:
    t_range.append(i*1e-9-4.218e-6)
    """ t_range.append(i*1e-9-1.0818e-5) """

""" for i in range(len(x_range)):
    print(str(x_range[i])+" : "+str(t_range[i])) """

h_range = []
for i in t_range:
    h_range.append(i*50/1.582e-5)

""" for i in range(len(x_range)):
    print(str(x_range[i])+" : "+str(h_range[i])) """

""" plt.figure()
plt.plot(x_range, t_range)
plt.xlabel('Horizontal position [mm]')
plt.ylabel('Time of first echo [s]')
plt.title("Time of First echo detected along Al block")
plt.grid()
plt.show() """

plt.figure()
plt.plot(x_range, h_range)
plt.xlabel('Horizontal position [mm]')
plt.ylabel('Depth [mm]')
plt.title("Depth of Al block")
plt.grid()
plt.show()