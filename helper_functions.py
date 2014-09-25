from math import *

def add(a,b):return a+b 
def mult(a,b):return a*b
def div(a,b): return a/b
def sqr(a):return a**2
def norm(a):return reduce(add, map(sqr, a))
def boo(i):return lambda x: x!=i
def apply(func, start, until, boo):
    return reduce(add, [func(r) for r in range(start, start+until) if boo(r)])
def hx(s,t):return [s*cos(t+pi/3*i) for i in range(6)]
def hy(s,t):return [s*sin(t+pi/3*i) for i in range(6)]
