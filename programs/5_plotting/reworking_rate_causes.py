#! /usr/bin/python

# Started 1 JAN 2012 by ADW: New Year's Day!

from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit # Nonlinear least squares
from matplotlib import rc

data = np.loadtxt('measured_parameters_20FEB2012.txt')

# Not needed - internal TeX handles it fine
#rc('text', usetex=True)
#rc('font', family='serif')

# Order: XES(5), DB03-1, DB03-2, BV-1 (noveg), BV-2 (veg)
experiment_names = ['XES02-SS', 'XES02-SF', 'XES02-SR', 'XES02-RF', 'XES02-RR', 'DB03-1', 'DB03-2', 'BV-1', 'BV-2']

# Import variables
M = data[:,1] # Loss of channel planform overlap [1/hr]
R = data[:,5] # Fluvial surface reworking [1/hr]
zetadot = data [:,9] # [m/hr]
etadot = (data [:,10]) / 1000 # In-channel aggradation rate [m/hr]
h = data[:,11] # Channel depth [mm]
b = data[:,12] # Channel system total width [m]
fw = data[:,13] # Wetted fraction [-]
D = np.loadtxt('D.txt')
datainQsQ = np.loadtxt('Qs_Q.txt')
Qs = datainQsQ[:,0] # [m^3/hr]
Q = datainQsQ[:,1] # [m^3/hr]
QsQ = Qs/Q # [-]

# Calculate variables
qs = data[:,14]# / h # sed flux [m/hr] - 20 FEB HAS /h IN THE CALC ALREADY
f_av = etadot/h
zetadot_av = b * f_av # Avulsion magnitude * frequency [m/hr]
# etadot_mig = q_s * \Xi * porosity (anything else?); \Xi-ish will be our slope
g = 9.80665
s = 2.65

###########################
##  CURVE FIT FUNCTIONS  ##
###########################

def lin_no_intercept(x,m):
  return m*x

def lin(x,m,b):
  return m*x + b

def lin_only_intercept(x,b):
  # Uses just intercept
  # for the purpose of calculating error from log so it doesn't get biased by one value
  # basically - to make a straight line fit like a power law
  return x + b

def power(x,a,n):
  return a*x**n

# For getting r^2 from covariance
def rsquared(cov, x, y):
  varx = np.std(x)**2
  vary = np.std(y)**2
  rsquared = cov**2/(varx*vary)
  return rsquared
  
#################################
##  FIGURES AND CURVE FITTING  ##
#################################

fig = plt.figure(figsize=(10,5))
fig.subplots_adjust(wspace=.4, hspace=.3)

# 4. f_av vs. R
ax = fig.add_subplot(122)
ax.grid(True)
"""
ax.plot(zetadot_av[:5]/qs[:5], R[:5], 'o',markersize=9,markerfacecolor='.5',label='XES02: Base level cycle delta')
ax.plot(zetadot_av[5]/qs[5], R[5], 'D',markersize=9,markerfacecolor='.2',label='DB03-1: Supercritical flow delta')
ax.plot(zetadot_av[6]/qs[6], R[6], 'D',markersize=9,markerfacecolor='.8',label='DB03-2: Subcritical flow delta')
ax.plot(zetadot_av[7]/qs[7], R[7], '^',markersize=9,markerfacecolor='.2',label='BV-1: Braided river')
ax.plot(zetadot_av[8]/qs[8], R[8], '^',markersize=9,markerfacecolor='.8',label='BV-2: Vegetated river')
"""
ax.plot(zetadot_av[0], R[0], 'o',markersize=9,markerfacecolor='.5',label='XES02: Base level cycle delta')
ax.plot(zetadot_av[2], R[2], 'o',markersize=9,markerfacecolor='.5',label='XES02: Base level cycle delta')
ax.plot(zetadot_av[4], R[4], 'o',markersize=9,markerfacecolor='.5',label='XES02: Base level cycle delta')
ax.plot(zetadot_av[5], R[5], 'D',markersize=9,markerfacecolor='.2',label='DB03-1: Supercritical flow delta')
#ax.plot(zetadot_av[6], R[6], 'D',markersize=9,markerfacecolor='.8',label='DB03-2: Subcritical flow delta')
plt.xlim( (-.05, plt.xlim()[1]) ) # To see full points on zero
plt.ylim( (-.1, plt.ylim()[1]) ) # To see full points on zero
xl = plt.xlim()
yl = plt.ylim()
#ax.plot(cf_x, cf_y,'g--',label=r'\dot{\zeta} = ' + coeff + r'q_s^str(rf[1])')
plt.xlim(xl)
plt.ylim(yl)
plt.xlabel('Avulsion magnitude times frequency, $\dot{\zeta}_{\mathrm{av}}$ [m/hr]')
plt.ylabel('Fluvial surface reworking rate, $R$ [1/hr]')
ax.text(0.9, 0.1,'B',horizontalalignment='center',
     verticalalignment='center', fontsize=26, 
     family='sans-serif', weight='bold',
     transform = ax.transAxes)
