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

# Calculate variables
qs = data[:,14]# / h # sed flux [m/hr] - 20 FEB HAS /h IN THE CALC ALREADY
f_av = etadot/h
etadot_av = b * f_av # Avulsion magnitude * frequency [m/hr]
# etadot_mig = q_s * \Xi * porosity (anything else?); \Xi-ish will be our slope

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

fig = plt.figure(figsize=(10,10))
fig.subplots_adjust(wspace=.4, hspace=.3)

# 1.d. M vs R
# All these old ones here
# Need to figure out what to do with this

# 2. zetadot vs. qs
#qs_vs_mig, qs_vs_mig_cov = curve_fit(lin_no_intercept, qs[2:-2], zetadot[2:-2])
qs_vs_mig, qs_vs_mig_cov = curve_fit(lin_no_intercept, qs[:-2], zetadot[:-2]) 
qs_vs_mig, qs_vs_mig_cov = curve_fit(power, qs[:-2], zetadot[:-2])
#qs_vs_mig, qs_vs_mig_cov = curve_fit(lin, qs[:-2], zetadot[:-2])
cf_x = np.linspace(1E-2,1E2,500)
#cf_y = lin(cf_x,qs_vs_mig[0],qs_vs_mig[1])
#cf_y = qs_vs_mig[0] * cf_x
cf_y = qs_vs_mig[0] * cf_x**qs_vs_mig[1]

#from matplotlib import rc
#rc('text', usetex=True)
#rc('font', family='serif')

ax = fig.add_subplot(221)
ax.grid(True)
ax.plot(qs[:5], zetadot[:5], 'o',markersize=9,markerfacecolor='.5',label='XES02')
ax.plot(qs[5], zetadot[5], 'D',markersize=9,markerfacecolor='.2',label='DB03-1')
ax.plot(qs[6], zetadot[6], 'D',markersize=9,markerfacecolor='.8',label='DB03-2')
ax.plot(qs[7], zetadot[7], '^',markersize=9,markerfacecolor='.2',label='BV-1')
ax.plot(qs[8], zetadot[8], '^',markersize=9,markerfacecolor='.8',label='BV-2')
plt.xlim( (-.5, plt.xlim()[1]) ) # To see full points on zero
plt.ylim( (-.1, plt.ylim()[1]) ) # To see full points on zero
xl = plt.xlim()
yl = plt.ylim()
#ax.plot(cf_x, cf_y,'g--',label=r'\dot{\zeta} = 2.11 q_s^0.67')
plt.xlim(xl)
plt.ylim(yl)
plt.xlabel('Sediment flux, $q_s$ [m/hr]')
plt.ylabel('Lateral mobility, $\dot{\zeta}$ [m/hr]')
ax.text(0.9, 0.1,'A',horizontalalignment='center',
     verticalalignment='center', fontsize=26, 
     family='sans-serif', weight='bold',
     transform = ax.transAxes)
#ax.loglog(qs[:-2], zetadot[:-2], 'b.')
#plt.show()
#plt.legend(loc=2,fancybox=True)

# 2. qs vs. zetadot, loglog
#fig = plt.figure()
ax = fig.add_subplot(222)
ax.grid(True)
ax.loglog(qs[:5], zetadot[:5], 'o',markersize=9,markerfacecolor='.5',label='XES02')
ax.loglog(qs[5], zetadot[5], 'D',markersize=9,markerfacecolor='.2',label='DB03-1')
ax.loglog(qs[6], zetadot[6], 'D',markersize=9,markerfacecolor='.8',label='DB03-2')
ax.loglog(qs[7], zetadot[7], '^',markersize=9,markerfacecolor='.2',label='BV-1')
ax.loglog(qs[8], zetadot[8], '^',markersize=9,markerfacecolor='.8',label='BV-2')
xl = plt.xlim()
yl = plt.ylim()
#ax.loglog(cf_x, cf_y,'g--')
plt.xlim(xl)
plt.ylim((yl[0],100))
plt.xlabel('Sediment flux, $q_s$ [m/hr]')
plt.ylabel('Lateral mobility, $\dot{\zeta}$ [m/hr]')
ax.text(0.9, 0.1,'B',horizontalalignment='center',
     verticalalignment='center', fontsize=26, 
     family='sans-serif', weight='bold',
     transform = ax.transAxes)

