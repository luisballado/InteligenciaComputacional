# -*- coding: utf-8 -*-
"""
@author: Victor Romero 
Nombre: Red RBF 
Requerimientos: Archivo del clasificador KMEANS
"""
import numpy as np
from kmeans import KMEANS

class rbf:
    #Definir el numero de neuronas de capa oculta y numero de neuronas de la capa de salida
    def __init__(self,n_oc=2,n_s=1):
        # Inicializar arquitectura de la red
        self.n_oc = n_oc # neuronas Gaussianas
        self.n_s = n_s
        # generar valores aleatoreos de los pesos sinapticos
        np.random.seed(0)
        self.w = np.random.rand(n_s,n_oc+1) #agregamos uno por el valor del umbral

    """
    Proceso de aprendizaje
    data_train - datos de entrenamiento
    labels - etiquetas
    l_rate - tasa de aprendizaje
    ep - numero max de epocas
    presicion - error minimo a tolerar
    """
    def APRENDER(self, data_train, labels, l_rate = 0.2, ep=100, press=0.1):
        # obtener centroides con clasificador kmeans y clusters los conjuntos
        centroides,clusters = self.AP_NO_SUPERVISADO(self.n_oc, data_train)
        # obtener varianza 
        varianza = self.VARIANZA(centroides, clusters)
        epocas,errores = self.AP_SUPERVISADO(data_train,labels,l_rate,ep,press,centroides,varianza)
        return epocas, errores, self.w, varianza, centroides

    #Inicializar k means donde le pasamos el numero de k donde es el numero de neuronas de la capa oculta
    def AP_NO_SUPERVISADO(self,k,X):
        clasificador  = KMEANS(k,50,0.1) #regresa el valor de conjuntos y centroides
        return clasificador.AGRUPAR(X)
            
    def AP_SUPERVISADO(self,data_train,labels,l_rate,ep,press,centroides,sigma):
        # generar seudomuestras
        Z = self.GET_SEUDOM(data_train,sigma,centroides)
        # agregar fila correspondiente a los valores de umbral de las neuronas
        u = np.ones((1,Z.shape[1]))
        Z = np.concatenate((u*-1,Z),axis=0)
        # parametros iniciales
        e_medio = 0 # error medio
        e_gbl = 1 # error global
        e_red = 1 # error de la red
        Errores = []
        epochs = 0 # epocas
        xi = np.empty((Z.shape[0],1)) # vector de caracteristas por muestra
        # secuencia de aprendizaje
        while (np.abs(e_red) > press):
            e_anterior = e_gbl
            for i in range(len(labels)):
                # obtener una muestra del conjunto Z
                xi[:,0] = Z[:,i]
                # obtener salida deseada
                di = labels[i]
                # generar salida de la red
                yi = self.SALIDA_RED(xi)
                # ajustar pesos w
                self.REGLA_DELTA(xi,di,yi,l_rate)
                # obtener salida con nuevos pesos
                yi = self.SALIDA_RED(xi)
                # computar el error cuadratico medio
                e_medio = e_medio + ((di-yi)**2)
            
            # computar el error global 
            e_gbl = (1/(len(labels)) * e_medio)
            e_red = np.abs(e_gbl - e_anterior) # error de la red
            Errores.append(e_red) # almacena el error
            # incrementa el numero de epocas
            epochs +=1
            # terminar aprendizaje si se supera el numero de epocas establecido
            if epochs > ep:
                break
        return epochs,Errores
    
    def REGLA_DELTA(self,xi,di,yi,l_rate):
        # computar el error
        e = (di-yi)
        # computar delta
        d = (dsigmoide(yi)) * e
        # ajustar pesos sinapticos
        self.w = self.w + (xi.T * l_rate * d)
        
    
    def SALIDA_RED(self,xi):
        yi = sigmoide(ACTIVAR_NEURONA(self.w,xi))
        return yi
    
    def GET_SEUDOM(self,data_train,varianza,centroides):
        Z = np.empty((centroides.shape[1],data_train.shape[1]))
        for i in range(data_train.shape[1]):
            distancia = np.empty(data_train.shape[1])
            for j in range(centroides.shape[1]):
                # computar distancia euclidiana
                distancia[i] = EUCLIDIANA(data_train[:,i],centroides[:,j])
                # computar peso de la muestra sobre el centroide
                Z[j,i] = PESO(distancia[i],varianza[j])
        return Z

    #recibe centroides y clusters
    #calcular la distancia euclidiana
    def VARIANZA(self,centros,clusters):
        # generar sigma
        varianza = np.empty(len(clusters)) #matriz respecto al numero de conjuntos
        for i in range(len(clusters)):
            conjunto = np.empty(len(clusters[i]))
            for j in range(len(clusters[i])):
                conjunto[j] = np.sum((clusters[i][j]-centros[:,i])**2)
                
            varianza[i] = ((1/len(clusters[i]))) * np.sum(conjunto)
        return varianza

    #Asumimos que tenemos el valor de los pesos, centroides y varianza
    def OPERACION(self,data_val, w,centroides,varianza):
        self.w = w
        y = []
        for i in range(data_val.shape[1]):
            distancia = np.empty(centroides.shape[1])
            ng = np.empty((centroides.shape[1],1))
            for c in range(centroides.shape[1]):
                distancia[c] = EUCLIDIANA(data_val[:,i], centroides[:,c])
            # activar neuronas gaussianas -> Seudomuestras
            for g in range(centroides.shape[1]):
                ng[g,:] = PESO(distancia[g], varianza[g])
            # agregar valor de umbral
            u = np.ones((1,ng.shape[1]))
            xi = np.concatenate((u*-1,ng),axis=0)
            # activar neuronas de salida
            yi = self.SALIDA_RED(xi)
            y.append(yi)
        return y

# función para activar una neurona
def ACTIVAR_NEURONA(w,x):
    return np.dot(w,x)

# función para computar la distancia Euclidiana
def EUCLIDIANA(x,y):
    return (np.sum((x-y))) # distancia euclidiana

# función pata convertir distancia a peso por kernel Gaussiano
def PESO(distancia,varianza):
    return np.exp(-(distancia**2)/(2*(varianza)))

# funcion sigmoidal
def sigmoide(x):
    return 1/(1+np.exp(-x))

def dsigmoide(x):
    s=1/(1+np.exp(-x))
    return s*(1-s)
