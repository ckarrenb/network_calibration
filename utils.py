# def set_ga():
    
def set_gene_params(n_pumps, rules='time', n_valves=0):
    if n_valves == 0:
        valves = False
    else:
        valves = True
    if rules == 'time':
        gene_space = [[0,1]]*24*n_pumps
        gene_type = [int]*24*n_pumps
        num_genes = len(gene_space)
        if valves:
            vdir_space = [[0,1]]*n_valves
            vset_space = [{'low':45.0, 'high':95.0, 'step':5.0}]*n_valves
            vstat_space = [[0,1,2]]*n_valves
            gene_space = gene_space + vdir_space + vset_space + vstat_space 
            gene_type = gene_type + [int]*len(vdir_space) + [float]*len(vset_space) + [int]*len(vstat_space)
            num_genes = len(gene_space)
    elif rules == 'condition':
        tank_space = [{'low':0, 'high':20, 'step':1}]*n_pumps
        ll_space = [{'low':0.1, 'high':0.9, 'step':0.01}]*n_pumps
        gene_space = tank_space + ll_space
        gene_type = [int]*len(tank_space) + [float]*len(ll_space)
        num_genes = len(gene_space)
        if valves:
            vdir_space = [[0,1]]*n_valves
            vset_space = [{'low':45.0, 'high':95.0, 'step':5.0}]*n_valves
            vstat_space = [[0,1,2]]*n_valves
            gene_space = gene_space + vdir_space + vset_space + vstat_space 
            gene_type = gene_type + [int]*len(vdir_space) + [float]*len(vset_space) + [int]*len(vstat_space)
            num_genes = len(gene_space)
        else:
            pass
    else:
        gene_space = [0,1]
        gene_type = int
        num_genes = n_pumps
    
    return gene_space, gene_type, num_genes
