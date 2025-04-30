import numpy as np
import wntr
import wntr.network.controls as controls
import pandas as pd
import random
import copy
import warnings

warnings.simplefilter('ignore', UserWarning)

class Model():
    def __init__(self, wn, solution, id):
        self.solution = solution
        # self.wn = wntr.network.WaterNetworkModel('NOKY_21.inp')
        self.wn = wn
        self.id = id
        self.results = None
        self.pumps = {}
        self.tanks = {}
        self.valves = {}
        
    def get_pumps(self):
        pump_list = [name for name, pump in self.wn.pumps()]
        for index, item in enumerate(pump_list):
            self.pumps[index] = item

    def get_tanks(self):
        tank_list = [name for name, tank in self.wn.tanks()]
        for index, item in enumerate(tank_list):
            self.tanks[index] = item

    def get_valves(self):
        valve_list = [name for name, valve in self.wn.valves()]
        for index, item in enumerate(valve_list):
            self.valves[index] = item

    def get_pipes(self):
        pipe_list = [name for name, pipe in self.wn.pipes()]

    def add_time_control(self, item, soln):
        pump = self.wn.get_link(item)
        for i, time in enumerate(soln):
            if i == 0:
                act = controls.ControlAction(pump, 'status', time)
                cond = controls.SimTimeCondition(self.wn, '=', '00:00')   
                name = str(pump) + '_' + str(i)     
                control = controls.Control(cond, act, name=name)
                self.wn.add_control(name, control)
            else:
                if soln[i] == soln[i-1]:
                    pass
                else:
                    act = controls.ControlAction(pump, 'status', time)
                    cond = controls.SimTimeCondition(self.wn, '=', str(i) + ':00')
                    name = str(pump) + '_' + str(i)
                    control = controls.Control(cond, act, name=name)
                    self.wn.add_control(name, control)
        
        # return wn

    def add_condition_control(self, item, soln):
        pump = self.wn.get_link(item)
        tank = self.wn.get_node(soln[0])
        ll = min(soln[1], soln[2])
        up = max(soln[1], soln[2])

        
    def split_time_solution(self):
        np = len(self.pumps)
        nv = len(self.valves)

        pump_soln = self.solution[0:24*np]
        nested_soln = [pump_soln[i:i+24] for i in range(0, len(pump_soln), 24)]
        
        valve_soln = self.solution[24*np:]
        dir_idx = valve_soln[0:nv]
        setting_idx = valve_soln[nv:2*nv]
        status_idx = valve_soln[2*nv:]
        
        valve = zip(dir_idx, setting_idx, status_idx)
        return nested_soln, valve
    
    def split_cond_solution(self):
        np = len(self.pumps)
        nv = len(self.valves)
        
        pump_soln = self.solution[0:3*np]
        tank_idx = pump_soln[0:np]
        ll_idx = pump_soln[np:2*np]
        up_idx = pump_soln[2*np:]
        
        valve_soln = self.solution[3*np:]
        dir_idx = valve_soln[0:nv]
        setting_idx = valve_soln[nv:2*nv]
        status_idx = valve_soln[2*nv:]

        pump = zip(tank_idx, ll_idx, up_idx)
        valve = zip(dir_idx, setting_idx, status_idx)

        return pump, valve
    
    def set_cond_model(self):
        self.wn.options.hydraulic.demand_model = 'DDA'
        self.wn.options.energy.global_price = 3.61e-8
        self.wn.options.energy.global_efficiency = 85.0
        self.wn.options.hydraulic.headloss='H-W'

        self.get_pumps()
        self.get_valves()
        self.get_tanks()
        
        pump_soln, valve_soln = self.split_cond_solution()

        for i, soln in enumerate(pump_soln):
            self.add_condition_control(self.pumps[i], soln)
            
        for i, soln in enumerate(valve_soln):
            self.add_valve_settings(self.valves[i], soln)
        
    def add_valve_settings(self, valve, soln):
        valve = self.wn.get_link(valve)
        if soln[0] == 0:
            pass
        else:
            valve.start_node, valve.end_node = valve.end_node, valve.start_node
        valve.initial_setting = soln[1]
        valve.initial_status = soln[2]
        
    def set_time_model(self):
        # print(self.id)
        self.wn.options.hydraulic.demand_model = 'DDA'
        self.wn.options.energy.global_price = 3.61e-8
        self.wn.options.energy.global_efficiency = 85.0
        self.wn.options.hydraulic.headloss='H-W'

        self.get_pumps()
        self.get_valves()

        pump_soln, valve_soln = self.split_time_solution()

        for i, soln in enumerate(pump_soln):
            self.add_time_control(self.pumps[i], soln)
            
        for i, soln in enumerate(valve_soln):
            self.add_valve_settings(self.valves[i], soln)
            
    def set_model(self):
        self.wn.options.hydraulic.demand_model = 'DDA'
        self.wn.options.energy.global_price = 3.61e-8
        self.wn.options.energy.global_efficiency = 85.0
        self.wn.options.hydraulic.headloss='H-W'

        nested_soln = [self.solution[i:i+24] for i in range(0, len(self.solution), 24)]

        for i, soln in enumerate(nested_soln):
            self.add_time_control(self.pumps[i], soln)
            
    def run_model(self):
        try:
            wn0 = copy.deepcopy(self.wn)
            sim = wntr.sim.EpanetSimulator(wn0)
            self.results = sim.run_sim(str(self.id))
        except:
            self.results = None
            print('no results')

        # return results

    def save_model(self, filename):
        self.set_time_model()
        filename = filename + '.inp'
        wntr.network.write_inpfile(self.wn, filename)
        print(f'Saved inp file {filename}.')
