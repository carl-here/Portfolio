# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 11:29:49 2026

@author: charl
"""

'''Liten kode som sjekker to likninger og om de passer til fikspunktsiterasjon'''
'''import numpy as np

f = lambda I: 1 - np.log(1+I)
g = lambda V: 2- np.exp(V)

I = 1
V = 1

for i in range(20):
    I = f(I)
    V = g(V)
    print(V)
    
'''
    
def kodekode(x, a, b):
    kodesvar = x * a + b
    return kodesvar


print(kodekode(b=3, a=4, x=1))  
