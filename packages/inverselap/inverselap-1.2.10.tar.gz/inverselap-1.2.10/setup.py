from distutils.core import  setup
import setuptools
packages = ['inverselap']# 唯一的包名，自己取名

setup(
    name='inverselap',
	version='1.2.10',
	author='renger',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown', 
    description="Provides a variety of numerical inversion methods for the inverse Laplace transform",
    packages=packages, 
    
    install_requires=[
            'mpmath>=1.2.1',
            'numpy>=1.19.3',
            'scipy>=1.5.4',
    ],
    package_dir={'requests': 'requests'},
)