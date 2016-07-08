#Graph the files

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
import time

#The (basically unchangeable conditions)
dt = 0.00002 #Time interval (around the size of mu for lambda0 * Td = 3200)
samptime = 0.00002 #How often to take a sample
sampspersec = 1 / samptime #Inverse
Td = 0.001734 #Time delay
T1 = 0.0012 #Time constant for variable 1
T2 = 0.00006 #Time constant for variable 2
transtime = 0.1
phi = np.pi / 4 #Filter phase displacement

#Simulation parameters
betatimesTd = 8.87 #this is the actual measurement that Aaron used, different than what he claims
beta = betatimesTd / Td #this is the real beta value, in the thousands.

#[100,250,500,1000,2000,3200,5000,10000,20000,30000]
filelist = [100,250,500,1000,2000,3200,5000,10000,20000,30000]
subs = ['']
deterministic = False

histogram = False
autocorr = False
poincare = True
attractor3d = False
points = False #legacy mode - look at photon counts
divs = False

#Calculate pure deterministic version
pbinw = 0.005
minp = 1.
maxp = 5.
ran = maxp - minp
num = int(ran / pbinw)
delay = Td / 4
vertical = False #True if slope gets too high
thickness = 1 #How many pbinws
#slicer = [[minp + 1.3 * ran / 8, minp + 7.3 * ran / 8], [minp, maxp]]
slicer = [[minp, maxp], [minp + 5.05 * ran / 8, minp + 6 * ran / 8]]
if vertical:
	slopey = (slicer[0][1] - slicer[0][0]) / (slicer[1][1] - slicer[1][0])
else:
	slope = (slicer[1][1] - slicer[1][0]) / (slicer[0][1] - slicer[0][0])


psecdet = [[0 for _ in range(num)] for x in range(num)]
finvt = open("detcomvt.out","r")
pvoltages = [[],[]]
T = float(finvt.readline())
for line in finvt:
	vwp, vwpt = line.split()
	pvoltages[0].append(float(vwp))
	pvoltages[1].append(float(vwpt))
for i in range(len(pvoltages[0])):
	vwp = pvoltages[0][i]
	vwpt = pvoltages[1][i]
	if int((vwp - minp) / pbinw) >= num or int((vwpt - minp) / pbinw) >= num or vwp <= minp or vwpt <= minp:
		continue
	psecdet[int((vwp - minp) / pbinw)][int((vwpt - minp) / pbinw)] += 1
print 'det done'

for fileno in range(len(filelist)):
	filename = filelist[fileno]

	plt.figure(10+fileno, figsize = (24,10))

	for lettno in range(len(subs)):
		lett = subs[lettno]
		#Reset data
		psec = [[0 for _ in range(num)] for x in range(num)]
		if vertical:
			pslice = [0 for i in range(int((slicer[1][1] - slicer[1][0]) / pbinw))]
		else:
			pslice = [0 for i in range(int((slicer[0][1] - slicer[0][0]) / pbinw))]

		print str(filename) + lett
		finvt = open(str(filename) + lett + "vt.out","r")

		pvoltages = [[],[]]
		T = float(finvt.readline())
		for line in finvt:
			vwp, vwpt = line.split()
			pvoltages[0].append(float(vwp))
			pvoltages[1].append(float(vwpt))

		window = int(Td / 4 * sampspersec)
		#print 'Let the graphing begin!'

		for i in range(len(pvoltages[0])):
			vwp = pvoltages[0][i]
			vwpt = pvoltages[1][i]
			if int((vwp - minp) / pbinw) >= num or int((vwpt - minp) / pbinw) >= num or vwp <= minp or vwpt <= minp:
				continue
			psec[int((vwp - minp) / pbinw)][int((vwpt - minp) / pbinw)] += 1

			if vertical:
				orig = vwpt
				x = slicer[0][0] + slopey * (vwpt - slicer[1][0])
				if abs(int((x - minp) / pbinw) - int((vwp - minp) / pbinw)) <= thickness:
					pslice[int((vwpt - slicer[1][0]) / pbinw)] += 1
			else:
				orig = vwp
				y = slicer[1][0] + slope * (vwp - slicer[0][0])
				if abs(int((y - minp) / pbinw) - int((vwpt - minp) / pbinw)) <= thickness:
					pslice[int((vwp - slicer[0][0]) / pbinw)] += 1

		#plt.title(str(filename) + ", bin width = " + str(pbinw) + ", points = " + str(np.sum(psec)))
		plt.subplot(121)
		plt.title('Photons per time delay = ' + str(filename), size = 20)
		#plt.ylim([0,num])
		#plt.xlim([0,num])
		plt.xlabel('Voltage one time delay ago, V(t - w)', size = 20)
		plt.ylabel('Voltage two time delays ago, V(t - 2w)', size = 20)
		plt.pcolormesh(minp + np.array(range(num + 1)) * pbinw, minp + np.array(range(num + 1)) * pbinw, np.transpose(np.array(psec)))

		plt.subplot(122)
		plt.title('Deterministic Limit', size = 20)
		plt.xlabel('Voltage one time delay ago, V(t - w)', size = 20)
		plt.ylabel('Voltage two time delays ago, V(t - 2w)', size = 20)
		plt.pcolormesh(minp + np.array(range(num + 1)) * pbinw, minp + np.array(range(num + 1)) * pbinw, np.transpose(np.array(psecdet)))

		plt.savefig(str(filename) + ".png", bbox_inches='tight', pad_inches=0)

print 'Program done'
