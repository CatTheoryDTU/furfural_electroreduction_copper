#!/usr/bin/env python
import numpy as np
import re
import sys
import os

from catmap import ReactionModel
from string import Template

include_rate_control = False
fed_setting = False

pH = 1
voltages = [(-1.2, 0.2)]
 
for i, item in enumerate(voltages):
	lower_, upper_ = item
	text = Template(open('fur_template.mkm').read())
	text = text.substitute(lower = lower_, upper = upper_)

	# setup model
	mkm_file = 'Fur_pH'+str(pH)+'.mkm'
	with open(mkm_file,'w') as f:
	    f.write(text)
	model = ReactionModel(setup_file = mkm_file)
	model.output_variables+=['production_rate', 'free_energy', 'selectivity', 'interacting_energy']
	model.run()

	# rates
	from catmap import analyze
	vm = analyze.VectorMap(model)
	vm.plot_variable = 'rate'
	vm.descriptor_labels = ['U vs. SHE (V)']
	vm.log_scale = True
	vm.min = 1e-8
	vm.max = 1e8
	fig = vm.plot(save=False)
	fig.savefig('rate'+'.png')

	# coverages
	vm = analyze.VectorMap(model)
	vm.log_scale = True
	vm.plot_variable = 'coverage'
	vm.descriptor_labels = ['coverage (ML)']
	vm.min = 1e-12
	vm.max = 1.01
	fig = vm.plot(save=False)
	fig.savefig('coverage'+'.png')

	# production rate
	vm.plot_variable = 'production_rate'
	vm.descriptor_labels = ['U vs. SHE (V)']
	vm.log_scale = True
	vm.min = 1e-8
	vm.max = 1e8
	fig = vm.plot(save=False)
	fig.savefig('production_rate'+'.png')

# post-processing
#os.system('./plot_all_pol.py')

