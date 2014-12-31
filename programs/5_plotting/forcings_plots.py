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

fig = plt.figure(figsize=(10,10))
fig.subplots_adjust(wspace=.4, hspace=.3)

#from matplotlib import rc
#rc('text', usetex=True)
#rc('font', family='serif')

# Nondimensional q_s and rate of lateral motion
# qs* = qs/[D*sqrt(D*g*(s-1)]
qs_star = qs/(D*np.sqrt(D*g*(s-1)))
# zetadot* = sqrt(D*g)
zetadot_star = zetadot / np.sqrt(D*g)

# 1. qs vs. zetadot, loglog
# Curve fit in log space for better fit to all data
#rf, rcov = curve_fit(lin_only_intercept, np.log10(qs), np.log10(zetadot), p0=(2.5))
#cf_x = np.linspace(1E-1, 1E2, 2)
#rf[0] = 10**rf[0]
#cf_y = lin_only_intercept(cf_x,rf[0])
#rs = rsquared(rcov, np.log10(qs), np.log10(zetadot))
# JUST XES02 AND DB03-1
#rf, rcov = curve_fit(lin_no_intercept, qs, zetadot, p0=(2.5))
#cf_x = np.linspace(min(qs)/10.,max(qs)*10.,10)
#cf_y = lin_no_intercept(cf_x,rf[0])
#rs = rsquared(rcov, qs[:6], zetadot[:6])
#fig = plt.figure()
ax = fig.add_subplot(221)
ax.grid(True)
ax.loglog(qs[:5], zetadot[:5], 'o',markersize=9,markerfacecolor='.5',label='XES02')
ax.loglog(qs[5], zetadot[5], 'D',markersize=9,markerfacecolor='.2',label='DB03-1')
ax.loglog(qs[6], zetadot[6], 'D',markersize=9,markerfacecolor='.8',label='DB03-2')
ax.loglog(qs[7], zetadot[7], '^',markersize=9,markerfacecolor='.2',label='BV-1')
ax.loglog(qs[8], zetadot[8], '^',markersize=9,markerfacecolor='.8',label='BV-2')
#xl = plt.xlim()
#yl = plt.ylim()
#plt.xlim(xl)
#plt.ylim((yl[0],100))
#ax.plot(cf_x, cf_y, 'k-')
plt.xlabel('Sediment flux, $q_s$ [m/hr]')
plt.ylabel('Lateral mobility, $\dot{\zeta}$ [m/hr]')
ax.text(0.9, 0.1,'A',horizontalalignment='center',
     verticalalignment='center', fontsize=26, 
     family='sans-serif', weight='bold',
     transform = ax.transAxes)


# 2. qs* vs. zetadot*, loglog
#rf, rcov = curve_fit(lin_no_intercept, QsQ, zetadot_star, p0=(2.5))
#cf_x = np.linspace(min(QsQ)/10.,max(QsQ)*10.,10)
#cf_y = lin_no_intercept(cf_x,rf[0])
#rf, rcov = curve_fit(power, QsQ, zetadot_star, p0=(2.5,2.5))
#cf_x = np.linspace(min(QsQ)/10.,max(QsQ)*10.,10)
#cf_y = power(cf_x,rf[0],rf[1])
# rs = rsquared(rcov, QsQ[:6], zetadot_star[:6]) # Think this is wrong.
#fig = plt.figure()
ax = fig.add_subplot(222)
ax.grid(True)
ax.loglog(QsQ[:5], zetadot_star[:5], 'o',markersize=9,markerfacecolor='.5',label='XES02')
ax.loglog(QsQ[5], zetadot_star[5], 'D',markersize=9,markerfacecolor='.2',label='DB03-1')
ax.loglog(QsQ[6], zetadot_star[6], 'D',markersize=9,markerfacecolor='.8',label='DB03-2')
ax.loglog(QsQ[7], zetadot_star[7], '^',markersize=9,markerfacecolor='.2',label='BV-1')
ax.loglog(QsQ[8], zetadot_star[8], '^',markersize=9,markerfacecolor='.8',label='BV-2')
xl = plt.xlim()
yl = plt.ylim()
#ax.loglog(cf_x, cf_y,'g--')
#plt.xlim(xl)
#plt.ylim((yl[0],100))
#plt.xlabel('$q_s^* = q_s / (D \sqrt{1.65 D g})$  [$-$]')
#ax.plot(cf_x, cf_y, 'k-')
plt.xlabel('Dimensionless sed. discharge $Q_s^* = Q_s / Q$  [$-$]')
plt.ylabel('Dimensionless lat. mobility $\dot{\zeta}^* = \dot{\zeta} / \sqrt{D g}$  [$-$]')
ax.text(0.9, 0.1,'B',horizontalalignment='center',
     verticalalignment='center', fontsize=26, 
     family='sans-serif', weight='bold',
     transform = ax.transAxes)

