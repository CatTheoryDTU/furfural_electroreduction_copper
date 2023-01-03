"""
Script to plot FED of PCET reactions on Cu(111) based on GC-DFT calculations
"""

#------------------------------------------
#   Importing the required packages
#------------------------------------------
get_ipython().run_line_magic('matplotlib', 'auto')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import UnivariateSpline

#------------------------------------------
#   Making the figure object
#------------------------------------------
fig, ax = plt.subplots(figsize=(9,5))
ax1=ax.twiny()

##define the function for plotting FEDs
def plot_energies(reaction_energies, activation_energies,  ax, color, ls, label):
    """plots free energy diagrams given reaction energies and activation
        energies,
    which should be same-length lists and a matploblit axes object 
    """
    half_width = 0.3
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    rxn_pathway = np.arange(len(reaction_energies)) # for stoichiometry
    #IS_energy = 0.
    IS_energy = 0.
    for i, rxn_number in enumerate(rxn_pathway):
        if i == 0:
            ax.plot([-half_width, half_width], [IS_energy, IS_energy], ls, color=color,label = label)
        FS_energy = IS_energy + reaction_energies[rxn_number] 
        TS_energy = IS_energy + activation_energies[rxn_number] 
        ax.plot([i + 1 - half_width, i + 1 + half_width], [FS_energy, FS_energy], ls, color=color)
        if abs(TS_energy - IS_energy) < 0.001 or abs(TS_energy - FS_energy) < 0.001:
            ax.plot([i + half_width, i + 1 - half_width], [IS_energy, FS_energy], ls, color=color)
        else:
            A = UnivariateSpline([i + half_width, i + 0.5, i + 1 - half_width], 
                                 [IS_energy, TS_energy, FS_energy],k=2) 
            x = np.linspace(i + half_width, i + 1 - half_width)
            ax.plot(x, A(x), ls, color=color) 
        IS_energy = FS_energy
    return ax


color1 = 'r'
color2 = 'black'
ls1 = '-'
ls2 = '--'


pH = 0
ph = 0.059*pH
beta = 0.5

colors=['black','r']
ls = ['-','--']

##use solvated energies in gpaw-sjm

#calculated symmetry factos for pcets: fcho-fchoh,fchoh-fch2oh; fchoh-fch, fch-fch2, fch2-fch3
betas = [0.55, 0.69, 0.59, 0.65, 0.50]

for i,u in enumerate([0,-0.5]):
    Ea1 = [0, 0.48+u*betas[0],0.97+u*betas[1],0]
    Ea3 = [0, 0.48+u*betas[0],1.03+u*betas[2],0.58+u*betas[3],0.62+u*betas[4],0]
    Er1 = [0.30,0.10+u,-0.34+u,-0.25]
    Er3 = [0.30,0.10+u,-0.16+u,-0.38+u,-0.77+u,-0.75]
    plot_energies(Er1, Ea1, ax1, color='r', ls=ls[i], label = None)
    plot_energies(Er3, Ea3, ax,  color='black', ls=ls[i], label = str(u) + 'V vs. RHE, pH = 1')

    
#set axes
ax1.spines['top'].set_color('r')
ax1.set_xlim(-0.2,6.2)
ax1.set_xticks([0, 1, 2, 3, 4]) 
ax1.set_xticklabels(['FCHO(l)', 'FCHO*', 'FCHOH*','FCH$_2$OH*', 'FCH$_2$OH(l)'], rotation=0.)
ax1.tick_params(labelsize=12,axis = 'x',colors='r',pad=10)

ax.set_xlim(-0.2,6.2)

ax.set_xticks([0, 1, 2, 3, 4, 5,6])
ax.set_xticklabels(['FCHO(l)', 'FCHO*','FCHOH*','FCH*+H$_2$O(g)','FCH$_2$*','FCH$_3$*','FCH$_3$(g)'], rotation=0.)
ax.tick_params(labelsize=12, axis = 'x', direction='out', colors='black',pad=10)
ax.spines['bottom'].set_color('black')
ax.set_ylim(-4,2)
ax.tick_params(labelsize=15,axis = 'y')
ax.set_ylabel('$\Delta G ^\Phi$ (eV)', fontsize=20)

ax.legend(loc='upper right', frameon=False, fontsize=12)
#ax1.legend(loc=1, frameon=False)
plt.tight_layout()
plt.show()
