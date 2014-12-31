#! /usr/bin/python

# Started 1 JAN 2012 by ADW: New Year's Day!

from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit # Nonlinear least squares
from matplotlib import rc

data = np.genfromtxt('measured_parameters_31DEC2011.txt')

experiments = ['XES02-SS', 'XES02-SF', 'XES02-SR', 'XES02-RF', 'XES02-RR', 'DB03-1', 'DB03-2', 'BV-1', 'BV-2']

# Not needed - internal TeX handles it fine
#rc('text', usetex=True)
#rc('font', family='serif')

# Order: XES(5), DB03-1, DB03-2, BV-1 (noveg), BV-2 (veg)

# Import variables
aM = data[:,0]
M = data[:,1] # Loss of channel planform overlap [1/hr]
aR = data[:,4]
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
qs = data[:,14] / h # sed flux [m/hr]
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

fig = plt.figure(figsize=(10,10))
fig.subplots_adjust(wspace=.4, hspace=.4)

# A: Scaled zetadot_f vs R
# All these old ones here
# Need to figure out what to do with this

ax = fig.add_subplot(221)
ax.loglog(zetadot_fR, R, 'ko')
plt.xlim( (-.5, plt.xlim()[1]) ) # To see full points on zero
plt.ylim( (-.1, plt.ylim()[1]) ) # To see full points on zero
ax.loglog([1E-4, 1E4],[1E-4, 1E4],'g-',label='Unity')
plt.xlim((1E-2,1E1))
plt.ylim((1E-2,1E1))
plt.legend(loc=2,fancybox=True)
leg = plt.gca().get_legend()
ltext  = leg.get_texts()  # all the text.Text instance in the legend
plt.setp(ltext, fontsize='small')    # the legend text fontsize
plt.xlabel('Rate of channel planform as a fraction\nof unchannelized reworkable fluvial surface,\n' + r'$\dot{\zeta}_f / (f_d (1 - p_R))$ [1/hr]',horizontalalignment='center', verticalalignment='top')
plt.ylabel('Fluvial surface reworking rate,\n' + r'$R$ [1/hr]', horizontalalignment='center')
ax.text(0.9, 0.1,'A',horizontalalignment='center',
     verticalalignment='center', fontsize=26, 
     family='sans-serif', weight='bold',
     transform = ax.transAxes)
#ax.text(0.1, 0.9,'Line is unity',
#        horizontalalignment='left',
#        verticalalignment='center', 
#        transform = ax.transAxes)
xl = [100, 100, 60, 0, 60, -15, 0, 0, 35]
yl = [-10, -20, -30, 65, -30, 0,  -60,   15, 35]
il = 0
for label,x,y in zip(experiments,zetadot_fR,R):
  if il >= 5:
    plt.annotate(label, 
      xy=(x,y), xytext=(xl[il],yl[il]), 
      textcoords='offset points', ha='right', va='bottom',
      #bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
      arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
      )
  il+=1

# B. \tau_R vs \tau_{\mathrm{fs},R}
R2 = R * (aR - pR)

f, cov = curve_fit(lin_no_intercept, np.array(list(tau_fsR[:rm]) + list(tau_fsR[rm+1:])), 3/np.array(list(R2[:rm]) + list(R2[rm+1:])) , 
sigma = np.sqrt( (np.array(list(tau_fsR[:rm]) + list(tau_fsR[rm+1:])))**2 + (3/np.array(list(R2[:rm]) + list(R2[rm+1:])))**2) )
cf_x = np.linspace(1E-2,1E2,500)
cf_y = lin_no_intercept( cf_x, f[0] )
# cf_y = lin_no_intercept( cf_x, linfit[0] )

