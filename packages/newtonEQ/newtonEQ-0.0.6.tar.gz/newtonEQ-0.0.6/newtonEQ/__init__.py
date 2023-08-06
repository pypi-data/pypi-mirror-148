from multipledispatch import dispatch
from math import *

GRAVITY = 9.81

# _________________UNIT CONVERSION_____________________

def xSI(val, units):
    '''converts a non SI distance to SI units
    
    Parameters:
        [int or float] val - Numerical Value
        [string] units - distance unit as a string 
    
    Return:
        Converted value from given units to meters

    '''
    lengths = ['km', 'ft', 'yds', 'yd', 'm', 'mi']
    if units not in lengths: return "invalid unit"

    if units == 'km': return val * 1000
    if units == 'yds' or val== 'yd': return val * 0.9144
    if units == 'ft': return val * 0.3048
    if units == 'mi': return val * 1609.34

def vSI(val, units):
    '''converts velocity to SI units
    
    Parameters:
        [int or float] val - Numerical Value
        [string] units - string in the form (dist/time)
    
    Return:
        Converted value from given units to meters/second

    '''
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

def radtodeg(x):
    '''Coverts an angle in radians to degrees'''
    return (x/(2*pi)) * 360

def degtorad(x):
    '''Coverts an angle in degrees to radians'''
    return (x/360) * (2 * pi)

# _________________VECTORS_____________________

# vector magnitude
def vmag(*args):
    '''finds the magnitude of an nth degree vector, given the components
    
    Parameters:
       [int or float] *args - Numerical values
    
    Return:
        the magnitude of the nth degree vector created by the parameters
    '''
    vsum = 0

    for arg in args:

        if type(arg) != int and type(arg) != float: raise TypeError("Invalid value inputted: " + str(arg))
        vsum += (arg**2)
        
        return (vsum**(1/2))
    
def vcomp(mag, angle, unit):
    '''finds vector components given the magnitude, angle from the origin, and degree unit
    
    Parameters:
        [int or float] mag - Megnitude of the vector
        [int or float] angle - angle from the positive x-axis (counter-clockwise)
        [string] unit - either "deg" or "rad"
    
    Return:
        the cos and sin component of the vector as a tuple

    '''
    tol = 1e-2
    if unit[0] == "D" or unit[0] == "d":
        returnval = [(mag * cos(degtorad(angle))) , (mag * sin(degtorad(angle)))]
    else:
        returnval = [(mag * cos(angle)) ,(mag * sin(angle))]
    
    for i in range(len(returnval)):
        if abs(returnval[i]) <= tol:
            returnval[i] = 0;
        if abs(returnval[i] - round(returnval[i])) < tol:
            returnval[i] = round(returnval[i])
    
    return tuple(returnval)

def dotprod(va, vb):
    '''finds the scalar product of the vectors given
    
    Parameters:
        [tuple] va, vb - vector components
    
    Return:
        the dot product of the vectors

    '''
    return (va[0] * vb[0] + va[1] * vb[1])

def crossprod(m1, m2, a, unit):
    '''finds the vector product of the vectors given
    
    Parameters:
        [tuple] va, vb - vector components
    
    Return:
        the dot product of the vectors

    '''
    if unit[0] == 'd' or unit[0] == 'D': a = degtorad(a)
    return m1*m2*sin(a)

def anglebetween(va, vb, unit):
    '''finds the angle between two vectors
    
    Parameters:
        [tuple or set] va, vb - vector components
        [string] unit - either "deg" or "rad"
    
    Return:
        the angle between the two vectors

    '''

    if unit[0] != 'd' and unit[0] != 'D': return acos(dotprod(va, vb) / (vmag(va[0], va[1]) * vmag(vb[1], vb[1])))
    else: return radtodeg(acos(dotprod(va, vb) / (vmag(va[0], va[1]) * vmag(vb[1], vb[1]))))

# _________CONVERTING BETWEEN TRANSLATION TO ROTATION___________

def convertrot(val, r):
    '''converts value to rotational counterpart
    
    Parameters:
        [int or float] val - numerical value in translational SI units
        [int or float] r - radius 
    
    Return:
        the value represented in rotational SI units
    
    '''
    return val / r

