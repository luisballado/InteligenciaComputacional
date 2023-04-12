import time, os
import argparse, sys
from datetime import datetime

import random

############################################################
#####################CORRER PROGRAMA########################
############################################################
# $ python3 sumo_run.py --show True --traffic Bajo
# $ python3 sumo_run.py --show True --traffic Medio
# $ python3 sumo_run.py --show True --traffic Alto
############################################################

# LIBRERIAS EXTERNAS

# TRACI - https://pypi.org/project/traci/
# pip install traci
#-------------------------------------------------
import traci
import traci.constants as tc
#-------------------------------------------------

# TABULATE - https://pypi.org/project/tabulate/
# pip install tabulate
#-------------------------------------------------
from tabulate import tabulate
#-------------------------------------------------

from logica_borrosa import *

#-----------Manejo de banderas---------------------
# --show True     - Mostrar GUI
# --show False    - Mostrar GUI
# --traffic Bajo  - Flujo bajo de trafico
# --traffic Medio - Flujo medio de trafico
# --traffic Alto  - Flujo alto de trafico
parser = argparse.ArgumentParser()
parser.add_argument("--show", help="Mostrar la interfaz de SUMO | True - para mostrar | False - para no mostrar")
parser.add_argument("--traffic", help="Modificar la carga de trafico - Bajo | Medio | Alto")
args = parser.parse_args()
#-------------------------------------------------

#sumoCmd = ["sumo-gui", "-c", "victoria_cluster.sumocfg"] #Comando directo

sumoCmd = []

#----------------LEVATAR SUMO--------------------------------
if (args.show == 'True'):
        sumoCmd.append("sumo-gui")
        sumoCmd.append("-c")
        sumoCmd.append("victoria_cluster.sumocfg")
else:
        print("SE MOSTRARA SIN INTERFAZ GRAFICA")
        sumoCmd.append("sumo")
        sumoCmd.append("-c")
        sumoCmd.append("victoria_cluster.sumocfg")
#------------------------------------------------------------
        
#----------------DEFINIR TRAFICO-----------------------------------
# Si no se define trafico, se toma el que se encuentra por default 
if(args.traffic == 'Bajo'):
        sumoCmd.append("-r")
        sumoCmd.append("victoria_cluster_ligero.rou.xml")

if(args.traffic == 'Medio'):
        sumoCmd.append("-r")
        sumoCmd.append("victoria_cluster_medio.rou.xml")

if(args.traffic == 'Alto'):
        sumoCmd.append("-r")
        sumoCmd.append("victoria_cluster_pesado.rou.xml")
#------------------------------------------------------------------

traci.start(sumoCmd)

#contador de ciclos de semaforos
semaforo = 0

#estado inicial
_siguiente_ = 0

#valores de trafico
_trafico_ = None

#etiqueta de carriles
carriles = [None,None,None,None]

#tiempo de inicio
#tiempo a consider cuando se inicia el sistema
tiempo = 30 

#cluster a controlar
tfl = "cluster_1387998613_1387998619_1387998643_1387998651" 

# ciclo de semaforo propuesto
# Los cada 5 caracteres es un semafor
# Los semaforos estan ordenados a favor de las manecillas del reloj
trafficsignal = ["GGGGGrrrrrrrrrrrrrrr","yyyyyrrrrrrrrrrrrrrr","rrrrrrrrrrrrrrrrrrrr",
                 "rrrrrGGGGGrrrrrrrrrr","rrrrryyyyyrrrrrrrrrr","rrrrrrrrrrrrrrrrrrrr",
                 "rrrrrrrrrrGGGGGrrrrr","rrrrrrrrrryyyyyrrrrr","rrrrrrrrrrrrrrrrrrrr",
                 "rrrrrrrrrrrrrrrGGGGG","rrrrrrrrrrrrrrryyyyy","rrrrrrrrrrrrrrrrrrrr"
]
        
pesado = 0
lane_area = ''
nuevo_estado = False

fuzzy = LogicaBorrosa()
fuzzy.conjuntos()

