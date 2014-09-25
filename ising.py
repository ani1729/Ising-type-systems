# ISING MODEL SIMULATOR
# Author: Aniruddha Bapat

# This is a simple code that calculates energy levels in a (spin-half) Ising model with spin-exchange. 
# The user can set the number of spins N, their spatial configuration, and the interaction coefficients (Jz, Jxy, h) 
# You can also set the interactions to be a function of distance. Some typical functions (constant,
# random, power law etc.) have been provided.

# Enjoy! 

###########################################

from math import *
import numpy as np
from time import clock
from helper_functions import * #refer to helper_functions.py in this repository
import itertools as it

T = clock()

# Some helpful functions
def kprod(args): return reduce(np.kron,args)
def hilb(s,i): return kprod(map(lambda x:s if x==i else I,range(N)))
def zint(pair):return SZ[pair[0]]*SZ[pair[1]] 
def xyint(pair):return SP[pair[0]]*SM[pair[1]]+SM[pair[0]]*SP[pair[1]]
def d(i,j):return sqrt(norm(pos[i]-pos[j]))
def sph(r,th,ph):return r*np.array([sin(th)*cos(ph),sin(th)*sin(ph),cos(th)])

# Some interaction functions
def constant(pair): return A
def gaussianrandom(pair): return np.random.normal(A,0.3*A) 
def uniformrandom(pair): return np.random.uniform(A-0.3,A+0.3)
def invpow(pair, power): return A*reduce(d,pair)**-power if pair[0]!=pair[1] else 0
def rkky(pair): return A*cos(B*reduce(d,pair))*reduce(d,pair)**-3 if pair[0]!=pair[1] else 0

N = 19 # No. of spins
neigh = [[i,j] for i in range(N) for j in range(N) if i!=j] #list of neighbour pairs
A = 1. 
B = pi 

Jxy = input("Jxy = ") #Coefficient for exchange dynamics
h =  input("h = ") #External magnetic field

# Spin positions. Currently a "concentric" triangular lattice 
pos = np.array([sph(0,0,0)] + map(lambda x: sph(1, pi/2, pi/3*x),range(6))
+ map(lambda x: sph(2, pi/2, pi/3*x),range(6)) + map(lambda x: sph(sqrt(3), pi/2, pi/6+pi/3*x),range(6)))

# Specify the sz-sz interaction function
Jz = lambda x: invpow(x,3)

###########################################
# Exact Diagonalization. Comment out this section for N > 10 or so. Otherwise, your program will explode! 

sz = 0.5*np.array([[1,0],[0,-1]])
sp = np.array([[0,0],[1,0]])
sm = np.array([[0,1],[0,0]])
I =  np.identity(2)

#[SZ,SP,SM] = map(lambda s: map(lambda i: hilb(s,i),range(N)),[sz,sp,sm])
#H=h*reduce(add,SZ)+reduce(add,map(lambda i:Jz(i)*zint(i)+Jxy*xyint(i),neigh))

#[evals, evecs] = linalg.eig(H)
#idx = evals.argsort()
#evals = evals[idx]
#evecs = evecs[:,idx]

#for i in range(len(evals)):
#    print "Eigenvalue = ",evals[i]#," with eigenvector"
    #print map(lambda x:round(abs(x),4),zip(*evecs)[i])

##############################
# Use this section to find the classical energies of the system (without external field or exchange dynamics). 
# Intended for large systems where exact diagonalization is too slow.

states = [1,-1] 
space = it.product(states, repeat=N) # Iterator over all 2^N spin states
E = []
large = 10000
ground = []
highest = []
Jarray = np.array([[Jz([i,j]) for i in range(N)] for j in range(N)])
for s in space:
    H = np.dot(np.dot(Jarray,s),s)
    E.append(H)
    if H < large: # Ground state
        ground = s
        Emin=H
    if H > -large: # Highest energy state
        highest = s
        Emax=H

print "running time = ", clock()-T
