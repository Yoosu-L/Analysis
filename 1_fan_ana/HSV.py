# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 12:40:10 2021

@author: Hao
"""

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

file = 'C:\\Users\\Hao\\Desktop\\awyb\\1.jpg'

# =============================================================================
# img_hsv = cv2.imread(file, cv2.COLOR_BGR2HSV)
# img_bgr = cv2.imread(file, 1)
# px1 = img_hsv[1,1]
# px2 = img_bgr[1,1]
# print(px1, px2)
# =============================================================================

def hsv(x):
    src = cv.imread(x)
    src_hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
    h,w,ch = np.shape(src_hsv)
    
    
    hest_h = np.zeros([181],dtype = np.int32)
    hest_s = np.zeros([256],dtype = np.int32)
    hest_v = np.zeros([256],dtype = np.int32)
    colorRange = np.zeros([7],dtype = np.int32)
    
    for row in range(h):
        for col in range(w):
            h, s, v = src_hsv[row, col]
            hest_h[h] +=1
            hest_s[s] +=1
            hest_v[v] +=1
            if h == 0:
                colorRange[0] +=1
            elif 7< h <= 23:
                colorRange[2] +=1
            elif 23 < h <= 35:
                colorRange[3] +=1
            elif 35< h <= 90:
                colorRange[4] +=1
            elif 90 < h <= 136:
                colorRange[5] +=1
            elif 136< h <= 169:
                colorRange[6] +=1
            else:
                colorRange[1] +=1
    
    # plt.plot(hest_h, color='r')
    # plt.xlim([-10,180])
    # plt.show()
    
# =============================================================================
#     hist = np.array([])
#     for i in range(180):
#         hist = np.concatenate((hist, np.full(hest_h[i], i)))
#     
#     kde = sm.nonparametric.KDEUnivariate(hist)
#     kde.fit(bw=3)
#     
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     
#     ax.hist(hist, bins=180, density=True, label='Histogram from samples')
#     ax.plot(kde.support, kde.density, lw=2, label='KDE from samples')
#     
#     ax.legend(loc='best')
#     ax.grid(True, zorder=-5)
#     
#     samples = np.linspace(0, 200, 101)
#     probs = kde.evaluate(samples)
#     maxima_index = probs.argmax()
#     maxima = samples[maxima_index]
#     print(maxima)
# =============================================================================
    
    black, red, orange, yellow, green, blue, violet = colorRange
    s = sum(colorRange)
    red_share = red/s
    orange_share = orange/s
    yellow_share = yellow/s
    green_share = green/s
    blue_share = blue/s
    violet_share = violet/s
    warm_share = (red+orange+yellow)/s
    cold_share = (green+blue+violet)/s
    return red_share, orange_share, yellow_share, green_share, blue_share, violet_share, warm_share, cold_share
    
hsv(file)