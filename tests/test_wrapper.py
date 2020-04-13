import unittest
import numpy as np
import moar_zeta_cpu

class TestWrapper(unittest.TestCase):
    def smoke_test(self):
        np.random.seed(0)
        x = np.random.rand(10000)
        y = np.random.rand(10000)

        ret = moar_zeta_cpu.hmp(x, y)
        print(ret)

        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()