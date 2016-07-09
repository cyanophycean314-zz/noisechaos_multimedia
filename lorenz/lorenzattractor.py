import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

runsim = True

points = [[],[],[]]
pointsp = [[],[],[]]

def getlorenzevol(x, y, z):
    dx = (10 * (y - x)) * dt
    dy = (28 * x - y - x * z) * dt
    dz = (x * y - 8/3 * z) * dt
    
    x += dx
    y += dy
    z += dz 
    
    return x, y, z

x, y, z = 0, 1, 0
xp, yp, zp = 0, 2, 0
xq, yq, zq = 0, 3, 0
dt = 0.01
t = 0
ctr = 0
tframe = [_ * 100 * dt for _ in range(10)]
tlim = tframe[-1]
while t < tlim:
    x,y,z = getlorenzevol(x,y,z)
    xp, yp, zp = getlorenzevol(xp,yp,zp)
    xq, yq, zq = getlorenzevol(xq,yq,zq)

    if abs(t - tframe[ctr]) < dt / 5:
        print t, " ", x - xp, ",", y-yp , ",", z - zp
        fig = plt.figure(figsize = (7,7))
        ax = fig.add_subplot(111, projection='3d')
        plt.hold(True)
        plt.title("Time = " + str(int(t)))
        plt.xlabel("x")
        plt.ylabel("y")
        plt.xlim([-20,25])
        plt.ylim([-30,30])
        ax.set_zlim(0,60)
        ax.scatter([x],[y],[z],marker='o',color='b')
        ax.scatter([xp],[yp],[zp],marker='o',color = 'r')
        ax.scatter([xq],[yq],[zq],marker='o',color = 'g')
        plt.savefig("lorenz" + str(int(t)), bbox_inches='tight', pad_inches=0)
        ctr += 1

    t += dt