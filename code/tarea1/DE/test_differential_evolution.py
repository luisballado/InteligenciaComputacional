import time #para las metricas de tiempo
import numpy as np #importar numpy para el manejo de vectores
import sys #para acceso de datos como argumentos

#Clase que engloba Evolucion Diferencial
from EvolucionDiferencial import *

#Ejecutar programa pasando los argumentos de max_iter, poblacion, semilla, dimension
#python3.10 test_differential_evolution.py 1000 21 1234 10 0.7 0.8

#100000 21 1234 10 0.7 0.8

max_iter  = int(sys.argv[1])
#max_iter = 100000
poblacion = int(sys.argv[2])
#poblacion = 21
semilla_hermitanio = int(sys.argv[3])
dimension = int(sys.argv[4])
#dimension = 10
F = float(sys.argv[5])
#F = 0.7
CR = float(sys.argv[6])
#CR = 0.8

###################ESFERA###########################
#regresar la sumatoria del vector de entrada
def sphere(x):
    return np.sum(x**2)

###################ROSENBROCK###################################
#se le pasa una lista con dos valores para las xs
#x[1:]  - el ultimo en la lista
#x[:-1] - el primero en la lista
def rosenbrock(x):
    return np.sum(100.0*(x[1:] - x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)

####################ACKLEY######################
#se le pasa una lista de x
def ackley(x):
    n = len(x)
    sum_sqr = 0
    sum_cos = 0
    
    for i in range(n):
        sum_sqr += x[i]**2
        sum_cos += np.cos(2 * np.pi * x[i])
        
    return -20 * np.exp(-0.2 * np.sqrt(1/n * sum_sqr)) - np.exp(1/n * sum_cos) + 20 + np.e

#Lista de las funciones a evaluar
funciones_objetivo = [sphere,ackley,rosenbrock]

#iterar para cada funcion objetivo
for func_obj in funciones_objetivo:

    if func_obj.__name__ == 'sphere':
        limite_superior =  5.12
        limite_inferior = -5.12
    elif func_obj.__name__ == 'ackley':
        limite_superior =  32.768
        limite_inferior = -32.768
    elif func_obj.__name__ == 'rosenbrock':
        limite_superior =  2.048
        limite_inferior = -2.048
    
    evaluar = DifferentialEvolution(dimension=dimension,
                                       tam_poblacion=poblacion,
                                       maximo=limite_superior,
                                       minimo=limite_inferior,
                                       funcion=func_obj,
                                       max_iter=max_iter,
                                       F=F,
                                       CR=CR,
                                       semilla=semilla_hermitanio)
    
    start_time = time.time()
    results = evaluar.run()

    if func_obj.__name__ == 'sphere':
        print("#######ESFERA########")
        #print(results)
        print("Minimo Esfera - %s" % min(n for n in results if n>0))
        print("Tiempo - %s segundos" % (time.time()-start_time))

    elif func_obj.__name__ == 'ackley':
        print("#######ACKLEY########")
        #print(results)
        print("Minimo - %s" % min(n for n in results if n>0))
        print("Tiempo - %s segundos" % (time.time()-start_time))

    elif func_obj.__name__ == 'rosenbrock':
        print("#######ROSENBROCK########")
        #print(results)
        print("Minimo ROSENBROCK - %s" % min(n for n in results if n>0))
        print("Tiempo - %s segundos" % (time.time()-start_time))
