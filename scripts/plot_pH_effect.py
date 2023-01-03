"""
Script to plot pH effect at -0.5V vs RHE based on simulations and experiments
"""

import matplotlib.pyplot as  plt
import numpy as np
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable

fig = plt.figure(figsize=(12,7))
fig, axes = plt.subplots(ncols=2, sharex=True)

ax1 = axes[0]
ax2 = axes[1]
divider = make_axes_locatable(ax1)
ax3 = divider.new_vertical(size="250%", pad=0.2)
fig.add_axes(ax3)

divider = make_axes_locatable(ax2)
ax4 = divider.new_vertical(size="250%", pad=0.2)
fig.add_axes(ax4)

#experiments
pH = [0.5,1,1.5,2]
fal = [[[0.22,-0.33],[-0.07,-0.22],[-0.41,-0.64],[-1.06,-0.70]],[-0.157,-0.341,-0.526,-0.711],[-8.24]*4]
mf = [[[0.71,0.66],[0.50,0.55],[-0.26,0.11],[-0.21,-0.77]],[-.44,-.67,-.905,-1.138],[-15.3,-15.8,-16.3,-16.76]]
labels = ['Experiment','PCET-theory','ECH-theory']
shapes = ['o','*','^']
lines = ['-','--','-.']
xx = np.linspace(0.5,2,100)

for i, lb in enumerate(labels):
    if lb == 'ECH-theory':
        FAL = [f for f in fal[i]]
        MF = [m for m in mf[i]]
    elif lb == 'Experiment':
        FAL = [sum(i)/len(i) for i in fal[i]]
        MF = [sum(i)/len(i) for i in mf[i]]
        fal_error = [np.std(i) for i in fal[i]]
        mf_error = [np.std(i) for i in mf[i]]
        ax1.errorbar(pH,FAL, yerr = fal_error, fmt='x',capsize=8,color='black',markersize=0)
        ax3.errorbar(pH,FAL, yerr = fal_error, fmt='x',capsize=8,color='black',markersize=0)
        ax2.errorbar(pH,MF, yerr = mf_error, fmt='x',capsize=8,color='black',markersize=0)
        ax4.errorbar(pH,MF, yerr = mf_error, fmt='x',capsize=8,color='black',markersize=0)
    else:
        FAL = fal[i]
        MF = mf[i]
    a1,b1 = np.polyfit(pH,FAL,1)
    a2,b2 = np.polyfit(pH,MF,1)
    ax1.scatter(pH, FAL, marker = shapes[i], s = 120, edgecolor='black', color = 'tab:orange', label = lb)
    ax3.scatter(pH, FAL, marker = shapes[i], s = 120, edgecolor='black', color = 'tab:orange')
    ax2.scatter(pH, MF, marker = shapes[i], s = 120, edgecolor='black', color = 'tab:green')
    ax4.scatter(pH, MF, marker = shapes[i], s = 120, edgecolor='black', color = 'tab:green')
    ax1.plot(xx, a1*xx+b1, color='tab:orange',ls=lines[i])
    ax3.plot(xx, a1*xx+b1, color='tab:orange',ls=lines[i])
    ax2.plot(xx, a2*xx+b2, color='tab:green',ls=lines[i])
    ax4.plot(xx, a2*xx+b2, color='tab:green',ls=lines[i])
    print(lb,a1,a2)
    #legend = ax1.legend(fontsize=14, frameon=False)
    #ax1.set_ylabel('log(j (mA/cm$^2$))', fontsize=16)


for ax in [ax1, ax2, ax3, ax4]:
    ax.set_xlim(0.4,2.1)
    ax.set_xticks(np.arange(0.5,2.1,0.5))
    ax.tick_params(labelsize=16)

#set breaks
ax1.set_ylim(-9,-8)
ax3.set_ylim(-2,1)

ax2.set_ylim(-17,-15)
ax4.set_ylim(-2,1)




# From https://matplotlib.org/examples/pylab_examples/broken_axis.html
d = .03  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax3.transAxes, color='k', clip_on=False)
ax3.plot((-d, d), (0, 0), **kwargs)        # top-left diagonal
ax3.plot((1 - d, 1 + d), (0, 0), **kwargs)        # top-right diagonal

kwargs.update(transform=ax1.transAxes)  # switch to the bottom axes
ax1.plot((-d, d), (1, 1), **kwargs)  # bottom-left diagonal
ax1.plot((1 - d, 1 + d), (1, 1), **kwargs)  # bottom-right diagonal

ax1.spines['top'].set_visible(False)
ax3.tick_params(bottom=False, labelbottom=False)
ax3.spines['bottom'].set_visible(False)

# From https://matplotlib.org/examples/pylab_examples/broken_axis.html
d = .03  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax4.transAxes, color='k', clip_on=False)
ax4.plot((-d, d), (0, 0), **kwargs)        # top-left diagonal
ax4.plot((1 - d, 1 + d), (0, 0), **kwargs)  # top-right diagonal

kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d, d), (1, 1), **kwargs)  # bottom-left diagonal
ax2.plot((1 - d, 1 + d), (1, 1), **kwargs)  # bottom-right diagonal

ax2.spines['top'].set_visible(False)
ax4.tick_params(bottom=False, labelbottom=False)
ax4.spines['bottom'].set_visible(False)

fig.tight_layout()

handles = legend.legendHandles
for i, handle in enumerate(handles):
    handle.set_edgecolor('black')
    handle.set_facecolor('white')
