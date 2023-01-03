"""
Script to plot total current densities with and without furfural on Cu electrodes

"""

import matplotlib.pyplot as  plt
import numpy as np
import pandas as pd

fig, ax = plt.subplots(figsize=(7.5,5.5))

U = [-0.11,-0.21,-0.26,-0.31,-0.36,-0.41,-0.46,-0.51, -0.56]
j_her_raw = [[-0.231,-0.138],[-0.292,-0.176],[-0.338,-0.215],[-0.4,-0.264],[-0.538,-0.372],[-0.937,-0.72],[-2.164,-1.724],[-4.972,-4.071], 
        [-10.434,-8.651]]
j_frr_raw = [[-0.369,-1.182],[-0.43,-1.274],[-0.507,-1.382],[-0.645,-1.52],[-1.09,-2.087],[-2.64,-3.714],[-5.862,-6.89],[-10.833,-11.692], 
        [-18.228,-18.504]]

def normalize_surface(J):
    J_nor = []
    
    for j in J:
        j_nor = []
        for jj in j:
            j_nor.append(jj*0.5)
        J_nor.append(j_nor)
    return J_nor

j_her = normalize_surface(j_her_raw)
j_frr = normalize_surface(j_frr_raw)

jher_avg = [sum(i)/len(i) for i in j_her]
jher_error = [np.std(i) for i in j_her]

jfrr_avg = [sum(i)/len(i) for i in j_frr]
jfrr_error = [np.std(i) for i in j_frr]


ax.plot(U,jher_avg,lw=1,color = 'red', ls = '--', marker = 'o', markeredgecolor='red', markersize = 10, markerfacecolor = 'white')
ax.plot(U,jfrr_avg,lw=1,color = 'k',marker = 'o', markeredgecolor='k', markersize = 10 ,markerfacecolor = 'white')

ax.errorbar(U,jher_avg, yerr = jher_error, fmt='x',capsize=8,color='red',markersize=0)
ax.errorbar(U,jfrr_avg, yerr = jfrr_error, fmt='x',capsize=8,color='black',markersize=0)

#plot setting
plt.xlabel('U (V vs. RHE)', fontsize=20)
plt.ylabel('j (mA/cm$^2$)', fontsize=20)
#plt.legend(fontsize=14,frameon=False)

plt.xlim(-0.8,-0.2)
plt.ylim(-10,1)
ax.tick_params(labelsize=20)
plt.tight_layout()