def converttrans(val, r):
    '''converts value to translational counterpart
    
    Parameters:
        [int or float] val - numerical value in rotational SI units
        [int or float] r - radius 
    
    Return:
        the value represented in translational SI units
    
    '''
    return val * r

# _________________QUADRATIC FORMULA_____________________

#
def quadsolve(a, b, c):
    '''solves the quadratic formula given the coefficients (outputs imaginary values as string tuples)
    
    Parameters:
        [int or float] a, b, c - coefficients of the polynomial
    
    Return:
        tuple of the possible solutions to the polynomial
    
    '''
    disc = (b**2) - (4*a*c)
    print(sqrt(abs(disc)))

    if disc > 0: return (((-b + sqrt(disc))/(2 * a)), ((-b - sqrt(disc))/(2 * a)))
    if disc == 0: return tuple(-b / (2* a))
    if disc < 0: return ((str((-b / (2* a)))+" + "+str((sqrt(abs(disc)))/(2*a))+" i"), (str((-b / (2* a)))+" - "+str((sqrt(abs(disc)))/(2*a))+" i"))

# _________________TRANSLATIONAL KINEMATICS_____________________

def calcv(x1, x2, t1, t2):
    '''calulating the velocity with two points
    
    Parameters:
        [int or float] x1, x2 - initial and final position
        [int or float] t1, t2 - initial and final times
    
    Return:
        the velocity of the object

    '''
    return ((x2-x1) / (t2-t1))  

def calca(v1, v2, t1, t2):
    '''calulating the acceleration with two points
    
    Parameters:
        [int or float] v1, v2 - initial and final velocity
        [int or float] t1, t2 - initial and final times
    
    Return:
        the acceleration of the object

    '''
    return ((v2-v1) / (t2-t1))    

def xfroma(a, t):
    '''gets the displacement from the acceleration
    
    Parameters:
        [int or float] a - acceleration
        [int or float] t - time passed
    
    Return:
        the displacement of the object
    
    '''
    return (1/2) * a * (t**2)

def vfroma(a, t):
    '''gets the velocity from the acceleration
    
    Parameters:
        [int or float] a - acceleration
        [int or float] t - time passed
    
    Return:
        the velocity of the object
    
    '''
    return  a * t

# __________________MOMENTS OF INERTIA_____________________

def moments(shape, axis):
    ''' Finds the formula for the moment of inertia for the given shape and axis
    
    Parameters:
        [string] shape - a two-word description of the shape
        [string] axis - an abbreviated description of the axis
    
    Return:
        a lambda function that calulates the moment of interia for the given cirumstance

    Valid Shapes:
        'thin cylinder', 
        'thick cylinder', 
        'solid cylinder',  
        'hollow ball', 
        'solid ball', 
        'thin rod', 
        'thin stick'
    
    Valid Axis:
        'parr' - parralel
        'perp' - perpendicular
        'edge' - only for the rod/stick
    '''

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
    '''finds the moment of inertia for a displaced item
    
    Parameters:
        [int or float] I - moment of inertia
        [int or float] m - mass
        [int or float] d - distance from axis of rotation
    
    Return:
        a function that calulates the moment of interia for the given cirumstance using parralel axis theorem
    
    '''
    return (I + m * d ** 2)

# __________________ENERGIES_____________________
def kinetic(m, v): 
    '''Outputs the value of kinetic energy given mass and velocity
    
    Parameters:
        [int or float] m - mass
        [int or float] v - velocity
    
    Return:
        a numerical value of the kinetic energy
    
    '''
    return ((1/2) * m * v**2)

def potent(m, h):
    '''Outputs the value of potential energy given mass and height
    
    Parameters:
        [int or float] m - mass
        [int or float] h - height
    
    Return:
        a numerical value of the potential energy
    
    '''
    return m * GRAVITY * h; 

def springwork(k, x):
    '''Outputs the value of work of a spring given distance and spring constant
    
    Parameters:
        [int or float] k - spring constant
        [int or float] x - distance the spring is altered
    
    Return:
        a numerical value of the potential energy the spring holds
    
    '''
    return kinetic(k, x)
