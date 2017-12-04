import numpy as np
import pandas as pd
import sys

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

nSims = 2500000
if len(sys.argv) >= 2: nSims = int(sys.argv[1])
print('running '+str(nSims)+' times')

univ = pd.read_csv('~/Desktop/CO_7th/myvoters.csv')

nDEM = univ.loc[univ.PARTY == 'DEM'].shape[0]
nDEM_f = univ.loc[(univ.PARTY == 'DEM') & (univ.GENDER == 'F')].shape[0]+(univ.loc[(univ.PARTY == 'DEM') & (univ.GENDER != 'M') & (univ.GENDER != 'F')].shape[0]/2)
nDEM_m = univ.loc[(univ.PARTY == 'DEM') & (univ.GENDER == 'M')].shape[0]+(univ.loc[(univ.PARTY == 'DEM') & (univ.GENDER != 'M') & (univ.GENDER != 'F')].shape[0]/2)

nUAF = univ.loc[univ.PARTY == 'UAF'].shape[0]
nUAF_f = univ.loc[(univ.PARTY == 'UAF') & (univ.GENDER == 'F')].shape[0]+(univ.loc[(univ.PARTY == 'UAF') & (univ.GENDER != 'M') & (univ.GENDER != 'F')].shape[0]/2)
nUAF_m = univ.loc[(univ.PARTY == 'UAF') & (univ.GENDER == 'M')].shape[0]+(univ.loc[(univ.PARTY == 'UAF') & (univ.GENDER != 'M') & (univ.GENDER != 'F')].shape[0]/2)

# PRIORS:
mf_gap = 0.04
# 18-20% of inds voting in primary
# 40% of Dems voting in primary-- check this against history

# 33% home-dist advantage
# 60% of women vote for Britney

danDEM_f = 0.35
danDEM_m = 0.40
danUAF_f = 0.45
danUAF_m = 0.50

my_exp = []

aSim = 0
while aSim <= nSims:
    if aSim%10000 == 0: print(aSim)

    #toDEM = np.random.uniform(0.30,0.55,1)[0]    
    #toUAF = np.random.uniform(0.15,0.25,1)[0]

    toDEM = np.random.normal(np.random.uniform(0.35,0.55,1),0.05,1)[0]
    #toUAF = toDEM/np.random.normal(2.36,0.2,1)[0]
    toUAF = np.random.normal(0.19,0.02,1)[0]

    toDEM_f = (1.+mf_gap/2)*toDEM
    toDEM_m = (1.-mf_gap/2)*toDEM

    toUAF_f = (1.+mf_gap/2)*toUAF
    toUAF_m = (1.-mf_gap/2)*toUAF

    vtrDEM = toDEM_f*nDEM_f+toDEM_m*nDEM_m
    vtrUAF = toUAF_f*nUAF_f+toUAF_m*nUAF_m
    
    # Experiment 1: Dan wins X% of DEMs & Y% of INDs
    # assume independent turnout among DEMs & UAFs

    danDEM = toDEM_f*nDEM_f*np.random.normal(danDEM_f,danDEM_f/10) + toDEM_m*nDEM_m*np.random.normal(danDEM_m,danDEM_m/10)
    danUAF = toUAF_f*nUAF_f*np.random.normal(danUAF_f,danUAF_f/10) + toUAF_m*nUAF_m*np.random.normal(danUAF_m,danUAF_m/10)

    if danDEM < 0: danDEM = 0
    if danUAF < 0: danUAF = 0
    if danDEM > vtrDEM: danDEM = vtrDEM
    if danUAF > vtrUAF: danUAF = vtrUAF

    my_exp.append([100.*vtrDEM/nDEM,100.*vtrUAF/nUAF,100.*(danDEM+danUAF)/(vtrDEM+vtrUAF)])

    aSim += 1

toDEM_bins = [2*x for x in range(15,31)]
toDEM_means = []

toUAF_bins = [2*x for x in range(7,14)]
toUAF_means = []

thresholds = [30,35,40,45,50]
thresholdDEM_wins = [[] for ib in thresholds]
thresholdUAF_wins = [[] for ib in thresholds]

# Calculate averages for DEM turnout bins
for nVal, aVal in enumerate(toDEM_bins):

    # Bin the simulations by DEM turnout
    bin_vals = [xRES for xRES in [an_exp[2] for an_exp in my_exp if (an_exp[0] >= aVal) and (aVal == toDEM_bins[-1] or an_exp[0] < toDEM_bins[nVal+1])]]
    toDEM_means.append(np.average(bin_vals))

    for nTH, aTH in enumerate(thresholds):

        # Within each bin, look at the fraction that exceed a threshold for Dan's vote share
        thresholdDEM_wins[nTH].append(len([xRES for xRES in bin_vals if xRES >= aTH])/len(bin_vals))

