import numpy as np
import wntr
import wntr.network.controls as controls
import pandas as pd
import random

inp_file = 'NOKY_18.inp'
wn = wntr.network.WaterNetworkModel(inp_file)

wn.options.hydraulic.demand_model = 'DDA'
wn.options.energy.global_price = 3.61e-8
wn.options.energy.global_efficiency = 85.0

def valve_candidates(wn, results, pressure_threshold):
    pressure = results.node['pressure']
    mask1 = pressure < pressure_threshold
    cols1 = mask1.any()
    n1 = cols1[cols1].index.tolist()

    mask2 = pressure >= pressure_threshold
    cols2 = mask2.all()
    n2 = cols2[cols2].index.tolist()

    all_pipes = [name for name, pipe in wn.pipes()]
    cand_pipes = [name for name, pipe in wn.pipes() if (pipe.diameter >= 0.1016 and pipe.diameter <= 0.3048) and (pipe.start_node_name in n1 and pipe.end_node_name not in n1 or pipe.end_node_name in n1 and pipe.end_node_name not in n1)]
    
    return cand_pipes

def add_time_control(wn, item, soln):
    pump = wn.get_link(item)
    for i, time in enumerate(soln):
        if i == 0:
            act = controls.ControlAction(pump, 'status', time)
            cond = controls.SimTimeCondition(wn, '=', '00:00')   
            name = str(pump) + '_' + str(i)     
            control = controls.Control(cond, act, name=name)
            wn.add_control(name, control)
        else:
            if times[i] == times[i-1]:
                pass
            else:
                act = controls.ControlAction(pump, 'status', time)
                cond = controls.SimTimeCondition(wn, '=', str(i) + ':00')
                name = str(pump) + '_' + str(i)
                control = controls.Control(cond, act, name=name)
                wn.add_control(name, control)
                
        return wn
    
def indicator_1(wn, results, pmin=0):
    demand_nodes = [name for name, junc in wn.junctions() if junc.base_demand > 0]
    pressure = results.node['pressure'][demand_nodes]
    min_press = pressure > pmin
    n = min_press.sum().sum()
    I_1 = n / (pressure.shape[1] * pressure.shape[0])   

    return round(I_1, 2)
    
def indicator_2(wn, results, pref=13.8):
    demand_nodes = [name for name, junc in wn.junctions() if junc.base_demand > 0]
    pressure = results.node['pressure'][demand_nodes]
    pressure = pressure.where(pressure <= pref, pref)
    p_ih = pressure.sum().sum()
    I_2 = p_ih / (pref * pressure.shape[1] * pressure.shape[0])

    return round(I_2, 2)
    
def indicator_3(wn, results, pmax=70):
    demand_nodes = [name for name, junc in wn.junctions() if junc.base_demand > 0]
    pressure = results.node['pressure'][demand_nodes]
    max_press = pressure < pmax
    n = max_press.sum().sum()
    I_3 = n / (pressure.shape[1] * pressure.shape[0])

    return round(I_3, 2)
    
def indicator_4(wn, results, maxprice=33740):
    all_pumps = [name for name, pump in wn.pumps()]
    status = results.link['status'][all_pumps]
    power = wn.query_link_attribute('power') / 1000
    efficiency = wn.options.energy.global_efficiency / 100
    price = wn.options.energy.global_price * 3.6e6
    total_cost = status * power / efficiency * price
    ind = 1 - total_cost.sum().sum() / maxprice

    return round(ind, 2)

def indicator_5(wn, results, vmax=1.8):
    large_pipes = [name for name, pipes in wn.pipes() if pipes.diameter > 0.40]
    velocity = results.link['velocity'][large_pipes]
    max_velocity = velocity < vmax
    n = max_velocity.sum().sum()
    I_5 = n / (velocity.shape[1] * velocity.shape[0]) 

    return round(I_5, 2)

def run_solution(solution, inp='NOKY_18.inp'):
    pump_dict = {
        0: 'PUMP1',
        1: 'PUMP2',
        2: 'PUMP3',
        3: 'PUMP4',
        4: 'PUMP5',
        5: 'PUMP6',
        6: 'PUMP7',
        7: 'PUMP8',
        8: 'PUMP9',
        9: 'PUMP10',
        10: 'PUMP11',
        11: 'PUMP12',
        12: 'PUMP13',
        13: 'PUMP14',
        14: 'PUMP15',
        15: 'PUMP16',
        16: 'PUMP17',
        17: 'PUMP18',
        18: 'PUMP19',
        19: 'PUMP20',
        20: 'PUMP21',
        21: 'PUMP22',
        22: 'PUMP23',
        23: 'PUMP24'
                 }
    
    inp_file = inp
    wn = wntr.network.WaterNetworkModel(inp_file)

    wn.options.hydraulic.demand_model = 'DDA'
    wn.options.energy.global_price = 3.61e-8
    wn.options.energy.global_efficiency = 85.0

    nested_soln = [solution[i:i+24] for i in range(0, len(solution), 24)]
    
    for i, soln in enumerate(nested_soln):
        wn = add_time_control(wn, self.pumps[i], soln)
        
    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()
    
class Model():
    def __init__(self, solution, inp='NOKY_19.inp'):
        self.solution = solution
        self.inp = inp
        self.pump_dict = {
            0: 'PUMP1',
            1: 'PUMP2',
            2: 'PUMP3',
            3: 'PUMP4',
            4: 'PUMP5',
            5: 'PUMP6',
            6: 'PUMP7',
            7: 'PUMP8',
            8: 'PUMP9',
            9: 'PUMP10',
            10: 'PUMP11',
            11: 'PUMP12',
            12: 'PUMP13',
            13: 'PUMP14',
            14: 'PUMP15',
            15: 'PUMP16',
            16: 'PUMP17',
            17: 'PUMP18',
            18: 'PUMP19',
            19: 'PUMP20',
            20: 'PUMP21',
            21: 'PUMP22',
            22: 'PUMP23',
            23: 'PUMP24'
        }

    def add_time_control(wn, item, soln):
        pump = wn.get_link(item)
        for i, time in enumerate(soln):
            if i == 0:
                act = controls.ControlAction(pump, 'status', time)
                cond = controls.SimTimeCondition(wn, '=', '00:00')   
                name = str(pump) + '_' + str(i)     
                control = controls.Control(cond, act, name=name)
                wn.add_control(name, control)
            else:
                if times[i] == times[i-1]:
                    pass
                else:
                    act = controls.ControlAction(pump, 'status', time)
                    cond = controls.SimTimeCondition(wn, '=', str(i) + ':00')
                    name = str(pump) + '_' + str(i)
                    control = controls.Control(cond, act, name=name)
                    wn.add_control(name, control)
        
        return wn
        
     def set_model(self):
        sim = wntr.sim.EpanetSimulator(wn)

        wn = wntr.network.WaterNetworkModel(inp_file)

        wn.options.hydraulic.demand_model = 'DDA'
        wn.options.energy.global_price = 3.61e-8
        wn.options.energy.global_efficiency = 85.0

        nested_soln = [self.solution[i:i+24] for i in range(0, len(self.solution), 24)]

        for i, soln in enumerate(nested_soln):
            wn = add_time_control(wn, self.pumps[i], soln)

        return wn

    def run_model(self, wn):
        sim = wntr.sim.EpanetSimulator(wn)
        results = sim.run_sim()

        return wn, results
# ax = wntr.graphics.plot_network(wn, node_attribute=pressure_at_1hr, node_range=[0,100], node_colorbar_label='Pressure (m)', filename='press_1hr.png')
