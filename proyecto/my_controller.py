import traci
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Create fuzzy control system
green_time = ctrl.Antecedent(np.arange(0, 61, 1), 'green_time')
delay = ctrl.Consequent(np.arange(0, 11, 1), 'delay')

green_time['low'] = fuzz.trimf(green_time.universe, [0, 0, 30])
green_time['medium'] = fuzz.trimf(green_time.universe, [0, 30, 60])
green_time['high'] = fuzz.trimf(green_time.universe, [30, 60, 60])

delay['low'] = fuzz.trimf(delay.universe, [0, 0, 5])
delay['medium'] = fuzz.trimf(delay.universe, [0, 5, 10])
delay['high'] = fuzz.trimf(delay.universe, [5, 10, 10])

rule1 = ctrl.Rule(green_time['low'], delay['high'])
rule2 = ctrl.Rule(green_time['medium'], delay['medium'])
rule3 = ctrl.Rule(green_time['high'], delay['low'])

delay_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
delay_sim = ctrl.ControlSystemSimulation(delay_ctrl)

# Connect to SUMO simulation
traci.start(['sumo-gui', '-c', 'sumo_config_file.sumocfg'])

# Control traffic light with fuzzy controller
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    current_delay = traci.edge.getWaitingTime('edge_1')
    delay_sim.input['green_time'] = traci.trafficlight.getPhaseDuration('tl_1')
    delay_sim.compute()
    new_duration = max(0, min(60, delay_sim.output['delay']))
    traci.trafficlight.setPhaseDuration('tl_1', new_duration)

traci.close()
