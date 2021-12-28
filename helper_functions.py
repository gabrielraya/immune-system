""" Provides the helper functions for the bacteria infection model """

import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns


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

    # init state count
    bacteria_states[0] = infection.state.count("bacteria")
    macrophage_states[0] = infection.state.count("macrophage")
    dendritic_states[0] = infection.state.count("dendritic")
    t_cell_states[0] = infection.state.count("t_cell")
    b_cell_states[0] = infection.state.count("b_cell")
        
        
    # simulate spread of bacteria over time
    for t in Ts[1:]: 
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



def run_simulations(n, init_state, model, m, n_, bf, delay_ads, T, exp_name, fig_dir=None):

    paths = np.zeros(n)

    # plotting
    fig, axs = plt.subplots(1, 2, figsize=(2*9, 3), sharey=False)
    axs[0] = plt.subplot2grid((1, 3), (0, 0), colspan=2)

    # run n simulations
    for i in range(n):
        Ts, states, infection = simulate(init_state, model, m, n_, bf, delay_ads, T)
        axs[0].plot(Ts, states["bacteria"], linewidth=0.4)
        paths[i]= states["bacteria"][-1]
    axs[0].set_title('Bacteria')

    axs[1] = plt.subplot2grid((1, 3), (0, 2))

    if n > 2: 
        sns.histplot(paths, kde=True, ax=axs[1])
        axs[1].set_title('Bacteria distribution at end state T')
    plt.savefig(fig_dir + '/{}_simulate.jpg'.format(exp_name), bbox_inches='tight')
    return paths


def run_simulations_no_plots(n, init_state, model, m, n_, bf, delay_ads, T):
    paths = np.zeros(n)
    # run n simulations
    for i in range(n):
        Ts, states, infection = simulate(init_state, model, m, n_, bf, delay_ads, T)
        paths[i]= states["bacteria"][-1]

    return paths

def get_statistics(infection, states):
    """ return some general statistics"""
    # check type case
    if infection.state.count('bacteria') == 0: 
        print("Case: Bacteria was killed")
    else :
        print("Bacteria was not killed\nNumber of bacteria", infection.state.count('bacteria'))
    print("Max number of bacteria at some point :", max(states['bacteria']))
    print("Max number of macrophage at some point :", max(states['macrophage']))
    print("Max number of dendritic at some point :", max(states['dendritic']))
    print("Max number of t_cell at some point :", max(states['t_cell']))
    print("Max number of b_cell at some point :", max(states['b_cell']))

    # max ratio
    ratio = states['bacteria']/states['macrophage']
    t = np.where(ratio == max(ratio))[0][0]
    print("Max ratio bacteria/macrophage {} at t={} no. bacteria {} no. macrophage {}".format(max(ratio), t-1, states['bacteria'][t], states['macrophage'][t]))

    print("Bacteria killed by macrophage: ", infection.bacteria_killed_by_macrophage)
    print("Bacteria killed by dendritic: ", infection.bacteria_killed_by_dendritic)
    print("Number ot times AIS was called: ", len(infection.AIS_ts))