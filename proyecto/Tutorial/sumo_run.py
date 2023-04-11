import time
import traci
import traci.constants as tc
from random import randrange
from tabulate import tabulate

#-------------------------------------------------
from fuzzylogic.classes import Domain, Set, Rule
from fuzzylogic.hedges import very
from fuzzylogic.functions import R, S
#-------------------------------------------------

#levantar sumo
sumoCmd = ["sumo-gui", "-c", "victoria_cluster.sumocfg"]

traci.start(sumoCmd)

semaforo = 0

#mientras exista un vehiculo la simulacion estata activa
while traci.simulation.getMinExpectedNumber() > 0:
        
        traci.simulationStep()  #simulador paso a paso
        
        #https://sumo.dlr.de/docs/TraCI/Vehicle_Value_Retrieval.html
        # Obtener el listado de los semaforos en el mapa
        # en nuestro ejemplo solo existen dos
        # ('cluster_1387998613_1387998619_1387998643_1387998651', 'joinedS_1387904547_1387904574_8302642379_8302642385')
        # siendo cluster el que nos interesa controlar
        trafficlights = traci.trafficlight.getIDList() 

        # Obtener el listado de las lane areas
        # ('e2_0', 'e2_1', 'e2_2', 'e2_3', 'e2_4', 'e2_5', 'e2_6', 'e2_7')
        detlist = traci.lanearea.getIDList()

        #print([traci.lanearea.getLastStepVehicleNumber(det) for det in detlist])
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
                my_dict[det] = round(porcentaje)

        print(my_dict)
        #Function descriptions
        #https://sumo.dlr.de/docs/TraCI/Traffic_Lights_Value_Retrieval.html#structure_of_compound_object_controlled_links
        #https://sumo.dlr.de/pydoc/traci._trafficlight.html#TrafficLightDomain-setRedYellowGreenState
        # ('cluster_1387998613_1387998619_1387998643_1387998651', 'joinedS_1387904547_1387904574_8302642379_8302642385')
        tflight = traci.trafficlight.getIDList()[0] #tomo el del cluster
        tl_state = traci.trafficlight.getRedYellowGreenState(tflight)
        tl_phase_duration = traci.trafficlight.getPhaseDuration(tflight)
        #tl_lanes_controlled = traci.trafficlight.getControlledLanes(trafficlights[0])
        tl_program = []
        tl_program = traci.trafficlight.getAllProgramLogics(tflight)
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
        print("TLS Program: ", tl_program)
        
        #exit()
        
        ##----------MACHINE LEARNING CODES/FUNCTIONS HERE----------##

        #CALCULAR EL NUEVO TIEMPO
        _time_ = [15,10,15,10,15,10,15,10,15]
        #CALCULAR LA NUEVA SECUENCIA
        '''
        if(semaforo<100):
                secuencia = "GGGGGrrrrrrrrrrrrrrr"
                semaforo = semaforo + 1
        elif(semaforo<130):
                secuencia = "yyyyyrrrrrrrrrrrrrrr"
                semaforo = semaforo + 1
        elif(semaforo<230):
                secuencia = "rrrrrGGGGGrrrrrrrrrr"
                semaforo = semaforo + 1
        elif(semaforo<260):
                secuencia = "rrrrryyyyyrrrrrrrrrr"
                semaforo = semaforo + 1
        else:
                semaforo = 0
        '''
        #["rrrrrrrrrrrrrrrrrrrr", "rrrrrgggggrrrrrggggg", "rrrrrrrrrrrrrrrrrrrr", "rrrrrrrrrrrrrrrrrrrr"]

        
        ##---------------------------------------------------------------##
        
        
        ##----------CONTROL Traffic Lights----------##
        
        #***SET FUNCTION FOR TRAFFIC LIGHTS***
        #REF: https://sumo.dlr.de/docs/TraCI/Change_Traffic_Lights_State.html
        
        trafficlightduration = _time_
        
        trafficsignal = ["GGGGGrrrrrrrrrrrrrrr","yyyyyrrrrrrrrrrrrrrr","rrrrrGGGGGrrrrrrrrrr",
                         "rrrrryyyyyrrrrrrrrrr","rrrrrrrrrrGGGGGrrrrr","rrrrrrrrrryyyyyrrrrr",
                         "rrrrrrrrrrrrrrrGGGGG","rrrrrrrrrrrrrrryyyyy","rrrrrrrrrrrrrrrrrrrr"]

        #trafficsignal = secuencia
        
        tfl = "cluster_1387998613_1387998619_1387998643_1387998651"
        traci.trafficlight.setPhaseDuration(tfl, trafficlightduration[randrange(8)])
        traci.trafficlight.setRedYellowGreenState(tfl, trafficsignal[randrange(8)])
        
        ##------------------------------------------------------##
        
traci.close() #cerrar interfaz
