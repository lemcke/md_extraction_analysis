import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt
from eos import EnergyVolumeEOS

def main():
	volume_data = np.arange(1, 10, dtype=np.float64)
	energy_data = np.exp(volume_data)

	noise = rand(energy_data.size)
	energy_data += noise

	s = EnergyVolumeEOS(volume_data, energy_data)

	# ---- Plot data and EOS models ---- #
	fig, ax = plt.subplots()
	ax.set_xlabel('volume')
	ax.set_ylabel('energy')

	ax.plot(s.volumes, s.energies, 'xr', label='data')


	# Volumes for displaying models:
	v_fine = np.linspace(s.volumes.min(), s.volumes.max(), 100)

	# Using fourth-degree polynomial:
	s.fit_func = EnergyVolumeEOS.poly_4
	s.fit()
	ax.plot(v_fine, s.model(v_fine), ':b', label='4th-deg. polynomial')

	# Using exponential model:
	s.fit_func = EnergyVolumeEOS.exponential
	s.fit()
	ax.plot(v_fine, s.model(v_fine), '--g', label='exponential')

	ax.legend()
	fig.tight_layout()
	plt.show()
	
	return 0

if __name__=='__main__':
	main()
