#!/usr/bin/python

from scipy.optimize import curve_fit
import csv, numpy, glob
from scipy.special import erf
import matplotlib.pyplot as plt

'''power function to optimize'''
def P(x, Po, Pmax, xo, w):
	return Po+0.5*Pmax*(1.-erf(2.**0.5*(x-xo)/w))


'''load and fit beam section'''
files = glob.glob('*.dat')
files.sort()
data_waist = []
plt.close()
fig, p = plt.subplots(2, 1)
for f in files:
	with open(f, 'r') as dest_f:
		raw = csv.reader(dest_f, delimiter = '\t', quotechar = '"')
		data = [value for value in raw]
	data = numpy.asarray(data, dtype = float)
	xmes = data[:,0]
	Pmes = data[:,1]

	'''optimization with non-linear least squares method'''
	Ppopt, Pcov = curve_fit(P, xmes, Pmes, method = 'trf')
	z = int(f.split('-')[-1].split('.')[0])
	w = Ppopt[3]
	w_sig = numpy.sqrt(numpy.diag(Pcov))[3]
	data_waist.append([z, w, w_sig])
	print('z = %.3f mm\t w = %.3f mm (+-%.3f mm)'%(z, w, 1.96*w_sig))

	'''plot'''
	p[0].plot(xmes, Pmes, 'o')
	p[0].plot(numpy.linspace(xmes[0], xmes[-1], 100), P(numpy.linspace(xmes[0], xmes[-1], 100), *Ppopt))

p[0].grid()

'''return waist(z) table'''
data_waist = numpy.asarray(data_waist, dtype = float)

'''waist function to optimize'''
def W(z, w0, z0):
	return w0*(1.+((z-z0)*1542e-6/(numpy.pi*w0**2))**2)**0.5

popt, cov = curve_fit(W, data_waist[:,0], data_waist[:,1])
w0 = popt[0]
w0_sig = numpy.sqrt(numpy.diag(cov))[0]
z0 = popt[1]
z0_sig = numpy.sqrt(numpy.diag(cov))[1]
print('\nz0 = %.3f mm (+-%.3f mm)\t w0 = %.3f mm (+-%.3f mm)'%(z0, 1.96*z0_sig, w0, 1.96*w0_sig))

p[1].plot(data_waist[:,0], data_waist[:,1], 'bo')
p[1].plot(data_waist[:,0], -data_waist[:,1], 'bo')
p[1].plot(numpy.linspace(min(data_waist[:,0]), max(data_waist[:,0]), 100), W(numpy.linspace(min(data_waist[:,0]), max(data_waist[:,0]), 100), *popt), 'r')
p[1].plot(numpy.linspace(min(data_waist[:,0]), max(data_waist[:,0]), 100), -W(numpy.linspace(min(data_waist[:,0]), max(data_waist[:,0]), 100), *popt), 'r')
p[1].grid()

plt.show()
