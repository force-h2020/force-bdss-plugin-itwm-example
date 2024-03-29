from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules = cythonize("c_fun_wo_papp.pyx", include_path = [numpy.get_include()])
)
