import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
import imageio
import pathlib
import glob


def plot_cell(Ts, states, infection, cell_name, color, name, fig_dir=None, show=True):
    plt.figure(figsize=(7, 4))
    plt.plot(Ts, states[cell_name], color=color, linewidth=0.8, label=cell_name) 
    plt.ylabel('# {}'.format(cell_name))
    plt.xlabel('Hours')
    plt.scatter(infection.AIS_ts, np.zeros_like(infection.AIS_ts), color='r', marker='o', label='AIS activated')
    plt.legend()
    plt.savefig(fig_dir + '/{}_{}.jpg'.format(name, cell_name), bbox_inches='tight')
    if show: 
        plt.show()
    else: 
        plt.close()
    
def plot_state(state, exp_name, name, fig_dir=None, show=True):
    fig = plt.figure(figsize=(7, 4))
    sns.histplot(state)
    plt.savefig(fig_dir + '/{}_{}_state.jpg'.format(exp_name, name), bbox_inches='tight')
    if show: 
        plt.show()
    else: 
        plt.close()
    
    
def plot_simulated_trajectories(Ts, states, cell_type, exp_name, fig_dir, show=False): 
    """plot the simulated paths"""
    plt.figure(figsize=(8,4))

    for step, path in enumerate(states[cell_type]):
        plt.plot(Ts, path, linewidth=0.4)
        plt.title(cell_type)
        plt.xlabel('Hours')
        plt.ylabel('Cells')
        plt.savefig(fig_dir + '/{:02d}_simulate_{}.png'.format(step, exp_name), bbox_inches='tight')

    plt.plot(Ts, states[cell_type].mean(axis=0), color='r', linewidth=1, label="Mean")
    plt.legend()
    plt.savefig(fig_dir + '/{:02d}_simulate_{}.jpg'.format(step+1, exp_name), bbox_inches='tight')
    
    # compute the means and std
    means = states['bacteria'].mean(axis=0)
    stds  = states['bacteria'].std(axis=0)

    plt.fill_between(Ts, means-stds, means+stds, alpha = 0.5, label="Std")
    plt.legend()
    plt.savefig(fig_dir + '/{}_simulate_mean.jpg'.format(exp_name), bbox_inches='tight')
    
    if show: 
        plt.show()
    else: 
        plt.close()
    
    
    
    
def draw_gif(name, figs_dir, glob_str):
    """
    Create a gif to visualize progress in the VAE
    :param name: save the file using this name
    :param figs_dir: path to save file
    :param glob_str: name pattern of the images to use
    :return: image gif
    """
    files = [file for file in pathlib.Path(figs_dir).glob(glob_str)]
    images = [imageio.imread(str(file),pilmode="RGB") for file in sorted(files)]
    imageio.mimsave('{}/{}'.format(figs_dir, name), images, duration=.1)