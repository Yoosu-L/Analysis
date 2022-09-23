# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 19:09:06 2021

@author: Hao
"""
import os
import sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.signal import argrelextrema
# from numpy import polyfit
from cumulative_peak_finding import cumulative_peak, gradient
# from scipy.signal import hilbert, chirp


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

first_point = 913
end_point_of_first = 1154
threshold = 1/3


with open(path_01, 'r') as csvfile:
    reader = csv.reader(csvfile)
    rows = [row for row in reader]

data = (np.array(rows[first_point:-1])).astype(np.float64)
x = data[:, 0]
y = data[:, 1]
data_first = (np.array(rows[first_point:end_point_of_first])).astype(np.float64)
x1 = data_first[:, 0]
y1 = data_first[:, 1]
T = x[1]-x[0]

# add zero paddings
zrs = 6000 # how many 0s added to the front and back
zrs1 = zrs + int((len(x)-len(x1))/2)

zero_padding_y = np.zeros(zrs)
first_x = x[0]-zrs*T
zero_padding_x = np.array([T*i+first_x for i in range(zrs)])
zero_padding_x_back = np.array([T*i+x[-1]+T for i in range(zrs)])
x = np.concatenate((zero_padding_x, x))
x = np.concatenate((x, zero_padding_x_back))
y = np.concatenate((zero_padding_y, y))
y = np.concatenate((y, zero_padding_y))

N = len(x)
fs = int(1/T)+1 #sampling rate (N/s)
df = fs/(N-1) 
f = [df*n for n in range(N)]
Y = np.fft.fft(y)*2/N
absY = [np.abs(i) for i in Y]
max_absY = max(absY)
fac = np.array([max_absY for i in range(len(absY))])
absY /= fac


zero_padding_y1 = np.zeros(zrs1)
first_x1 = x1[0]-zrs1*T
zero_padding_x1 = np.array([T*i+first_x1 for i in range(zrs1)])
zero_padding_x1_back = np.array([T*i+x1[-1]+T for i in range(zrs1)])
x1 = np.concatenate((zero_padding_x1, x1))
x1 = np.concatenate((x1, zero_padding_x1_back))
y1 = np.concatenate((zero_padding_y1, y1))
y1 = np.concatenate((y1, zero_padding_y1))

N1 = len(x1)
df1 = fs/(N1-1)
f1 = [df1*n for n in range(N1)]
Y1 = np.fft.fft(y1)*2/N1
absY1 = [np.abs(i) for i in Y1]
max_absY1 = max(absY1)
fac1 = np.array([max_absY1 for i in range(len(absY1))])
absY1 /= fac1


# max_absY_index = absY.index(max_absY)

f = f[0:int(1e7/df)]
f1 = f1[0:int(1e7/df1)]
absY = absY[0:int(1e7/df)]
absY1 = absY1[0:int(1e7/df1)]

# diff = absY1 - absY
# div = absY / absY1



max_whole_array = argrelextrema(np.array(absY), np.greater)
# max_overlap_array = argrelextrema(np.array(absY*absY1)**0.5, np.greater)
max_freq_every_list = []
max_amp_every_list = []
max_freq_pos = []
n = 0

for i in max_whole_array:
    for j in i:
        if absY[j] > threshold:
            if f[j] < 5e6:
                max_amp_every_list.append(absY[j])
                max_freq_every_list.append(f[j])
                
                
max_freq_list, max_amp_list = cumulative_peak(max_freq_every_list, max_amp_every_list)
# max_freq_list = max_freq_list[4:-1]
# max_amp_list = max_amp_list[4:-1]

print(max_freq_list)
print(max_amp_list)

# min_whole_array = argrelextrema(div, np.greater)
# for i in min_whole_array:
#     for j in i:
#         if div[j] <= 1.5:
#             if f[j] in max_freq_every_list:
#                 print(f[j])

# =============================================================================
# max_every_array = argrelextrema(np.array(max_amp_list), np.greater)
# 
# for i in max_every_array:
#     for j in i:
#         max_freq_list.append(max_freq_every_list[j])
#         max_freq_pos.append(j)
# 
# if max_freq_pos:
#     for i in range(max_freq_pos[0],max_freq_pos[-1]+1):
#         if i not in max_freq_pos:
#             max_freq_every_list.remove(max_freq_every_list[i-n])
#             n += 1
# =============================================================================

# peak_number, freq_value, coeff, uncertainty = gradient(max_freq_every_list)
a = [2049434.852813315, 2623897.652465532, 3229412.4953421936, 3726245.1869333005, 4549124.332381071]
peak_number, freq_value, coeff, uncertainty = gradient(a)


plt.figure()
plt.plot(f, absY)
# plt.plot(f1, absY1)
plt.plot(max_freq_list, max_amp_list, 'rx')
# plt.plot(max_freq_every_list, max_amp_every_list, 'rx')
# plt.legend(labels=['Whole Waveform','Envelope'],loc='best')
plt.xlim(0,1e7)
plt.xlabel('freq(Hz)')
plt.title("FFT")
plt.grid()
plt.show()

# plt.figure()
# plt.plot(f1, absY1)
# plt.xlim(0,1e7)
# plt.xlabel('freq(Hz)')
# plt.title("FFT")
# plt.grid()
# plt.show()

# plt.figure()
# plt.plot(f, diff)
# plt.xlim(0,1e7)
# plt.xlabel('freq(Hz)')
# plt.title("Whole waveform FFT subtracted by envelope")
# plt.grid()
# plt.show()

# plt.figure()
# plt.plot(max_freq_every_list, max_amp_every_list, 'rx')
# plt.xlim(1e6,4e6)
# plt.xlabel('freq(Hz)')
# plt.title("Local maxim above threshold")
# plt.grid()
# plt.show()

plt.figure()
plt.plot(x, y)
plt.xlabel('Time(s)')
plt.title("Ultrasound transmitted in 48.2mm Al")
plt.grid()
plt.show()

plt.figure()
# plt.plot(peak_number, max_freq_every_list, 'rx')
plt.plot(peak_number, a, 'rx')
plt.plot(peak_number, freq_value, 'k-')
plt.legend(labels=['data points',"gradient="+str(int(coeff))+"±"+str(int(uncertainty))], loc = 'upper left')
plt.title("Frequency at each peak")
plt.xlabel('Peak #')
plt.ylabel('Frequency')
plt.grid()
plt.show()