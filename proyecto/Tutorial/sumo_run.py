import traci
#import time
import traci.constants as tc
import pytz #time
import datetime
from random import randrange

#Sacar tiempo
def getdatetime():
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        currentDT = utc_now.astimezone(pytz.timezone("America/Monterrey"))
        DATIME = currentDT.strftime("%d-%m-%Y %H:%M:%S")

        return DATIME

#levantar sumo
#COMANDO -c ARCHIVO
sumoCmd = ["sumo-gui", "-c", "victoria_cluster.sumocfg"]

traci.start(sumoCmd)

#comenzar simulacion cuando hasta que llegue un vehiculo
while traci.simulation.getMinExpectedNumber() > 0:
        
        traci.simulationStep();

        #https://sumo.dlr.de/docs/TraCI/Vehicle_Value_Retrieval.html
        trafficlights=traci.trafficlight.getIDList();
        detlist = traci.lanearea.getIDList()
        vehicles=traci.vehicle.getIDList();
        """
        
        
        
        #para todos los carros en el simulador

        for i in range(0,len(vehicles)):
                
                #Function descriptions
                #https://sumo.dlr.de/docs/TraCI/Vehicle_Value_Retrieval.html
                #https://sumo.dlr.de/pydoc/traci._vehicle.html#VehicleDomain-getSpeed
                vehid = vehicles[i]
                x, y = traci.vehicle.getPosition(vehicles[i])
                coord = [x, y]
                lon, lat = traci.simulation.convertGeo(x, y)
                gpscoord = [lon, lat]
                spd = round(traci.vehicle.getSpeed(vehicles[i])*3.6,2)
                edge = traci.vehicle.getRoadID(vehicles[i])
                lane = traci.vehicle.getLaneID(vehicles[i])
                displacement = round(traci.vehicle.getDistance(vehicles[i]),2)
                turnAngle = round(traci.vehicle.getAngle(vehicles[i]),2)
                nextTLS = traci.vehicle.getNextTLS(vehicles[i])
                
                #Packing of all the data for export to CSV/XLSX
                #vehList = [getdatetime(), vehid, coord, gpscoord, spd, edge, lane, displacement, turnAngle, nextTLS]
                
                print("######################################################################")
                print("Vehicle: ", vehicles[i], " at datetime: ", getdatetime())
                print("CO2Emission ", vehicles[i], ": ", traci.vehicle.getCO2Emission(vehicles[i])," mg/s")
                
                print(vehicles[i], " >>> Position: ", coord, "\nGPS Position: ", gpscoord,\
                      "\nSpeed: ", round(traci.vehicle.getSpeed(vehicles[i])*3.6,2), "km/h", \
                      #Returns the id of the edge the named vehicle was at within the last step.
                      " \nEdgeID of veh: ", traci.vehicle.getRoadID(vehicles[i]),\
                      #Returns the id of the lane the named vehicle was at within the last step.
                      " \nLaneID of veh: ", traci.vehicle.getLaneID(vehicles[i]), \
                      #Returns the distance to the starting point like an odometer.
                      " \nDistance: ", round(traci.vehicle.getDistance(vehicles[i]),2), "m", \
                      #Returns the angle in degrees of the named vehicle within the last step.
                      " \nVehicle orientation: ", round(traci.vehicle.getAngle(vehicles[i]),2), "deg", \
                      #Return list of upcoming traffic lights [(tlsID, tlsIndex, distance, state), ...]
                      " \nUpcoming traffic lights: ", traci.vehicle.getNextTLS(vehicles[i]), \
                )
                """
        
                
                #print([traci.lanearea.getLastStepVehicleNumber(det) for det in detlist])
                #https://sumo.dlr.de/docs/TraCI/Lane_Area_Detector_Value_Retrieval.html
        for det in detlist:
                print("######################################################################")
                print("LANE AREA DETECTOR: " + det)
                # --------------------------------------------------------------------------------------------------------
                # Returns the ID of the lane the detector is placed at.
                print("LaneID : " + traci.lanearea.getLaneID(det))
                # --------------------------------------------------------------------------------------------------------
                # Returns the length of the detector in meters.
                print("Length: " + str(traci.lanearea.getLength(det)) + "m")
                # --------------------------------------------------------------------------------------------------------
                # Returns the number of lane area detectors within the scenario (the given DetectorID is ignored)
                print("ID Count: " + str(traci.lanearea.getIDCount))
                # --------------------------------------------------------------------------------------------------------
                # Returns the starting position of the detector at it's lane, counted from the lane's begin, in meters.
                print("Position: " + str(traci.lanearea.getPosition(det)))
                # --------------------------------------------------------------------------------------------------------
                # Returns the mean speed of vehicles that have been within the named area detector within the last simulation step [m/s]
                print("LastStepMeanSpeed: " + str(traci.lanearea.getLastStepMeanSpeed(det)))
                # --------------------------------------------------------------------------------------------------------
                # Returns the list of ids of vehicles that have been within the detector in the last simulation step
                print("VehicleIDs : " + str(traci.lanearea.getLastStepVehicleIDs(det)))
                # --------------------------------------------------------------------------------------------------------
                # Returns the percentage of space the detector was occupied by a vehicle [%]
                print("LastStepOccupancy : " + str(traci.lanearea.getLastStepOccupancy(det))+"%")
                # --------------------------------------------------------------------------------------------------------
                # Returns the number of vehicles which were halting during the last time step
                print("JamVehicle: " + str(traci.lanearea.getJamLengthVehicle(det)))
                # --------------------------------------------------------------------------------------------------------
                # Returns the length of the jam in meters
                print("JamLengthMeters: " + str(traci.lanearea.getJamLengthMeters(det)))
                # --------------------------------------------------------------------------------------------------------
                # The average percentage of the detector length that was occupied by a vehicle during the current interval
                print("IntervalOccupancy: " + str(traci.lanearea.getIntervalOccupancy(det))+"%")
                # --------------------------------------------------------------------------------------------------------
                # The average (time mean) speed of vehicles during the current interval
                print("IntervalMeanSpeed: " + str(traci.lanearea.getIntervalMeanSpeed(det)))
                # --------------------------------------------------------------------------------------------------------
                # The number of vehicles (or persons, if so configured) that passed the detector during the current interval
                print("IntervalVehicleNumber: " + str(traci.lanearea.getIntervalVehicleNumber(det)))
                # --------------------------------------------------------------------------------------------------------
                # The maximum jam length in meters during the current interval
                print("JamInMeters: " + str(traci.lanearea.getIntervalMaxJamLengthInMeters(det)))
                # --------------------------------------------------------------------------------------------------------
                # The number of vehicles (or persons, if so configured) that passed the detector during the previous interval
                print("IntervalVehicleNumber: " + str(traci.lanearea.getLastIntervalVehicleNumber(det)))
                # --------------------------------------------------------------------------------------------------------
                # The maximum jam length in meters during the previous interval
                print("LastIntervalVehicleNumber: " + str(traci.lanearea.getLastIntervalMaxJamLengthInMeters(det)))
                # --------------------------------------------------------------------------------------------------------
                print("---------------------------------------------------")                        
                print("CARROS EN ZONA ultimo paso: " + str(traci.lanearea.getLastStepVehicleNumber(det)))
                print("###################################################")                        
                
                
                """
                print("$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%$")
                IDsOfEdges = traci.edge.getIDList();
                print("IDs of the edges:", IDsOfEdges)
                print("$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%$")
                IDsOfJunctions = traci.junction.getIDList();
                print("IDs of the edges:", IDsOfJunctions)
                """
                
                #idd = traci.vehicle.getLaneID(vehicles[i])
                
                tlsList = []
                
                for k in range(0,len(trafficlights)):
                        
                        #Function descriptions
                        #https://sumo.dlr.de/docs/TraCI/Traffic_Lights_Value_Retrieval.html#structure_of_compound_object_controlled_links
                        #https://sumo.dlr.de/pydoc/traci._trafficlight.html#TrafficLightDomain-setRedYellowGreenState
                        
                        #if idd in traci.trafficlight.getControlledLanes(trafficlights[k]):
                                
                                tflight = trafficlights[k]
                                tl_state = traci.trafficlight.getRedYellowGreenState(trafficlights[k])
                                tl_phase_duration = traci.trafficlight.getPhaseDuration(trafficlights[k])
                                tl_lanes_controlled = traci.trafficlight.getControlledLanes(trafficlights[k])
                                tl_program = []
                                #tl_program = traci.trafficlight.getCompleteRedYellowGreenDefinition(trafficlights[k])
                                tl_next_switch = traci.trafficlight.getNextSwitch(trafficlights[k])
                                
                                #Packing of all the data for export to CSV/XLSX
                                tlsList = [tflight, tl_state, tl_phase_duration, tl_lanes_controlled, tl_program, tl_next_switch]
                                
                                print(trafficlights[k], " --->", \
                                      #Returns the named tl's state as a tuple of light definitions from rRgGyYoO, for red,
                                      #green, yellow, off, where lower case letters mean that the stream has to decelerate
                                      " TL state: ", traci.trafficlight.getRedYellowGreenState(trafficlights[k]), "\n" \
                                      #Returns the default total duration of the currently active phase in seconds; To obtain the
                                      #remaining duration use (getNextSwitch() - simulation.getTime()); to obtain the spent duration
                                      #subtract the remaining from the total duration
                                      " TLS phase duration: ", traci.trafficlight.getPhaseDuration(trafficlights[k]), "\n" \
                                      #Returns the list of lanes which are controlled by the named traffic light. Returns at least
                                      #one entry for every element of the phase state (signal index)                                
                                      " Lanes controlled: ", traci.trafficlight.getControlledLanes(trafficlights[k]), "\n", \
                                      #Returns the complete traffic light program, structure described under data types                                      
                                      " TLS Program: ", traci.trafficlight.getCompleteRedYellowGreenDefinition(trafficlights[k]), "\n"
                                      #Returns the assumed time (in seconds) at which the tls changes the phase. Please note that
                                      #the time to switch is not relative to current simulation step (the result returned by the query
                                      #will be absolute time, counting from simulation start);
                                      #to obtain relative time, one needs to subtract current simulation time from the
                                      #result returned by this query. Please also note that the time may vary in the case of
                                      #actuated/adaptive traffic lights
                                      " Next TLS switch: ", traci.trafficlight.getNextSwitch(trafficlights[k]))
                                
                                
                ##----------MACHINE LEARNING CODES/FUNCTIONS HERE----------##


                ##---------------------------------------------------------------##


                ##----------CONTROL Traffic Lights----------##

                #***SET FUNCTION FOR TRAFFIC LIGHTS***
                #REF: https://sumo.dlr.de/docs/TraCI/Change_Traffic_Lights_State.html
                
                trafficlightduration = [5,37,5,35]
                
                trafficsignal = ["rrrrrGGGggrrrrrGGGgg", "rrrrryyyyyrrrrryyyyy", "GGGggrrrrrGGGggrrrrr", "yyyyyrrrrryyyyyrrrrr"]
                
                tfl = "cluster_1387998613_1387998619_1387998643_1387998651"
                traci.trafficlight.setPhaseDuration(tfl, trafficlightduration[randrange(4)])
                traci.trafficlight.setRedYellowGreenState(tfl, trafficsignal[randrange(4)])

                ##------------------------------------------------------##
                

traci.close()







