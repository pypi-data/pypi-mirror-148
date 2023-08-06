from distutils.core import  setup
import setuptools
packages = ['inverselap']# 唯一的包名，自己取名
setup(name='inverselap',
	version='1.2.5',
	author='renger',
    description="Provides a variety of numerical inversion methods for the inverse Laplace transform",
    packages=packages, 
    package_dir={'requests': 'requests'},)