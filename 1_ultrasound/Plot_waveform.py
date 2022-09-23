from gettext import find
from re import I
import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.signal import argrelextrema
from numpy import polyfit
from cumulative_peak_finding import gradient, read, find_peak, calculate, plot

p_pre = 'C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\Ex2-data\\T00'
p_pree = 'C:\\Users\\Hao\\Desktop\\Ultrasound\\Data_files\\Ex2-data\\T0'
bp = 7213 # base point (12813 for previous data) 7213
td = 0.4 # Threshold (0.15 for previous data)
n = 130
x_p = 0
if n < 152:
    x_p = str(n*2-218) + 'mm'
else:
    x_p = str(n*2-266) + 'mm'

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
print(n_first)

plot(x, y, f, absY, absY1, x_p, w=True, fft=True)


x, y, f, absY, absY1, mi, ma = read(p, n_first-30, n_first+1200, zrs=0, main_freq=3.2e6, s=8e5, first=False)

""" y = abs(y) """

amp_defect_region = max(y[0:1200])
if n_first<20009:
    amp_nondefect_region = max(y[20009-n_first:21247-n_first])
else:
    amp_nondefect_region = amp_defect_region 
    



""" plot(x, y, f, absY, absY1, x_p, w=True, fft=True) """

""" def find_ratio(n):
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

    x, y, f, absY, absY1, mi, ma = read(p, n_first-30, n_first+1200, zrs=0, main_freq=3.2e6, s=8e5, first=False)
    y = abs(y)
    amp_defect_region = max(y[0:1200])
    if n_first<20009:
        amp_nondefect_region = max(y[20009-n_first:21247-n_first])
    else:
        amp_nondefect_region = amp_defect_region
    ratio = amp_defect_region/amp_nondefect_region

    return ratio

ratio_list = []
x_list = []
for i in range(118,152):
    r = find_ratio(i)
    ratio_list.append(r)
    x_list.append(i*2-218)

for i in range(176,204):
    r = find_ratio(i)
    ratio_list.append(r)
    x_list.append(i*2-266)

for i in range(len(x_list)):
    print(str(x_list[i])+" : "+str(ratio_list[i]))

plt.figure()
plt.plot(x_list, ratio_list)
plt.xlabel('Horizontal position [mm]')
plt.ylabel('Ratio')
plt.title("Ratio of Peaks")
plt.grid()
plt.show() """


""" 

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

plt.figure()
plt.plot(peak_number, mini_f, 'rx')
plt.plot(peak_number, tmini_f, 'k-')
plt.legend(labels=['data points',"gradient="+str(int(coeff))+"±"+str(int(uncertainty))], loc = 'upper left')
plt.title("Frequency at each peak")
plt.xlabel('Peak #')
plt.ylabel('Frequency')
plt.grid()
plt.show() 

"""