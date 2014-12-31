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
ax = fig.add_subplot(221)
ax.grid(True)
ax.loglog(qs[:5], zetadot[:5], 'o',markersize=9,markerfacecolor='.5',label='XES02')
ax.loglog(qs[5], zetadot[5], 'D',markersize=9,markerfacecolor='.2',label='DB03-1')
ax.loglog(qs[6], zetadot[6], 'D',markersize=9,markerfacecolor='.8',label='DB03-2')
ax.loglog(qs[7], zetadot[7], '^',markersize=9,markerfacecolor='.2',label='BV-1')
ax.loglog(qs[8], zetadot[8], '^',markersize=9,markerfacecolor='.8',label='BV-2')
plt.xlabel('Sediment flux, $q_s$ [m/hr]')
plt.ylabel('Lateral mobility, $\dot{\zeta}$ [m/hr]')
ax.text(0.9, 0.1,'A',horizontalalignment='center',
     verticalalignment='center', fontsize=26, 
     family='sans-serif', weight='bold',
     transform = ax.transAxes)
ax.text(0.05, 0.95, 'Channel mobility increases with\nincreasing sediment flux', transform = ax.transAxes, style='italic', size='medium', horizontalalignment='left', verticalalignment='top')

# 2. qs* vs. zetadot*, loglog
ax = fig.add_subplot(222)
ax.grid(True)
ax.loglog(QsQ[:5], zetadot_star[:5], 'o',markersize=9,markerfacecolor='.5',label='XES02')
ax.loglog(QsQ[5], zetadot_star[5], 'D',markersize=9,markerfacecolor='.2',label='DB03-1')
ax.loglog(QsQ[6], zetadot_star[6], 'D',markersize=9,markerfacecolor='.8',label='DB03-2')
ax.loglog(QsQ[7], zetadot_star[7], '^',markersize=9,markerfacecolor='.2',label='BV-1')
ax.loglog(QsQ[8], zetadot_star[8], '^',markersize=9,markerfacecolor='.8',label='BV-2')
xl = plt.xlim()
yl = plt.ylim()
plt.xlabel('Dimensionless sed. discharge $Q_s^* = Q_s / Q$  [$-$]')
plt.ylabel('Dimensionless lat. mobility $\dot{\zeta}^* = \dot{\zeta} / \sqrt{D g}$  [$-$]')
ax.text(0.05, 0.95, 'Dimensionless channel mobility\nincreases with increasing\nsediment-to-water\ndischarge ratio', transform = ax.transAxes, style='italic', size='medium',horizontalalignment='left', verticalalignment='top')
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

handles, labels = ax.get_legend_handles_labels()
#handles = [handles[0], handles[0], handles[1], handles[2], handles[0], handles[3], handles[4]]
#labels = ['', labels[0], labels[1], labels[2], '', labels[3], labels[4]]
#plt.legend(handles, labels, loc='upper right',numpoints=1,fancybox=True)
plt.legend(handles[:3], labels[:3], loc='upper right', bbox_to_anchor=(1, 1), numpoints=1, fancybox=True)
leg = plt.gca().get_legend()
leg.set_title('Deltas')
ltext  = leg.get_texts()  # all the text.Text instance in the legend
plt.setp(ltext, fontsize='small')    # the legend text fontsize

leg2 = plt.legend(handles[3:], labels[3:], loc='upper right', numpoints=1, bbox_to_anchor=(0.6, 1), fancybox=True)
leg2.set_title('Inland\nRivers')
ltext2  = leg2.get_texts()  # all the text.Text instance in the legend
plt.setp(ltext2, fontsize='small')    # the legend text fontsize
plt.gca().add_artist(leg)
ax.text(0.15, 0.4, 'Avulsions play little role\nin setting overall\nchannel mobility', horizontalalignment='left', verticalalignment='center', style='italic')

"""
line1 = plt.text(0,0,'DELTAS')
line2 = plt.Line2D(range(1), range(1), color="white", marker='o',markerfacecolor="green")
line3 = plt.Line2D(range(1), range(1), color="white", marker='o',markersize=5, markerfacecolor="slategray")
line4 = plt.Line2D(range(1), range(1), color="white", marker='o',markersize=10,markerfacecolor="slategray")
plt.legend((line1,line2,line3,line4),('Thing 1','Thing 2', 'Thing 3', 'Thing 4'),numpoints=1, loc=1)
"""

