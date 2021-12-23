import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns


def plot_cell(Ts, states, infection, cell_name, color, name, fig_dir=None):
    plt.figure(figsize=(7, 4))
    plt.plot(Ts, states[cell_name], color=color, linewidth=0.8, label=cell_name) 
    plt.ylabel('# {}'.format(cell_name))
    plt.xlabel('Hours')
    plt.scatter(infection.AIS_ts, np.zeros_like(infection.AIS_ts), color='r', marker='o', label='AIS activated')
    plt.legend()
    plt.savefig(fig_dir + '/{}_{}.jpg'.format(name, cell_name), bbox_inches='tight')
    plt.show()
    
def plot_state(state, exp_name, name, fig_dir=None):
    fig = plt.figure(figsize=(7, 4))
    sns.histplot(state)
    plt.savefig(fig_dir + '/{}_{}_state.jpg'.format(exp_name, name), bbox_inches='tight')
    plt.show()