# 3. zetadot vs avulsion
"""
# Log axes don't cut it: remove data that disagree
# (because f_av = 0: only qs important)
fig = plt.figure()
ax = fig.add_subplot(121)
ax.loglog(zetadot_av, zetadot, 'ko')
#ax.loglog(zetadot_av[2:-2], zetadot[2:-2], 'ko')
ax = fig.add_subplot(122)
#ax.plot(zetadot_av[2:-2], zetadot[2:-2], 'ko')
ax.plot(zetadot_av, zetadot, 'ko')
"""
#fig = plt.figure()
ax = fig.add_subplot(223)
ax.grid(True)
ax.plot(zetadot_av[:5], zetadot[:5], 'o',markersize=9,markerfacecolor='.5',label='XES02')
ax.plot(zetadot_av[5], zetadot[5], 'D',markersize=9,markerfacecolor='.2',label='DB03-1')
ax.plot(zetadot_av[6], zetadot[6], 'D',markersize=9,markerfacecolor='.8',label='DB03-2')
ax.plot(zetadot_av[7], zetadot[7], '^',markersize=9,markerfacecolor='.2',label='BV-1')
ax.plot(zetadot_av[8], zetadot[8], '^',markersize=9,markerfacecolor='.8',label='BV-2')
plt.xlim( (-.05, plt.xlim()[1]) ) # To see full points on zero line
plt.ylim( (-.1, plt.ylim()[1]) ) # To see full points on zero
plt.xlabel('Avulsion magnitude times frequency, $\dot{\zeta}_{\mathrm{av}}$ [m/hr]')
plt.ylabel('Lateral mobility, $\dot{\zeta}$ [m/hr]')
ax.text(0.9, 0.1,'C',horizontalalignment='center',
     verticalalignment='center', fontsize=26, 
     family='sans-serif', weight='bold',
     transform = ax.transAxes)

plt.legend(loc='upper right',numpoints=1,fancybox=True)
leg = plt.gca().get_legend()
ltext  = leg.get_texts()  # all the text.Text instance in the legend
plt.setp(ltext, fontsize='small')    # the legend text fontsize


# 4. R vs. f_av
ax = fig.add_subplot(224)
ax.grid(True)
"""
ax.plot(zetadot_av[:5]/qs[:5], R[:5], 'o',markersize=9,markerfacecolor='.5',label='XES02: Base level cycle delta')
ax.plot(zetadot_av[5]/qs[5], R[5], 'D',markersize=9,markerfacecolor='.2',label='DB03-1: Supercritical flow delta')
ax.plot(zetadot_av[6]/qs[6], R[6], 'D',markersize=9,markerfacecolor='.8',label='DB03-2: Subcritical flow delta')
ax.plot(zetadot_av[7]/qs[7], R[7], '^',markersize=9,markerfacecolor='.2',label='BV-1: Braided river')
ax.plot(zetadot_av[8]/qs[8], R[8], '^',markersize=9,markerfacecolor='.8',label='BV-2: Vegetated river')
"""
ax.plot(zetadot_av[:5], R[:5], 'o',markersize=15,markerfacecolor='.5',label='XES02: Base level cycle delta')
ax.plot(zetadot_av[5], R[5], 'D',markersize=15,markerfacecolor='.2',label='DB03-1: Supercritical flow delta')
ax.plot(zetadot_av[6], R[6], 'D',markersize=15,markerfacecolor='.8',label='DB03-2: Subcritical flow delta')
ax.plot(zetadot_av[7], R[7], '^',markersize=9,markerfacecolor='.2',label='BV-1: Braided river')
ax.plot(zetadot_av[8], R[8], '^',markersize=9,markerfacecolor='.8',label='BV-2: Vegetated river')
plt.xlim( (-.05, plt.xlim()[1]) ) # To see full points on zero
plt.ylim( (-.1, plt.ylim()[1]) ) # To see full points on zero
xl = plt.xlim()
yl = plt.ylim()
#ax.plot(cf_x, cf_y,'g--',label=r'\dot{\zeta} = ' + coeff + r'q_s^str(rf[1])')
plt.xlim(xl)
plt.ylim(yl)
plt.xlabel('Avulsion magnitude times frequency, $\dot{\zeta}_{\mathrm{av}}$ [m/hr]')
plt.ylabel('Fluvial surface reworking rate, $R$ [1/hr]')
ax.text(0.9, 0.1,'D',horizontalalignment='center',
     verticalalignment='center', fontsize=26, 
     family='sans-serif', weight='bold',
     transform = ax.transAxes)
#plt.legend(loc=2,fancybox=True)

#plt.figure()
#plt.plot(f_av, R, 'k.')


#plt.savefig('../figures/mobility_forcings.pdf', transparent=True)
plt.show()

