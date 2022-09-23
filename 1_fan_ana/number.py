# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 21:07:57 2021

@author: Hao
"""

import os

x = 0
Path1 = 'D:\picture\\1\\P'
Path2 = 'D:\picture\\wangyibo_new\\W'
Path3 = 'D:\picture\\yangmi_new\\YM'
Path4 = 'D:\picture\\yiyangqianxi_new\\Y'
Path5 = 'D:\picture\\zhangyixing_new\\Y'

def number(n, path, r=10):
    for i in range(r):
        p = path + str(i+1) + '\\'
        files = os.listdir(p)
        for file in files:
            if file[-4:] == '.jpg':
                n +=1
    return n

# for i in range(4):
#     path = 'D:\picture\\1\\P' + str(i+1) + '\\'
#     files = os.listdir(path)
#     for file in files:
#         if file[-4:] == '.jpg':
#             n +=1

print(number(number(number(number(number(x, Path1, 4), Path2), Path3), Path4), Path5))