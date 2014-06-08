from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'Compute',
  ext_modules = cythonize("count.pyx"),
)
