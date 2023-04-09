import traci
import traci.constants as tc
import pytz #time
import datetime
from random import randrange

#levantar sumo
sumoCmd = ["sumo-gui", "-c", "victoria_cluster.sumocfg"]

traci.start(sumoCmd)

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
        for det in detlist:
                print("######################################################################")
                # Returns Area Detector ID and returns the length of the detector in meters.
                print("LANE AREA DETECTOR: " + det + " | " + "AREA SENSOR: " + str(round(traci.lanearea.getLength(det))) + " m")
                #--------------------------------------------------------------------------------------------------------
                # Calcular el procentaje real de llenado
                porcentaje =  (traci.lanearea.getJamLengthMeters(det)/traci.lanearea.getLength(det))*100
                print("PORCENTAJE LLENO: " + str(round(porcentaje)) + " %" + " | " + "JamInMeters: " + str(round(traci.lanearea.getIntervalMaxJamLengthInMeters(det),2)) + " | " + "VELOCIDAD PROMEDIO: " + str(traci.lanearea.getLastStepMeanSpeed(det)) + " m/s")
                # --------------------------------------------------------------------------------------------------------
                print("---------------------------------------------------")                        
                print("#CARROS (LASTSTEP): " + str(traci.lanearea.getLastStepVehicleNumber(det)) + " | " + "#CARROS (TRAFICO): " + str(traci.lanearea.getJamLengthVehicle(det))) # Returns the number of vehicles which were halting during the last time step
                print("---------------------------------------------------")
                                
        tlsList = []
                
        #Function descriptions
        #https://sumo.dlr.de/docs/TraCI/Traffic_Lights_Value_Retrieval.html#structure_of_compound_object_controlled_links
        #https://sumo.dlr.de/pydoc/traci._trafficlight.html#TrafficLightDomain-setRedYellowGreenState
        
        tflight = trafficlights[0]
        tl_state = traci.trafficlight.getRedYellowGreenState(trafficlights[0])
        tl_phase_duration = traci.trafficlight.getPhaseDuration(trafficlights[0])
        tl_lanes_controlled = traci.trafficlight.getControlledLanes(trafficlights[0])
        tl_program = []
        #tl_program = traci.trafficlight.getCompleteRedYellowGreenDefinition(trafficlights[k])
        tl_next_switch = traci.trafficlight.getNextSwitch(trafficlights[0])
        
        #Packing of all the data for export to CSV/XLSX
        tlsList = [tflight, tl_state, tl_phase_duration, tl_lanes_controlled, tl_program, tl_next_switch]
        
        print(trafficlights[0], " --->", \
              #Returns the named tl's state as a tuple of light definitions from rRgGyYoO, for red,
              #green, yellow, off, where lower case letters mean that the stream has to decelerate
              " TL state: ", traci.trafficlight.getRedYellowGreenState(trafficlights[0]), "\n" \
              #Returns the default total duration of the currently active phase in seconds; To obtain the
              #remaining duration use (getNextSwitch() - simulation.getTime()); to obtain the spent duration
              #subtract the remaining from the total duration
              " TLS phase duration: ", traci.trafficlight.getPhaseDuration(trafficlights[0]), "\n" \
              #Returns the list of lanes which are controlled by the named traffic light. Returns at least
              #one entry for every element of the phase state (signal index)                                
              " Lanes controlled: ", traci.trafficlight.getControlledLanes(trafficlights[0]), "\n", \
              #Returns the complete traffic light program, structure described under data types                                      
              " TLS Program: ", traci.trafficlight.getCompleteRedYellowGreenDefinition(trafficlights[0]), "\n"
              #Returns the assumed time (in seconds) at which the tls changes the phase. Please note that
              #the time to switch is not relative to current simulation step (the result returned by the query
              #will be absolute time, counting from simulation start);
              #to obtain relative time, one needs to subtract current simulation time from the
              #result returned by this query. Please also note that the time may vary in the case of
              #actuated/adaptive traffic lights
              " Next TLS switch: ", traci.trafficlight.getNextSwitch(trafficlights[0]))
        
        ##----------MACHINE LEARNING CODES/FUNCTIONS HERE----------##

        #CALCULAR EL NUEVO TIEMPO
        time = [40,40,40,40]
        #CALCULAR LA NUEVA SECUENCIA
        secuencia = ["rrrrrrrrrrrrrrrrrrrr", "rrrrrgggggrrrrrggggg", "rrrrrrrrrrrrrrrrrrrr", "rrrrrrrrrrrrrrrrrrrr"]
        
        ##---------------------------------------------------------------##
        
        
        ##----------CONTROL Traffic Lights----------##
        
        #***SET FUNCTION FOR TRAFFIC LIGHTS***
        #REF: https://sumo.dlr.de/docs/TraCI/Change_Traffic_Lights_State.html
        
        trafficlightduration = time
        
        #trafficsignal = ["rrrrrGGGggrrrrrGGGgg", "rrrrryyyyyrrrrryyyyy", "GGGggrrrrrGGGggrrrrr", "yyyyyrrrrryyyyyrrrrr"]
        #trafficsignal = ["rrrrrGGGggrrrrrGGGgg", "rrrrryyyyyrrrrryyyyy", "rrrrrrrrrrrrrrrrrrrr", "rrrrrrrrrrrrrrrrrrrr"]
        trafficsignal = secuencia
        
        tfl = "cluster_1387998613_1387998619_1387998643_1387998651"
        traci.trafficlight.setPhaseDuration(tfl, trafficlightduration[randrange(4)])
        traci.trafficlight.setRedYellowGreenState(tfl, trafficsignal[randrange(4)])
        
        ##------------------------------------------------------##
        
traci.close() #cerrar interfaz
