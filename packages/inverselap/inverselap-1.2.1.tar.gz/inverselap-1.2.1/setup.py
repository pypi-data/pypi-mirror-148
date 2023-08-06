from distutils.core import  setup
import setuptools
packages = ['inverselap']# 唯一的包名，自己取名
setup(name='inverselap',
	version='1.2.1',
	author='renger',
    description="A small example package",
    packages=packages, 
    package_dir={'requests': 'requests'},)