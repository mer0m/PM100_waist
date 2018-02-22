#!/usr/bin/env python

import argparse, time, os
import matplotlib.pyplot as plt

#==============================================================================

# Path
PATH = os.getcwd()
# File footer
OFILENAME = '130'

#==============================================================================

def parse():
	"""
	Specific parsing procedure for transfering data from Thorlabs PM100D.
	:returns: populated namespace (parser)
	"""
	parser = argparse.ArgumentParser(description = 'Acquire data from Thorlabs PM100D',
									 epilog = 'Example: \'./pm100d.py -st 10 -o toto\' logs PM100D every 10 seconds to output file YYYYMMDD-HHMMSS-toto.dat')

	parser.add_argument('-p',
						action='store',
						dest='path',
						default=PATH,
						help='Absolute path (default '+PATH+')')

	parser.add_argument('-o',
						action='store',
						dest='ofile',
						default=OFILENAME,
						help='Output data filename (default '+OFILENAME+')')

	args = parser.parse_args()
	return args

#==============================================================================

class usbtmc:
	def __init__(self, device):
		self.device = device
		self.FILE = os.open(device, os.O_RDWR)

	def write(self, command):
		os.write(self.FILE, command);

	def read(self, length = 4000):
		return os.read(self.FILE, length)

	def getName(self):
		self.write("*IDN?")
		return self.read(300)

	def sendReset(self):
		self.write("*RST")

#==============================================================================

class instrument:
	"""Class to control a SCPI compatible instrument"""
	def __init__(self, device):
		print 'Connecting to device %s...' %device
		self.meas = usbtmc(device)
		self.name = self.meas.getName()
		print self.name
		print '  --> Ok'

	def write(self, command):
		"""Send an arbitrary command directly to the scope"""
		self.meas.write(command)

	def read(self, command):
		"""Read an arbitrary amount of data directly from the scope"""
		return self.meas.read(command)

	def reset(self):
		"""Reset the instrument"""
		self.meas.sendReset()

	def value(self):
		self.write('MEAS?')
		return self.read(300)

#==============================================================================

def acqu_PM100D(instrument, path, ofile):

	t0 = time.time()
	filename = time.strftime("%Y%m%d-%H%M%S", time.gmtime(t0)) + '-' + ofile + '.dat'
	print('Opening %s' %filename)
	data_file = open(filename, 'wr', 0)
	dx = 0.

	xmes = []
	Pmes = []
	plt.ion()
	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	line1, = ax1.plot(xmes, Pmes, 'o')

	# Infinite loop
	while True:
		try:
			keypressed = raw_input("Press Enter to continue...\n")

			if keypressed.isdigit():
				print('Closing %s' %filename)
				data_file.close()
				t0 = time.time()
				filename = time.strftime("%Y%m%d-%H%M%S", time.gmtime(t0)) + '-' + keypressed + '.dat'
				print('Opening %s' %filename)
				data_file = open(filename, 'wr', 0)
				dx = 0.

				xmes = []
				Pmes = []
				line1, = ax1.plot(xmes, Pmes, 'o')

			else:
				# Power values
				sensors_values = instrument.value()
				sensors_values = sensors_values.replace('E', 'e')
				string = "%f\t%s" % (dx , sensors_values)
				data_file.write(string) # Write in a file
				print(string)

				xmes.append(dx)
				Pmes.append(float(sensors_values))

				dx = dx + 0.05

			line1.set_data(xmes, Pmes)
			ax1.relim()
			ax1.autoscale_view()
			fig.canvas.draw()

		except Exception as ex:
			print 'Exception during controler data reading: ' + str(ex)

		except KeyboardInterrupt:
			print '\n  --> Disconnected'
			data_file.close()

			# To stop the loop in a clean way
			break

#==============================================================================

def main():
	"""
	Main script
	"""
	# Parse command line
	args = parse()
	# path
	path = args.path
	# Data output filename
	ofile = args.ofile

	try:
		pm100 = instrument("/dev/usbtmc0")

		# acquisition with 2 sec. timeout
		acqu_PM100D(pm100, path, ofile)

	except Exception as ex:
			print 'Oups '+str(ex)
	print 'Program ending\n'

#==============================================================================

if __name__ == "__main__":
	main()
