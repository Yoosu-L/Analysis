# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 16:41:23 2021

@author: Hao
"""

import os
import sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import matplotlib.pyplot as plt
import numpy as np
from cumulative_peak_finding import gradient, read, find_peak, calculate


path_00 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0000ALL.CSV"
path_01 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0001ALL.CSV"
path_02 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0002ALL.CSV"
path_03 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0003ALL.CSV"
path_04 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0004ALL.CSV"
path_05 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0005ALL.CSV"

x, y, f, absY, absY1, mi, ma = read(path_02, 1572, 1588, zrs=100, main_freq=4e6)
f_diff, diff, mini_f, mini_amp = find_peak(8, f, absY, absY1, mi, ma)
peak_number, tmini_f, coeff, uncertainty = gradient(mini_f)
print(calculate(coeff, uncertainty, 6350))



n = []
li = []
for i in range(100):
    try:
        x, y, f, absY, absY1, mi, ma = read(path_03, 1571, 1601, zrs=100*i, main_freq=4e6)
        f_diff, diff, mini_f, mini_amp = find_peak(8, f, absY, absY1, mi, ma)
        peak_number, tmini_f, coeff, uncertainty = gradient(mini_f)
        a, b = calculate(coeff, uncertainty, 6350)
        li.append(a*1000)
        n.append(i)
    except TypeError:
        continue
    
plt.figure()
plt.plot(n, li)
plt.xlabel('Number of zero [100]')
plt.ylabel('Depth [mm]')
plt.title("Depth varies with number of zero padding")
plt.grid()
plt.show()

print(np.mean(li))
