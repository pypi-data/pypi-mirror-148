from distutils.core import  setup
import setuptools
packages = ['inverselap']# 唯一的包名，自己取名
setup(name='inverselap',
	version='1.2.6',
	author='renger',
    long_description='README.md',
    long_description_content_type="text/markdown",
    description="Provides a variety of numerical inversion methods for the inverse Laplace transform",
    packages=packages, 
    package_dir={'requests': 'requests'},)