#ax.arrow(0.5,0.5,0.1,0.1, linewidth=0.1, head_width=0.2, length_includes_head=True, shape='full', transform = ax.transAxes)

# 5. q_s vs. R
ax = fig.add_subplot(121)
ax.grid(True)
# experiment_names = ['XES02-SS', 'XES02-SF', 'XES02-SR', 'XES02-RF', 'XES02-RR', 'DB03-1', 'DB03-2', 'BV-1', 'BV-2']
ax.plot(qs[1], R[1], 'o',markersize=9,markerfacecolor='.5',label='XES02: Base level cycle delta')
ax.plot(qs[3], R[3], 'o',markersize=9,markerfacecolor='.5',label='XES02: Base level cycle delta')
ax.plot(qs[6], R[6], 'D',markersize=9,markerfacecolor='.8',label='DB03-2: Subcritical flow delta')
ax.plot(qs[7], R[7], '^',markersize=9,markerfacecolor='.2',label='BV-1: Braided river')
ax.plot(qs[8], R[8], '^',markersize=9,markerfacecolor='.8',label='BV-2: Vegetated river')
"""
ax.plot(Qs[1]/Q[1], R[1], 'o',markersize=9,markerfacecolor='.5',label='XES02: Base level cycle delta')
ax.plot(Qs[3]/Q[3], R[3], 'o',markersize=9,markerfacecolor='.5',label='XES02: Base level cycle delta')
ax.plot(Qs[6]/Q[6], R[6], 'D',markersize=9,markerfacecolor='.8',label='DB03-2: Subcritical flow delta')
ax.plot(Qs[7]/Q[7], R[7], '^',markersize=9,markerfacecolor='.2',label='BV-1: Braided river')
ax.plot(Qs[8]/Q[8], R[8], '^',markersize=9,markerfacecolor='.8',label='BV-2: Vegetated river')
"""
#plt.xlim( (-.05, plt.xlim()[1]) ) # To see full points on zero
#plt.ylim( (-.1, plt.ylim()[1]) ) # To see full points on zero
#xl = plt.xlim((0,10))
#yl = plt.ylim((0,3))
#ax.plot(cf_x, cf_y,'g--',label=r'\dot{\zeta} = ' + coeff + r'q_s^str(rf[1])')
#plt.xlim(xl)
#plt.ylim(yl)
plt.xlabel('Sediment flux, $q_s$ [m/hr]')
plt.ylabel('Fluvial surface reworking rate, $R$ [1/hr]')
ax.text(0.9, 0.1,'A',horizontalalignment='center',
     verticalalignment='center', fontsize=26, 
     family='sans-serif', weight='bold',
     transform = ax.transAxes)

plt.savefig('../figures/reworking_rate_causes.pdf', transparent=True)
plt.show()

