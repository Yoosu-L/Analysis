# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 11:14:06 2021

@author: Hao
"""

# from scipy.fft import fft, fftfreq, fftshift
import numpy as np
import matplotlib.pyplot as plt
import csv


path_0 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0000CH2.CSV"
path_1 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0001CH2.CSV"
path_2 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0002CH2.CSV"
path_3 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0003CH2.CSV"
path_4 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0004CH2.CSV"
path_5 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0005CH2.CSV"
path_6 = "C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\T0006CH2.CSV"

with open(path_3, 'r') as csvfile:
    reader = csv.reader(csvfile)
    rows = [row for row in reader]

data = (np.array(rows[18016:-1])).astype(np.float64)
x = data[:, 0]
y = data[:, 1]
N = len(x)
T = x[1]-x[0]
fs = int(1/T)+1 #sampling rate (N/s)
df = fs/(N-1) 
f = [df*n for n in range(N)]

# fft_y = fft(y)
# abs_y = np.abs(fft_y)
    
Y = np.fft.fft(y)*2/N
absY = [np.abs(x) for x in Y]


plt.figure()
plt.plot(f, absY)
plt.xlim(0,1e7)
plt.xlabel('freq(Hz)')
plt.title("FFT of medium bandwidth")
plt.grid()
plt.show()

plt.figure()
plt.plot(x, y)
plt.xlabel('Time(s)')
plt.title("medium bandwidth")
plt.grid()
plt.show()
