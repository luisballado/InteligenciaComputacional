import time, os
import argparse, sys

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

# FUZZYLOGIC - https://pypi.org/project/fuzzylogic/
# pip install fuzzylogic
#-------------------------------------------------
from fuzzylogic.classes import Domain, Set, Rule
from fuzzylogic.hedges import very
from fuzzylogic.functions import R, S
#-------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("--show", help="Mostrar la interfaz de SUMO | True - para mostrar | False - para no mostrar")
parser.add_argument("--traffic", help="Modificar la carga de trafico - Bajo | Medio | Alto")
args = parser.parse_args()

#sumoCmd = ["sumo-gui", "-c", "victoria_cluster.sumocfg"]

sumoCmd = []

#levantar sumo
if (args.show == 'True'):
        sumoCmd.append("sumo-gui")
        sumoCmd.append("-c")
        sumoCmd.append("victoria_cluster.sumocfg")
else:
        print("SE MOSTRARA SIN INTERFAZ GRAFICA")
        sumoCmd.append("sumo")
        sumoCmd.append("-c")
        sumoCmd.append("victoria_cluster.sumocfg")
        
if(args.traffic == 'Bajo'):
        sumoCmd.append("-r")
        sumoCmd.append("victoria_cluster_ligero.rou.xml")

if(args.traffic == 'Medio'):
        sumoCmd.append("-r")
        sumoCmd.append("victoria_cluster_medio.rou.xml")

if(args.traffic == 'Alto'):
        sumoCmd.append("-r")
        sumoCmd.append("victoria_cluster_pesado.rou.xml")
        

traci.start(sumoCmd)

#contador de ciclos de semaforos
semaforo = 0

#estado inicial
_siguiente_ = 0

#tiempo de inicio
tiempo = 50 

#cluster a controlar
tfl = "cluster_1387998613_1387998619_1387998643_1387998651" 

#ciclo de semaforo propuesto
trafficsignal = ["GGGGGrrrrrrrrrrrrrrr","yyyyyrrrrrrrrrrrrrrr","rrrrrGGGGGrrrrrrrrrr",
                 "rrrrryyyyyrrrrrrrrrr","rrrrrrrrrrGGGGGrrrrr","rrrrrrrrrryyyyyrrrrr",
                 "rrrrrrrrrrrrrrrGGGGG","rrrrrrrrrrrrrrryyyyy"]
        
pesado = 0
lane_area = ''
nuevo_estado = False

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
        _time_ = 20 #[15,10,15,10,15,10,15,10,15]
        #CALCULAR LA NUEVA SECUENCIA

        #hacer programa para pasarle tiempo pero debe respetar el ciclo del programa
        
        secuencia = trafficsignal[_siguiente_] #inicia con la secuencia [0]
        
        #el tiempo me va decir que debo cambiar estado
        #DEBO PONERLE UNA COLA
        if(semaforo==tiempo):
                #calcular nuevo tiempo y pasar nueva secuencia
                ## CREAR FUZZY LOGIC
                temp  = Domain("Temperature", -80, 80)
                hum   = Domain("Humidity", 0, 100)
                motor = Domain("Speed", 0, 2000)
                
                temp.cold = S(0,20)
                temp.hot = R(15,30)
                
                hum.dry = S(20,50)
                hum.wet = R(40,70)
                
                motor.fast = R(1000,1500)
                motor.slow = ~motor.fast
        
                rules = Rule({(temp.hot, hum.dry): motor.fast,
                              (temp.cold, hum.dry): very(motor.slow),
                              (temp.hot, hum.wet): very(motor.fast),
                              (temp.cold, hum.wet): motor.slow,
                })
                
                values = {hum: 45, temp: 22}
                
                print("*********************rules***************************")
                print(rules(values))
                                
                tiempo = 50
                
                if((len(trafficsignal)-1) <= _siguiente_):
                        _siguiente_ = 0
                else:
                        _siguiente_ = _siguiente_ + 1
                        
                secuencia = trafficsignal[_siguiente_]
                
                semaforo = 0

                if("yyyyy" in secuencia):
                        tiempo = 10
                
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

        print("*******************************************")
        print(trafficsignal)
        print(traci.trafficlight.getPhaseDuration(tflight))
        print(trafficlightduration)
        print("*******************************************")
        
        ##------------------------------------------------------##
        
traci.close() #cerrar interfaz
