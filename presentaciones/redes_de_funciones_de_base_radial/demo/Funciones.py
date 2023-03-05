# -*- coding: utf-8 -*-
"""
Funciones a plotear

"""
import numpy as np

# funcion
def funcion1(t1,t2):
    x = np.arange(t1, t2, 0.2) # -11 - 10
    fx = []
    s=0
    for i in x:
        if (-10 <= i) and (i < -2):
            s = -2.186*i-12.864
        elif (-2 <= i) and (i < 0):
            s = 4.246*i
        elif (0 <= i) and (i < 10):
            s = 10*np.exp((-0.05*i)-0.5) * (np.sin((0.03*i + 0.7)*i))
        fx.append(s)
    # normalizar valores entre 0 -1
    xnor = []
    for j in fx:
        xnor.append((1)/(max(fx)-min(fx))*(j-min(fx)))
    
    # validacion
    x2 = np.arange(-10, 11, 0.5)
    fx2 = []
    for i in x2:
        if (-10 <= i) and (i < -2):
            s2 = -2.186*i-12.864
        elif (-2 <= i) and (i < 0):
            s2 = 4.246*i
        elif (0 <= i) and (i < 10):
            s2 = 10*np.exp((-0.05*i)-0.5) * (np.sin((0.03*i + 0.7)*i))
        fx2.append(s2)
    # normalizar valores entre 0 -1
    xnor2 = []
    for j in fx2:
        xnor2.append((1)/(max(fx)-min(fx))*(j-min(fx)))
    
    X1 = np.empty((len(x),1),float)
    X2 = np.empty((len(x2),1),float)
    X1[:,0]=x
    X2[:,0]=x2
    d1 = xnor
    d2 = xnor2
    return X1,d1,X2,d2
