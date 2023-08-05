import unittest
import numpy as np
import matplotlib.pyplot as plt

from intelligen import interpolate

X = np.array([-1, 0, 4,  1, 7, 8])
X = np.concatenate((X, X+10))
Y = np.array([ 4, 2, 3, -2, 6, 6])
Y = np.concatenate((Y, Y+1))

_x = np.linspace(min(X),max(X),1000)

Lagran = interpolate.lagrange(X.reshape(-1),Y.reshape(-1))

class TestInterpolate(unittest.TestCase):
    """Tests for `intelligen` package."""
    
    def test_lagrange(self):
        Lagran(_x)
    

if __name__ == '__main__':
    unittest.main()
