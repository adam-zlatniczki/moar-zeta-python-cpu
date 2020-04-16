import os
from ctypes import cdll, c_double, c_uint, c_void_p, POINTER, cast, byref

""" Load OS specific shared library """
cpp_dll_path = os.path.join(os.path.dirname(__file__), "moar_zeta_cpp_openmp.dll")
cpp_so_path = os.path.join(os.path.dirname(__file__), "moar_zeta_cpp_openmp.so")

libc = None

if os.name == "posix":
    libc = cdll.LoadLibrary(cpp_so_path)
else:
    libc = cdll.LoadLibrary(cpp_dll_path)

if libc is None:
    raise Exception("Compiled shared library not found! Make sure you installed the package without errors!")

libc.hmp_value_py.argtypes = [POINTER(c_double), POINTER(c_double), c_uint, c_uint, c_uint, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_uint, c_uint ]
libc.hmp_value_py.restype = c_void_p


def hmp(x, y, n_tests=50, k=None):
    """
    Calculates the test statistic (average zeta) and its corresponding (harmonic mean) p-value in both directions between X and Y.

    :param x: The X sample points
    :type x: numpy array
    :param y: The Y sample points
    :type y: numpy array
    :param n_tests: The number of tests to do in the multiple testing procedure (50 by default)
    :type n_tests: int
    :param k: The number of neighbors to use in the kNN part ( ceil(sqrt(sample size)) by default )
    :type k: int
    :return: HMP X, avg. zeta X, HMP Y, avg. zeta Y
    :rtype: float, float, float, float
    """

    if x.shape[0] != y.shape[0]:
        raise "X and Y sample doesn't have the same number of points!"

    x_arr = (c_double * x.size)()
    y_arr = (c_double * y.size)()

    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            x_arr[i*x.shape[1] + j] = c_double(x[i,j])

        for j in range(y.shape[1]):
            y_arr[i*y.shape[1] + j] = c_double(y[i,j])

    d_x = c_uint(x.shape[1])
    d_y = c_uint(y.shape[1])
    n = c_uint(len(x))

    n_tests = c_uint(n_tests)

    if k is None:
        k = 0
    k = c_uint(k)

    hmp_x = c_double()
    avg_zeta_x = c_double()
    hmp_y = c_double()
    avg_zeta_y = c_double()

    libc.hmp_value_py(
        cast(x_arr, POINTER(c_double)),
        cast(y_arr, POINTER(c_double)),
        d_x,
        d_y,
        n,
        byref(hmp_x),
        byref(avg_zeta_x),
        byref(hmp_y),
        byref(avg_zeta_y),
        n_tests,
        k
    )

    return hmp_x.value, avg_zeta_x.value, hmp_y.value, avg_zeta_y.value


