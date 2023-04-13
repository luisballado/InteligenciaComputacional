####################################################################
# FUZZYLOGIC - https://pypi.org/project/fuzzylogic/
# pip install fuzzylogic
####################################################################
from fuzzylogic.classes import Domain, Set, Rule
from fuzzylogic.hedges import very
from fuzzylogic.functions import R, S, triangular
####################################################################

class LogicaBorrosa:

    #Dominios
    def __init__(self):
        self.trafico  = Domain("Jam", 0, 100)
        self.espera   = Domain("Waiting", 0, 240)
        self.duracion = Domain("Time", 0, 60)

    #Conjuntos Difusos
    def conjuntos(self):
        self.trafico.bajo  = S(25,50)
        self.trafico.alto  = R(50,75)
        self.trafico.medio = triangular(25, 75)
        
        self.espera.bajo  = S(60,120)
        self.espera.alto  = R(120,240)
        self.espera.medio = triangular(60, 180)
        
        self.duracion.bajo  = S(10,20)
        self.duracion.alto  = R(20,40)
        self.duracion.medio = triangular(10, 30)

    #Reglas de Inferencia
    def inferencia(self,traffic_data,time_data):
        rules = Rule({
            (self.trafico.bajo, self.espera.bajo): self.duracion.bajo,
            (self.trafico.bajo, self.espera.medio): self.duracion.bajo,
            (self.trafico.bajo, self.espera.alto): self.duracion.bajo,
            (self.trafico.medio, self.espera.bajo): self.duracion.medio,
            (self.trafico.medio, self.espera.medio): self.duracion.medio,
            (self.trafico.medio, self.espera.alto): self.duracion.medio,
            (self.trafico.alto, self.espera.bajo): self.duracion.alto,
            (self.trafico.alto, self.espera.medio): self.duracion.alto,
            (self.trafico.alto, self.espera.alto): self.duracion.alto
        })
        
        values = {self.trafico: traffic_data, self.espera: time_data}

        return int(rules(values))
