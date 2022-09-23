# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 23:23:20 2021

@author: Hao
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
from numpy import polyfit
from scipy.signal import argrelextrema

def read(path, first_point, end_point_of_first, zrs=6000, main_freq=4e6, s=5e5, first=True):
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile) 
        rows = [row for row in reader]
    
    data = (np.array(rows[first_point:-1])).astype(np.float64)
    x = data[:, 0]
    y = data[:, 1]
    
    if first == True:
        plt.figure()
        plt.plot(x[: end_point_of_first-first_point], y[: end_point_of_first-first_point])
        plt.xlabel('Time(s)')
        plt.ylabel('Amplitude(arb.)')
        """ plt.title("First Echo") """
        plt.grid()
        plt.show()
        
    data_first = (np.array(rows[first_point:end_point_of_first])).astype(np.float64)
    x1 = data_first[:, 0]
    y1 = data_first[:, 1]
    T = x[1]-x[0]
    
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
    mi = min(range(len(f)), key=lambda i: abs(f[i]-(main_freq-s)))
    ma = min(range(len(f)), key=lambda i: abs(f[i]-(main_freq+s)))
    max_absY = max(absY[mi:ma])
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
    Y1 = np.fft.fft(y1)*2/N1
    absY1 = [np.abs(i) for i in Y1]
    max_absY1 = max(absY1)
    fac1 = np.array([max_absY1 for i in range(len(absY1))])
    absY1 /= fac1
    
    f = f[0:int(1e7/df)]
    absY = absY[0:int(1e7/df)]
    absY1 = absY1[0:int(1e7/df1)]
    
    
    return x, y, f, absY, absY1, mi, ma

def find_peak(n_p, f, absY, absY1, mi, ma):
    threshold = 0.005
    f_diff = f[mi:ma]
    diff = absY1[mi:ma] - absY[mi:ma]
    mini_po = argrelextrema(np.array(diff), np.less)
    mini_f = []
    mini_amp = []
    while len(mini_f) < n_p:
        for i in mini_po[0]:
            if diff[i] <=threshold:
                mini_f.append(f_diff[i])
                mini_amp.append(diff[i])
        d_dif = [j-i for i, j in zip(mini_f[:-1], mini_f[1:])]
        d_diff = np.abs([j-i for i, j in zip(d_dif[:-1], d_dif[1:])])
        if d_dif:
            Thres = np.mean(d_dif)/2
            for i in d_diff:
                if i > Thres:
                    mini_f = []
                    mini_amp = []
        else:
            mini_f = []
            mini_amp = []
        threshold += 0.001
        if threshold > 1:
            return
    # print(threshold)
    # print(Thres)
    # print(d_dif)
    # print(d_diff)
        
    return f_diff, diff, mini_f, mini_amp

def find_peak_planB(n_p, f, absY, absY1, mi, ma):
    mi -= 50
    ma += 50
    f_diff = f[mi:ma]
    diff = absY1[mi:ma] - absY[mi:ma]
    

def calculate(g, u, v):
    thickness = v/(2*g)
    thickness_error = thickness*u/g
    return thickness, thickness_error

def cumulative_peak(ax, ay):
    maxy = 0
    miny = ay[-1]
    list1 = []
    
    for i in range(len(ay)):
        if ay[i] > maxy:
            list1.append(i)
            maxy = ay[i]
            
    for i in range(1, len(ay)):
        if ay[-i] >= miny:
            list1.append(-i+len(ay))
            miny = ay[-i]
    
    list1.sort()
    list1 = [i for i in set(list1)]
    list2 = [ax[i] for i in list1]
    list3 = [ay[i] for i in list1]
    
    return list2, list3

def gradient(ay):
    number_of_peak = len(ay)
    peak_number = [i+1 for i in range(number_of_peak)]

    coeff = polyfit(peak_number, ay, 1)
    coeff_y = [coeff[0]*i+coeff[1] for i in peak_number]
    ay = np.array(ay)
    coeff_y = np.array(coeff_y)
    Var = sum(((coeff_y-ay)/ay)**2)/len(coeff_y)
    sd = Var**0.5
    uncertainty = sd*coeff[0]
    
    return peak_number, coeff_y, coeff[0], uncertainty

def plot(x, y, f, absY, absY1, num, w=True, fft=True):
    if w==True:
        plt.figure()
        plt.plot(x, y)
        plt.xlabel('Time(s)')
        plt.ylabel('Amplitude(arb.)')
        """ plt.title("Ultrasound transmitted in Al "+str(num)) """
        plt.grid()
        plt.show()
    
    if fft==True:
        plt.figure()
        plt.plot(f, absY)
        plt.plot(f, absY1)
        plt.xlim(0,1e7)
        plt.xlabel('freq(Hz)')
        plt.title("FFT"+str(num))
        plt.legend(labels=['Whole Waveform','Envelope'],loc='best')
        plt.grid()
        plt.show()

def find_first_peak(path, threshold):
    x, y, _, _, _, _, _ = read(path, 1572, 1588, zrs=0, main_freq=5e6, first=False)
    