#mientras exista un vehiculo la simulacion estata activa
while traci.simulation.getMinExpectedNumber() > 0:
        
        traci.simulationStep()  #simulador paso a paso
        
        #https://sumo.dlr.de/docs/TraCI/Vehicle_Value_Retrieval.html
        # Obtener el listado de los semaforos en el mapa
        # en nuestro ejemplo solo existen dos
        # ('cluster_1387998613_1387998619_1387998643_1387998651', 'joinedS_1387904547_1387904574_8302642379_8302642385')
        # siendo cluster el que nos interesa controlar
        # trafficlights = traci.trafficlight.getIDList() 

        # Obtener el listado de las lane areas
        # ('e2_0', 'e2_1', 'e2_2', 'e2_3', 'e2_4', 'e2_5', 'e2_6', 'e2_7')
        detlist = traci.lanearea.getIDList()
        
        #https://sumo.dlr.de/docs/TraCI/Lane_Area_Detector_Value_Retrieval.html
        #para todos los detectarea e2 hacer
        my_dict = {}
        
        porcentaje_1 = round((((traci.lanearea.getJamLengthMeters('e2_7')/traci.lanearea.getLength('e2_7'))*100) +
                        ((traci.lanearea.getJamLengthMeters('e2_5')/traci.lanearea.getLength('e2_5'))*100)) / 2)
        lane_area_length_1 = (traci.lanearea.getLength('e2_7')+traci.lanearea.getLength('e2_5'))/2 
        jam_meters_1 = max(traci.lanearea.getIntervalMaxJamLengthInMeters('e2_7'),traci.lanearea.getIntervalMaxJamLengthInMeters('e2_5'))
        prom_velocity_1 = ((traci.lanearea.getLastStepMeanSpeed('e2_7'))+(traci.lanearea.getLastStepMeanSpeed('e2_5')))/2
        cars_last_step_1 = ((traci.lanearea.getLastStepVehicleNumber('e2_7'))+(traci.lanearea.getLastStepVehicleNumber('e2_5')))
        cars_in_jam_1 = ((traci.lanearea.getJamLengthVehicle('e2_7'))+(traci.lanearea.getJamLengthVehicle('e2_5')))

        area_lane = [
                ["LANE AREA DETECTOR", 'e2_7 e2_5'],
                ["AREA SENSOR", str(round(lane_area_length_1)) + " m"],
                ["PORCENTAJE LLENO", str(porcentaje_1)+" %"],
                ["JamInMeters", str(round(jam_meters_1,2))],
                ["VELOCIDAD PROMEDIO", str(prom_velocity_1)+" m/s"],
                ["#CARROS(LASTSTEP)", str(cars_last_step_1)],
                ["#CARROS (TRAFICO): ", str(cars_in_jam_1)]
        ]

        print('****************************LANE************************************')
        print(tabulate(area_lane))
        print('********************************************************************')
                
        porcentaje_2 = round((((traci.lanearea.getJamLengthMeters('e2_2')/traci.lanearea.getLength('e2_2'))*100) +
                        ((traci.lanearea.getJamLengthMeters('e2_0')/traci.lanearea.getLength('e2_0'))*100)) / 2)
        lane_area_length_2 = (traci.lanearea.getLength('e2_2')+traci.lanearea.getLength('e2_0'))/2 
        jam_meters_2 = max(traci.lanearea.getIntervalMaxJamLengthInMeters('e2_2'),traci.lanearea.getIntervalMaxJamLengthInMeters('e2_0'))
        prom_velocity_2 = ((traci.lanearea.getLastStepMeanSpeed('e2_2'))+(traci.lanearea.getLastStepMeanSpeed('e2_0')))/2
        cars_last_step_2 = ((traci.lanearea.getLastStepVehicleNumber('e2_2'))+(traci.lanearea.getLastStepVehicleNumber('e2_0')))
        cars_in_jam_2 = ((traci.lanearea.getJamLengthVehicle('e2_2'))+(traci.lanearea.getJamLengthVehicle('e2_0')))

        area_lane = [
                ["LANE AREA DETECTOR", 'e2_2 e2_0'],
                ["AREA SENSOR", str(round(lane_area_length_2)) + " m"],
                ["PORCENTAJE LLENO", str(porcentaje_2)+" %"],
                ["JamInMeters", str(round(jam_meters_2,2))],
                ["VELOCIDAD PROMEDIO", str(prom_velocity_2)+" m/s"],
                ["#CARROS(LASTSTEP)", str(cars_last_step_2)],
                ["#CARROS (TRAFICO): ", str(cars_in_jam_2)]
        ]

        print('****************************LANE************************************')
        print(tabulate(area_lane))
        print('********************************************************************')
        
        porcentaje_3 = round((((traci.lanearea.getJamLengthMeters('e2_6')/traci.lanearea.getLength('e2_6'))*100) +
                        ((traci.lanearea.getJamLengthMeters('e2_4')/traci.lanearea.getLength('e2_4'))*100)) / 2)
        lane_area_length_3 = (traci.lanearea.getLength('e2_6')+traci.lanearea.getLength('e2_4'))/2 
        jam_meters_3 = max(traci.lanearea.getIntervalMaxJamLengthInMeters('e2_6'),traci.lanearea.getIntervalMaxJamLengthInMeters('e2_4'))
        prom_velocity_3 = ((traci.lanearea.getLastStepMeanSpeed('e2_6'))+(traci.lanearea.getLastStepMeanSpeed('e2_4')))/2
        cars_last_step_3 = ((traci.lanearea.getLastStepVehicleNumber('e2_6'))+(traci.lanearea.getLastStepVehicleNumber('e2_4')))
        cars_in_jam_3 = ((traci.lanearea.getJamLengthVehicle('e2_6'))+(traci.lanearea.getJamLengthVehicle('e2_4')))

        area_lane = [
                ["LANE AREA DETECTOR", 'e2_6 e2_4'],
                ["AREA SENSOR", str(round(lane_area_length_3)) + " m"],
                ["PORCENTAJE LLENO", str(porcentaje_3)+" %"],
                ["JamInMeters", str(round(jam_meters_3,2))],
                ["VELOCIDAD PROMEDIO", str(prom_velocity_3)+" m/s"],
                ["#CARROS(LASTSTEP)", str(cars_last_step_3)],
                ["#CARROS (TRAFICO): ", str(cars_in_jam_3)]
        ]

        print('****************************LANE************************************')
        print(tabulate(area_lane))
        print('********************************************************************')
        
        porcentaje_4 = round((((traci.lanearea.getJamLengthMeters('e2_1')/traci.lanearea.getLength('e2_1'))*100) +((traci.lanearea.getJamLengthMeters('e2_3')/traci.lanearea.getLength('e2_3'))*100)) / 2)
        lane_area_length_4 = (traci.lanearea.getLength('e2_1')+traci.lanearea.getLength('e2_3'))/2 
        jam_meters_4 = max(traci.lanearea.getIntervalMaxJamLengthInMeters('e2_1'),traci.lanearea.getIntervalMaxJamLengthInMeters('e2_3'))
        prom_velocity_4 = ((traci.lanearea.getLastStepMeanSpeed('e2_1'))+(traci.lanearea.getLastStepMeanSpeed('e2_3')))/2
        cars_last_step_4 = ((traci.lanearea.getLastStepVehicleNumber('e2_1'))+(traci.lanearea.getLastStepVehicleNumber('e2_3')))
        cars_in_jam_4 = ((traci.lanearea.getJamLengthVehicle('e2_1'))+(traci.lanearea.getJamLengthVehicle('e2_3')))

        area_lane = [
                ["LANE AREA DETECTOR", 'e2_1 e2_3'],
                ["AREA SENSOR", str(round(lane_area_length_4)) + " m"],
                ["PORCENTAJE LLENO", str(porcentaje_4)+" %"],
                ["JamInMeters", str(round(jam_meters_4,2))],
                ["VELOCIDAD PROMEDIO", str(prom_velocity_4)+" m/s"],
                ["#CARROS(LASTSTEP)", str(cars_last_step_4)],
                ["#CARROS (TRAFICO): ", str(cars_in_jam_4)]
        ]

        print('****************************LANE************************************')
        print(tabulate(area_lane))
        print('********************************************************************')
                        
        """
        for det in detlist:

                # Calcular el procentaje real de llenado
                porcentaje =  (traci.lanearea.getJamLengthMeters(det)/traci.lanearea.getLength(det))*100 
                lane_area_length = traci.lanearea.getLength(det)
                jam_meters = traci.lanearea.getIntervalMaxJamLengthInMeters(det)
                prom_velocity = traci.lanearea.getLastStepMeanSpeed(det)
                cars_last_step = traci.lanearea.getLastStepVehicleNumber(det)
                cars_in_jam = traci.lanearea.getJamLengthVehicle(det)

                
                if((porcentaje > 0) and (pesado <= porcentaje)):
                        nuevo_estado = True
                        pesado = porcentaje
                        lane_area = det
                else:
                        lane_area = det
                        pesado = porcentaje
                        nuevo_estado = False
                
                area_lane = [
                        ["LANE AREA DETECTOR", det],
                        ["AREA SENSOR", str(round(lane_area_length)) + " m"],
                        ["PORCENTAJE LLENO", str(round(porcentaje))+" %"],
                        ["JamInMeters", str(round(jam_meters,2))],
                        ["VELOCIDAD PROMEDIO", str(prom_velocity)+" m/s"],
                        ["#CARROS(LASTSTEP)", str(cars_last_step)],
                        ["#CARROS (TRAFICO): ", str(cars_in_jam)]
                ]
                
                print(tabulate(area_lane))
        """
        ######################################
        ## SABER QUE CARRIL SE LLENO PRIMERO
        ######################################
        # PARA TENER UNA COLA
        ######################################
        
        #Evaluar en un tiempo que 
        if(pesado>0):
                print("Ciclos: " + str(semaforo))
                print("el pesado es: " + lane_area + " con:" + str(pesado))
                #exit()
        
        #Function descriptions
        #https://sumo.dlr.de/docs/TraCI/Traffic_Lights_Value_Retrieval.html#structure_of_compound_object_controlled_links
        #https://sumo.dlr.de/pydoc/traci._trafficlight.html#TrafficLightDomain-setRedYellowGreenState
        # ('cluster_1387998613_1387998619_1387998643_1387998651', 'joinedS_1387904547_1387904574_8302642379_8302642385')
        tflight = traci.trafficlight.getIDList()[0] #tomo el del cluster
        tl_state = traci.trafficlight.getRedYellowGreenState(tflight)  #tomar estado actual del semaforo
        tl_phase_duration = traci.trafficlight.getPhaseDuration(tflight) #tomar el tiempo actual del semaforo
        #tl_lanes_controlled = traci.trafficlight.getControlledLanes(trafficlights[0])
        #tl_program = []
        #tl_program = traci.trafficlight.getAllProgramLogics(tflight)
        tl_next_switch = traci.trafficlight.getNextSwitch(tflight)
        
        traffic_lights = [
                ["CLUSTER",tflight],
                #Returns the named tl's state as a tuple of light definitions from rRgGyYoO, for red, green, yellow, off, where lower case letters mean that the stream has to decelerate
                ["TL state",tl_state],
                #Returns the default total duration of the currently active phase in seconds; To obtain the
                #remaining duration use (getNextSwitch() - simulation.getTime()); to obtain the spent duration
                #subtract the remaining from the total duration
                ["TLS phase duration", tl_phase_duration],
                #Returns the assumed time (in seconds) at which the tls changes the phase. Please note that
                #the time to switch is not relative to current simulation step (the result returned by the query
                #will be absolute time, counting from simulation start);
                #to obtain relative time, one needs to subtract current simulation time from the
                #result returned by this query. Please also note that the time may vary in the case of
                #actuated/adaptive traffic lights
                ["Next TLS switch", tl_next_switch]
        ]

        print(tabulate(traffic_lights))

        #Returns the complete traffic light program, structure described under data types
        #print("TLS Program: ", tl_program)

        ##----------MACHINE LEARNING CODES/FUNCTIONS HERE----------##
                
        #CALCULAR EL NUEVO TIEMPO
        #_time_ = 20

        #CALCULAR LA NUEVA SECUENCIA
        
        #inicia con la primer secuencia [0]
        secuencia = trafficsignal[_siguiente_]
        
        #el tiempo me va decir que debo cambiar estado
        #DEBO PONERLE UNA COLA
        if(semaforo==tiempo):
                #calcular nuevo tiempo y pasar nueva secuencia

                #/////////////////////////////////////////////////////////
                # SABER QUE TRAFICO TIENE EL SIGUIENTE
                #/////////////////////////////////////////////////////////

                espera = 0
                ahora = datetime.now()
                
                if(_siguiente_ == 0):
                        #modificar el tiempo del carril 0
                        #ver si ya pase por aqui, si no poner el datetime actual
                        _trafico_ = porcentaje_1
                        
                        if(carriles[0] is None):
                                carriles[0] = ahora
                        else:
                                espera = (ahora - carriles[0]).seconds
                                carriles[0] = ahora

                                print("######ESPERA#######")
                                print(ahora)
                                print(carriles[0])
                                print("carril: " + str(_siguiente_) + " tiempo: " + str(espera))
                                print("######ESPERA#######")

                elif(_siguiente_ == 3):
                        #modificar el tiempo del carril 3
                        _trafico_ = porcentaje_2
                        if(carriles[1] is None):
                                carriles[1] = ahora
                        else:
                                espera = (ahora - carriles[1]).seconds
                                carriles[1] = ahora

                                print("######ESPERA#######")
                                print(ahora)
                                print(carriles[0])
                                print("carril: " + str(_siguiente_) + " tiempo: " + str(espera))
                                print("######ESPERA#######")
                        
                elif(_siguiente_ == 6):
                        #modificar el tiempo del carril 6
                        _trafico_ = porcentaje_3
                        if(carriles[2] is None):
                                carriles[2] = ahora
                        else:
                                espera = (ahora - carriles[2]).seconds
                                carriles[2] = ahora

                                print("######ESPERA#######")
                                print(ahora)
                                print(carriles[0])
                                print("carril: " + str(_siguiente_) + " tiempo: " + str(espera))
                                print("######ESPERA#######")
                                

                elif(_siguiente_ == 9):
                        #modificar el tiempo del carril 9
                        _trafico_ = porcentaje_4
                        if(carriles[3] is None):
                                carriles[3] = ahora
                        else:
                                espera = (ahora - carriles[3]).seconds
                                carriles[3] = ahora

                                print("######ESPERA#######")
                                print(ahora)
                                print(carriles[0])
                                print("carril: " + str(_siguiente_) + " tiempo: " + str(espera))
                                print("######ESPERA#######")

                
                
                ## CREAR FUZZY LOGIC
                tiempo = fuzzy.inferencia(tiempo,20)
                
                print("*********************rules***************************")
                print(str(tiempo))
                
                if((len(trafficsignal)-1) <= _siguiente_):
                        _siguiente_ = 0
                else:
                        _siguiente_ = _siguiente_ + 1
                        
                secuencia = trafficsignal[_siguiente_]

                semaforo = 0                
                
                #PONER BARRERAS DE TIEMPO PARA AMARILLO Y ROJO
                if("yyyyy" in secuencia or "rrrrrrrrrrrrrrrrrrrr" in secuencia):
                        tiempo = 5

        #alguien que cuente y me diga cuando cambiar de secuencia con el tiempo mas reciente
        traci.trafficlight.setPhaseDuration(tfl, tiempo)
        traci.trafficlight.setRedYellowGreenState(tfl, secuencia)
                
        #conocer el siguiente estado
        semaforo = semaforo + 1
        
        ##---------------------------------------------------------------##
        ##----------CONTROL Traffic Lights----------##
        
        #***SET FUNCTION FOR TRAFFIC LIGHTS***
        #REF: https://sumo.dlr.de/docs/TraCI/Change_Traffic_Lights_State.html

        trafficlightduration = tiempo

        print("##############################################")
        print(trafficsignal)
        print(traci.trafficlight.getPhaseDuration(tflight))
        print(trafficlightduration)
        print("##############################################")
                
        ##------------------------------------------------------##
        
traci.close() #cerrar interfaz
