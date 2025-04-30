import pandas as pd
import wntr
import wntr.network.controls as controls
import numpy as np
from performance import Performance
from model import Model
import random

pt_soln = [random.randint(0, 1) for i in range(24*42)]
dir_soln = [random.randint(0,1) for i in range(21)]
set_soln = random.choices([i for i in range(45, 96, 5)], k=21)
stat_soln = [random.randint(0, 2) for i in range(21)] 

inp_file = 'NOKY_21.inp'
wn = wntr.network.WaterNetworkModel(inp_file)
sim = wntr.sim.EpanetSimulator(wn)
results = sim.run_sim()
results.node.keys()
# solution = np.load('best_soln.npy')
# solution = pt_soln + dir_soln + set_soln + stat_soln
    
# model = Model(wn, solution)
# # model.save_model('NOKY_19_opt_02')
# model.set_time_model()
# model.run_model()
# output = Performance(model)
# fitness = output.fitness_calc()

# print(fitness)
