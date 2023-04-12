####################################################################
# FUZZYLOGIC - https://pypi.org/project/fuzzylogic/
# pip install fuzzylogic
####################################################################
from fuzzylogic.classes import Domain, Set, Rule
from fuzzylogic.hedges import very
from fuzzylogic.functions import R, S, triangular
####################################################################
import argparse

############ PRUEBA DE CONCEPTO ####################################
# EJECUTAR:
# $ python3 fuzzy_example_docu.py --traffic 10 --time 300
# -- traffic : porcentaje de trafico respecto a area sensada
# -- time    : tiempo desde la ultima vez que participo el semaforo
####################################################################

parser = argparse.ArgumentParser()
parser.add_argument("--traffic",help="carga de trafico")
parser.add_argument("--time",help="tiempo en liberar carga")
args = parser.parse_args()

trafico  = Domain("Jam", 0, 100)
espera   = Domain("Waiting", 0, 240)
duracion = Domain("Time", 0, 60)

trafico.bajo  = S(25,50)
trafico.alto  = R(50,75)
trafico.medio = triangular(25, 75)

espera.bajo  = S(60,120)
espera.alto  = R(120,240)
espera.medio = triangular(60, 180)

duracion.bajo  = S(15,30)
duracion.alto  = R(30,60)
duracion.medio = triangular(15, 45)

rules = Rule({
    (trafico.bajo, espera.bajo): duracion.bajo,
    (trafico.bajo, espera.medio): duracion.bajo,
    (trafico.bajo, espera.alto): duracion.bajo,
    (trafico.medio, espera.bajo): duracion.medio,
    (trafico.medio, espera.medio): duracion.medio,
    (trafico.medio, espera.alto): duracion.medio,
    (trafico.alto, espera.bajo): duracion.alto,
    (trafico.alto, espera.medio): duracion.alto,
    (trafico.alto, espera.alto): duracion.alto
})

values = {trafico: int(args.traffic), espera: int(args.time)}

print("tiempo semaforo->> " + str(rules(values)))
