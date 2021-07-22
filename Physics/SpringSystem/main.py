import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class SpringNode:
    def __init__(self, n):
        self.fr = n
        self.to = n + 1


class SpringSystem:

    # Init setup
    def __init__(self, m=1, g=0, L=1, KD=0, KS=1, NP=2):
        self.m = m
        self.g = g
        self.L = L
        self.KD = KD
        self.KS = KS
        self.NP = NP * 2
        self.NS = 0
        self.EK = np.array([0 for x in range(self.NP)], dtype=float)
        self.ES = np.array([0 for x in range(self.NP)], dtype=float)
        self.ESUM = []
        self.EKUM = []
        self.ETOTAL = []
        self.time_elapsed = 0
        self.particleX = np.array([[0 for x in range(2)] for y in range(self.NP)], dtype=float)
        self.particleV = np.array([[0 for x in range(2)] for y in range(self.NP)], dtype=float)
        self.particleV[0][1] = 0
        self.particleV[1][1] = 0
        self.particlegraph = []

        # Initial position
        xpos = 1
        for i in range(self.NP):

            ypos = 0
            if (i % 2) == 0:
                xpos = (i + 1) * L
                self.particleX[i, 0] = xpos
            else:
                self.particleX[i, 0] = -xpos

            if i is not self.NP - 1 and (i % 2) == 0:
                self.particlegraph.append(SpringNode(i))
                self.NS = self.NS + 1

        # Initial force

        self.f = np.array([[0 for x in range(2)] for y in range(self.NP)], dtype=float)
        self.fsum = np.array([[0 for x in range(2)] for y in range(self.NP)], dtype=float)
        for s in range(self.NS):
            r = self.particleX[self.particlegraph[s].fr][:] - self.particleX[self.particlegraph[s].to][:]
            runit = r / np.linalg.norm(r)
            rdot = self.particleV[self.particlegraph[s].fr][:] - self.particleV[self.particlegraph[s].to][:]
            for i in range(self.NP):
                self.f[i, :] = -(self.KS * (np.linalg.norm(r) - self.L)-self.KD*(rdot*runit)) * runit

                if i == self.particlegraph[s].fr:
                    self.fsum[i, :] = self.fsum[i, :] + self.f[i, :]
                elif i == self.particlegraph[s].to:
                    self.fsum[i, :] = self.fsum[i, :] - self.f[i, :]

            self.fsum[:, 1] = self.fsum[:, 1] - self.m * self.g



    def step(self, dt):

        # half euler backstep
        if self.time_elapsed == 0:
            for i in range(self.NP):
                    self.particleV[i, :] = self.particleV[i, :] - (self.fsum[i, :].dot(dt)) / 2

        # Update force and position
        else:
            self.fsum = np.array([[0 for x in range(2)] for y in range(self.NP)], dtype=float)
            for s in range(self.NS):
                r = self.particleX[self.particlegraph[s].fr][:] - self.particleX[self.particlegraph[s].to][:]
                runit = r / np.linalg.norm(r)
                test = np.linalg.norm(r)
                rdot = self.particleV[self.particlegraph[s].fr][:] - self.particleV[self.particlegraph[s].to][:]
                self.ES[s] = np.sum((self.KS * (np.linalg.norm(r) - self.L) ** 2) / 2)
                for i in range(self.NP):
                    self.f[i, :] = -(self.KS * (np.linalg.norm(r) - self.L) - self.KD * (rdot*runit)) * runit

                    if i == self.particlegraph[s].fr:
                        self.fsum[i, :] = self.fsum[i, :] + self.f[i, :]
                        self.particleV[i, :] = self.particleV[i, :] - self.fsum[i, :].dot(dt) / self.m
                        self.particleX[i, :] = self.particleX[i, :] - self.particleV[i, :].dot(dt)
                        self.EK[i] = np.sum((self.m * self.particleV[i, :] ** 2) / 2)
                    elif i == self.particlegraph[s].to:
                        self.fsum[i, :] = self.fsum[i, :] - self.f[i, :]
                        self.particleV[i, :] = self.particleV[i, :] - self.fsum[i, :].dot(dt) / self.m
                        self.particleX[i, :] = self.particleX[i, :] - self.particleV[i, :].dot(dt)
                        self.EK[i] = np.sum((self.m * self.particleV[i, :] ** 2) / 2)


        self.ESUM.append(np.sum(self.ES[:]))
        self.EKUM.append(np.sum(self.EK[:]))
        self.ETOTAL.append(np.sum(self.ES[:])+np.sum(self.EK[:]))
        self.time_elapsed += dt


particlesystem = SpringSystem()


# Figure

def get_cmap(n, name='hsv'):
    # Returns color after index
    return plt.cm.get_cmap(name, n)


def init():
    global particlesystem
    partgraph.set_data(particlesystem.particleX[:, 0], particlesystem.particleX[:, 1])
    x = np.linspace(0, particlesystem.time_elapsed)
    energySline.set_data(x, particlesystem.ESUM[-1])
    energyKline.set_data(x, particlesystem.EKUM[-1])
    energyTOTline.set_data(x, particlesystem.ETOTAL[-1])
    time_text.set_text('')
    return partgraph, time_text,


def animate(i):
    global particlesystem, x
    dt = 1. / 80
    particlesystem.step(dt)
    partgraph.set_data(particlesystem.particleX[:, 0], particlesystem.particleX[:, 1])
    if particlesystem.time_elapsed < 50:
        x.append(particlesystem.time_elapsed)
        energySline.set_data(x, particlesystem.ESUM)
        energyKline.set_data(x, particlesystem.EKUM)
        energyTOTline.set_data(x, particlesystem.ETOTAL)
    time_text.set_text('time = %.1f' % particlesystem.time_elapsed)
    return partgraph, time_text, energySline, energyKline, energyTOTline


fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(4, 1, (1, 2))
ay = fig.add_subplot(4, 1, 4)
x = []
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
ay.set_xlim(0, 50)
ay.set_ylim(0, 60)
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
partgraph, = ax.plot([], [], 'o-', ms=6)
energySline, = ay.plot([], [], '-', ms=6)
energyKline, = ay.plot([], [], '-', ms=6, color='red')
energyTOTline, = ay.plot([], [], '-', ms=6, color='black')
ay.legend([energySline, energyKline], ["Spring", "Kinetic"])
animate(0)

ani = animation.FuncAnimation(fig, animate, interval=0.00001, init_func=init, blit=True)


plt.show()
