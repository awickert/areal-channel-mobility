#! /usr/bin/python

# Started 1 JAN 2012 by ADW: New Year's Day!

from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit # Nonlinear least squares
from matplotlib import rc

data = np.genfromtxt('measured_parameters_20FEB2012.txt')

experiments = ['XES02-SS', 'XES02-SF', 'XES02-SR', 'XES02-RF', 'XES02-RR', 'DB03-1', 'DB03-2', 'BV-1', 'BV-2']

# Not needed - internal TeX handles it fine
#rc('text', usetex=True)
#rc('font', family='serif')

# Order: XES(5), DB03-1, DB03-2, BV-1 (noveg), BV-2 (veg)

# Import variables
M = data[:,1] # Loss of channel planform overlap [1/hr]
R = data[:,5] # Fluvial surface reworking [1/hr]
pM = data[:,2] # Overlap asymptote [-]
pR = data[:,6] # RW asymptote [-]
aM = data[:,0] # Overlap y-intercept
aR = data[:,4] # RW y-intercept
zetadot_f = data[:,8] # [1/hr]
zetadot = data [:,9] # [m/hr]
etadot = (data [:,10]) / 1000 # In-channel aggradation rate [m/hr]
h = data[:,11] # Channel depth [mm]
b = data[:,12] # Channel system total width [m]
fw = data[:,13] # Wetted fraction [-]

# Calculate variables
fd = 1-fw
Phi = 2*fw*fd
qs = data[:,14]# / h # sed flux [m/hr] - 20 FEB HAS /h IN THE CALC ALREADY
f_av = etadot/h
etadot_av = b * f_av # Avulsion magnitude * frequency [m/hr]
# etadot_mig = q_s * \Xi * porosity (anything else?); \Xi-ish will be our slope
tau_chM = ( fw * (1 - Phi) * (1 - pM) * ( 1 - np.exp(-3) ) ) / zetadot_f
tau_fsR = fd * (1 - pR) * (1 - np.exp(-3)) / zetadot_f
zetadot_fR = zetadot_f/( fd * (1-pR))
BR = fd * (1-pR) # Dimensionless unoccupied fluvial surface width
bM = fw * (1-Phi) * (1-pM) # Dimensionless channel width for loss of overlap to random equivalence

# Remove nans
rm = np.isnan(M).nonzero()[0][0]
fwrm = np.array(list(fw[:rm]) + list(fw[rm+1:]))
MbM = M*bM
RBR = R*BR

###########################
##  CURVE FIT FUNCTIONS  ##
###########################

def lin_no_intercept(x,m):
  return m*x

def lin(x,m,b):
  return m*x + b

def power(x,a,n):
  return a*x**n

#################################
##  FIGURES AND CURVE FITTING  ##
#################################

fig = plt.figure(figsize=(6,6))
fig.subplots_adjust(left=.1, bottom=.1)
cf_x = np.linspace(1E-2,1E2,500)


plt.show()

