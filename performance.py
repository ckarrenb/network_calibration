import wntr
import numpy as np
import wntr.network.controls as controls
import random
import pandas as pd

class Performance():

    def __init__(self, 
                 model, 
                 pmin=0, 
                 pref=13.8, 
                 pmax=70, 
                 maxprice=33740, 
                 vmax=1.8, 
                 weights={
                     0:10, 
                     1:5, 
                     2:8, 
                     3:1, 
                     4:3
                 }
             ):
        
        self.model = model
        self.results = self.model.results
        self.wn = self.model.wn
        self.pmin = pmin
        self.pref = pref
        self.pmax = pmax
        self.maxprice = maxprice
        self.vmax = vmax
        self.weights = weights

        self.all_pumps = [name for name, pump in self.wn.pumps()]
        self.demand_nodes = [name for name, junc in self.wn.junctions() if junc.base_demand >0]
        self.large_pipes = [name for name, pipes in self.wn.pipes() if pipes.diameter > 0.40]
        self.all_nodes = [name for name, junc in self.wn.junctions()]
        
        # self.pressure = self.results.node['pressure'][self.demand_nodes]
        self.pressure = self.results.node['pressure'][self.all_nodes]
        self.N = self.pressure.shape[1] * self.pressure.shape[0]
        

    def indicator_1(self):
        """
            Function to calculate the value for performance indicator 1. 
        Indicator 1 measures the total number of hours each node has service 
        (P > 0).
         
        """
        w = self.weights[0]
        min_press = self.pressure > self.pmin
        n = min_press.sum().sum()
        I_1 = n / self.N * w
        
        return round(I_1, 2)

    def indicator_2(self):
        """
            Function to calculate the value for performance indicator 2. 
        Indicator 2 measures the total number of hours each node maintains minimum service pressure 
        (pressure is greater than 13.8).
         
        """
        w = self.weights[1]
        pressure = self.pressure.where(self.pressure <= self.pref, self.pref)
        p_ih = pressure.sum().sum()
        I_2 = p_ih / (self.pref * pressure.shape[1] * pressure.shape[0]) * w

        return round(I_2, 2)

    def indicator_3(self):
        """
            Function to calculate the value for performance indicator 3. 
        Indicator 3 measures the total number of hours each node maintains pressure below maximum service pressure 
        (pressure is less than 70).
         
        """
        w = self.weights[2]
        max_press = self.pressure < self.pmax
        n = max_press.sum().sum()
        I_3 = n / self.N * w
        
        return round(I_3, 2)

    def indicator_4(self):
        """
            Function to calculate the value for performance indicator 4. 
        Indicator 4 measures the total cost of operating the pumps.
        
        """
        w = self.weights[3]
        status = self.results.link['status'][self.all_pumps]
        power = self.wn.query_link_attribute('power') / 1000
        efficiency = self.wn.options.energy.global_efficiency / 100
        price = self.wn.options.energy.global_price * 3.6e6
        total_cost = status * power / efficiency * price
        I_4 = 1 - total_cost.sum().sum() / self.maxprice * w

        return round(I_4, 2)

    def indicator_5(self):
        """
            Function to calculate the value for performance indicator 5. 
        Indicator 5 measures the the number of hours that large pipes maintain velocity below maximum velocity.
        
        """
        w = self.weights[4]
        velocity = self.results.link['velocity'][self.large_pipes]
        max_velocity = velocity < self.vmax
        n = max_velocity.sum().sum()
        I_5 = n / (velocity.shape[1] * velocity.shape[0]) * w

        return round(I_5, 2)

    def perf_calc(self):
        I_1 = self.indicator_1()
        I_2 = self.indicator_2()
        I_3 = self.indicator_3()
        I_4 = self.indicator_4()
        I_5 = self.indicator_5()

        return(I_1, I_2, I_3, I_4, I_5)

    def fitness_calc(self):
        I_1, I_2, I_3, I_4, I_5 = self.perf_calc()
        fitness = (I_1 + I_2 + I_3 + I_4 + I_5) / sum(self.weights.values())
        
        return fitness
    
    
        