# 4. f_av vs. R
ax = fig.add_subplot(224)
ax.grid(True)
"""
ax.plot(zetadot_av[:5]/qs[:5], R[:5], 'o',markersize=9,markerfacecolor='.5',label='XES02: Base level cycle delta')
ax.plot(zetadot_av[5]/qs[5], R[5], 'D',markersize=9,markerfacecolor='.2',label='DB03-1: Supercritical flow delta')
ax.plot(zetadot_av[6]/qs[6], R[6], 'D',markersize=9,markerfacecolor='.8',label='DB03-2: Subcritical flow delta')
ax.plot(zetadot_av[7]/qs[7], R[7], '^',markersize=9,markerfacecolor='.2',label='BV-1: Braided river')
ax.plot(zetadot_av[8]/qs[8], R[8], '^',markersize=9,markerfacecolor='.8',label='BV-2: Vegetated river')
"""
ax.plot(zetadot_av[:5], R[:5], 'o',markersize=9,markerfacecolor='.5',label='XES02: Base level cycle delta')
ax.plot(zetadot_av[5], R[5], 'D',markersize=9,markerfacecolor='.2',label='DB03-1: Supercritical flow delta')
ax.plot(zetadot_av[6], R[6], 'D',markersize=9,markerfacecolor='.8',label='DB03-2: Subcritical flow delta')
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
ax.hlines(y=(-0.05,1.05), xmin=-0.02, xmax=0.04, linewidth=1)
ax.vlines(0.04, -0.05, 1.05, linewidth=1)
ax.annotate('Reworking rates in\nsystems with little to\nno aggradation scale\nwith sediment flux', xy=(0.05, 0.4),  xycoords='data',
            xytext=(0.2, 0.4), style='italic',
            arrowprops=dict(facecolor='black', shrink=0.1, width=2, frac=.3, headwidth=8),
            horizontalalignment='left', verticalalignment='center')
ax.text(0.33, 2.3, 'The higher reworking\nrates in aggrading systems\nare driven by avulsions', horizontalalignment='center', verticalalignment='center', style='italic', rotation=37)
#ax.arrow(0.5,0.5,0.1,0.1, linewidth=0.1, head_width=0.2, length_includes_head=True, shape='full', transform = ax.transAxes)

"""
# 5. q_s vs. R
ax = fig.add_subplot(225)
ax.grid(True)
# experiment_names = ['XES02-SS', 'XES02-SF', 'XES02-SR', 'XES02-RF', 'XES02-RR', 'DB03-1', 'DB03-2', 'BV-1', 'BV-2']
ax.plot(qs[:2], R[:2], 'o',markersize=21,markerfacecolor='.5',label='XES02: Base level cycle delta')
ax.plot(qs[2], R[2], 'o',markersize=9,markerfacecolor='.5',label='XES02: Base level cycle delta')
ax.plot(qs[3], R[3], 'o',markersize=21,markerfacecolor='.5',label='XES02: Base level cycle delta')
ax.plot(qs[4], R[4], 'o',markersize=9,markerfacecolor='.5',label='XES02: Base level cycle delta')
ax.plot(qs[5], R[5], 'D',markersize=9,markerfacecolor='.2',label='DB03-1: Supercritical flow delta')
ax.plot(qs[6], R[6], 'D',markersize=9,markerfacecolor='.8',label='DB03-2: Subcritical flow delta')
ax.plot(qs[7], R[7], '^',markersize=21,markerfacecolor='.2',label='BV-1: Braided river')
ax.plot(qs[8], R[8], '^',markersize=21,markerfacecolor='.8',label='BV-2: Vegetated river')
#plt.xlim( (-.05, plt.xlim()[1]) ) # To see full points on zero
#plt.ylim( (-.1, plt.ylim()[1]) ) # To see full points on zero
#xl = plt.xlim((0,10))
#yl = plt.ylim((0,3))
#ax.plot(cf_x, cf_y,'g--',label=r'\dot{\zeta} = ' + coeff + r'q_s^str(rf[1])')
#plt.xlim(xl)
#plt.ylim(yl)
plt.xlabel('Sediment flux, $q_s$ [m/hr]')
plt.ylabel('Fluvial surface reworking rate, $R$ [1/hr]')
ax.text(0.9, 0.1,'E',horizontalalignment='center',
     verticalalignment='center', fontsize=26, 
     family='sans-serif', weight='bold',
     transform = ax.transAxes)
"""

plt.savefig('../figures/mobility_forcings.pdf', transparent=True)
plt.show()

