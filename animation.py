import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns

# animation packages
from matplotlib.animation import FuncAnimation 
from IPython.display import HTML

 
def run_animation(states, ais_ts, interval):
    pause = False
    def simData():
        T = len(states["bacteria"])
        dt = 1
        t = 0
        while t < T:
            if not pause:
                x = np.random.rand(int(states["bacteria"][t]),2).reshape(-1,2)
                y = np.random.rand(int(states["macrophage"][t]),2).reshape(-1,2)
                z = np.random.rand(int(states["dendritic"][t]),2).reshape(-1,2)
                tt = np.random.rand(int(states["t_cell"][t]),2).reshape(-1,2)
                b = np.random.rand(int(states["b_cell"][t]),2).reshape(-1,2)
                t = t + dt
            yield x, y, z, tt,b, t

    def onClick(event):
        nonlocal  pause
        pause ^= True

    def simPoints(simData):
        x, y, z, tt, b, t = simData
        time_text.set_text(time_template%(t))
        if (len(ais_ts)>=1 ) and (int(t) == ais_ts[0]):
            alert_text.set_text("Adaptive Immune System Activated!")
        l1.set_data(x[:,0], x[:,1]) 
        l2.set_data(y[:,0], y[:,1]) 
        l3.set_data(z[:,0], z[:,1]) 
        l4.set_data(tt[:,0], tt[:,1])
        l5.set_data(b[:,0], b[:,1])
        return l1, l2, l3, l4, l5, time_text, alert_text

    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_axes([0, 0, 1, 1], frameon=False)

    l1, = ax.plot([], [], 'ro', ms=10, label='bacteria')
    l2, = ax.plot([], [], 'go', ms=10, label='macrophage')
    l3, = ax.plot([], [], 'bo', ms=10, label='dendritic')
    l4, = ax.plot([], [], 'yo', ms=10, label='t_cell')
    l5, = ax.plot([], [], 'o', ms=10, label='b_cell')
    ax.set_ylim(-.3, 1.3)
    ax.set_xlim(-.3, 1.3)
    plt.legend()
    
    time_template = 'Hour = %.1f hr'
    time_text = ax.text(0.1, 0.9, '', transform=ax.transAxes)
    alert_text = ax.text(0.4, 0.9, '', transform=ax.transAxes, color='red')
    fig.canvas.mpl_connect('button_press_event', onClick)
    animation = FuncAnimation(fig, simPoints, simData, blit=False, interval=interval, repeat=False)
    plt.show()
    return animation