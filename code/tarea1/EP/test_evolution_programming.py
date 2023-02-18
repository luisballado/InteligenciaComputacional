import time #para las metricas de tiempo
import numpy as np #importar numpy para el manejo de vectores
import sys #para acceso de datos como argumentos

#Clase que engloba Programacion Evolutiva
from ProgramacionEvolutiva import *

# python3.10 test_evolution_programming.py 1000 21 1234 10 4

#max_iter = 100000
#tam_poblacion = 21
#_semilla_ = sys.argv[1]
#dimension = 10
#num_torneos = 4

max_iter = int(sys.argv[1])
tam_poblacion = int(sys.argv[2])
_semilla_ = int(sys.argv[3])
dimension = int(sys.argv[4])
num_torneos = int(sys.argv[5])

###################ESFERA###########################
#regresar la sumatoria del vector de entrada
def sphere(x):
    return np.sum(np.power(x,2))

####################ACKLEY######################
#se le pasa una lista de x
def ackley(x):
    first_sum = np.sum(x**2)
    second_sum = np.sum(np.cos(2*np.pi*x))
    n = float(len(x))
    return -20*np.exp(-0.2*np.sqrt(first_sum/n)) - np.exp(second_sum/n) + 20 + np.exp(1)

###################ROSENBROCK###################################
#se le pasa una lista con dos valores para las xs
#x[1:]  - el ultimo en la lista
#x[:-1] - el primero en la lista
def rosenbrock(x):
    return np.sum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)


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

    evaluar = EvolutionProgramming(dimension=dimension,tam_poblacion=tam_poblacion,max_iter=max_iter,minimo=limite_inferior,maximo=limite_superior,funcion=func_obj,semilla=_semilla_,num_torneos=num_torneos)

    start_time = time.time()
    poblacion = evaluar.generate_population()
    results = evaluar.evolucionar(poblacion)
    
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
