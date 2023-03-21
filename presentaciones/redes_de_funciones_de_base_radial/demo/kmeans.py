# -*- coding: utf-8 -*-
"""
kmeans
"""

import numpy as np
import matplotlib.pyplot as plt

class KMEANS():
    def __init__(self, k=2, max_iter=100, u=0.001):
        self.k=k
        self.max_iter=max_iter
        self.u=u
    
    def AGRUPAR(self, X):
        self.X=X
        self.n_muestras=X.shape[1]
        # matrix de centroides
        self.c=np.empty((X.shape[0],self.k))
        # asugnar valor inicial a centroides
        for i in range(self.k):
            self.c[:,i]=self.X[:,i]
        # actualiza centroides
        for it in range(self.max_iter):
            # generar grupós vscios
            grupos=[[] for _ in range(self.k)]
            c_anterior=self.c
            # matrix de distancias
            distancia=np.empty((self.n_muestras,self.k))
            
            # calcular la distancia euclidiana entre c y x
            # para cada centroide
            for i in range(self.k):
                # para cada muestra
                for n in range(self.n_muestras):
                    # computar la distancia Euclidiana
                    distancia[n,i]=EUCLIDIANA(self.X[:,n],self.c[:,i])
            
            # comparar las distancias para cada c y almacenar en los conjuntos correspondientes
            for j in range(self.n_muestras):
                # ordenar de menor a mayor
                indice=np.argmin(distancia[j,:])
                print("clase ", indice)
                # almacenar muestra j en conjunto indice
                grupos[indice].append(self.X[:,j])
            
            # nuevos centroides
            self.new_c = self.NEW_CENT(grupos)

            # cambio anterio de centroides
            converge = self.CAMBIO(self.new_c, c_anterior)
            print("cambio ", converge)
            # actualar el valor de centroides
            self.c = self.new_c
            
            # si se ha rebazado el umbral de cambio salir
            if self.u>converge:
                break
            
            # graficar
            """
            for i in range(len(grupos[0])):
                data=grupos[0][i]
                print(data)
                print(data[0])
                #print(data[1])
                plt.scatter(x=data[0], y=data[1],c='blue', s=100, marker='o')
            
            for i in range(len(grupos[0])):
                data=grupos[1][i]
                plt.scatter(x=data[0], y=data[1],c='red', s=100, marker='o')
            
            # graficar los centroides
            for j in range(self.c.shape[1]):
                plt.scatter(x=self.c[0,j], y=self.c[1,j], c='black', s=200, marker='x')
            
            plt.show()
            """
            #plt.savefig('algo'+str(rr)+'.png')
        return self.c, grupos
        
    
    def NEW_CENT(self, grupos):
        new_cent = np.empty((self.c.shape))
        for i in range(self.k):
            new_cent[:,i]=np.median(grupos[i],axis=0)
        return new_cent
    
    def CAMBIO(self, new,old):
        a=np.sum((new-old)/old)
        return np.abs(a)
        
    
def EUCLIDIANA(x,y):
    return np.sqrt(np.sum((x-y)**2))
            
