"""
Script to plot partial current densities of FCH2OH and FCH3
"""

import matplotlib.pyplot as  plt
import numpy as np
import pandas as pd

fig, ax = plt.subplots(figsize=(7.5,5.5))

#data from Zamaan

U = [-0.40,-0.43,-0.45,-0.48,-0.50,-0.60,-0.65]
j_fal = [[0.032,0.30],[0.43,0.41],[0.75,0.68],[0.75,1.09],[1.184,0.859],[1.16],[0.713]]
j_mf = [[0.63,0.28],[1.88,1.93],[2.35,2.23],[2.88,2.92],[3.17,4.46],[7.558],[7.278]]

def log(J):
    J_log = []
    
    for j in J:
        j_log = []
        for jj in j:
            j_log.append(np.log10(jj))
        J_log.append(j_log)
    return J_log

j_fal = log(j_fal)
j_mf = log(j_mf)

jfal_avg = [sum(i)/len(i) for i in j_fal]
jfal_error = [np.std(i) for i in j_fal]

jmf_avg = [sum(i)/len(i) for i in j_mf]
jmf_error = [np.std(i) for i in j_mf]


ax.plot(U[:-4],jfal_avg[:-4],lw=0,label = 'FCH$_2$OH', marker = 'o', markeredgecolor='k', markersize = 15, color = 'tab:orange')
ax.plot(U[:-4],jmf_avg[:-4],lw=0,label = 'FCH$_3$', marker = 'o', markeredgecolor='k', markersize = 15 ,color = 'tab:green')
ax.plot(U[-4:],jfal_avg[-4:],lw=0,label = 'FCH$_2$OH', marker = 'o', markeredgecolor='tab:orange', markersize = 15, color = 'w')
ax.plot(U[-4:],jmf_avg[-4:],lw=0,label = 'FCH$_3$', marker = 'o', markeredgecolor='tab:green', markersize = 15 ,color = 'w')

ax.errorbar(U[:-2],jfal_avg[:-2], yerr = jfal_error[:-2], fmt='x',capsize=8,color='black',markersize=0)
ax.errorbar(U[:-2],jmf_avg[:-2], yerr = jmf_error[:-2], fmt='x',capsize=8,color='black',markersize=0)

#Tafel slope fitting
x1 = U[0:3]
y1 = jfal_avg[0:3]
x2 = U[0:3]
y2 = jmf_avg[0:3]
a1,b1 = np.polyfit(x1,y1,1)
a2,b2 = np.polyfit(x2,y2,1)
print(1/a1*1000,1/a2*1000)

xx = np.linspace(-5,5,100)
ax.plot(xx, a1*xx+b1, color='tab:orange')
ax.plot(xx, a2*xx+b2, color='tab:green')

#plot setting
plt.xlabel('U (V vs. RHE)', fontsize=20)
plt.ylabel('log(j (mA/cm$^2$))', fontsize=20)
#plt.legend(fontsize=14,frameon=False)

plt.xlim(-0.8,-0.2)
plt.ylim(-2,2)
ax.tick_params(labelsize=20)
plt.tight_layout()
