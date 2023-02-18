import random
import numpy as np
import sys

class EvolutionProgramming(object):
    #inicializar con los parametros
    def __init__(self,dimension,tam_poblacion,max_iter,minimo,maximo,funcion,num_torneos,mutation_rate=0.01,semilla=None):
        self.dimension = dimension #dimension del problema
        self.tam_poblacion = tam_poblacion #tam de poblacion
        self.max_iter = max_iter   #maximas iteraciones
        self.minimo = minimo       #limite inferior
        self.maximo = maximo       #limite superior
        self.funcion = funcion     #funcion objetivo
        self.num_torneos = num_torneos  #num de torneos
        self.mutation_rate = mutation_rate  #ratio de mutacion
        self.semilla = semilla           #semilla
        
    #crear poblacion respecto al tamanio dado
    def generate_population(self):
        if self.semilla != None:
            random.seed(self.semilla)
        poblacion = []
        #se crea la poblacion
        for i in range(self.tam_poblacion):
            individuo = np.array([random.uniform(self.minimo,self.maximo) for j in range(self.dimension)])
            poblacion.append(individuo)
        return poblacion

    def evolucionar(self,poblacion):
        if self.semilla != None:
            random.seed(self.semilla)
        for i in range(self.max_iter):
            nueva_poblacion = []
                
        for individual in poblacion:
            torneo = random.sample(poblacion,self.num_torneos)
            winner = min(torneo,key=self.funcion) #conocer el mejor
            #ajustar desviacion con regla de 1/5
            sigma = self.mutation_rate * (self.maximo-(self.minimo)) / 5
            mutante = individual + np.random.normal(0,sigma,self.dimension)
                        
            if self.funcion(mutante) < self.funcion(winner):
                nueva_poblacion.append(mutante)
            else:
                nueva_poblacion.append(winner)
            
        poblacion = nueva_poblacion
        return min(poblacion, key=self.funcion)

