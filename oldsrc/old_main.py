import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import os
import sys

from tools.parse import parse_command

import oldsrc.solutions as sol
import oldsrc.coefficients as coef

def animate_2D(paramsfile):
    (choice, ns, ms, a, c, Ntime, tmax) = np.loadtxt(paramsfile)
    Ntime = int(Ntime)
    ns = int(ns)
    ms = int(ms)
    show = False
    # --------------------------------------------------------
    # things you can change

    save = True # choose to save the animation as a file
    dirname = 'animations' # folder name to store animations
    filename = f'old_wave_{choice}_n_{ns}_m_{ms}_c_{c}.mp4' # animation file name (must be mp4)

    # --------------------------------------------------------


    tlist = np.linspace(0,tmax,Ntime)
    dt = tmax/(Ntime-1)
    fps = int(1/dt)

    # coefficients for wave function
    (A,B) = coef.coef(ns, ms, a, choice)


    # wave function
    def u(r, theta, t):
        return sol.wave_solution(r, theta, t, A, B, a, c, ns, ms)

    rlist = np.linspace(0,a,100, endpoint=True)
    thetalist = np.linspace(0, 2*np.pi, 100)

    rmesh, thetamesh = np.meshgrid(rlist,thetalist)
    X, Y = rmesh*np.cos(thetamesh), rmesh*np.sin(thetamesh)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')

    # --------------------------------------------------------
    # animation

    def animate(i):
        ax.clear()
        ax.set_zlim([-2,2]) # arbitrary, you can change this if you want
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("u")
        surf = ax.plot_surface(X, Y, u(rmesh, thetamesh, tlist[i]), cmap=plt.cm.YlGnBu_r)
        return surf,

    anim = ani.FuncAnimation(
        fig, animate, frames=Ntime, interval=20, blit=False)


    if save:
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        writer=ani.FFMpegWriter(bitrate=5000, fps=fps)
        anim.save(dirname + '/' + filename, writer=writer)
        print(f'saving animation to {dirname}/{filename}')

    if show:
        plt.show()

