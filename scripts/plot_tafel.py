"""
Script to plot Tafels for different electroreduction products: H2, FCH2OH and FCH3
"""

#!/usr/bin/env python
import pickle
import sys
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from catmap.model import ReactionModel
from matplotlib.pyplot import cm
from matplotlib import rc
from matplotlib.ticker import NullFormatter
from pylab import *
from matplotlib.font_manager import FontProperties

class Object(object):
    pass

mathtext_prop = {'fontset' : 'custom',
                 'it' : 'serif:italic',
                 'sf' : 'Helvetica:bold',
                 'cal' : 'serif:italic:bold'}
rc('font', family='serif', serif='Helvetica')
rc('mathtext', **mathtext_prop)
rc('xtick', labelsize=15)
rc('ytick', labelsize=15)

def get_data(pickle_file):
    a = pickle.load(open(pickle_file,'rb'))
    data = Object()
    #COVERAGES
    data.coverage_names = model.output_labels['coverage']
    coverage_map = np.array(a['coverage_map'], dtype="object")
    data.voltage = []
    scaler_array = coverage_map[:,0]
    for s in scaler_array:
        data.voltage.append(s[0])
    coverage_mpf = coverage_map[:,1]
    data.coverage = np.zeros((len(coverage_mpf),len(data.coverage_names)))
    for i in range(0,len(coverage_mpf)):
        for j in range(0,len(coverage_mpf[i])):
            float_rate = float(coverage_mpf[i][j])
            data.coverage[i][j]=float_rate
    #PRODUCTION RATES
    data.prod_names = model.output_labels['production_rate']
    production_rate_map = np.array(a['production_rate_map'], dtype="object")
    production_rate_mpf = production_rate_map[:,1]
    data.production_rate = np.zeros((len(production_rate_mpf),len(data.prod_names)))
    data.voltage = np.zeros((len(production_rate_mpf),1))
    for i in range(0,len(production_rate_mpf)):
        data.voltage[i][0] = production_rate_map[:,0][i][0]
        for j in range(0,len(data.prod_names)):
            float_rate = float(production_rate_mpf[i][j])
            data.production_rate[i][j]=float_rate
    #RATES
    data.rate_names = model.output_labels['rate']
    rate_map = np.array(a['rate_map'], dtype="object")
    rate_mpf = rate_map[:,1]
    data.rate = np.zeros((len(rate_mpf),len(data.rate_names)))
    for i in range(0,len(rate_mpf)):
        for j in range(0,len(rate_mpf[i])):
            float_rate = float(rate_mpf[i][j])
            data.rate[i][j]=float_rate
    return data

def convert_TOF(A): # Given a list, convert all the TOF to j(mA/cm2) using 0.161*TOF(According to Heine's ORR paper)
    C = [1*rate for rate in A]
    print(C)
    B = [-0.161*rate for rate in A]
    print(B)
    return B

# plots
color_list = ['#BF3F3F','#F47A33','#FFE228','#7FBF3F','#3FBFBF','#3F7FBF','#3F3FBF','#7F3FBF','#BF3F7F','#BF3F3F','#333333','#000000']
#pH = ['13']
#pH = ['0','1','2','2.5','3','4','7','10','12','14']
#voltages = [(-0.7,-2.0),(0.2,-0.7),(1.1,0.2),(2.0,1.1)]
pH = 0.5
voltages = [(-1.2,0.2)]
#voltages = [(-1,-0.8),(-0.8, -0.6),(-0.6, -0.4),(-0.4, -0.2), (-0.2, 0), (0, 0.2)]
#voltages = [(-1,-0.6),(-0.6, -0.2),(-0.2, 0.2)]
# all pH
alpha = 0.5
rhe = pH*0.059
for i, item in enumerate(voltages):
    lower_, upper_ = item
    log_file = 'Fur_pH'+str(pH)+'_'+str(alpha)+'.log'
    model = ReactionModel(setup_file = log_file)
    pickle_file = 'Fur_pH'+str(pH)+'_'+str(alpha)+'.pkl'
    phX = get_data(pickle_file)

    # plot partial current densities for different  products
    products = ['H2_g','FCH2OH_g', 'FCH3_g']
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    for product in products:
        idx=phX.prod_names.index(product)
        print(idx)
        if product == 'H2_g':
            data=np.column_stack((phX.voltage, 2*phX.production_rate[:,idx]))
            x=data[np.argsort(data[:, 0])][:,0]
            y=convert_TOF(data[np.argsort(data[:, 0])][:,1]*-0.5)
            ax.plot(x+rhe,np.log10(y),color='tab:blue', linewidth=1.5, label = 'H$_2$')
        elif product == 'FCH2OH_g':
            data=np.column_stack((phX.voltage, 2*phX.production_rate[:,idx]))
            x=data[np.argsort(data[:, 0])][:,0]
            y=convert_TOF(data[np.argsort(data[:, 0])][:,1]*-0.5)
            ax.plot(x+rhe,np.log10(y), color='tab:orange',linewidth=1.5, label = 'FCH$_2$OH')				
        else:
            data=np.column_stack((phX.voltage, 4*phX.production_rate[:,idx]))
            x=data[np.argsort(data[:, 0])][:,0]
            y=convert_TOF(data[np.argsort(data[:, 0])][:,1]*-1)
            ax.plot(x+rhe,np.log10(y), color='tab:green',linewidth=1.5, label = 'FCH$_3$')


leg = plt.legend(loc='upper right', ncol=1, prop={'size':9}, fancybox=True, shadow=False)
leg.get_frame().set_facecolor('none')
leg.get_frame().set_linewidth(0.0)
plt.gcf().subplots_adjust(bottom=0.18, left=0.18)
plt.xlim((-0.7,-0.2))
plt.ylim((-1,3))
plt.xlabel(r'U (V vs. RHE)', fontsize=16)
plt.ylabel(r'log(j(mA/cm$^{2}$))', fontsize=16)
fig_name = 'tafel.png'
fig.savefig(fig_name,dpi=200)
plt.close()
