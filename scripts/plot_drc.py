"""
Script to plot degree of rate controls for different products against the adsorption energies of main intermediates
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
#import csv
from operator import itemgetter
from matplotlib import cm
from matplotlib import rc
from matplotlib.ticker import NullFormatter

text = np.loadtxt('rate_control_table.txt', skiprows=1)

print(text[0])
text = text[text[:,0].argsort()]
newtext = np.array(text).transpose()
print(newtext.shape)

products = ['CH4_g', 'FCH2OH_g', 'FCH3_g', 'FCHO_g', 'H2O_g', 'H2_g', 'H_g', 'OH_g', 'ele_g']
#species = ['H_dl', 'FCH2OH_s', 'FCH2O_s', 'FCH2_s', 'FCH3_s', 'FCHOH_s', 'FCHO_s', 'FCH_s', 'H_s', 'OH_s', 'O_s', 'FCH-ele-H-OH_s', 'FCH-ele-H-O_s', 'FCH2O-ele-H_s', 'FCHO-ele-H_s', 'FCHOH-ele-H_s', 'H-H_s', 'H-ele-H_s', 'H-ele_s', 'H2O-H-ele_s', 'H2O-ele_s', 'HO-H_s']
species = ['H_dl', 'FCH2OH_s', 'FCH2O_s', 'FCH2_s', 'FCH3_s', 'FCHOH_s', 'FCHO_s', 'FCH_s', 'H_s', 'OH_s', 'FCH-ele-H-OH_s', 'FCH-ele-H-O_s', 'FCH2O-ele-H_s', 'FCHO-ele-H_s', 'FCHOH-ele-H_s', 'H-H_s', 'H-ele-H_s', 'H-ele_s', 'H2O-H-ele_s', 'H2O-ele_s', 'HO-H_s']



voltage=newtext[0]
print(voltage)
temperature=newtext[1]

#x axis
xx=np.linspace(-5,5,30)
y = xx*0

#set colors
colors = plt.cm.hsv(np.linspace(0,1,32))[::-1]

#main plotting code
##the rows are drc values for each voltage, the volumes are resolution set in mkm.file
##by default, catmap.drc put the drc values of each product against different species at the first row of each 'product section', which equals to (Nrows-2)/Nproducts 

for i,p in enumerate(products):
    fig,ax = plt.subplots(figsize=(8,8))
    for n,s in enumerate(species):
        ax.plot(voltage,newtext[2+756*i+n],color=colors[n],label=p+'/'+s)
    ax.legend(fontsize=5,ncol=3)
    fig.savefig(p+'DRC.png',dpi=100,bbox_inches='tight')        

ax.set_ylim(-1.1,1.1)
ax.set_xlim(-1,0.2)

ax.set_xlabel('U (V vs. SHE)',fontsize=20)
ax.set_ylabel('Degree of rate control',fontsize=20)




