import numpy as np
from scipy.optimize import curve_fit
from scipy.misc import derivative

class EnergyVolumeEOS:
	"""
	Energy-volume equation of state (EOS).

	Attributes
	----------
	volumes:   <numpy.ndarray> of volumes
	energies:  <numpy.ndarray> of energies
	fit_func:  <callable> function to use as EOS
	fit_guess: <array-like> of guess parameters for EOS
	fit_covar: <numpy.ndarray> EOS covariance matrix
	fit_coeff: <numpy.ndarray> EOS coefficients

	Methods
	-------
	fit:   fit `fit_func` to `volumes` and `energies`
	       using <scipy.optimize.curve_fit>
	model: defined as `fit_func` with `fit_coeff`
	
	...as well as getters for all attributes,
	and setters for `volumes`, `energies`, `fit_func`,
	`fit_guess`, `fit_coeff`.

	Aliases
	-------
	`energies` => `e`
	`volumes`  => `v`
	
	Example
	-------
	>>> s = EnergyVolumeEOS(volume_data, energy_data)
	>>>
	>>> v_fine = np.linspace(s.volumes.min(), s.volumes.max(), 100)
	>>> 
	>>> # ---- Plot data and EOS models ---- #
	>>> fig, ax = plt.subplots()
	>>> ax.set_xlabel('volume')
	>>> ax.set_ylabel('energy')
	>>> 
	>>> ax.plot(s.volumes, s.energies, 'xr', label='data')
	>>> 
	>>> # Using fourth-degree polynomial:
	>>> s.fit_func = EnergyVolumeEOS.poly_4
	>>> s.fit()
	>>> ax.plot(v_fine, s.model(v_fine), ':b', label='4th-deg. polynomial')
	>>> 
	>>> # Using exponential model:
	>>> s.fit_func = EnergyVolumeEOS.exponential
	>>> s.fit()
	>>> ax.plot(v_fine, s.model(v_fine), '--g', label='exponential')
	"""

	def __init__(self, volumes, energies, fit_func=None, guess=None):
		"""
		Initialize <State> object.

		Input
		-----
		volumes:	<array-like> volume "x" data
		energies:	<array-like> energy "y" data
		fit_func:	<callable> energy-volume model
		guess:		<array-like> guess coefficients for fit function
		"""
		self._v = np.asarray(volumes).flatten()
		self._e = np.asarray(energies).flatten()
		assert self._v.size == self._e.size

		self._fit_func = fit_func
		self._fit_guess = guess
		self._fit_coeff = None # Calculated by fitting model to data.
		self._fit_covar = None # ...

	# ---- fit model to data ---- #
	def fit(self):
		coeffs, cov = curve_fit(
			self._fit_func, self._v, self._e, self._fit_guess
		)

		self._fit_coeff = coeffs
		self._fit_cov = cov
	
	def model(self, volumes):
		return self._fit_func(volumes, *self._fit_coeff)
	
	# ---- built-in models ---- #
	@staticmethod
	def poly_4(x, x0, a, b, c, d, e):
		"""Fourth-degree Taylor polynomial."""
		_x = x - x0
		return a + b*_x + c*_x*_x + d*_x*_x*_x + e*_x*_x*_x*_x
	
	@staticmethod
	def exponential(x, x0, a, b, c):
		"""Exponential model."""
		return a * np.exp(b * (x - x0)) + c
	
	# ---- physical functions ---- #
	def p_v(self, volumes=self._v):
		"""Returns pressure(s) given volume(s)."""
		return -1.0 * derivative(self.model, volumes)
	
	# ---- aliases/getters ---- #
	@property
	def v(self):
		return self._v
	
	@property
	def e(self):
		return self._e
	
	@property
	def volumes(self):
		return self._v
	
	@property
	def energies(self):
		return self._e

	@property
	def fit_func(self):
		return self._fit_func

	@property
	def fit_guess(self):
		return self._fit_guess
	
	@property
	def fit_coeff(self):
		return self._fit_coeff
	
	@property
	def fit_covar(self):
		return self._fit_covar
	
	# ---- setters ---- #
	@volumes.setter
	def volumes(self, value):
		self._v = value
	
	@energies.setter
	def energies(self, value):
		self._e = value

	@fit_func.setter
	def fit_func(self, func):
		self._fit_func = func

	@fit_guess.setter
	def fit_guess(self, value):
		self._fit_guess = value

	@fit_coeff.setter
	def fit_coeff(self, value):
		self._fit_coeff = value
