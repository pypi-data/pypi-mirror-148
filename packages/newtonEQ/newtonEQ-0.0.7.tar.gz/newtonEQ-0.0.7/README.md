![](https://i.ibb.co/gy8Mxrp/newtonEQ.png)

**newtonEQ** is a library of formulas that can be applied to newtonian physics problems.

## Installation

Use the package manager [pip]
(https://pip.pypa.io/en/stable/) to install newtonEQ.

```bash
pip install newtonEQ
```

## Usage

newtonEQ has a variety of different functions that allow for the simplification of solving college/physics problems. For example to find the components of a vector:

```python
from newtonEQ import vcomp

#input the magnitude, angle from the positive x-axis, and the degree unit
vcomp(5, 36.9, "deg")

#this would return a tuple of the x and y components of the vector
```

The list of broad subjects covered so far are:

 - Vectors
 - Unit Conversion
 - Quadratic Equations
 - Moment of Inertia
 - Translational and Rotational Kinematics

A more robust guide on how to use the functions is on the way. 

## Contributing

If you have discovered a bug in my code, or you want to change something about it, feel free to contact me at s.varadaraj03@gmail.com.

## License
[MIT](https://choosealicense.com/licenses/mit/)

---