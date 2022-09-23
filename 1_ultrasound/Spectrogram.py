# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 00:49:45 2021

@author: Hao
"""
import os
import sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import argrelextrema
from cumulative_peak_finding import gradient


path_0 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0000CH2.CSV"
path_1 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0001CH2.CSV"
path_2 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0002CH2.CSV"
path_3 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0003CH2.CSV"
path_4 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0004CH2.CSV"
path_5 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0005CH2.CSV"
path_6 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0006CH2.CSV"
path_00 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0000ALL.CSV"
path_01 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0001ALL.CSV"
path_02 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0002ALL.CSV"
path_03 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0003ALL.CSV"
path_04 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0004ALL.CSV"
path_05 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0005ALL.CSV"

n = 16

p1 = 'C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\data\\T000'
p2 = 'C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\data\\T00'
if n < 10:
    path = p1 + str(n) + 'CH1.CSV'
else:
    path = p2 + str(n) + 'CH1.CSV'

zrs = 6000
first_point = 1734

with open(path, 'r') as csvfile:
    reader = csv.reader(csvfile)
    rows = [row for row in reader]

data = (np.array(rows[first_point:-1])).astype(np.float64)
x = data[:, 0]
y = data[:, 1]
dt = x[1]-x[0]
fs = 1/dt

zero_padding_y = np.zeros(zrs)
first_x = x[0]-zrs*dt
zero_padding_x = np.array([dt*i+first_x for i in range(zrs)])
zero_padding_x_back = np.array([dt*i+x[-1]+dt for i in range(zrs)])
x = np.concatenate((zero_padding_x, x))
x = np.concatenate((x, zero_padding_x_back))
y = np.concatenate((zero_padding_y, y))
y = np.concatenate((y, zero_padding_y))

f, t, Sxx = signal.spectrogram(y, fs)

max_value = 0
max_Sxx = 0
for i in Sxx:
    if max(i) > max_value:
        max_value = max(i)
        max_Sxx = i

max_pos_Sxx = argrelextrema(np.array(max_Sxx), np.greater)
max_p = []

for i in max_pos_Sxx:
    for j in i:
        if max_Sxx[j] > max(max_Sxx)/70:
            max_p.append(j)

max_Sxx_list = [max_Sxx[i] for i in max_p]
max_t_list = [t[i] for i in max_p]

peak_number, freq_value, coeff, uncertainty = gradient(max_t_list)



plt.pcolormesh(t, f, Sxx, shading='Gouraud')
plt.ylim(top=1e7)
# plt.xlim(0, 1.2e-4)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.title("5.1mm spectrogram")
plt.colorbar()
plt.show()

plt.figure()
plt.plot(t, max_Sxx)
plt.plot(max_t_list, max_Sxx_list, 'rx')
# plt.xlim(2e-5, 4e-5)
plt.xlabel('Time(s)')
plt.title("Intensity varies with time")
plt.grid()
plt.show()

plt.figure()
plt.plot(peak_number, max_t_list, 'rx')
plt.plot(peak_number, freq_value)
plt.legend(labels=['data points',"gradient="+str(coeff)+"±"+str(uncertainty)], loc = 'upper left')
# plt.xlim(2e-5, 4e-5)
plt.title("Time at each max intensity")
plt.xlabel('Peak #')
plt.ylabel("time")
plt.grid()
plt.show()