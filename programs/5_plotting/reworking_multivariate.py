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

# Multivariate ordinary least squares
# http://www.scipy.org/Cookbook/OLS
import ols
y = R
x = np.concatenate((np.array([qs]), np.array([zetadot_av]))).transpose() # col 1 = qs, col 2 = zetadot_av
mymodel = ols.ols(y,x,'R',['qs','zetadot_av'])
coeff = mymodel.b
myfit = coeff[0] + qs * coeff[1] + zetadot_av * coeff[2]
plt.plot(myfit, y, 'ko'); plt.show()
plt.plot(coeff[0] + qs * coeff[1] + zetadot_av * coeff[2]); plt.show()

# Now linear regression for no-avulsion, followed by linear regression for avulsion (with no-avulsion correction applied)
# Non-avulsing
Rnoav = np.concatenate((np.array([R[1]]), np.array([R[3]]), R[6:]))
qsnoav = np.concatenate((np.array([qs[1]]), np.array([qs[3]]), qs[6:]))
f1, cov1 = curve_fit(lin_no_intercept, qsnoav, Rnoav, p0=(2.5))
cf_x = np.linspace(0, 5, 2)
cf_y = f1 * cf_x
plt.figure(1)
plt.plot(qsnoav,Rnoav,'ko'); plt.plot(cf_x,cf_y)#; plt.show()
# Subtract non-avulsing curve fit from all data (i.e. qs effects)
Rmod = R - f1*R
f2, cov2 = curve_fit(lin_no_intercept, zetadot_av, Rmod, p0=(2.5))
cf_x = np.linspace(0, 1.2, 2)
cf_y = f2 * cf_x
plt.figure(2)
plt.plot(zetadot_av,Rmod,'ko'); plt.plot(cf_x,cf_y); plt.show()

# Now power law regression for no-avulsion, followed by power law regression for avulsion (with no-avulsion correction applied)
# Non-avulsing
Rnoav = np.concatenate((np.array([R[1]]), np.array([R[3]]), R[6:]))
qsnoav = np.concatenate((np.array([qs[1]]), np.array([qs[3]]), qs[6:]))
f1, cov1 = curve_fit(power, qsnoav, Rnoav, p0=(2.5,2.5))
cf_x = np.linspace(0, 5, 100)
cf_y = f1[0] * cf_x**f1[1]
plt.figure(1)
plt.plot(qsnoav,Rnoav,'ko'); plt.plot(cf_x,cf_y)#; plt.show()
plt.xlabel(r'$q_s$', fontsize=16)
plt.ylabel(r'$R$', fontsize=16)
plt.title('Power law fit to data with no significant avulsions')
# Subtract non-avulsing curve fit from all data (i.e. qs effects)
Rmod = R - f1[0]*R**f1[1]
f2, cov2 = curve_fit(power, zetadot_av, Rmod, p0=(2.5,2.5))
cf_x = np.linspace(0, 1.2, 100)
cf_y = f2[0] * cf_x**f2[1]
plt.figure(2)
plt.plot(zetadot_av,Rmod,'ko'); plt.plot(cf_x,cf_y)
plt.xlabel(r'$\dot{\zeta}_{av}$', fontsize=16)
plt.ylabel(r'$R$', fontsize=16)
plt.title(r'Power law fit to all data, corrected for $q_s$ influences')
plt.show()

#plt.plot(zetadot_av,R,'ko'); plt.plot(cf_x,cf_y); plt.show()

# Now power law regression for no-avulsion, followed by linear regression for avulsion (with no-avulsion correction applied)
# Non-avulsing
Rnoav = np.concatenate((np.array([R[1]]), np.array([R[3]]), R[6:]))
qsnoav = np.concatenate((np.array([qs[1]]), np.array([qs[3]]), qs[6:]))
f1, cov1 = curve_fit(power, qsnoav, Rnoav, p0=(2.5,2.5))
cf_x = np.linspace(0, 5, 100)
cf_y = f1[0] * cf_x**f1[1]
plt.figure(1)
plt.plot(qsnoav,Rnoav,'ko'); plt.plot(cf_x,cf_y)#; plt.show()
# Subtract non-avulsing curve fit from all data (i.e. qs effects)
Rmod = R - f1[0]*R**f1[1]
f2, cov2 = curve_fit(lin_no_intercept, zetadot_av, Rmod, p0=(2.5))
cf_x = np.linspace(0, 1.2, 2)
cf_y = f2 * cf_x
plt.figure(2)
plt.plot(zetadot_av,Rmod,'ko'); plt.plot(cf_x,cf_y); plt.show()



fig = plt.figure(figsize=(5,5))
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

