from constants import *
import numpy as np
from warnings import warn
import matplotlib.pyplot as plt

class one_dimensional_simulation:
	def __init__(self, Δ_t, Δ_x, E_0, H_0):
		self.Δ_t=Δ_t
		self.Δ_x=Δ_x

		self.N_x=len(E_0)

		self.sim_time=0

		self.pos_center=int(self.N_x/2)

		self.mE=self.Δ_t/(ε*self.Δ_x)
		self.mH=self.Δ_t/(μ*self.Δ_x)

		self.E=E_0
		self.H=H_0

		self.E_source=lambda n: 0

		self.t=0

		# defaults
		# self.E=np.zeros((401,1))
		# self.H=np.zeros((401,1))
		# self.t=0
		# self.E_source=lambda n: 0
		# ε=ε_0
		# μ=μ_0


	def step(self, T=-1):
		if T<0:
			num_time_steps=1	# one step by default
		else:
			if T<=self.sim_time:
				warn('No steps will be taken since the simulation has already progressed beyond or up to time '+str(T))
				pass

			num_time_steps=int((T-self.sim_time)/self.Δ_t)

		
		for n in range(num_time_steps):
			n+=int(self.sim_time/self.Δ_t)
			for k in range(0,self.N_x-1):
				self.H[k]=self.H[k]+self.mH*( self.E[k+1] - self.E[k] )
			self.H[self.N_x-1]=self.H[k]+self.mH*( 0 - self.E[k] )


			self.E[0]=self.E[0]+self.mE*( self.H[0] - 0 )
			for k in range(1,self.N_x):
				self.E[k]=self.E[k]+self.mE*( self.H[k] - self.H[k-1] )

			self.E[self.pos_center]=self.E_source(n)


		self.sim_time=T 	# update to time of simulation





x=one_dimensional_simulation(0.18e-9, 5.4e-2, np.zeros((401,1)), np.zeros((401,1)))
# x.E_source=lambda n: np.sin(2*np.pi*278e6*x.Δ_t*n)
x.E_source=lambda n: np.exp(-((n-8)**2)/16)
x.step(10e-9)
plt.plot(x.E)


plt.show()
