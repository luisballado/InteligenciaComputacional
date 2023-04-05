import traci
import time
import traci.constants as tc
import pytz
import datetime
from random import randrange
import pandas as pd

#Sacar tiempo
def getdatetime():
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        currentDT = utc_now.astimezone(pytz.timezone("America/Monterrey"))
        DATIME = currentDT.strftime("%d-%m-%Y %H:%M:%S")

        return DATIME

def flatten_list(_2d_list):
        flat_list = []
        for element in _2d_list:
                if type(element) is list:
                        for item in element:
                                flat_list.append(item)
                else:
                        flat_list.append(element)
                        
        return flat_list

#levantar sumo
#COMANDO -c ARCHIVO
#sumoCmd = ["sumo-gui", "-c", "osm.sumocfg"]
sumoCmd = ["sumo-gui", "-c", "cluster_lanearea60.sumocfg"]

traci.start(sumoCmd)

#packVehicleData = []
#packTLSData = []
#packBigData = []

#Run a simulation until all vehicles have arrived
while traci.simulation.getMinExpectedNumber() > 0:
        
        traci.simulationStep();
        
        vehicles=traci.vehicle.getIDList();
        trafficlights=traci.trafficlight.getIDList();
        detlist = traci.lanearea.getIDList()

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
                
                
                #print([traci.lanearea.getLastStepVehicleNumber(det) for det in detlist])
                for det in detlist:
                        print("######################################################################")
                        print("LaneID : " + traci.lanearea.getLaneID(det))
                        print("ID Count: " + str(traci.lanearea.getIDCount))
                        print("Position: " + str(traci.lanearea.getPosition(det)))
                        print("LastStepMeanSpeed: " + str(traci.lanearea.getLastStepMeanSpeed(det)))
                        print("VehicleIDs : " + str(traci.lanearea.getLastStepVehicleIDs(det)))
                        print("LastStepOccupancy : " + str(traci.lanearea.getLastStepOccupancy(det)))
                        print("JamVehicle: " + str(traci.lanearea.getJamLengthVehicle(det)))
                        print("JamLengthMeters: " + str(traci.lanearea.getJamLengthMeters(det)))
                        print("IntervalOccupancy: " + str(traci.lanearea.getIntervalOccupancy(det)))
                        print("IntervalMeanSpeed: " + str(traci.lanearea.getIntervalMeanSpeed(det)))
                        print("IntervalVehicleNumber: " + str(traci.lanearea.getIntervalVehicleNumber(det)))
                        print("JamInMeters: " + str(traci.lanearea.getIntervalMaxJamLengthInMeters(det)))
                        print("IntervalMeanSpeed: " + str(traci.lanearea.getIntervalMeanSpeed(det)))
                        print("IntervalVehicleNumber: " + str(traci.lanearea.getLastIntervalVehicleNumber(det)))
                        print("LastIntervalVehicleNumber: " + str(traci.lanearea.getLastIntervalMaxJamLengthInMeters(det)))
                        print("---------------------------------------------------")                        
                        print("CARROS EN ZONA: " + str(traci.lanearea.getLastStepVehicleNumber(det)))
                        print("###################################################")                        
                        
                #print([traci.lanearea.getLastStepVehicleNumber(det) for det in detlist])

                
                
                """
                print("$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%$")
                IDsOfEdges = traci.edge.getIDList();
                print("IDs of the edges:", IDsOfEdges)
                print("$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%$")
                IDsOfJunctions = traci.junction.getIDList();
                print("IDs of the edges:", IDsOfJunctions)
                """
                
                idd = traci.vehicle.getLaneID(vehicles[i])
                
                tlsList = []
                
                for k in range(0,len(trafficlights)):
                        
                        #Function descriptions
                        #https://sumo.dlr.de/docs/TraCI/Traffic_Lights_Value_Retrieval.html#structure_of_compound_object_controlled_links
                        #https://sumo.dlr.de/pydoc/traci._trafficlight.html#TrafficLightDomain-setRedYellowGreenState
                        
                        if idd in traci.trafficlight.getControlledLanes(trafficlights[k]):
                                
                                tflight = trafficlights[k]
                                tl_state = traci.trafficlight.getRedYellowGreenState(trafficlights[k])
                                tl_phase_duration = traci.trafficlight.getPhaseDuration(trafficlights[k])
                                tl_lanes_controlled = traci.trafficlight.getControlledLanes(trafficlights[k])
                                tl_program = traci.trafficlight.getCompleteRedYellowGreenDefinition(trafficlights[k])
                                tl_next_switch = traci.trafficlight.getNextSwitch(trafficlights[k])
                                
                                #Packing of all the data for export to CSV/XLSX
                                tlsList = [tflight, tl_state, tl_phase_duration, tl_lanes_controlled, tl_program, tl_next_switch]
                                
                                print(trafficlights[k], " --->", \
                                      #Returns the named tl's state as a tuple of light definitions from rRgGyYoO, for red,
                                      #green, yellow, off, where lower case letters mean that the stream has to decelerate
                                      " TL state: ", traci.trafficlight.getRedYellowGreenState(trafficlights[k]), " |" \
                                      #Returns the default total duration of the currently active phase in seconds; To obtain the
                                      #remaining duration use (getNextSwitch() - simulation.getTime()); to obtain the spent duration
                                      #subtract the remaining from the total duration
                                      " TLS phase duration: ", traci.trafficlight.getPhaseDuration(trafficlights[k]), " |" \
                                      #Returns the list of lanes which are controlled by the named traffic light. Returns at least
                                      #one entry for every element of the phase state (signal index)                                
                                      " Lanes controlled: ", traci.trafficlight.getControlledLanes(trafficlights[k]), " |", \
                                      #Returns the complete traffic light program, structure described under data types                                      
                                      " TLS Program: ", traci.trafficlight.getCompleteRedYellowGreenDefinition(trafficlights[k]), " |"
                                      #Returns the assumed time (in seconds) at which the tls changes the phase. Please note that
                                      #the time to switch is not relative to current simulation step (the result returned by the query
                                      #will be absolute time, counting from simulation start);
                                      #to obtain relative time, one needs to subtract current simulation time from the
                                      #result returned by this query. Please also note that the time may vary in the case of
                                      #actuated/adaptive traffic lights
                                      " Next TLS switch: ", traci.trafficlight.getNextSwitch(trafficlights[k]))
                                
                #Pack Simulated Data
                #packBigDataLine = flatten_list([vehList, tlsList])
                #packBigData.append(packBigDataLine)

                
                ##----------MACHINE LEARNING CODES/FUNCTIONS HERE----------##


                ##---------------------------------------------------------------##


                ##----------CONTROL Vehicles and Traffic Lights----------##

                #***SET FUNCTION FOR VEHICLES***
                #REF: https://sumo.dlr.de/docs/TraCI/Change_Vehicle_State.html
                NEWSPEED = 15 # value in m/s (15 m/s = 54 km/hr)

                if vehicles[i]=='veh2':
                        traci.vehicle.setSpeedMode('veh2',0)
                        traci.vehicle.setSpeed('veh2',NEWSPEED)


                #***SET FUNCTION FOR TRAFFIC LIGHTS***
                #REF: https://sumo.dlr.de/docs/TraCI/Change_Traffic_Lights_State.html
                
                trafficlightduration = [5,37,5,35,6,3]
                #trafficsignal = ["GGGGGGGGGGGGGGGG", "GGGGGGGGGGGGGGGG", "GGGGGGGGGGGGGGGG", "GGGGGGGGGGGGGGGG", "GGGGGGGGGGGGGGGG", "GGGGGGGGGGGGGGGG"]
                trafficsignal = ["rrrrrrGGGGgGGGrr", "yyyyyyyyrrrrrrrr", "rrrrrGGGGGGrrrrr", "rrrrryyyyyyrrrrr", "GrrrrrrrrrrGGGGg", "yrrrrrrrrrryyyyy"]
                tfl = "cluster_4260917315_5146794610_5146796923_5146796930_5704674780_5704674783_5704674784_5704674787_6589790747_8370171128_8370171143_8427766841_8427766842_8427766845"
                
                traci.trafficlight.setPhaseDuration(tfl, trafficlightduration[randrange(6)])
                traci.trafficlight.setRedYellowGreenState(tfl, trafficsignal[randrange(6)])

                ##------------------------------------------------------##
                

traci.close()

#Generate Excel file
"""
columnnames = ['dateandtime', 'vehid', 'coord', 'gpscoord', 'spd', 'edge', 'lane', 'displacement', 'turnAngle', 'nextTLS', \
                       'tflight', 'tl_state', 'tl_phase_duration', 'tl_lanes_controlled', 'tl_program', 'tl_next_switch']
dataset = pd.DataFrame(packBigData, index=None, columns=columnnames)
dataset.to_excel("output.xlsx", index=False)
time.sleep(5)
"""







