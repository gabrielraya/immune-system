""" Provides the helper functions for the bacteria infection model """

import numpy as np


def init_state(lambda_ = 5):
    """ create an instance of the initial state of the system """
    
    # take the bacteria infection to follow a poisson distribution 
    n_bacteria = np.random.poisson(lambda_)
    
    # take the marophage infection to follow a poisson distribution with same 
    n_macrophabe = np.random.poisson(lambda_)
    
    # initial state of the bacteria infection 
    init_state_system = ['dendritic']
    init_state_system.extend(['bacteria']*n_bacteria)
    init_state_system.extend(['macrophage']*n_bacteria)
    
    return init_state_system


def simulate(init_state, model, m, n_, bf, delay_ads, T):
    """
    delay_ads: delay for adaptive system
    """
    # init class 
    infection = model(init_state, m, n_, bf, delay_ads)

    # time partion 
    Ts = np.arange(0,T)

    # state of each cell at a given t
    bacteria_states, macrophage_states, dendritic_states,  t_cell_states, b_cell_states = np.zeros(len(Ts)), np.zeros(len(Ts)), np.zeros(len(Ts)), np.zeros(len(Ts)), np.zeros(len(Ts))

    # simulate spread of bacteria over time
    for t in Ts: 
        # run mutation 
        selected_cell = infection.mutate(t)
        # count
        bacteria_states[t] = infection.state.count("bacteria")
        macrophage_states[t] = infection.state.count("macrophage")
        dendritic_states[t] = infection.state.count("dendritic")
        t_cell_states[t] = infection.state.count("t_cell")
        b_cell_states[t] = infection.state.count("b_cell")
    
    states = { "bacteria": bacteria_states,
                "macrophage": macrophage_states,
                "dendritic": dendritic_states,
                "t_cell" : t_cell_states,
                "b_cell" : b_cell_states
               }
    
    return Ts, states, infection


