# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 18:39:35 2021

@author: Victor Romero
Nombre: RBF
Requerimientos: Archivo del clasificador RBF
"""

import numpy as np
import matplotlib.pyplot as plt
from RBF import rbf
from Funciones import funcion1

# matriz de muestras de aprendizaje

X,d,X2,d2=funcion1(-11, 10)

# Inicializar datos
f, c = X.shape
fac_ap = 0.02
precision = 0.01
epocas = 1000 #2000
# Arquitectura de la red
n_ocultas = 2 #probar de 2 hasta 7
n_salida = 1

# Iniciar Red
red = rbf(n_ocultas, n_salida)

epochs, Er,w,var,cent = red.APRENDER(X.T,d,fac_ap,epocas,precision)
print("Total epocas:", epochs)

y = red.OPERACION(X2.T,w,cent,var)
y = np.array(y)
y = y[:, 0, 0]
print("salidas: ", y)

# Grafica la funcion
#figure(1)
plt.grid()
plt.ylabel("f(x)", fontsize=12)
plt.xlabel("t", fontsize=12)
plt.title("Aproximador de funciones", fontsize=14)
plt.plot(X2[:,0], y, 'b', label="Señal obtenida")
plt.plot(X[:,0], d, 'r', label="Señal deseada")
plt.legend(loc='upper right')
plt.savefig('prueba.png')
#plt.show()

#figure(2)
plt.grid()  # Activar rejilla
plt.ylabel("Error", fontsize=12)
plt.xlabel("Épocas", fontsize=12)
plt.title("RBF", fontsize=14)
Er = np.array(Er)
Er = Er[:, 0, 0]
plt.plot(Er, 'g', label="Error cuadratico")
plt.legend(loc='upper right')
#plt.show()
plt.savefig('prueba2.png')
