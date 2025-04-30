import numpy as np
import pandas as pd
import wntr
import wntr.network.controls as controls
import pygad
from performance import Performance
from model import Model
from utils import set_gene_params
import time
import random
import copy 

inp_file = 'NOKY_31.inp'
# thread_wn = wntr.network.WaterNetworkModel(inp_file)
global wn, count
wn = wntr.network.WaterNetworkModel(inp_file)

def set_wn():
    global wn
    wn = wntr.network.WaterNetworkModel(inp_file)

def set_count(s=0):
    global count
    count = s
    
def on_start(ga_instance):
    set_wn()
    set_count()
    
def on_generation(ga_instance):
    global count
    count += 1
    set_wn()
    print(count)
    print('generation: ', ga_instance.generations_completed)
    print('fitness of best solution: ', ga_instance.best_solution()[1])
    
def fitness_func(ga_instance, solution, solution_idx):
    # global wn, count
    # try:
    #     global wn, count
    #     count += 2
    #     soln_wn = copy.deepcopy(wn)
    #     # print('even: ', count)
    # except:
    #     set_count(s=1)
    #     set_wn()
    #     # global count
    #     # count = 1
    #     soln_wn = copy.deepcopy(wn)
        # count += 2
        # print('odd: ', count)
    # print(count)
    soln_wn = copy.deepcopy(wn)
    model = Model(soln_wn, solution, solution_idx)
    model.set_time_model()
    model.run_model()
    output = Performance(model)
    fitness = output.fitness_calc()

    return fitness

num_generations = 20
num_parents_mating = 8
n_pumps = 42
n_valves = 0
rules = 'time'
init_pop = []
sol_per_pop = 60
# num_genes = 24 * 42

gene_space, gene_type, num_genes = set_gene_params(n_pumps, rules, n_valves)    

for i in range(sol_per_pop):
    r = random.choices([0,1], k=num_genes)
    init_pop.append(r)
    
best_soln = np.load('best_soln_valves_15_20.npy', allow_pickle=True)
init_pop[0] = best_soln

filename = 'noky_pump_opt' + '_' + str(num_generations) + str(sol_per_pop)

start_time = time.time()

if __name__ == '__main__':
    
    ga_instance = pygad.GA(
        num_generations=num_generations,
        num_parents_mating=num_parents_mating,
        # sol_per_pop=sol_per_pop,
        on_start=on_start,
        on_generation=on_generation, 
        initial_population=init_pop,
        # num_genes=num_genes,
        # suppress_warnings=True,
        fitness_func=fitness_func,
        gene_space=gene_space,
        gene_type=gene_type,
        parallel_processing=['thread', 5]
    )

    ga_instance.run()
    ga_instance.plot_fitness()
    ga_instance.save(filename=filename)
    solution, solution_fitness, solution_idx = ga_instance.best_solution(ga_instance.last_generation_fitness)


    np.save(f'best_soln_{n_valves}_{num_generations}_{sol_per_pop}.npy', solution)
    model1 = Model(wn, solution, solution_idx)
    model1.save_model(filename)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Elapsed time: ", round(elapsed_time/60, 2), " minutes")