plt.legend(loc=2,numpoints=1,fancybox=True)
leg = plt.gca().get_legend()
ltext  = leg.get_texts()  # all the text.Text instance in the legend
plt.setp(ltext, fontsize='small')    # the legend text fontsize


# 3. zetadot vs avulsion
"""
# Log axes don't cut it: remove data that disagree
# (because f_av = 0: only qs important)
fig = plt.figure()
ax = fig.add_subplot(121)
ax.loglog(etadot_av, zetadot, 'ko')
#ax.loglog(etadot_av[2:-2], zetadot[2:-2], 'ko')
ax = fig.add_subplot(122)
#ax.plot(etadot_av[2:-2], zetadot[2:-2], 'ko')
ax.plot(etadot_av, zetadot, 'ko')
"""
#fig = plt.figure()
ax = fig.add_subplot(223)
ax.grid(True)
ax.plot(etadot_av[:5], zetadot[:5], 'o',markersize=9,markerfacecolor='.5',label='XES02: Base level cycle delta')
ax.plot(etadot_av[5], zetadot[5], 'D',markersize=9,markerfacecolor='.2',label='DB03-1: Supercritical flow delta')
ax.plot(etadot_av[6], zetadot[6], 'D',markersize=9,markerfacecolor='.8',label='DB03-2: Subcritical flow delta')
ax.plot(etadot_av[7], zetadot[7], '^',markersize=9,markerfacecolor='.2',label='BV-1: Braided river')
ax.plot(etadot_av[8], zetadot[8], '^',markersize=9,markerfacecolor='.8',label='BV-2: Vegetated river')
plt.xlim( (-.05, plt.xlim()[1]) ) # To see full points on zero line
plt.ylim( (-.1, plt.ylim()[1]) ) # To see full points on zero
plt.xlabel('Avulsion magnitude times frequency, $\dot{\zeta}_{\mathrm{av}}$ [m/hr]')
plt.ylabel('Lateral mobility, $\dot{\zeta}$ [m/hr]')
ax.text(0.9, 0.1,'C',horizontalalignment='center',
     verticalalignment='center', fontsize=26, 
     family='sans-serif', weight='bold',
     transform = ax.transAxes)

"""
fig = plt.figure()
ax = fig.add_subplot(111)
ax.loglog(etadot_av+1E-10, zetadot, 'ko')
"""

# 4. R vs. f_av
rf, rcov = curve_fit(lin, etadot_av, R, p0=(2.5,.6))
cf_x = np.linspace(-5,10,50)
cf_y = lin(cf_x,rf[0],rf[1])

#fig = plt.figure()
ax = fig.add_subplot(224)
ax.grid(True)
ax.plot(etadot_av[:5], R[:5], 'o',markersize=9,markerfacecolor='.5',label='XES02: Base level cycle delta')
ax.plot(etadot_av[5], R[5], 'D',markersize=9,markerfacecolor='.2',label='DB03-1: Supercritical flow delta')
ax.plot(etadot_av[6], R[6], 'D',markersize=9,markerfacecolor='.8',label='DB03-2: Subcritical flow delta')
ax.plot(etadot_av[7], R[7], '^',markersize=9,markerfacecolor='.2',label='BV-1: Braided river')
ax.plot(etadot_av[8], R[8], '^',markersize=9,markerfacecolor='.8',label='BV-2: Vegetated river')
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


plt.savefig('/home/awickert/Documents/geology_docs/papers/Working copies/Channel mobility - methods/figures/mobility_forcings.pdf', transparent=True)
plt.show()

