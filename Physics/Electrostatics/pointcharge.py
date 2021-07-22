import sys
import numpy as np
import scipy.constants as sp
import matplotlib.pyplot as plt
from matplotlib.patches import Circle



q = [0, (0, 0, 10)]

r = 10
theta = np.linspace(0, 2 * np.pi)
xline = r * np.cos(theta)
yline = r * np.sin(theta)
zline = 0

X, Y, Z = np.meshgrid(xline, yline, zline)
rp = [X, Y, Z]
rel = q[1]-rp[0]
mag = np.linalg.norm(rel)
unit = rel/mag
E = (1/(4*np.pi*sp.epsilon_0*mag**2))*unit
ETOT = 0
for i in E:
    ETOT += i
fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)
ax.set_zlim(0, 20)
ax.plot(*q)
ax.plot(xline, yline, zline)
ax.scatter(*q[1])

plt.show()
