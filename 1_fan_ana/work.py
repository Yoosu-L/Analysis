# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 01:17:50 2021

@author: Hao
"""

import os
import threading


# =============================================================================
# def worker(file):
#     multiprocessing.subprocess.Popen(['screen', 'C:\\Users\\hao\\Desktop\\a.py'])
#     multiprocessing.subprocess.Popen(['screen', 'C:\\Users\\hao\\Desktop\\b.py'])
#     multiprocessing.subprocess.Popen(['screen', 'C:\\Users\\hao\\Desktop\\c.py'])
#     # your subprocess code
# 
# 
# if __name__ == '__main__':
#     files = ["C:\\Users\\hao\\Desktop\\a.py","C:\\Users\\hao\\Desktop\\b.py","C:\\Users\\hao\\Desktop\\c.py"]
#     for i in files:
#         p = multiprocessing.Process(target=worker, args=(i,))
#         p.start()
# =============================================================================
        
def a():
    os.system('python C:\\Users\\Hao\\.spyder-py3\\Code\\ym.py')
    
def b():
    os.system('python C:\\Users\\Hao\\.spyder-py3\\Code\\yyqx.py')

def c():
    os.system('python C:\\Users\\Hao\\.spyder-py3\\Code\\RGBVSPAD.py')
    
thread = []
thread.append(threading.Thread(target=a))
thread.append(threading.Thread(target=b))
thread.append(threading.Thread(target=c))

if __name__ == '__main__':
    for t in thread:
        t.setDaemon(True)
        t.start()
