from typing import overload
from math import *

# vector magnitude
def vmag(*args):
    vsum = 0

    if type(args[0]) == int or type(args[0]) == float:
        for arg in args:
            vsum += (arg**2)

        return (vsum**(1/2))
    
    else:
        return None

#finding vector components
def vcomp(mag, angle, unit):
    tol = 1e-5
    if unit[0] == "D" or unit[0] == "d":
        returnval = [(mag * cos(((2*pi)/360)*angle)) ,((mag * sin(((2*pi)/360)*angle)))]
    else:
        returnval = [(mag * cos(angle)) ,(mag * sin(angle))]
    
    for i in range(len(returnval)):
        if abs(returnval[i]) <= tol:
            returnval[i] = 0;
    
    return tuple(returnval);

#quadratic formula
def quadsolve(a, b, c):
    disc = (b**2) - (4*a*c)
    print(sqrt(abs(disc)))

    if disc > 0: return (((-b + sqrt(disc))/(2 * a)), ((-b - sqrt(disc))/(2 * a)))
    if disc == 0: return (-b / (2* a))
    if disc < 0: return ((str((-b / (2* a)))+" + "+str((sqrt(abs(disc)))/(2*a))+" i"), (str((-b / (2* a)))+" - "+str((sqrt(abs(disc)))/(2*a))+" i"))

#calulating the velocity        
def calcv(x1, x2, t1, t2):
    return ((x2-x1) / (t2-t1))    

# @overload
# def calcv(a, t):
#     return (a * t)  

