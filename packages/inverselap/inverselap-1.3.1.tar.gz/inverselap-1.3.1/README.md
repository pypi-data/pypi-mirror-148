## Numerical inversion of Laplace transform

1.Use the following statement to import



	from inverselap import inverse


### One-dimensional Laplace inversion

Take a one-dimensional function as an example


	def fs_1d(s):
	return 1/(s+1)


2.1 method Gaver-Stehfest

Use the following statement for inversion: inverse.GS_1d(f,t,M), f means functon, t meanstime parameter， M means the number of nodes, M is a positive even number while 14, 16 and 18 are recommended



	inverse.GS_1d(f,1,18)


2.2 method Euler

Use the following statement for inversion: inverse.Euler_1d(f,t,M), f means functon, t meanstime parameter， M means the number of nodes, M is a positive number while 17 and 19 are recommended


	inverse.Euler_1d(fs_1d,1,19)


2.3 method Talbot

Use the following statement for inversion: inverse.Talbot_1d(f,t,M), f means functon, t meanstime parameter, M means the number of nodes, M is a positive number while 21 is recommended


	inverse.Talbot_1d(fs_1d,1,21)


### Two-dimensional Laplace inversion

Take a rwo-dimensional function as an example


	def fs_2d(s1,s2):
	return 1/(s1+1)/(s2+2)


3.1 method series

Use the following statement for inversion: inverse.series_2d(f,t1,t2,N,c1,c2), f means functon, t1 and t2 mean time parameter, N means the number of nodes, N is a positive number while 64 and 128 is recommended, c1 and c2 should be larger than the s1 and s2 where the value fs_2d(s1,s2) is infinite if possible. 


	inverse.series_2d(fs_2d,1,1,128,0,-1)


3.2 method partial

Use the following statement for inversion: inverse.Partial_2d(f,t1,t2,N,par1,par2), f means functon, t1 and t2 mean time parameter, N means the number of nodes, N is a positive number while 64 and 128 is recommended, alpha1 and alpha1 should be the s1 and s2 where the value fs_2d(s1,s2) is infinite if possible. 


	inverse.Partial_2d(fs_2d,1,1,128,-1,-2)


3.3 mtehod Talbot

Use the following statement for inversion: inverse.Talbot_2d(f,t1,t2,M), f means functon, t1 and t2 mean time parameter, M means the number of nodes, M is a positive number while 21 is recommended


	inverse.Talbot_2d(fs_2d,1,1,18)



3.4 mtehod Euler

Use the following statement for inversion: inverse.Euler_2d(f,t1,t2,M), f means functon, t1 and t2 mean time parameter, M means the number of nodes, M is a positive number while 17 and 19 are recommended


	inverse.Euler_2d(fs_2d,1,1,21)


3.5 method epsilon

Use the following statement for inversion: inverse.epsilon(f,t1,t2,alpha1,alpha2), f means functon, t1 and t2 mean time parameter, alpha1 and alpha1 should be the s1 and s2 where the value fs_2d(s1,s2) is infinite if possible. 



	inverse.inverse.epsilon(fs_2d,1,1,-1,-1)


