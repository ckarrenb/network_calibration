import numpy as np
import pandas as pd
import wntr
import wntr.network.controls as controls
import pygad
from performance import Performance
from model import Model
import time
import copy 

inp_file = 'NOKY_21.inp'
# wn = wntr.network.WaterNetworkModel(inp_file)

def set_inp(inp_file):
    wn = wntr.network.WaterNetworkModel(inp_file)
    thread_wn = copy.deepcopy(wn)
    
    return thread_wn

def on_start(ga_instance):
    global wn
    wn = set_inp(inp_file)
    
def on_generation(ga_instance):
    print('on_generation()')
        
def fitness_func(ga_instance, solution, solution_idx):
    model = Model(solution)
    model.set_model()
    model.run_model()
    output = Performance(model)
    fitness = output.fitness_calc()

    return fitness

num_generations = 10
num_parents_mating = 2

sol_per_pop = 20

num_genes = (42 * 3) + (20 * 3) 

filename = 'noky_pump_opt' + '_' + str(num_generations) + str(sol_per_pop)
start_time = time.time()

ga_instance = pygad.GA(
    num_generations=num_generations,
    num_parents_mating=num_parents_mating,
    sol_per_pop=sol_per_pop,
    # on_start=on_start,
    on_generation=on_generation,
    num_genes=num_genes,
    fitness_func=fitness_func,
    gene_space=[0,1],
    # parallel_processing=['thread', 5]
)

ga_instance.run()

end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time: ", round(elapsed_time/60, 2), " minutes")
ga_instance.save(filename=filename)
ga_instance.plot_fitness()

solution, solution_fitness, solution_idx = ga_instance.best_solution(ga_instance.last_generation_fitness)
np.save('best_soln.npy', solution)
model = Model(solution)
model.save_model(filename)
