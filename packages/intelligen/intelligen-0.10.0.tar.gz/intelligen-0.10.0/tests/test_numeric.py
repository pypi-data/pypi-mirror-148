import unittest
from intelligen import numeric

def f(x): return x**3 + 2*x**2 + 10*x - 20
def df(x): return 3*x**2 + 4*x + 10
def ddf(x): return 6*x + 4
ROOT = 1.36880

class TestNumeric(unittest.TestCase):
    """Tests for `intelligen` package."""

    def test_newton(self):
        z = numeric.newton(f, df, 1, 0.01, True)[0]
        self.assertAlmostEqual(z, ROOT, 3)

    def test_bisection(self):
        z = numeric.bisection(f, 1, 2, 0.01, True)[0]
        self.assertAlmostEqual(z, ROOT, 3)

    def test_regula_falsi(self):
        z = numeric.regula_falsi(f, 1, 2, 0.01, True)[0]
        self.assertAlmostEqual(z, ROOT, 3)
    
    def test_secant(self):
        z = numeric.secant(f, 1, 2, 0.01, True)[0]
        self.assertAlmostEqual(z, ROOT, 3)
    
    def test_newton(self):
        z = numeric.newton2(f, df, ddf, 1, 0.01, True)[0]
        self.assertAlmostEqual(z, ROOT, 3)

if __name__ == '__main__':
    unittest.main()