# Calculate averages for UAF turnout bins
for nVal, aVal in enumerate(toUAF_bins):
    
    # Bin the simulations by UAF turnout
    bin_vals = [xRES for xRES in [an_exp[2] for an_exp in my_exp if (an_exp[1] >= aVal) and (aVal == toUAF_bins[-1] or an_exp[1] < toUAF_bins[nVal+1])]]
    toUAF_means.append(np.average(bin_vals))

    for nTH, aTH in enumerate(thresholds):

        # Within each bin, look at the fraction that exceed a threshold for Dan's vote share
        try:
            thresholdUAF_wins[nTH].append(len([xRES for xRES in bin_vals if xRES >= aTH])/len(bin_vals))
        except:
            thresholdUAF_wins[nTH].append('n/a')

fig = plt.figure()
ax=fig.gca()
plt.hexbin([an_exp[0] for an_exp in my_exp],[an_exp[2] for an_exp in my_exp], alpha=0.60,cmap='YlGnBu')
ax.annotate(r'Mean [%] $\rightarrow$',xy=(toDEM_bins[0]-1,25),xycoords='data',ha='right',va='center',fontsize=7,weight='bold',annotation_clip=False)
for nBin, aBin in enumerate(toDEM_bins):
    ax.annotate(str(round(toDEM_means[nBin],1)),xy=(aBin+1,25+0.1*(-1)**nBin),xycoords='data',ha='center',va='center',fontsize=6,annotation_clip=False)
    plt.plot([aBin,aBin],[0,100],color='grey')

    for nTH, aTH in enumerate(thresholdDEM_wins):
        b_str = str(round(aTH[nBin]*100.,1))
        if b_str == '100.0': b_str = '100'                    
        ax.annotate(b_str,xy=(aBin+1,thresholds[nTH]+1+0.1*(-1)**nBin),xycoords='data',ha='center',va='center',fontsize=7,annotation_clip=False)

for nTH, aTH in enumerate(thresholds):
    plt.plot([0,100],[thresholds[nTH],thresholds[nTH]],color='grey')
    ax.annotate('Odds of vote\nshare $\geq$ '+str(aTH)+r'% $\rightarrow$',xy=(21,thresholds[nTH]+1),
                xycoords='data',ha='left',va='center',fontsize=7,annotation_clip=False,weight='bold')

plt.xlim(20,65)
plt.ylim(20,60)
ax.set_xlabel('Democratic turnout [% of active Dem. voters]')
ax.set_ylabel('PCT to Dan')
fig.savefig('./plots/dan_vs_dem_turnout.pdf',format='pdf')
print('writing dan_vs_dem_turnout.pdf')

plt.cla()
plt.hexbin([an_exp[1] for an_exp in my_exp], [an_exp[2] for an_exp in my_exp], alpha=0.60,cmap='YlGn')
ax.annotate(r'Mean [%] $\rightarrow$',xy=(toUAF_bins[0]-1,25),xycoords='data',ha='right',va='center',weight='bold',fontsize=7,annotation_clip=False)
for nBin, aBin in enumerate(toUAF_bins):
    ax.annotate(str(round(toUAF_means[nBin],1)),xy=(aBin+1,25+0.1*(-1)**nBin),xycoords='data',ha='center',va='center',fontsize=6,annotation_clip=False)
    plt.plot([aBin,aBin],[0,100],color='grey')

    for nTH, aTH in enumerate(thresholdUAF_wins):
        try:
            b_str = str(round(aTH[nBin]*100.,1))
            if b_str == '100.0': b_str = '100' 
            ax.annotate(b_str,xy=(aBin+1,thresholds[nTH]+1+0.1*(-1)**nBin),xycoords='data',ha='center',va='center',fontsize=7,annotation_clip=False,weight='bold')
        except: pass

for nTH, aTH in enumerate(thresholds):
    plt.plot([0,100],[thresholds[nTH],thresholds[nTH]],color='grey')
    ax.annotate('Odds of vote\nshare $\geq$ '+str(int(aTH))+r'% $\rightarrow$',xy=(11,thresholds[nTH]+1),
                xycoords='data',ha='left',va='center',fontsize=7,annotation_clip=False,weight='bold')

plt.xlim(10,30)
plt.ylim(20,60)
ax.set_xlabel('Unaffiliated turnout [% of active Ind. voters]')
ax.set_ylabel('PCT to Dan [%]')
fig.savefig('./plots/dan_vs_uaf_turnout.pdf',format='pdf')
print('writing dan_vs_ind_turnout.pdf')
plt.close('all')
#ax = fig.gca(projection='3d')

#ax.plot_surface(toDEM, toUAF, danPCT, rstride=8, cstride=8, alpha=0.3)
#cset = ax.contour(toDEM, toUAF, danPCT, zdir='z', offset=-0.1, cmap=cm.coolwarm)
#cset = ax.contour(toDEM, toUAF, danPCT, zdir='x', offset=-0.1, cmap=cm.coolwarm)
#cset = ax.contour(toDEM, toUAF, danPCT, zdir='y', offset=-0.1, cmap=cm.coolwarm)

#ax.set_xlabel('Democratic turnout')
#ax.set_xlim(0.1,0.9)
#ax.set_ylabel('Unaffiliated turnout')
#ax.set_ylim(0.1,0.9)
#ax.set_zlabel('Percent of vote for Dan')
#ax.set_zlim(0.1,0.9)
#plt.show()

# Experiment 2: look at turnout & Britney's advantage among women
