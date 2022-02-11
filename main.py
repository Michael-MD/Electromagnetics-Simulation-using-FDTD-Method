import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# constants
c_0=3e8
delta_t=.1

eps_yy=1
mu_xx=eps_yy




# update coefficiencts
mEy=c_0*delta_t/eps_yy
mHx=c_0*delta_t/mu_xx


N=100
delta_z=0.1
T=10


Ey=np.zeros((N,1))
Hx=np.zeros((N,1))

for t in range(0,T):
	# update H field
	for z in range(0,N-1):
		Hx[z]=Hx[z]+mHx*(Ey[z+1]-Ey[z])/delta_z
	Hx[N-1]=Hx[N-1]+mHx*(0-Ey[N-1])/delta_z

	# update E field
	Ey[0]=Ey[0]+mEy*(Hx[0]-0)/delta_z
	for z in range(1,N):
		Ey[z]=Ey[z]+mEy*(Hx[z]-Hx[z-1])/delta_z


	


# 	plt.plot(Ey)
# 	plt.plot(Hx)


# plt.show()


