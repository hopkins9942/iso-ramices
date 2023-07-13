import galpy
from galpy.orbit import Orbit
from galpy.potential import MWPotential2014 as mwp14
import astropy.units as u

import numpy as np
import matplotlib.pyplot as plt

o = Orbit([1,
            0,
            1,
            1/8, #/8 for scaling to galpy's natural units
            0,
            0])
o.integrate(np.linspace(0,10,101), mwp14)
o.plot()


# for small variations in R, maximum z is appproximately R-independant
# Therefore max z to jz can be apprximated by starting orbits at different
# z values, no veloicty, and measure jz
#

zs = np.linspace(0,1,101)
jzs = np.zeros(len(zs))
for i in range(len(zs)):
    o = Orbit([1,
                0,
                1,
                zs[i]/8, #/8 for scaling to galpy's natural units
                0,
                0])
    jzs[i] = o.jz(pot=mwp14)*(220 * 8) # scaling from natual to physical
    
print(jzs)


def Jz(z):
    A = 37.7
    B = 24.5
    return np.where(z<0.1, A*z**2, B*z**1.7-0.1)
                    
fig,ax = plt.subplots()
ax.plot(zs,jzs)
ax.plot(zs, Jz(zs))
ax.set_ylabel(r'$J_z / kms^{-1}kpc$')
ax.set_xlabel(r'$z_{\mathrm{max}} / kpc$')
fig.savefig('../plots/Jzzmax.png', dpi=300)

fig,ax = plt.subplots()
ax.plot(zs[zs<0.3],jzs[zs<0.3])
ax.plot(zs[zs<0.3], Jz(zs[zs<0.3]))
ax.set_ylabel(r'$J_z / kms^{-1}kpc$')
ax.set_xlabel(r'$z_{\mathrm{max}} / kpc$')

#Ting and Rix 2019

def age(Jz):
    return np.where(Jz>1.16, (Jz-1)/1.6, 0.1)

# J. Christianses's talk

fig,ax = plt.subplots()
ax.plot(zs[zs>0.1], age(jzs[zs>0.1]))
ax.set_ylabel('age / Gyr')
ax.axhline(8,c='C1', alpha=0.5)
ax.axvline(0.72,c='C1', alpha=0.5)
ax.set_xlabel(r'$z_{\mathrm{max}} / kpc$')
ax.set_xscale('log')
fig.savefig('../plots/agezmax.png', dpi=300)

A = np.array([0.126,0.200,0.316,0.500,0.713])
pr = np.array([29,27.5,21,19,17])

fig,ax = plt.subplots()
ax.plot(A, pr)
ax.set_ylabel('planets per 100 stars')
ax.set_xlabel(r'$z_{\mathrm{max}} / kpc$')
ax.set_xscale('log')
ax.set_yscale('log')
fig.savefig('../plots/planetszmax.png', dpi=300)

fig,ax = plt.subplots()
ax.plot(age(Jz(A)), pr)
ax.set_ylabel('planets per 100 stars')
ax.set_xlabel('age / Gyr')
# ax.set_ylim(5,100)
ax.set_xscale('log')
ax.set_yscale('log')
fig.savefig('../plots/planetsage.png', dpi=300)






