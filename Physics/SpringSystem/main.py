import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import Animation


class SpringSystem:

    # Init setup.
    def __init__(self, m=1, g=0, L=1, KD=0, NP=1):
        self.m = m
        self.g = g
        self.L = L
        self.KD = KD
        self.NP = NP * 2
        self.particles = np.array([[0 for x in range(2)] for y in range(self.NP)])
        xpos = 1
        for i in range(self.NP):

            ypos = 0
            if (i % 2) == 0:
                xpos = (i + 1) * L
                self.particles[i][0] = xpos
            else:
                self.particles[i][0] = -xpos

        fx = np.array([0 for x in range(NP)])
        fy = np.array([m * g for y in range(NP)])
        fsum = np.array([[0 for x in range(2)] for y in range(NP)])
        #for i in range(NP):
            #self.particles[i] = self.particles[i] - (fsum[i][:] * dt) / 2




particlesystem = SpringSystem()


# Figure

def get_cmap(n, name='hsv'):
    # Returns color after index
    return plt.cm.get_cmap(name, n)


fig = plt.figure()
ax = fig.add_subplot(111)
cmap = get_cmap(particlesystem.NP)
for xpos, ypos in particlesystem.particles:
    ax.add_artist(Circle((xpos, ypos), 0.05, color=cmap(xpos)))
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
plt.show()
