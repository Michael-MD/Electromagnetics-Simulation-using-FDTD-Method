from constants import *
import numpy as np
from warnings import warn
import matplotlib.pyplot as plt


from PIL import Image
import cv2


class one_dimensional_simulation:
	def __init__(self, delta_t, delta_x, E_0, H_0):
		self.delta_t=delta_t
		self.delta_x=delta_x

		self.N_x=len(E_0)

		self.sim_time=0

		self.pos_center=int(self.N_x/2)

		self.mE=self.delta_t/(eps_0*self.delta_x)
		self.mH=self.delta_t/(mu_0*self.delta_x)

		self.mE=lambda k: self.delta_t/(eps_0*self.delta_x) if k<200 else self.delta_t/(eps_0*4*self.delta_x)
		self.mH=lambda k: self.delta_t/(mu_0*self.delta_x) if k<200 else self.delta_t/(mu_0*self.delta_x)



		self.eta=np.sqrt(mu_0/eps_0)

		self.E=E_0
		self.H=H_0
		self.H_tilde=self.H*self.eta

		


		self.E_source=lambda n: 0




	def step(self, T=-1):
		if T<0:
			num_time_steps=1	# one step by default
		else:
			if T<=self.sim_time:
				warn('No steps will be taken since the simulation has already progressed beyond or up to time '+str(T))
				pass

			num_time_steps=int((T-self.sim_time)/self.delta_t)

		
		self.E_edge_left=[0,0,0]
		self.H_edge_left=[0,0,0]

		self.E_edge_right=[0,0,0]
		self.H_edge_right=[0,0,0]


		for n in range(num_time_steps):
			n+=int(self.sim_time/self.delta_t)


			self.H[0]=self.H_edge_left[1]
			self.H[self.N_x-1]=self.H_edge_right[2]
			for k in range(0,self.N_x-1):
				self.H[k]=self.H[k]+self.mH(k)*( self.E[k+1] - self.E[k] )			


			self.H_tilde=self.H*self.eta


			self.E[0]=self.E_edge_left[1]
			self.E[self.N_x-1]=self.E_edge_right[2]
			for k in range(1,self.N_x):
				self.E[k]=self.E[k]+self.mE(k)*( self.H[k] - self.H[k-1] )
			

			# ---------------------------------------------

			self.H_edge_left[2]=self.H_edge_left[1]
			self.H_edge_left[1]=self.H_edge_left[1]
			self.H_edge_left[0]=self.H[1]

			self.H_edge_right[2]=self.H_edge_right[1]
			self.H_edge_right[1]=self.H_edge_right[1]
			self.H_edge_right[0]=self.H[-2]

			# ---------------------------------------------

			self.E_edge_left[2]=self.E_edge_left[1]
			self.E_edge_left[1]=self.E_edge_left[1]
			self.E_edge_left[0]=self.E[1]

			self.E_edge_right[2]=self.E_edge_right[1]
			self.E_edge_right[1]=self.E_edge_right[1]
			self.E_edge_right[0]=self.E[-2]


			self.E[25]=self.E_source(n)


		self.sim_time=T 	# update to time of simulation




x=one_dimensional_simulation(0.18e-9, 5.4e-2, np.zeros((401,1)), np.zeros((401,1)))
# x.E_source=lambda n: np.sin(2*np.pi*278e6*x.delta_t*n)
x.E_source=lambda n: np.exp(-((n-8)**2)/16)


for i in range(0,50,10):
	x.step(i*1e-9)

	plt.plot(x.E)
	# plt.plot(x.H_tilde)

	plt.show()