ax = fig.add_subplot(222)
ax.loglog(tau_fsR, 3/(R*(aR-pR)), 'ko')
ax.loglog(cf_x, cf_y,'g--')
ax.loglog(cf_x, 3.16*cf_x,'r-.', label=r'${\tau_M}/{\tau_{\mathrm{ch,M}}}$ = 3.16')
ax.loglog([1E-4, 1E4],[1E-4, 1E4],'g-', label=r'${\tau_M}/{\tau_{\mathrm{ch,M}}}$ = 1')
plt.xlim((1E-1,1E2))
plt.ylim((1E-1,1E2))
plt.legend(loc=2,fancybox=True)
leg = plt.gca().get_legend()
ltext  = leg.get_texts()  # all the text.Text instance in the legend
plt.setp(ltext, fontsize='small')    # the legend text fontsize
plt.xlabel('Shortest possible time for 95\% fluvial\n surface reworking, ' + r'$\tau _{\mathrm{fs,R}}$',horizontalalignment='center')
plt.ylabel('Time required for 95\% fluvial surface\n reworking, ' + r'$\tau_R = 3/R$ [hr]',horizontalalignment='center')
ax.text(0.9, 0.1,'B',horizontalalignment='center',
     verticalalignment='center', fontsize=26, 
     family='sans-serif', weight='bold',
     transform = ax.transAxes)
ax.text(0.1, 0.9,r'$\frac{\tau_R}{\tau_{\mathrm{fs,R}}}$ = ' + '%.2f' %f[0],
        horizontalalignment='left',
        verticalalignment='center', 
        transform = ax.transAxes)
xl = [100, 100, 60, 0, 60, -15, 0, 0, 35]
yl = [-10, -20, -30, 65, -30, 0,  -60,   15, 35]
il = 0
for label,x,y in zip(experiments,tau_fsR,3/R):
  if il >= 5:
    plt.annotate(label, 
      xy=(x,y), xytext=(xl[il],yl[il]), 
      textcoords='offset points', ha='right', va='bottom',
      #bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
      arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
      )
  il+=1

print f


# C. \tau_M vs \tau{\mathrm{ch},M}
#M2 = M * (aM - pM)

f, cov = curve_fit(lin_no_intercept, np.array(list(tau_chM[:rm]) + list(tau_chM[rm+1:])), 3/np.array(list(M[:rm]) + list(M[rm+1:])),
sigma = np.sqrt( (np.array(list(tau_chM[:rm]) + list(tau_chM[rm+1:])))**2 + (3/np.array(list(M[:rm]) + list(M[rm+1:])))**2 ) ) 
cf_y = lin_no_intercept( cf_x, f[0] )

ax = fig.add_subplot(223)
ax.loglog(tau_chM, 3/M, 'ko')
ax.loglog(cf_x, cf_y,'g--')
ax.loglog(cf_x, 3.16*cf_x,'r-.', label=r'${\tau_M}/{\tau_{\mathrm{ch,M}}}$ = 3.16')
ax.loglog([1E-4, 1E4],[1E-4, 1E4],'g-', label=r'${\tau_M}/{\tau_{\mathrm{ch,M}}}$ = 1')
plt.xlim((1E-2,1E2))
plt.ylim((1E-2,1E2))
plt.legend(loc=2,fancybox=True)
leg = plt.gca().get_legend()
ltext  = leg.get_texts()  # all the text.Text instance in the legend
plt.setp(ltext, fontsize='small')    # the legend text fontsize
#llines = leg.get_lines()  # all the lines.Line2D instance in the legend
#frame  = leg.get_frame()  # the patch.Rectangle instance surrounding the legend

plt.xlabel('Shortest possible time for 95\% loss\n of planform overlap, ' + r'$\tau _{\mathrm{ch,M}}$',horizontalalignment='center')
plt.ylabel('Time required for 95\% loss of planform\noverlap, ' + r'$\tau_M = 3/M$ [hr]',horizontalalignment='center')
ax.text(0.9, 0.1,'C',horizontalalignment='center',
     verticalalignment='center', fontsize=26, 
     family='sans-serif', weight='bold',
     transform = ax.transAxes)
#ax.text(0.1, 0.9,r'$\frac{\tau_M}{\tau_{\mathrm{ch,M}}}$ = ' + '%.2f' %f[0],
#        horizontalalignment='left',
#        verticalalignment='center', 
#        transform = ax.transAxes)

xl = [100, 100, 60, 0, 60, -15, 0, 0, 35]
yl = [-10, -20, -30, 65, -30, 0,  -60,   15, 35]
il = 0
for label,x,y in zip(experiments,tau_chM,3/M):
  if il >= 5:
    plt.annotate(label, 
      xy=(x,y), xytext=(xl[il],yl[il]), 
      textcoords='offset points', ha='right', va='bottom',
      #bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
      arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
      )
  il+=1

