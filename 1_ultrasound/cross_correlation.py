# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 09:04:50 2021

@author: Hao
"""
import os
import sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from cumulative_peak_finding import gradient

n = 14

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

with open(path, 'r') as csvfile:
    reader = csv.reader(csvfile)
    rows = [row for row in reader]

data_first_echo = (np.array(rows[start:end])).astype(np.float64)
data = (np.array(rows[start:-1])).astype(np.float64)
x_1 = data_first_echo[:, 0]
x = data[:, 0]
y_1 = data_first_echo[:, 1]
y = data[:, 1]
dt = x_1[1]-x_1[0]
T_1 = x_1[-1]-x_1[0]
T = x[-1]-x[0]
number_first_point = int(T_1/dt)+2
number_all_point = int(T/dt)+2
number_point = number_all_point - number_first_point
segment_list = []
correlation_list = []
time_list = []

nm = 0

for i in range(number_point-1):
    # print(np.array(rows[start+i+1:end+i+1]).astype(np.float64)[:, 1])
    segment_list.append((np.array(rows[start+i+1:end+i+1])).astype(np.float64)[:, 1])
    time_list.append(x_1[0]+(nm+1)*dt)
    nm += 1

for i in segment_list:
    correlation_list.append(float(np.correlate(abs(y_1), abs(i))))
    
# max_whole_array = argrelextrema(np.array(correlation_list), np.greater)
# threshold = max(correlation_list)/10
# max_cor_every_list = []
# max_t_every_list = []
# max_cor_every_list.append(correlation_list[0])
# max_t_every_list.append(time_list[0])
# for i in max_whole_array:
#     for j in i:
#         if correlation_list[j] > threshold:
#             max_cor_every_list.append(correlation_list[j])
#             max_t_every_list.append(time_list[j])
# print(max_cor_every_list, max_t_every_list)

# max_t_list = [max_t_every_list[0]]
# max_t_list.append(max_t_every_list[7])
# max_t_list.append(max_t_every_list[10])
# max_cor_list = [max_cor_every_list[0]]
# max_cor_list.append(max_cor_every_list[7])
# max_cor_list.append(max_cor_every_list[10])

# peak_number, freq_value, coeff, uncertainty = gradient(max_t_list)

# plt.figure()
# plt.plot(x, (y)**2)
# plt.xlabel('Time(s)')
# plt.title("Squared waveform (50.1mm Al)")
# plt.grid()
# plt.show()

# plt.figure()
# plt.plot(x_1, (y_1)**2)
# plt.xlabel('Time(s)')
# plt.title("First Echo")
# plt.grid()
# plt.show()

plt.figure()
plt.plot(time_list, correlation_list)
# plt.plot(max_t_every_list, max_cor_every_list, 'rx')
plt.ylabel('Correlation value')
plt.xlabel('Time [sec]')
plt.title("Cross-Correlation "+str(n))
plt.grid()
plt.show()

# plt.figure()
# plt.plot(time_list, correlation_list)
# plt.plot(max_t_list, max_cor_list, 'rx')
# plt.ylabel('Correlation value')
# plt.xlabel('Time [sec]')
# plt.title("Cross-Correlation (50.1mm)")
# plt.grid()
# plt.show()

# plt.figure()
# plt.plot(peak_number, max_t_list, 'rx')
# plt.plot(peak_number, freq_value)
# plt.legend(labels=['data points',"gradient="+str(coeff)+"±"+str(uncertainty)], loc = 'upper left')
# plt.title("Time at each max correlation value")
# plt.xlabel('Peak #')
# plt.ylabel("time")
# plt.grid()
# plt.show()
