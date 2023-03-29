import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

coldGas = pd.read_table('../GCEModel/Enrichment_Log_ColdGas.txt', index_col=False, delimiter = ',\s')
events  = pd.read_table('../GCEModel/Events.txt', index_col=False, delimiter = ',\s')

# print(df)
# # print(data.colnames)
# print(df.iloc[0])

# print(df.columns)

# print(df['RingIndex'][30:60])
# print(df['RingRadius'][30:60])


# mask = (df['RingIndex']==40)

# print(df[mask])

# print(df[mask]['Time'][-10:], df[mask]['Stellar_Fe'][-10:])
# print(data['Time'])
# print(dataTotal)



# By looking through Testing folder of RAMICES_II repo I think 
# Total_Fe in Enrichment_Log_ColdGas is [Fe/H]
# and StarMassFormed in Events is SM formed in timestep.
# Match on ring and time to get stellar mass formed in each ring at each [Fe/H]
# - doesn't account for migration, but J mentioned this was a fudge

ringNum = 100
stepNum = 1200

#Evolution of each ring
for i in range(ringNum):
    ringEvents = events[events['RingIndex'] == i ]
    ringColdGas = coldGas[coldGas['RingIndex'] == i ]
    
    # fig, ax = plt.subplots()
    # ax.plot(ringColdGas['Time'], ringColdGas['Total_Fe'])
    # looks right, montonically increases to 0.0(outer disk)-0.5(inner disk)
    
    
    
# Evolution of sine morte [Fe/H] distribution

FeBinNum = 35
FeBins = np.linspace(-3,0.5, num=FeBinNum+1)
# FeHist = np.zeros(FeBinNum)
ringRadii = np.linspace(0, 20, num=ringNum+1)
times = [0.5, 2, 12-4.5, 12]

fig,ax = plt.subplots()
for t in reversed(times):
    timeEvents = events[events['Time']<=t]
    timeColdGas = coldGas[coldGas['Time']<=t]
    # getting points before each time lim
    
    
    out = ax.hist(timeColdGas['Total_Fe'],  bins=FeBins,
            weights=timeEvents['StarMassFormed'], 
            label = str(t)+'Gyr')
    print(out)
ax.set_ylabel('Sine Morte Stellar Mass Distribution')
ax.set_xlabel('[Fe/H]')
ax.legend()
fig.savefig('../plots/stars.png', dpi=300)
    
# ISO distribution
FeH_p = np.array([-0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4])
fH2O_p = np.array([0.5098, 0.4905, 0.4468, 0.4129, 0.3563, 0.2918, 0.2173, 0.1532, 0.06516])
compPoly = np.polynomial.polynomial.Polynomial.fit(FeH_p, fH2O_p, 3)
FeHLow = FeH_p[0]
FeHHigh = FeH_p[-1]
fH2OLow = compPoly(FeH_p[-1])
fH2OHigh = compPoly(FeH_p[0])
def comp(FeH):
    return np.where(FeHLow<=FeH, np.where(FeH<FeHHigh,
                                          compPoly(FeH),
                                          fH2OLow), fH2OHigh)

beta=1
fHHOBins = np.linspace(fH2OLow+0.0001, fH2OHigh-0.0001)
fig,ax = plt.subplots()
for t in reversed(times):
    timeEvents = events[events['Time']<=t]
    timeColdGas = coldGas[coldGas['Time']<=t]
    # getting points before each time lim
    
    out = ax.hist(comp(timeColdGas['Total_Fe']),  bins=fHHOBins,
            weights=timeEvents['StarMassFormed']*10**(beta*timeColdGas['Total_Fe']),
            label = str(t)+'Gyr')
    print(out)
ax.set_ylabel('ISO Distribution')
ax.set_xlabel('fH2O')
ax.legend()
fig.savefig('../plots/ISOs.png', dpi=300)


totals=[]
starTotals=[]
fineTimes=np.linspace(0,12)
for t in fineTimes:
    timeEvents = events[events['Time']<=t]
    timeColdGas = coldGas[coldGas['Time']<=t]
    starTotals.append(timeEvents['StarMassFormed'].sum())
    totals.append((timeEvents['StarMassFormed']*10**(beta*timeColdGas['Total_Fe'])).sum())
    
fig,ax = plt.subplots()
ax.plot(fineTimes, starTotals, label='stars')
ax.plot(fineTimes, totals, label='ISOs')
ax.set_xlabel('time')
ax.legend()
fig.savefig('../plots/starsvISOs.png', dpi=300)



    