"""
fig = plt.figure()
ax = fig.add_subplot(111)
ax.loglog(etadot_av+1E-10, zetadot, 'ko')
"""

# D. \tau_R vs \tau_M

#f, cov = curve_fit(power, 3/np.array(list(R[:rm]) + list(R[rm+1:])), 3/np.array(list(M[:rm]) + list(M[rm+1:])), 
#sigma= np.sqrt( (3/np.array(list(R[:rm]) + list(R[rm+1:])))**2 + (3/np.array(list(M[:rm]) + list(M[rm+1:])))**2) )
#cf_y = power(cf_x,f[0],f[1])
f, cov = curve_fit(lin_no_intercept, np.array(list(RBR[:rm]) + list(RBR[rm+1:])), np.array(list(MbM[:rm]) + list(MbM[rm+1:])), 
sigma= np.sqrt( (np.array(list(RBR[:rm]) + list(RBR[rm+1:])))**2 + (np.array(list(MbM[:rm]) + list(MbM[rm+1:])))**2) )
cf_y = lin_no_intercept( cf_x, f[0] )

#fig = plt.figure()
ax = fig.add_subplot(224)
#plt.loglog(3/R * fw, 3/M, 'ko')
ax.plot(RBR, MbM, 'ko')
#ax.loglog(cf_x, cf_y,'g--')
#ax.plot(cf_x, cf_y,'g--')
#ax.loglog([1E-4, 1E4],[1E-4, 1E4],'g-')
ax.plot([0,10],[0,10],'g-',label='Unity')
plt.xlim((0,1.4))
plt.ylim((0,1.4))
#plt.xlim((1E-2,1E1))
#plt.ylim((1E-2,1E1))
plt.legend()
leg = plt.gca().get_legend()
ltext  = leg.get_texts()  # all the text.Text instance in the legend
plt.setp(ltext, fontsize='small')    # the legend text fontsize
#plt.xlabel('Time required for 95\% fluvial surface\n reworking, ' + r'$\tau_R = 3/R$ [hr]',horizontalalignment='center')
#plt.ylabel('Time required for 95\% loss of planform\noverlap, ' + r'$\tau_M = 3/M$ [hr]',horizontalalignment='center')
plt.xlabel('Scaled fluvial surface reworking rate,\n' + r"$R \cdot (B-b)^'_*$ [1/hr]",horizontalalignment='center')
plt.ylabel('Scaled rate of loss of planform\noverlap, ' + r"$M \cdot b^'_*$ [1/hr]",horizontalalignment='center')
ax.text(0.9, 0.1,'D',horizontalalignment='center',
     verticalalignment='center', fontsize=26, 
     family='sans-serif', weight='bold',
     transform = ax.transAxes)
# NOT DYNAMIC: CAN'T FIGURE OUT HOW TO DO IT IN EXPONENT
#ax.text(0.1, 0.9,r'$\tau_R$ = ' + '%.2f' %f[0] + r'$\tau_M^{0.90}$' ,
#        horizontalalignment='left',
#        verticalalignment='center', 
#        transform = ax.transAxes)
#ax.text(0.1, 0.9,r'$\frac{\tau_M}{\tau_{R}}$ = ' + '%.2f' %f[0],
#        horizontalalignment='left',
#        verticalalignment='center', 
#        transform = ax.transAxes)
#ax.text(0.1, 0.9,'Line is unity',
#        horizontalalignment='left',
#        verticalalignment='center', 
#        transform = ax.transAxes)
xl = [100, 100, 60, 0, 60, -15, 0, 0, 35]
yl = [-10, -20, -30, 65, -30, 0,  -60,   15, 35]
il = 0
for label,x,y in zip(experiments,RBR,MbM):
  if il >= 5:
    plt.annotate(label, 
      xy=(x,y), xytext=(xl[il],yl[il]), 
      textcoords='offset points', ha='right', va='bottom',
      #bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
      arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
      )
  il+=1


#plt.savefig('/home/awickert/Documents/geology_docs/papers/Working copies/Channel mobility - methods/figures/timescale_comparison.pdf', transparent=True)
plt.show()

