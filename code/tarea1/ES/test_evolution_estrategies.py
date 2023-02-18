import time #para las metricas de tiempo
import numpy as np #importar numpy para el manejo de vectores
import sys #para acceso de datos como argumentos

#Clase Abstracta que engloba Estrategias Evolutivas
from EstrategiasEvolutivas import *

#Ejecutar programa pasando el max_iteraciones, dimension, semilla
#python3.10 test_evolution_estrategies.py 1000 10 123 21

max_iteraciones = int(sys.argv[1])
#max_iteraciones = 100000
dimension = int(sys.argv[2])
#dimension = 10
semilla = int(sys.argv[3])
#semilla = 123
tam_poblacion = int(sys.argv[4])

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
    first_sum = np.sum(x**2)
    second_sum = np.sum(np.cos(2*np.pi*x))
    n = x.shape[0]
    return -20*np.exp(-0.2*np.sqrt(first_sum/n)) - np.exp(second_sum/n) + 20 + np.e


#Lista de las funciones a evaluar
funciones_objetivo = [sphere, ackley, rosenbrock]

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

    evaluar = EvolutionStrategyPlus(mu=10, sigma=0.1, objective_func=func_obj, n_iterations=max_iteraciones,semilla=semilla,tam_poblacion=tam_poblacion,dimension=dimension,minimo=limite_inferior,maximo=limite_superior)
    
    x0 = np.random.uniform(limite_inferior,limite_superior,dimension)

    start_time = time.time()
    results = evaluar.run(x0)
    
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
