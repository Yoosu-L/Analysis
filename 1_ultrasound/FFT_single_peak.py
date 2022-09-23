# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 13:41:25 2021

@author: Hao
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.signal import argrelextrema
from numpy import polyfit


path_0 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0000CH2.CSV"
path_1 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0001CH2.CSV"
path_2 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0002CH2.CSV"
path_3 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0003CH2.CSV"
path_4 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0004CH2.CSV"
path_5 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0005CH2.CSV"
path_6 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0006CH2.CSV"

with open(path_2, 'r') as csvfile:
    reader = csv.reader(csvfile)
    rows = [row for row in reader]

data = (np.array(rows[9858:11919])).astype(np.float64)
x = data[:, 0]
y = data[:, 1]
T = x[1]-x[0]
print(len(x))

zrs = 0 # how many 0s added to the front and back
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

# fft_y = fft(y)
# abs_y = np.abs(fft_y)

Y = np.fft.fft(y)*2/N
absY = [np.abs(i) for i in Y]

max_absY = max(absY)
max_absY_index = absY.index(max_absY)
# freq = (f[max_absY_index])

threshold = max_absY/7
max_whole_array = argrelextrema(np.array(absY), np.greater)
max_freq_every_list = []
max_freq_list = []
max_amp_list = []
max_freq_pos = []
n = 0

for i in max_whole_array:
    for j in i:
        if absY[j] > threshold:
            if f[j] < 5e6:
                max_amp_list.append(absY[j])
                max_freq_every_list.append(f[j])
            
max_every_array = argrelextrema(np.array(max_amp_list), np.greater)

for i in max_every_array:
    for j in i:
        max_freq_list.append(max_freq_every_list[j])
        max_freq_pos.append(j)

if max_freq_pos:
    for i in range(max_freq_pos[0],max_freq_pos[-1]+1):
        if i not in max_freq_pos:
            max_freq_every_list.remove(max_freq_every_list[i-n])
            n += 1


print("frequency of every local maxima in fft: ")
print(max_freq_every_list)
print("\nfrequency of maxima of local maxima in fft: ")
print(max_freq_list)

# print(max_freq_part_list)

    


number_of_peak = len(max_freq_every_list)
peak_number = [i+1 for i in range(number_of_peak)]

coeff = polyfit(peak_number, max_freq_every_list, 1)
coeff_y = [coeff[0]*i+coeff[1] for i in peak_number]
max_freq_every_list = np.array(max_freq_every_list)
coeff_y = np.array(coeff_y)
Var = sum(((coeff_y-max_freq_every_list)/max_freq_every_list)**2)/len(coeff_y)
sd = Var**0.5
uncertainty = sd*coeff[0]



plt.figure()
plt.plot(f, absY)
plt.xlim(0,1e7)
plt.xlabel('freq(Hz)')
plt.ylabel('Magnitude(arb.)')
""" plt.title("FFT") """
# plt.text(0.7e7, 0.008, 'x='+str(int(freq))+'Hz')
plt.grid()
plt.show()

plt.figure()
plt.plot(x, y)
plt.xlabel('Time(s)')
plt.title("Ultrasound transmitted in 12mm Al")
plt.grid()
plt.show()

# plt.figure()
# plt.plot(peak_number, max_freq_every_list, 'rx')
# plt.plot(peak_number, coeff_y, 'k-')
# plt.text(1, 3e6, "gradient="+str(coeff[0])+"±"+str(uncertainty))
# plt.title("Frequency at each peak")
# plt.xlabel('Peak #')
# plt.ylabel('Frequency')
# plt.show()