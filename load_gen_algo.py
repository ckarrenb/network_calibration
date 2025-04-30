import numpy as np
import pandas as pd
import wntr
import wntr.network.controls as controls
import pygad
import time
import copy
from performance import Performance
from model import Model
from utils import set_gene_params

init_soln = np.load('best_soln_valves_15_20.npy', allow_pickle=True)
print(init_soln)
