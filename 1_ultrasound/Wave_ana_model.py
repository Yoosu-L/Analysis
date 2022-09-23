# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 13:38:07 2021

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

path_0 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0000CH2.CSV"
path_2 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0002CH2.CSV"
path_00 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0000ALL.CSV"
path_01 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0001ALL.CSV"
path_02 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0002ALL.CSV"
path_03 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0003ALL.CSV"
path_04 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0004ALL.CSV"
path_05 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0005ALL.CSV"

x, y, f, absY, absY1, mi, ma = read(path_00, 16, -1, zrs=0, main_freq=4e6, first=True)

try:
    # first parameter is minimum number of point to be found
    f_diff, diff, mini_f, mini_amp = find_peak(8, f, absY, absY1, mi, ma)
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


# plt.figure()
# plt.plot(f, absY)
# plt.plot(f, absY1)
# plt.xlim(0,1e7)
# plt.xlabel('freq(Hz)')
# plt.title("FFT")
# plt.legend(labels=['Whole Waveform','Envelope'],loc='best')
# plt.grid()
# plt.show()

# plt.figure()
# plt.plot(x, y)
# plt.xlabel('Time(s)')
# plt.title("Ultrasound transmitted in 5.48mm Al")
# plt.grid()
# plt.show()

""" plot(x, y, f, absY, absY1, num=1) """

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