# -*- coding: utf-8 -*-
"""
Created on Sat Aug 28 20:22:33 2021

@author: Hao
"""

from PIL import Image
import os

mwidth=200
mheight=400

d = 'Y10' #
initial_n = 5231 #


initial_n -=1
path = 'D:\picture\zhangyixing\\'+d+'\\' #
savePath = 'D:\picture\zhangyixing_new\\'+d+'\\' #

if os.path.isdir(savePath):
    pass
else:
    os.mkdir(savePath)

p = path+'jpg.bat'

files = os.listdir(path)
n = 0
for file in files:
    if file[-4:] == '.jpg':
        n +=1

def jpg():
    fp = open(p, 'w')
    fp.write('ren *.gif *.jpg')
    fp.close()

def process_image(path, savePath):
    i = 1
    while i <= n:
        image = Image.open(path+str(i+initial_n)+'.jpg').convert('RGB')
        w,h = image.size
        if w<=mwidth and h<=mheight:
            print('It is OK.')
        if (1.0*w/mwidth) > (1.0*h/mheight):
            scale = 1.0*w/mwidth
            new_im = image.resize((int(w/scale), int(h/scale)), Image.ANTIALIAS)
 
        else:
            scale = 1.0*h/mheight
            new_im = image.resize((int(w/scale),int(h/scale)), Image.ANTIALIAS)     
        new_im.save(savePath+str(i)+'.jpg')
        new_im.close()
        i += 1
  
        
jpg()
a = input('Have you run the file? (y/n)\n')
if a == 'y':
    process_image(path, savePath)
else:
    pass
