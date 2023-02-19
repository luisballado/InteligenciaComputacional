import numpy as np
from abc import ABC, abstractmethod
import random

class EvolutionStrategy(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def generate_population(self):
        pass
    
    @abstractmethod
    def run(self):
        pass

class EvolutionStrategyPlus(EvolutionStrategy):

    def __init__(self, mu, sigma, objective_func, n_iterations,semilla,tam_poblacion,dimension,minimo,maximo):
        self.mu = mu
        self.sigma = sigma
        self.objective_func = objective_func
        self.n_iterations = n_iterations
        self.best_solution = None
        self.semilla = semilla
        self.tam_poblacion = tam_poblacion
        self.dimension = dimension
        self.minimo = minimo
        self.maximo = maximo
        
    def generate_population(self):
        if self.semilla != None:
            random.seed(self.semilla)
            np.random.seed(self.semilla)
        poblacion = []
        #se crea la poblacion
        for i in range(self.dimension):
            individuo = np.array([random.uniform(self.minimo,self.maximo) for j in range(self.dimension)])
            poblacion.append(individuo)
        return poblacion
        
    def run(self):

        #crear poblacion
        poblacion = np.random.uniform(self.minimo,self.maximo,self.dimension)
        
        if(self.semilla != None):
            np.random.seed(int(self.semilla))
        
        for iteration in range(self.n_iterations):
            solutions = np.random.normal(poblacion, self.sigma, (self.mu, poblacion.shape[0]))
            objectives = [self.objective_func(solution) for solution in solutions]
            best_solution = solutions[np.argmin(objectives)]
            if self.best_solution is None or self.objective_func(best_solution) < self.objective_func(self.best_solution):
                self.best_solution = best_solution
            poblacion = best_solution
        return self.best_solution

class EvolutionStrategyComma(EvolutionStrategy):

    def __init__(self, mu, sigma, objective_func, n_iterations,semilla):
        self.mu = mu
        self.sigma = sigma
        self.objective_func = objective_func
        self.n_iterations = n_iterations
        self.best_solution = None
        self.semilla = semilla
        self.tam_poblacion = tam_poblacion
        self.dimension = dimension
        self.minimo = minimo
        self.maximo = maximo
        
    def generate_population(self):
        if self.semilla != None:
            random.seed(self.semilla)
        poblacion = []
        #se crea la poblacion
        for i in range(self.tam_poblacion):
            individuo = np.array([random.uniform(self.minimo,self.maximo) for j in range(self.dimension)])
            poblacion.append(individuo)
        return poblacion
        
    def run(self, x0):
        if(self.semilla != None):
            np.random.seed(int(self.semilla))
        for iteration in range(self.n_iterations):
            solutions = np.random.normal(x0, self.sigma, (self.mu, x0.shape[0]))
            objectives = [self.objective_func(solution) for solution in solutions]
            sorted_solutions = solutions[np.argsort(objectives)]
            x0 = np.mean(sorted_solutions[:self.mu//2], axis=0)
            if self.best_solution is None or self.objective_func(x0) < self.objective_func(self.best_solution):
                self.best_solution = x0
        return self.best_solution
