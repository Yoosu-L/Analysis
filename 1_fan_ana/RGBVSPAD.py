# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 18:50:23 2021

@author: Hao
"""

import cv2 as cv
import csv
import numpy as np
import os


n = 0
path = ''
savePath = 'C:\\picture\\'

def Calculate(x):
    src = cv.imread(x)
    src_hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
    # cv.imshow("q",src)
    h,w,ch = np.shape(src)
    hest_r = np.zeros([256],dtype = np.int32)
    hest_g = np.zeros([256],dtype = np.int32)
    hest_b = np.zeros([256],dtype = np.int32)
    hest_h = np.zeros([181],dtype = np.int32)
    hest_s = np.zeros([256],dtype = np.int32)
    hest_v = np.zeros([256],dtype = np.int32)
    colorRange = np.zeros([7],dtype = np.int32)
    
    sumv = 0
    sums = 0
    for row in range(h):
        for col in range(w):
            b, g, r = src[row,col]
            hest_r[r] +=1
            hest_g[g] +=1
            hest_b[b] +=1
            r = r/255
            g = g/255
            b = b/255
            sumv += max(r, g, b)
            if max(r, g, b) == 0:
                sums += 0;
            else:
                sums += 1-(min(r, g, b)/max(r, g, b))
            
            hu, s, v = src_hsv[row, col]
            hest_h[hu] +=1
            hest_s[s] +=1
            hest_v[v] +=1
            if hu == 0:
                colorRange[0] +=1
            elif 7< hu <= 23:
                colorRange[2] +=1
            elif 23 < hu <= 35:
                colorRange[3] +=1
            elif 35< hu <= 90:
                colorRange[4] +=1
            elif 90 < hu <= 136:
                colorRange[5] +=1
            elif 136< hu <= 169:
                colorRange[6] +=1
            else:
                colorRange[1] +=1
                
    # plt.plot(hest_r,color = "r")
    # plt.plot(hest_b,color = "b")
    # plt.plot(hest_g,color = "g")
    # plt.xlim([0,256])
    # plt.show()
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    sumR = sumG = sumB = 0
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
    
    for i in range(256):
        sumR += hest_r[i]*i/255
        sumG += hest_g[i]*i/255
        sumB += hest_b[i]*i/255
    R_mean = sumR/(h*w)
    G_mean = sumG/(h*w)
    B_mean = sumB/(h*w)
    # print('R_mean = ' + str(R_mean)+
    #       '\n' + 'G_mean = ' + str(G_mean)+ 
    #       '\n' + 'B_mean = ' + str(B_mean))
    
    sumr = sumg = sumb = 0
    # for row in range(h):
    #     for col in range(w):
    #         b, g, r = src[row,col]
    #         sumr += (r-R_mean)**2
    #         sumg += (g-G_mean)**2
    #         sumb += (b-B_mean)**2
    
    for i in range(256):
        sumr += hest_r[i]*(i/255-R_mean)**2
        sumg += hest_g[i]*(i/255-G_mean)**2
        sumb += hest_b[i]*(i/255-B_mean)**2

    R_var = sumr/(h*w)
    G_var = sumg/(h*w)
    B_var = sumb/(h*w)
    # print('R_var = ' + str(R_var)+
    #       '\n' + 'G_var = ' + str(G_var)+ 
    #       '\n' + 'B_var = ' + str(B_var))
    
    sumv = 0
    V_mean = 0.299 * R_mean + 0.587 * G_mean + 0.114 * B_mean
    S_mean = sums/(h*w)
    sumS = 0
    for row in range(h):
        for col in range(w):
            b, g, r = src[row,col]
            r = r/255
            g = g/255
            b = b/255
            v = 0.299 * r + 0.587 * g + 0.114 * b
            sumv += (v-V_mean)**2
            if max(r, g, b) == 0:
                sumS += (0-S_mean)**2
            else:
                sumS += ((1-(min(r, g, b)/max(r, g, b)))-S_mean)**2
    V_var = sumv/(h*w)
    S_var = sumS/(h*w)
    # print('V_mean = ' + str(V_mean)+
    #       '\n' + 'S_mean = ' + str(S_mean)+
    #       '\n' + 'V_var = ' + str(V_var)+
    #       '\n' + 'S_var = ' + str(S_var))
    
    P = 0.69*V_mean + 0.22*S_mean
    A = -0.31*V_mean + 0.6*S_mean
    D = -0.76*V_mean + 0.32*S_mean
    
    return [[R_mean, R_var, G_mean, G_var, B_mean, B_var, S_mean, S_var, V_mean, V_var, P, A, D, red_share, orange_share, yellow_share, green_share, blue_share, violet_share, warm_share, cold_share]]
    

def auto(n, path, savePath):
    i = 1
    l = [['R_mean', 'R_var', 'G_mean', 'G_var', 'B_mean', 'B_var', 'S_mean', 'S_var', 'V_mean', 'V_var', 'Pleasure', 'Arousal', 'Dominance', 'red_share', 'orange_share', 'yellow_share', 'green_share', 'blue_share', 'violet_share', 'warm_share', 'cold_share']]
    while i <= n:
        Path = path + str(i) + '.jpg'
        l += Calculate(Path)
        print(str(i)+' Done')
        i += 1
        
    # with open(savePath + '3.csv', 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerows(l)
    
    return l


eacno = [['Extraversion', 'Agreeableness', 'Conscientiousness', 'Neuroticism', 'Openness']]

for i in range(4):
    n = 0
    path = 'D:\picture\\1\\P' + str(i+1) + '\\'
    print(path)
    files = os.listdir(path)
    for file in files:
        if file[-4:] == '.jpg':
            n +=1
    lis = auto(n, path, savePath)
    R_mean, R_var, G_mean, G_var, B_mean, B_var, S_mean, S_var, V_mean, V_var, P, A, D, red_share, orange_share, yellow_share, green_share, blue_share, violet_share, warm_share, cold_share = np.mean(np.array(lis[1:]), 0)
    Extraversion = 0.191*B_var + 0.196*G_var + 0.22*R_var + 0.239*V_var + 0.122*S_mean + 0.1*A + 0.132*red_share + 0.132*orange_share - 0.202*green_share - 0.111*blue_share + 0.179*warm_share - 0.179*cold_share
    Agreeableness = 0.132*B_mean + 0.15*G_mean + 0.132*R_mean + 0.18*V_mean + 0.2*P - 0.136*D + 0.124*blue_share
    Conscientiousness = 0.192*B_mean + 0.158*B_var + 0.195*G_mean + 0.148*G_var + 0.187*R_mean + 0.109*R_var + 0.183*V_mean + 0.159*P -0.151*A - 0.191*D + 0.237*red_share - 0.127*green_share
    Neuroticism = -0.109*B_mean - 0.106*V_mean + 0.103*D + 0.1*yellow_share
    Openness = -0.101*R_mean - 0.11*B_var - 0.111*S_var - 0.101*V_mean - 0.115*P - 0.116*green_share
    eacno += [[Extraversion, Agreeableness, Conscientiousness, Neuroticism, Openness]]
    print(path+' was done')
    
with open(savePath + 'star.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(eacno)


# R_mean, R_var, G_mean, G_var, B_mean, B_var, S_mean, S_var, V_mean, V_var, P, A, D, red_share, orange_share, yellow_share, green_share, blue_share, violet_share, warm_share, cold_share = np.mean(np.array(lis[1:]), 0)
# Extraversion = 0.191*B_var + 0.196*G_var + 0.22*R_var + 0.239*V_var + 0.122*S_mean + 0.1*A + 0.132*red_share + 0.132*orange_share - 0.202*green_share - 0.111*blue_share + 0.179*warm_share - 0.179*cold_share
# Agreeableness = 0.132*B_mean + 0.15*G_mean + 0.132*R_mean + 0.18*V_mean + 0.2*P - 0.136*D + 0.124*blue_share
# Conscientiousness = 0.192*B_mean + 0.158*B_var + 0.195*G_mean + 0.148*G_var + 0.187*R_mean + 0.109*R_var + 0.183*V_mean + 0.159*P -0.151*A - 0.191*D + 0.237*red_share - 0.127*green_share
# Neuroticism = -0.109*B_mean - 0.106*V_mean + 0.103*D + 0.1*yellow_share
# Openness = -0.101*R_mean - 0.11*B_var - 0.111*S_var - 0.101*V_mean - 0.115*P - 0.116*green_share

# print('Extraversion:', Extraversion)
# print('Agreeableness:', Agreeableness)
# print('Conscientiousness:', Conscientiousness)
# print('Neuroticism:', Neuroticism)
# print('Openness:', Openness)
