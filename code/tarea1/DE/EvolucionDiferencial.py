import numpy as np
import random
import sys
import math
import copy
import time

#Clase para todos los individuos en la poblacion
class PoblacionDE(object):
    def __init__(self,dimension,maximo=None,minimo=None):
        self.solution=[] #vector de soluciones
        self.minimo=minimo
        self.maximo=maximo

        for i in range(dimension):
            
            if(minimo!=None and maximo!=None):
                self.solution=np.append(self.solution,(random.uniform(minimo,maximo)))
            else:
                self.solution=np.append(self.solution,float(random.random()))
        

class DifferentialEvolution(object):
    def __init__(self,dimension,tam_poblacion,maximo,minimo,funcion,max_iter,F=0.6,CR=0.8,semilla=None):
        self.dimension = dimension #dimension del problema
        self.poblacion = [PoblacionDE(dimension,maximo,minimo) for i in range(tam_poblacion)] #se crea la poblacion 
        self.max_iter = max_iter #maximas iteraciones
        self.minimo = minimo    #limite inferior
        self.maximo = maximo    #limite superior
        self.tam_poblacion = tam_poblacion #size de la poblacion
        self.funcion = funcion    #funcion objetivo
        self.F = F       #Factor de amplitud
        self.CR = CR     #Constante de recombinacion
        self.semilla = semilla  #cambiar semillas
        self.mutanteV = PoblacionDE(dimension,maximo,minimo)
        self.trialV = [PoblacionDE(dimension,maximo,minimo) for i in range(tam_poblacion)]
        self.mejor_individuo = PoblacionDE(dimension,maximo,minimo)
        self.mejor_individuo.value = sys.float_info.max

    def run(self):
        contador = 0

        #poner semilla para variar los aleatorios
        if(self.semilla != None):
            random.seed(self.semilla)

        #ciclar con el max de iteraciones
        while (contador<self.max_iter):
            for index in range(self.tam_poblacion):
                r1 = random.randrange(self.tam_poblacion) #seleccionar un randon de
                r2 = random.randrange(self.tam_poblacion) #cardinalidad de la poblacion

                #evitar que r1 & r2 sean iguales
                if r1==r2:
                    r2 = random.randrange(self.tam_poblacion)
                r3 = random.randrange(self.tam_poblacion)

                #evitar que sea igual a r1 o r2
                if r3 == r1 or r3 == r2:
                    r3 = random.randrange(self.tam_poblacion)

                #se calcula el vector mutado con la ecuacion
                self.mutanteV.solucion = self.poblacion[r1].solution + self.F * (self.poblacion[r2].solution - self.poblacion[r3].solution)
                #print('antes del cruce ', self.poblacion[index].value, ' ', self.poblacion[index].solution)
                #print('antes del mutante ', self.mutanteV.value, ' ', self.mutanteV.solution)
                #print('antes del trial ', self.trialV[index].value,' ',self.trialV[index].solution)

                J_r = random.randrange(self.dimension)
                
                #crear un vector de prueba - para evitar estancamientos
                for j in range(self.dimension):
                    r_cj = random.random()

                    if r_cj < self.CR or j==J_r:
                        #print("individuo ",index, 'cae aqui en el mutado para el parametro')
                        #se toma del vector mutado esa dimension
                        self.trialV[index].solution[j] = copy.deepcopy(self.mutanteV.solution[j])
                        #time.sleep(1)
                        #print('despues de cambiar un parametro',self.poblacion[index].solution)
                        #print('despues de cambiar un parametro trial',self.trialV[index].solution)
                    else:
                        #si no se toma del original
                        #print('particula ',index,' cae aqui para el parametro',j)
                        self.trialV[index].solution[j] = self.poblacion[index].solution[j]

                #print("despues del cruce")
                #print("despues del cruce ", self.poblacion[index].value,' ',self.poblacion[index].solution)
                #print("despues del mutante ", self.mutantV.value, ' ', self.mutantV.solution)
                #print("despues del trial ", self.trialV[index].value, ' ', self.trialV[index].solution)
                self.trialV[index].value = self.funcion(self.trialV[index].solution)
                self.poblacion[index].value = self.funcion(self.poblacion[index].solution)
                

                #si el fitness es mejor que el vector original
                if self.trialV[index].value < self.poblacion[index].value:
                    self.poblacion[index].solution = copy.deepcopy(self.trialV[index].solution)
                    self.poblacion[index].value = copy.deepcopy(self.trialV[index].value)
                    
            for i in range(self.tam_poblacion):

                #guardar el individuo que dio mejores resultados
                if self.poblacion[i].value < self.mejor_individuo.value:
                    self.mejor_individuo = copy.deepcopy(self.poblacion[i])
            
            contador = contador +1
        return self.mejor_individuo.solution
