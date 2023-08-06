# from logging.config import valid_ident
# from multipledispatch import dispatch
from math import *

GRAVITY = 9.81

# _________________UNIT CONVERSION_____________________

def xSI(val, units):
    '''converts a non SI distance to SI units'''
    lengths = ['km', 'ft', 'yds', 'yd', 'm', 'mi']
    if units not in lengths: return "invalid unit"

    if units == 'km': return val * 1000
    if units == 'yds' or val== 'yd': return val * 0.9144
    if units == 'ft': return val * 0.3048
    if units == 'mi': return val * 1609.34

def vSI(val, units):
    '''converts velocity to SI units'''
    totals = ['knots' , 'knot', 'mph']
    times = ['s', 'min', 'hr', 'h', 'day', 'yr']

    components = units.split('/')
    

    if(components) == [units]:
        if components[0] not in totals: return "invalid unit: " + units
        if components[0] == 'knots' or components[0] == 'knot': return val * (1/1.94)
        return val * (1/2.24)
    
    if components[1] not in times: return "invalid unit: " + units


    if xSI(val, components[0]) == "invalid unit": return "invalid unit: " + units
    val = xSI(val, components[0])

    if components[1] == 'min': val /= 60
    if components[1] == 'hr' or components[1] == 'h': val /= 3600
    if components[1] == 'day': val /= (3600 * 24)
    if components[1] == 'yr': val /= (3600 * 24 * 365)
    
    return val

# _________________VECTORS_____________________

# vector magnitude
def vmag(*args):
    '''finds the magnitude of an nth degree vector, given the components'''
    vsum = 0

    if type(args[0]) == int or type(args[0]) == float:
        for arg in args:
            vsum += (arg**2)

        return (vsum**(1/2))
    
    else:
        return None

def vcomp(mag, angle, unit):
    '''finds vector components given the magnitude, angle from the origin, and degree unit'''
    tol = 1e-5
    if unit[0] == "D" or unit[0] == "d":
        returnval = [(mag * cos(((2*pi)/360)*angle)) ,((mag * sin(((2*pi)/360)*angle)))]
    else:
        returnval = [(mag * cos(angle)) ,(mag * sin(angle))]
    
    for i in range(len(returnval)):
        if abs(returnval[i]) <= tol:
            returnval[i] = 0;
    
    return tuple(returnval);

# _________________QUADRATIC FORMULA_____________________

#
def quadsolve(a, b, c):
    '''solves the quadratic formula given the coefficients (outputs imaginary values as string tuples)'''
    disc = (b**2) - (4*a*c)
    print(sqrt(abs(disc)))

    if disc > 0: return (((-b + sqrt(disc))/(2 * a)), ((-b - sqrt(disc))/(2 * a)))
    if disc == 0: return (-b / (2* a))
    if disc < 0: return ((str((-b / (2* a)))+" + "+str((sqrt(abs(disc)))/(2*a))+" i"), (str((-b / (2* a)))+" - "+str((sqrt(abs(disc)))/(2*a))+" i"))

# _________________TRANSLATIONAL KINEMATICS_____________________

def calcv(x1, x2, t1, t2):
    '''calulating the velocity with two points'''
    return ((x2-x1) / (t2-t1))  

def calca(v1, v2, t1, t2):
    '''calulating the acceleration with two points'''
    return ((v2-v1) / (t2-t1))    

def xfroma(a, t):
    '''gets the displacement from the acceleration'''
    return (1/2) * a * (t**2)

def vfroma(a, t):
    '''gets the velocity from the acceleration'''
    return  a * t

# _________CONVERTING BETWEEN TRANSLATION TO ROTATION___________

def convertrot(val, r):
    '''converts value to rotational counterpart'''
    return val / r

def converttrans(val, r):
    '''converts value to translational counterpart'''
    return val * r

# __________________MOMENTS OF INERTIA_____________________

def moments(shape, axis):
    ''' Finds the formula for the moment of inertia for the given shape and axis'''

    valid_shapes = ['thin cylinder', 'thick cylinder', 'solid cylinder',  'hollow ball', 'solid ball', 'thin rod', 'thin stick']
    valid_axises = ['parr', 'perp', 'edge']

    shape = shape.lower()
    axis = axis.lower()

    if shape not in valid_shapes or axis not in valid_axises: return lambda *args: "invalid"

    if shape == 'thin cylinder' and axis == 'parr': return (lambda m, r: m * (r**2))
    if shape == 'thin cylinder' and axis == 'perp': return (lambda m, r, l: (.5 * m * (r**2)) + ((1/12) * m * l**2))
    if shape == 'thick cylinder' and axis == 'parr': return (lambda m, r1, r2: ((1/2) * m * (r1**2 + r2 ** 2)))
    if shape == 'thick cylinder' and axis == 'perp': return (lambda m, r1, r2, l: ((1/4) * m * (r1**2 + r2 ** 2)) + ((1/12) * m * (2 * l)**2))
    if shape == 'solid cylinder' and axis == 'parr': return (lambda m, r: ((1/2) * m * (r**2)))
    if shape == 'solid cylinder' and axis == 'perp': return (lambda m, r, l: (.25 * m * (r**2)) + ((1/12) * m * l**2))
    if shape == 'solid ball':  return (lambda m, r: (2/5) * m * (r**2))
    if shape == 'hollow ball': return (lambda m, r: (2/3) * m * (r**2))
    if (shape == 'thin rod' or shape == 'thin stick') and axis == 'perp': return (lambda m, l: (1/12) * m * (l**2))
    if (shape == 'thin rod' or shape == 'thin stick') and axis == 'edge': return (lambda m, l: (1/3) * m * (l**2))

def parraxis(I, m, d):
    '''finds the moment of inertia for a displaced item'''
    return (I + m * d ** 2)

# __________________ENERGIES_____________________
def kinetic(m, v): 
    '''Outputs the value of kinetic energy given mass and velocity'''
    return ((1/2) * m * v**2)

def potent(m, h):
    '''Outputs the value of potential energy given mass and height'''
    return m * GRAVITY * h; 

def springwork(k, x):
    '''Outputs the value of work of a spring given distance and spring constant'''
    return kinetic(k, x)



