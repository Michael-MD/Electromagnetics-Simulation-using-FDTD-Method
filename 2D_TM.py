from constants import *
import numpy as np
from warnings import warn
import matplotlib.pyplot as plt
import matplotlib as mpl


from PIL import Image
import cv2


class two_dimensional_simulation:
	def __init__(self, delta_t, delta_x, E_z_0, H_x_0, H_y_0):
		self.delta_t=delta_t
		self.delta_x=delta_x
		self.delta_y=self.delta_x

		self.N_x,self.N_y=E_z_0.shape

		self.sim_time=0

		self.pos_center_x=int(self.N_x/2)
		self.pos_center_y=int(self.N_y/2)

		self.mEz=self.delta_t/(eps_0*delta_x)	# assume delta_x=delta_y
		self.mHx=-self.delta_t/(mu_0*self.delta_y)
		self.mHy=self.delta_t/(mu_0*self.delta_x)

		self.E_z=E_z_0
		self.H_x=H_x_0
		self.H_y=H_y_0


		self.E_source=lambda n: 0




	def step(self, T=-1):
		if T<0:
			num_time_steps=1	# one step by default
		else:
			if T<=self.sim_time:
				warn('No steps will be taken since the simulation has already progressed beyond or up to time '+str(T))
				pass

			num_time_steps=int((T-self.sim_time)/self.delta_t)
		
		for n in range(num_time_steps):
			print(n)
			n+=int(self.sim_time/self.delta_t)
			

				
			for i in range(0,self.N_x):
				for j in range(0,self.N_x-1):
					self.H_x[i,j]=self.H_x[i,j]+self.mHx*( self.E_z[i,j+1] - self.E_z[i,j] )

				self.H_x[i,self.N_x-1]=self.H_x[i,self.N_x-1]+self.mHx*( 0 - self.E_z[i,self.N_x-1] )		
			# print('section 1 comp')

			for j in range(0,self.N_x):
				for i in range(0,self.N_x-1):
					self.H_y[i,j]=self.H_y[i,j]+self.mHy*( self.E_z[i+1,j] - self.E_z[i,j] )
				self.H_y[self.N_x-1,j]=self.H_y[self.N_x-1,j]+self.mHy*( 0 - self.E_z[self.N_x-1,j] )

			# print('section 2 comp')
			for i in range(1,self.N_x):
				self.E_z[i,0]=self.E_z[i,0]+self.mEz*( self.H_y[i,0] - self.H_y[i-1,0] - self.H_x[i,0] + 0 )
				for j in range(1,self.N_x):
					self.E_z[0,j]=self.E_z[0,j]+self.mEz*( self.H_y[0,j] - 0 - self.H_x[0,j] + self.H_x[0,j-1] )
					self.E_z[i,j]=self.E_z[i,j]+self.mEz*( self.H_y[i,j] - self.H_y[i-1,j] - self.H_x[i,j] + self.H_x[i,j-1] )
				
			# print('section 3 comp')

			# for  in range(1,self.N_x):
			# 	self.E_z[i,0]=self.E_z[i,0]+self.mEz*( self.H_y[i,0] - self.H_y[i-1,0] - self.H_x[i,0] + 0 )
			# 	for j in range(1,self.N_x):
			# 		self.E_z[i,j]=self.E_z[i,j]+self.mEz*( self.H_y[i,j] - self.H_y[i-1,j] - self.H_x[i,j] + self.H_x[i,j-1] )
				

			for j in range(0,self.N_x-1):
				for i in range(0,self.N_x-1):
					self.E_z[self.N_x-1,j]=self.E_z[i,j]+self.mEz*( 0 - self.H_y[i-1,j] - self.H_x[i,j+1] + self.H_x[i,j-1] )

			# print('section 4 comp')

			self.E_z[self.pos_center_x,self.pos_center_y]=self.E_source(n)


		# self.sim_time=T 	# update to time of simulation




x=two_dimensional_simulation(0.13e-9, 5.4e-2, np.zeros((201,201)), np.zeros((201,201)), np.zeros((201,201)))
x.E_source=lambda n: np.sin(2*np.pi*278e6*x.delta_t*n)


x.step(500*x.delta_t)


fig = plt.figure(2)

cmap2 = mpl.colors.LinearSegmentedColormap.from_list('my_colormap',
                                           ['black','white'],
                                           256)

img2 = plt.imshow(x.E_z,interpolation='nearest',
                    cmap = cmap2,
                    origin='lower')

plt.colorbar(img2,cmap=cmap2)

fig.savefig("image2.png")









